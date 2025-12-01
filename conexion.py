import mysql.connector

# Conexión a tu base de datos local
conexion = mysql.connector.connect(
    host="127.0.0.1",              # Dirección local del servidor MySQL
    user="root",                   # Usuario de tu base de datos (según tu imagen)
    password="tu_contraseña_real",# Aquí va tu contraseña real de MySQL
    database="lab1_api_gestion_medica"  # Nombre de tu base de datos
)

# Consulta a la tabla 'citas'
cursor = conexion.cursor()
cursor.execute("SELECT * FROM citas")
resultados = cursor.fetchall()

# Mostrar resultados
for fila in resultados:
    print(fila)

# Cerrar conexión
conexion.close()
