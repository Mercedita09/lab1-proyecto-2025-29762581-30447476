from conexion import conectar

def consultar_profesionales():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombres, apellidos FROM Profesionales")
    resultados = cursor.fetchall()
    for fila in resultados:
        print(fila)
    cursor.close()
    conexion.close()

def insertar_profesional(nombres, apellidos, registro):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO Profesionales (nombres, apellidos, registroProfesional) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombres, apellidos, registro))
    conexion.commit()
    print("✅ Profesional insertado correctamente")
    cursor.close()
    conexion.close()
