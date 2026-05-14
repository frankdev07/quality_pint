# etl_customers.py (Refactorizado con Seguridad)

import pandas as pd
from sqlalchemy import create_engine
import pymysql
import os
from dotenv import load_dotenv

# 1. Cargar las credenciales desde el archivo secreto .env
load_dotenv()

USUARIO = os.getenv('DB_USUARIO')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
BASE_DE_DATOS = os.getenv('DB_NOMBRE')

# 2. Crear el "Motor" de conexión usando las variables seguras
try:
    cadena_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}/{BASE_DE_DATOS}"
    motor = create_engine(cadena_conexion)
    print(f"✅ Motor de conexión configurado para la base: {BASE_DE_DATOS}")
except Exception as e:
    print(f"❌ Error al configurar el motor: {e}")

# 3. Datos de prueba (Esto luego vendrá de la extracción real de FoxPro)
datos_falsos = {
    'customer_code': ['CLI-001', 'CLI-002'],
    'customer_segment': ['A', 'B'],
    'full_name': ['Taller El Volcán', 'Pinturas y Más S.A.'],
    'phone': ['7777-8888', '2222-3333'],
    'allows_credit': [True, False],
    'credit_limit': [500.00, 0.00],
    'max_credit_days': [30, 0]
}

df_mock = pd.DataFrame(datos_falsos)

# 4. Proceso de Carga
try:
    print(f"\nIniciando carga de {len(df_mock)} registros en 'dim_customers'...")
    
    # Usamos el motor seguro
    df_mock.to_sql(
        name='dim_customers', 
        con=motor, 
        if_exists='append', 
        index=False
    )
    
    print("¡Éxito! Los datos se guardaron correctamente sin exponer credenciales.")
except Exception as e:
    print(f"Ocurrió un error en la conexión o en la carga: {e}")