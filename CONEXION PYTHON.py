from dash import Dash, html, dcc
import plotly.express as px
import psycopg2

def connect_to_postgres(host, database, user, password):
    """Establece la conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='Base_Datos_Medicamentos',
            user='postgres',
            password='123456789'
        )
        print("¡Conexión exitosa a PostgreSQL!")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

def execute_query(conn, query):
    """Ejecuta una consulta SQL en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print("Error al ejecutar la consulta:", e)
        return None

def close_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn is not None:
        conn.close()
        print("Conexión cerrada.")

# Parámetros de conexión
host = "localhost"
database = "Base_Datos_Medicamentos"
user = "postgres"
password = "123456789"

# Conexión a PostgreSQL
conn = connect_to_postgres(host, database, user, password)


