"""
Script para cargar datos de ejemplo en la base de datos de FERREMAS
Para ejecutar este script:
1. Asegúrate que la base de datos esté creada
2. Ejecuta este archivo con Python: python cargar_datos.py
"""

from app import app, db, Usuario, Producto, Pedido, DetallePedido
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

# Verificar si la base de datos existe
def cargar_datos_ejemplo():
    with app.app_context():
        # Eliminar datos existentes para evitar duplicados
        DetallePedido.query.delete()
        Pedido.query.delete()
        Producto.query.delete()
        Usuario.query.delete()
        
        print("Creando usuarios de ejemplo...")
        
        # Crear usuarios de ejemplo
        usuarios = [
            {
                'email': 'admin@ferremas.cl',
                'password': generate_password_hash('admin123'),
                'nombre': 'Administrador',
                'tipo': 'admin'
            },
            {
                'email': 'vendedor@ferremas.cl',
                'password': generate_password_hash('vendedor123'),
                'nombre': 'Juan Vendedor',
                'tipo': 'vendedor'
            },
            {
                'email': 'bodeguero@ferremas.cl',
                'password': generate_password_hash('bodeguero123'),
                'nombre': 'Pedro Bodeguero',
                'tipo': 'bodeguero'
            },
            {
                'email': 'contador@ferremas.cl',
                'password': generate_password_hash('contador123'),
                'nombre': 'María Contadora',
                'tipo': 'contador'
            },
            {
                'email': 'cliente@ejemplo.com',
                'password': generate_password_hash('cliente123'),
                'nombre': 'Carlos Cliente',
                'tipo': 'cliente'
            }
        ]
        
        for usuario_data in usuarios:
            usuario = Usuario(**usuario_data)
            db.session.add(usuario)
        
        print("Creando productos de ejemplo...")
        
        # Crear productos de ejemplo
        productos = [
            {
                'nombre': 'Taladro Eléctrico Bosch',
                'descripcion': 'Taladro eléctrico profesional con múltiples velocidades y accesorios.',
                'precio': 89990,
                'stock': 25,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Herramientas Eléctricas'
            },
            {
                'nombre': 'Set de Destornilladores Stanley',
                'descripcion': 'Set de 10 destornilladores para diferentes tipos de tornillos.',
                'precio': 15990,
                'stock': 50,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Herramientas Manuales'
            },
            {
                'nombre': 'Martillo Carpintero Stanley',
                'descripcion': 'Martillo de carpintero con mango ergonómico y gran resistencia.',
                'precio': 12990,
                'stock': 30,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Herramientas Manuales'
            },
            {
                'nombre': 'Sierra Circular Makita',
                'descripcion': 'Sierra circular profesional para cortes precisos en madera y otros materiales.',
                'precio': 129990,
                'stock': 15,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Herramientas Eléctricas'
            },
            {
                'nombre': 'Caja de Tornillos Varios',
                'descripcion': 'Caja con más de 500 tornillos de diferentes tamaños y tipos.',
                'precio': 9990,
                'stock': 40,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Fijaciones'
            },
            {
                'nombre': 'Pintura Látex Blanca 1 Galón',
                'descripcion': 'Pintura látex de alta calidad para interiores, color blanco.',
                'precio': 19990,
                'stock': 60,
                'imagen': '/static/img/producto-default.jpg',
                'categoria': 'Pinturas'
            }
        ]
        
        for producto_data in productos:
            producto = Producto(**producto_data)
            db.session.add(producto)
        
        # Guardar los cambios
        db.session.commit()
        
        print("¡Datos de ejemplo cargados con éxito!")

if __name__ == "__main__":
    # Crear carpeta de imágenes si no existe
    os.makedirs('static/img', exist_ok=True)
    
    # Cargar datos de ejemplo
    cargar_datos_ejemplo()