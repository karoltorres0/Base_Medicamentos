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

# Función para obtener los precios de medicamentos por principio activo
def get_prices_by_active_principle(conn):
    query = """
        SELECT cm.principioactivo, AVG(cm.cantidad) AS precio_promedio
        FROM Composicion_Medicamento cm
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

# Obtener precios de medicamentos por principio activo
prices_data = get_prices_by_active_principle(conn)

# Cerrar conexión a PostgreSQL
conn.close()

# Preparar datos para el gráfico de barras
principios_activos = [row[0] for row in prices_data]
precios_promedio = [row[1] for row in prices_data]

# Crear aplicación Dash
app = Dash(__name__)

# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Comparación de Precios de Medicamentos por Principio Activo"),
    dcc.Graph(
        id='active-principle-prices-bar-chart',
        figure={
            'data': [
                {'y': principios_activos, 'x': precios_promedio, 'type': 'bar', 'orientation': 'h'}
            ],
            'layout': {
                'title': 'Comparación de Precios de Medicamentos por Principio Activo',
                'xaxis': {'title': 'Precio Promedio'},
                'yaxis': {'title': 'Principio Activo'}
            }
        }
    )
])

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)

