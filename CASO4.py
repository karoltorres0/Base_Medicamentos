from dash import Dash, html, dcc
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

# Función para obtener la proporción de prescripciones médicas por principio activo
def get_prescriptions_by_active_principle(conn):
    query = """
        SELECT cm.principioactivo, COUNT(cum.expediente) AS cantidad_prescripciones
        FROM Composicion_Medicamento cm
        INNER JOIN Control_Unico_Medicamentos cum ON cm.expediente = cum.expediente
        GROUP BY cm.principioactivo
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

# Obtener proporción de prescripciones médicas por principio activo
prescriptions_data = get_prescriptions_by_active_principle(conn)

# Cerrar conexión a PostgreSQL
conn.close()

# Preparar datos para el gráfico circular
labels = [row[0] for row in prescriptions_data]
values = [row[1] for row in prescriptions_data]

# Crear aplicación Dash
app = Dash(__name__)

# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Análisis de Prescripciones Médicas por Principio Activo"),
    dcc.Graph(
        id='prescriptions-by-active-principle-pie-chart',
        figure={
            'data': [
                go.Pie(labels=labels, values=values)
            ],
            'layout': {
                'title': 'Proporción de Prescripciones Médicas por Principio Activo'
            }
        }
    )
])

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)