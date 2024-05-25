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

# Función para obtener los datos de medicamentos por tipo de enfermedad
def get_medicines_by_disease(conn):
    query = """
        SELECT atc, descripcioncomercial, COUNT(*) AS cantidad
        FROM Medicamento
        GROUP BY atc, descripcioncomercial
        ORDER BY atc
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

# Obtener datos de medicamentos por tipo de enfermedad
medicines_data = get_medicines_by_disease(conn)

# Cerrar conexión a PostgreSQL
conn.close()

# Preparar datos para el gráfico de barras
atc = [row[0] for row in medicines_data]
descripcioncomercial = [row[1] for row in medicines_data]
cantidad = [row[2] for row in medicines_data]

# Crear aplicación Dash
app = Dash(__name__)

# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Análisis de Medicamentos por Tipo de Enfermedad"),
    dcc.Graph(
        id='medicine-by-disease-bar-chart',
        figure={
            'data': [
                {'x': atc, 'y': cantidad, 'type': 'bar', 'name': 'Cantidad de Medicamentos'}
            ],
            'layout': {
                'title': 'Distribución de Medicamentos por Tipo de Enfermedad (Clasificación ATC)',
                'xaxis': {'title': 'Clasificación ATC'},
                'yaxis': {'title': 'Cantidad de Medicamentos'}
            }
        }
    )
])

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)