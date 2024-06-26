from dash import Dash, html, dcc
from dash.dependencies import Input, Output
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

# Función para obtener la evolución temporal de registros sanitarios activos
def get_active_sanitary_records(conn):
    query = """
        SELECT fechaexpedicion, COUNT(*) AS registros_activos
        FROM Registro_Sanitario
        WHERE CURRENT_DATE BETWEEN fechaexpedicion AND fechavencimiento
        GROUP BY fechaexpedicion
        ORDER BY fechaexpedicion
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

# Obtener la evolución temporal de registros sanitarios activos
active_records_data = get_active_sanitary_records(conn)

# Cerrar conexión a PostgreSQL
conn.close()

# Preparar datos para el gráfico de líneas
fechas = [row[0] for row in active_records_data]
registros_activos = [row[1] for row in active_records_data]

# Crear aplicación Dash
app = Dash(__name__)

# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Evolución Temporal de Registros Sanitarios Activos"),
    dcc.Graph(
        id='active-records-line-chart',
        figure={
            'data': [
                go.Scatter(x=fechas, y=registros_activos, mode='lines', name='Registros Activos')
            ],
            'layout': {
                'title': 'Evolución Temporal de Registros Sanitarios Activos',
                'xaxis': {'title': 'Fecha de Expedición'},
                'yaxis': {'title': 'Cantidad de Registros Activos'}
            }
        }
    )
])

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)