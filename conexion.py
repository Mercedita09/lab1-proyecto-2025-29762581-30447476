import mysql.connector

def conectar():
    conexion = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='gestion_salud'
    )
    return conexion
