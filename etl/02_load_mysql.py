# Este script es para cargar datos a MySQL usando SQLAlchemy y pandas.

import pandas as pd
from sqlalchemy import create_engine
import pymysql

# 1. Configuración de tu conexión a MySQL local
# Cambia 'tu_usuario', 'tu_contraseña' y 'ferreteria_juan_db' por tus datos reales
USUARIO = 'frank_cafe'
PASSWORD = '1Hmh!2UEy.BE'
HOST = 'localhost' # Como estás en WSL, usualmente es localhost o 127.0.0.1
BASE_DE_DATOS = 'quality_pint' # El nombre de tu base de datos

# 2. Crear el "Motor" de conexión
cadena_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}/{BASE_DE_DATOS}"
motor = create_engine(cadena_conexion)

# 3. Crear datos falsos (Mock Data) simulando lo que extraeríamos de FoxPro
datos_falsos = {
    'customer_code': ['CLI-001', 'CLI-002'],
    'customer_segment': ['A', 'B'],
    'full_name': ['Taller El Volcán', 'Pinturas y Más S.A.'],
    'phone': ['7777-8888', '2222-3333'],
    'allows_credit': [True, False],
    'credit_limit': [500.00, 0.00],
    'max_credit_days': [30, 0]
}

# Transformamos el diccionario en un DataFrame de Pandas
df_mock = pd.DataFrame(datos_falsos)

print("Datos listos para enviar:")
print(df_mock)

# 4. Intentar cargar los datos a MySQL
try:
    print("\nConectando a la base de datos y cargando información...")
    # if_exists='append' significa que si la tabla existe, solo agrega las filas nuevas al final
    # index=False evita que pandas suba la columna de los números de fila (0, 1, 2)
    df_mock.to_sql(name='dim_customers', con=motor, if_exists='append', index=False)
    print("¡Éxito! Los datos simulados se guardaron en MySQL.")
except Exception as e:
    print(f"Ocurrió un error en la conexión o en la carga: {e}")