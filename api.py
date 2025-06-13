from flask import Flask, jsonify, request
import sqlite3
import json

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ferremas.db')
    conn.row_factory = sqlite3.Row
    return conn

# API para consultar productos (publicador)
@app.route('/api/productos', methods=['GET'])
def get_productos():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto['id'],
            'nombre': producto['nombre'],
            'descripcion': producto['descripcion'],
            'precio': producto['precio'],
            'stock': producto['stock'],
            'categoria': producto['categoria']
        })
    
    return jsonify({
        'productos': productos_list,
        'total': len(productos_list)
    })

# API para consultar stock específico (publicador)
@app.route('/api/productos/<int:producto_id>/stock', methods=['GET'])
def get_stock(producto_id):
    conn = get_db_connection()
    producto = conn.execute('SELECT id, nombre, stock FROM producto WHERE id = ?', 
                           (producto_id,)).fetchone()
    conn.close()
    
    if producto is None:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    return jsonify({
        'id': producto['id'],
        'nombre': producto['nombre'],
        'stock_disponible': producto['stock']
    })

# API para actualizar stock (publicador)
@app.route('/api/productos/<int:producto_id>/stock', methods=['PUT'])
def update_stock(producto_id):
    data = request.get_json()
    
    if 'stock' not in data:
        return jsonify({'error': 'Se requiere el campo stock'}), 400
    
    conn = get_db_connection()
    conn.execute('UPDATE producto SET stock = ? WHERE id = ?', 
                (data['stock'], producto_id))
    conn.commit()
    
    # Verificar si se actualizó algún registro
    if conn.total_changes == 0:
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    conn.close()
    return jsonify({'message': 'Stock actualizado correctamente'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)