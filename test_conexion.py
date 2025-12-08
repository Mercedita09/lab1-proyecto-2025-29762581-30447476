from conexion import conectar

conexion = conectar()

if conexion:
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personas_atendidas;")
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)
    conexion.close()
