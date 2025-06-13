from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import hashlib
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-ferremas'

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('ferremas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Función para verificar contraseñas
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()

# Rutas para las páginas principales
@app.route('/')
def index():
    conn = get_db_connection()
    productos = conn.execute('SELECT * FROM producto').fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuario WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if usuario and check_password(usuario['password'], password):
            session['usuario_id'] = usuario['id']
            session['usuario_tipo'] = usuario['tipo']
            
            # Redirigir según el tipo de usuario
            if usuario['tipo'] == 'cliente':
                return redirect(url_for('index'))
            elif usuario['tipo'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif usuario['tipo'] == 'vendedor':
                return redirect(url_for('vendedor_dashboard'))
            elif usuario['tipo'] == 'bodeguero':
                return redirect(url_for('bodeguero_dashboard'))
            elif usuario['tipo'] == 'contador':
                return redirect(url_for('contador_dashboard'))
        
        flash('Email o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nombre = request.form['nombre']
        
        # Verificar si el usuario ya existe
        conn = get_db_connection()
        usuario_existente = conn.execute('SELECT * FROM usuario WHERE email = ?', (email,)).fetchone()
        
        if usuario_existente:
            conn.close()
            flash('El email ya está registrado')
            return redirect(url_for('registro'))
        
        # Crear nuevo usuario
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        conn.execute('INSERT INTO usuario (email, password, nombre, tipo) VALUES (?, ?, ?, ?)',
                    (email, hashed_password, nombre, 'cliente'))
        conn.commit()
        conn.close()
        
        flash('Registro exitoso, ahora puedes iniciar sesión')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_tipo', None)
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []
    
    items_carrito = []
    total = 0
    
    conn = get_db_connection()
    for item in session['carrito']:
        producto = conn.execute('SELECT * FROM producto WHERE id = ?', (item['producto_id'],)).fetchone()
        if producto:
            subtotal = producto['precio'] * item['cantidad']
            total += subtotal
            items_carrito.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
    conn.close()
    
    return render_template('carrito.html', items=items_carrito, total=total)

@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    if 'carrito' in session:
        session['carrito'] = [item for item in session['carrito'] if item['producto_id'] != producto_id]
        session.modified = True
        flash('Producto eliminado del carrito')
    
    return redirect(url_for('carrito'))

@app.route('/realizar_pedido')
def realizar_pedido():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para realizar un pedido')
        return redirect(url_for('login'))
    
    if 'carrito' not in session or not session['carrito']:
        flash('Tu carrito está vacío')
        return redirect(url_for('carrito'))
    
    # Redireccionar al proceso de pago con Webpay
    return render_template('carrito.html', mostrar_metodos_pago=True)

@app.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    
    cantidad = int(request.form.get('cantidad', 1))
    
    # Verificar si el producto ya está en el carrito
    for item in session['carrito']:
        if item['producto_id'] == producto_id:
            item['cantidad'] += cantidad
            session.modified = True
            flash('Producto actualizado en el carrito')
            return redirect(url_for('carrito'))
    
    # Agregar nuevo producto al carrito
    session['carrito'].append({
        'producto_id': producto_id,
        'cantidad': cantidad
    })
    session.modified = True
    
    flash('Producto agregado al carrito')
    return redirect(url_for('carrito'))

# Dashboards para diferentes roles
@app.route('/admin')
def admin_dashboard():
    if 'usuario_id' not in session or session['usuario_tipo'] != 'admin':
        return redirect(url_for('login'))
    
    return render_template('admin_dashboard.html')

@app.route('/vendedor')
def vendedor_dashboard():
    if 'usuario_id' not in session or session['usuario_tipo'] != 'vendedor':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido WHERE estado = "pendiente"').fetchall()
    conn.close()
    
    return render_template('vendedor_dashboard.html', pedidos=pedidos)

@app.route('/bodeguero')
def bodeguero_dashboard():
    if 'usuario_id' not in session or session['usuario_tipo'] != 'bodeguero':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido WHERE estado = "aprobado"').fetchall()
    conn.close()
    
    return render_template('bodeguero_dashboard.html', pedidos=pedidos)

@app.route('/contador')
def contador_dashboard():
    if 'usuario_id' not in session or session['usuario_tipo'] != 'contador':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido').fetchall()
    conn.close()
    
    return render_template('contador_dashboard.html', pedidos=pedidos)

# Rutas para el proceso de pago con Webpay
@app.route('/proceso_pago', methods=['POST'])
def proceso_pago():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para realizar un pedido')
        return redirect(url_for('login'))
    
    if 'carrito' not in session or not session['carrito']:
        flash('Tu carrito está vacío')
        return redirect(url_for('carrito'))
    
    # Calcular el total del carrito
    total = 0
    conn = get_db_connection()
    for item in session['carrito']:
        producto = conn.execute('SELECT precio FROM producto WHERE id = ?', (item['producto_id'],)).fetchone()
        if producto:
            subtotal = producto['precio'] * item['cantidad']
            total += subtotal
    conn.close()
    
    # Generar un ID de orden aleatorio para la simulación
    orden_id = random.randint(10000, 99999)
    session['orden_temp'] = {
        'id': orden_id,
        'monto': total
    }
    
    return render_template('webpay_simulacion.html', orden_id=orden_id, monto=total)

@app.route('/confirmar_pago', methods=['POST'])
def confirmar_pago():
    if 'orden_temp' not in session:
        flash('Error en el proceso de pago. Inténtalo nuevamente.')
        return redirect(url_for('carrito'))
    
    orden_id = session['orden_temp']['id']
    monto = session['orden_temp']['monto']
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # En una implementación real, aquí se registraría el pedido en la base de datos
    
    # Limpiar el carrito
    session['carrito'] = []
    session.pop('orden_temp', None)
    
    flash('¡Pago realizado con éxito!')
    return render_template('pago_confirmado.html', orden_id=orden_id, monto=monto, fecha=fecha)

if __name__ == '__main__':
    print("Iniciando la aplicación Flask...")
    try:
        print("Servidor iniciándose en http://127.0.0.1:5000/")
        app.run(host='0.0.0.0', debug=True)
    except Exception as e:
        print(f"ERROR AL INICIAR: {e}")
        import traceback
        traceback.print_exc()