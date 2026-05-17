import os
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURACIÓN Y CREDENCIALES
# ==========================================
load_dotenv()

USUARIO = os.getenv('DB_USUARIO')
PASSWORD = os.getenv('DB_PASSWORD')
HOST = os.getenv('DB_HOST')
BASE_DE_DATOS = os.getenv('DB_NOMBRE')
RUTA_ORIGEN = os.getenv('RUTA_ORIGEN_DATOS')

# ==========================================
# 2. FASE DE EXTRACCIÓN (Extract)
# ==========================================
def extraer_datos():
    print(f"[1/3] Extrayendo archivos desde: {RUTA_ORIGEN}...")
    
    # NOTA: Aquí irá tu lógica real para leer el archivo .DBF
    # Por ahora, inyectamos el DataFrame simulado para mantener el motor andando
    datos_simulados = {
        'customer_code': ['CLI-001', 'CLI-002'],
        'customer_segment': ['A', 'B'],
        'full_name': ['Taller El Volcán', 'Pinturas y Más S.A.'],
        'phone': ['7777-8888', '2222-3333'],
        'allows_credit': [True, False],
        'credit_limit': [500.00, 0.00],
        'max_credit_days': [30, 0]
    }
    df = pd.DataFrame(datos_simulados)
    return df

# ==========================================
# 3. FASE DE TRANSFORMACIÓN (Transform)
# ==========================================
def transformar_datos(df):
    print("[2/3] Limpiando y transformando la información...")
    
    # Estandarización de datos para evitar errores en la base de datos
    df['full_name'] = df['full_name'].str.upper().str.strip()
    
    # Aquí puedes agregar cálculos complejos a futuro (ej. scoring crediticio)
    
    return df

# ==========================================
# 4. FASE DE CARGA (Load)
# ==========================================
def cargar_datos(df):
    print("[3/3] Conectando a MySQL y cargando datos...")
    try:
        cadena_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}/{BASE_DE_DATOS}"
        motor = create_engine(cadena_conexion)
        
        # if_exists='replace' sobrescribe la tabla para tener siempre la info al día
        df.to_sql(name='dim_customers', con=motor, if_exists='replace', index=False)
        print("✅ ¡Carga exitosa! La base de datos está lista para ser consultada.")
    except Exception as e:
        print(f"❌ Error crítico durante la carga a MySQL: {e}")

# ==========================================
# 5. ORQUESTADOR (El Botón de Encendido)
# ==========================================
def ejecutar_pipeline():
    print("=== INICIANDO MOTOR ETL ===")
    
    # El flujo de trabajo secuencial
    df_crudo = extraer_datos()
    df_limpio = transformar_datos(df_crudo)
    cargar_datos(df_limpio)
    
    print("=== PIPELINE FINALIZADO CON ÉXITO ===")

# Punto de entrada del script
if __name__ == "__main__":
    ejecutar_pipeline()