import os
import pandas as pd
from sqlalchemy import create_engine, text
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
        'customer_code': ['CLI-001', 'CLI-002', 'CLI-003'],
        'customer_segment': ['A', 'B', 'C'],
        'full_name': ['Taller El Volcán', 'Pinturas y Más S.A.', 'Constructora La Cima'],
        'phone': ['7777-8888', '2222-3333', '2525-9999'],
        'allows_credit': [True, False, True],
        'credit_limit': [500.00, 0.00, 1500.00],
        'max_credit_days': [30, 0, 45]
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
    print("[3/3] Conectando a MySQL y ejecutando estrategia UPSERT...")
    try:
        cadena_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}/{BASE_DE_DATOS}"
        motor = create_engine(cadena_conexion)
        
        # PASO A: Cargar a la Zona de Aterrizaje (Staging Area)
        # Aquí usamos 'replace' porque stg_customers es una tabla temporal sin llaves foráneas
        df.to_sql(name='stg_customers', con=motor, if_exists='replace', index=False)
        print("   -> Datos extraídos depositados en stg_customers (Zona temporal).")
        
        # PASO B: Ejecutar el UPSERT hacia la tabla de Dimensiones final
        # Este código SQL revisa: si el código de cliente ya existe, actualiza sus datos. Si no, lo inserta nuevo.
        query_upsert = text("""
            INSERT INTO dim_customers (customer_code, customer_segment, full_name, phone, allows_credit, credit_limit, max_credit_days)
            SELECT customer_code, customer_segment, full_name, phone, allows_credit, credit_limit, max_credit_days
            FROM stg_customers
            ON DUPLICATE KEY UPDATE
            customer_segment = VALUES(customer_segment),
            full_name = VALUES(full_name),
            phone = VALUES(phone),
            allows_credit = VALUES(allows_credit),
            credit_limit = VALUES(credit_limit),
            max_credit_days = VALUES(max_credit_days);
        """)
        
        # Ejecutamos el query de forma segura (Transacción)
        with motor.begin() as conexion:
            conexion.execute(query_upsert)
            
        print("✅ ¡Carga exitosa! Clientes nuevos insertados y existentes actualizados.")
        
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