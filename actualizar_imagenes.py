import sqlite3

# Conectar a la base de datos
print("Conectando a la base de datos...")
conn = sqlite3.connect('ferremas.db')
cursor = conn.cursor()

# Actualizar las rutas de las imágenes
print("Actualizando rutas de imágenes...")
actualizaciones = [
    (1, '/static/img/taladro_bosch.jpg'),
    (2, '/static/img/destornilladores_stanley.jpg'),
    (3, '/static/img/martillo_stanley.jpg'),
    (4, '/static/img/sierra_makita.jpg'),
    (5, '/static/img/tornillos_varios.jpg'),
    (6, '/static/img/pintura_latex.jpg')
]

for id_producto, ruta_imagen in actualizaciones:
    print(f"Actualizando producto {id_producto} con imagen: {ruta_imagen}")
    cursor.execute('UPDATE producto SET imagen = ? WHERE id = ?', (ruta_imagen, id_producto))

# Guardar los cambios
print("Guardando cambios...")
conn.commit()
conn.close()

print("¡Imágenes actualizadas con éxito!")
print("Ahora puedes ejecutar 'python app.py' para iniciar la aplicación nuevamente.")