import sqlite3
import os
from datetime import datetime
import hashlib

print("Iniciando script de carga de datos (versión SQLite directo)...")

# Verificar si la base de datos existe y eliminarla para empezar fresco
if os.path.exists('ferremas.db'):
    os.remove('ferremas.db')
    print("Base de datos anterior eliminada.")

# Crear la conexión a la base de datos
conn = sqlite3.connect('ferremas.db')
cursor = conn.cursor()

# Crear tablas
print("Creando tablas en la base de datos...")

# Tabla de usuarios
cursor.execute('''
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL
)
''')

# Tabla de productos
cursor.execute('''
CREATE TABLE producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    imagen TEXT,
    categoria TEXT
)
''')

# Tabla de pedidos
cursor.execute('''
CREATE TABLE pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha TIMESTAMP NOT NULL,
    estado TEXT NOT NULL,
    metodo_pago TEXT NOT NULL,
    metodo_entrega TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
)
''')

# Tabla de detalles de pedido
cursor.execute('''
CREATE TABLE detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedido (id),
    FOREIGN KEY (producto_id) REFERENCES producto (id)
)
''')

print("Tablas creadas correctamente.")

# Función simple para generar hash de contraseñas (similar a lo que hace werkzeug)
def generar_hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insertar usuarios de ejemplo
print("Creando usuarios de ejemplo...")
usuarios = [
    ('admin@ferremas.cl', generar_hash_password('admin123'), 'Administrador', 'admin'),
    ('vendedor@ferremas.cl', generar_hash_password('vendedor123'), 'Juan Vendedor', 'vendedor'),
    ('bodeguero@ferremas.cl', generar_hash_password('bodeguero123'), 'Pedro Bodeguero', 'bodeguero'),
    ('contador@ferremas.cl', generar_hash_password('contador123'), 'María Contadora', 'contador'),
    ('cliente@ejemplo.com', generar_hash_password('cliente123'), 'Carlos Cliente', 'cliente')
]

cursor.executemany(
    'INSERT INTO usuario (email, password, nombre, tipo) VALUES (?, ?, ?, ?)',
    usuarios
)

# Insertar productos de ejemplo
print("Creando productos de ejemplo...")
productos = [
    ('Taladro Eléctrico Bosch', 'Taladro eléctrico profesional con múltiples velocidades y accesorios.', 89990, 25, '/static/img/producto-default.jpg', 'Herramientas Eléctricas'),
    ('Set de Destornilladores Stanley', 'Set de 10 destornilladores para diferentes tipos de tornillos.', 15990, 50, '/static/img/producto-default.jpg', 'Herramientas Manuales'),
    ('Martillo Carpintero Stanley', 'Martillo de carpintero con mango ergonómico y gran resistencia.', 12990, 30, '/static/img/producto-default.jpg', 'Herramientas Manuales'),
    ('Sierra Circular Makita', 'Sierra circular profesional para cortes precisos en madera y otros materiales.', 129990, 15, '/static/img/producto-default.jpg', 'Herramientas Eléctricas'),
    ('Caja de Tornillos Varios', 'Caja con más de 500 tornillos de diferentes tamaños y tipos.', 9990, 40, '/static/img/producto-default.jpg', 'Fijaciones'),
    ('Pintura Látex Blanca 1 Galón', 'Pintura látex de alta calidad para interiores, color blanco.', 19990, 60, '/static/img/producto-default.jpg', 'Pinturas')
]

cursor.executemany(
    'INSERT INTO producto (nombre, descripcion, precio, stock, imagen, categoria) VALUES (?, ?, ?, ?, ?, ?)',
    productos
)

# Crear carpeta de imágenes si no existe
os.makedirs('static/img', exist_ok=True)
print("Carpeta de imágenes verificada.")

# Guardar los cambios
conn.commit()
conn.close()

print("¡Datos de ejemplo cargados con éxito!")
print("Script completado correctamente.")