from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import psycopg2
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import psycopg2

# Función para conectar a PostgreSQL
def connect_to_postgres(host, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("¡Conexión exitosa a PostgreSQL!")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

# Función para obtener los datos de medicamentos próximos a vencerse
def get_near_expired_medicines(conn, days_threshold=30):
    query = f"""
        SELECT COUNT(*) AS cantidad, fechavencimiento
        FROM Registro_Sanitario
        WHERE fechavencimiento BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '{days_threshold} days'
        GROUP BY fechavencimiento
        ORDER BY fechavencimiento
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

# Parámetros de conexión a PostgreSQL
host = "localhost"
database = "Base_Datos_Medicamentos"
user = "postgres"
password = "123456789"

# Conexión a PostgreSQL
conn = connect_to_postgres(host, database, user, password)

# Obtener datos de medicamentos próximos a vencerse
medicines_data = get_near_expired_medicines(conn, days_threshold=30)

# Cerrar conexión a PostgreSQL
conn.close()

# Preparar datos para el gráfico de barras
fechas = [row[1] for row in medicines_data]
cantidades = [row[0] for row in medicines_data]

# Crear aplicación Dash
app = Dash(__name__)

# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Medicamentos Próximos a Vencerse"),
    dcc.Graph(
        id='expired-medicines-bar-chart',
        figure={
            'data': [
                {'x': fechas, 'y': cantidades, 'type': 'bar', 'name': 'Cantidad de Medicamentos'}
            ],
            'layout': {
                'title': 'Cantidad de Medicamentos Próximos a Vencerse en los Próximos 30 Días',
                'xaxis': {'title': 'Fecha de Vencimiento'},
                'yaxis': {'title': 'Cantidad de Medicamentos'}
            }
        }
    )
])

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)
    
