import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Quality Pint | Cuentas por Cobrar", page_icon="🎨", layout="wide")

# 2. Conexión a la Base de Datos (Corregido a quality_pint)
USUARIO = 'frank_cafe'
PASSWORD = '1Hmh!2UEy.BE'
HOST = 'localhost' # Como estás en WSL, usualmente es localhost o 127.0.0.1
BASE_DE_DATOS = 'quality_pint' # El nombre de tu base de datos

@st.cache_data
def obtener_datos_cobros():
    cadena_conexion = f"mysql+pymysql://{USUARIO}:{PASSWORD}@{HOST}/{BASE_DE_DATOS}"
    motor = create_engine(cadena_conexion)
    query = "SELECT * FROM vw_cuentas_por_cobrar"
    df = pd.read_sql(query, motor)
    return df

# 3. Interfaz de Usuario (UI)
st.title("📊 Panel de Cuentas por Cobrar - Quality Pint")
st.markdown("---")

try:
    df_cobros = obtener_datos_cobros()
    
    # 4. Lógica de Negocios: Calcular Días de Mora y Estado Visual
    # Convertimos las fechas de SQL a formato de fecha en Pandas
    df_cobros['Fecha_Vencimiento'] = pd.to_datetime(df_cobros['Fecha_Vencimiento'])
    hoy = pd.Timestamp(datetime.now().date())
    
    # Calculamos cuántos días han pasado desde que venció
    df_cobros['Dias_Mora'] = (hoy - df_cobros['Fecha_Vencimiento']).dt.days
    
    # Creamos un semáforo visual (Rojo vencido, Verde al día)
    def asignar_semaforo(dias):
        if dias > 0:
            return "🔴 Vencido"
        else:
            return "🟢 Al día"
            
    df_cobros['Alerta'] = df_cobros['Dias_Mora'].apply(asignar_semaforo)

    # 5. Métricas Clave (KPIs)
    total_deuda = df_cobros['Saldo_Pendiente'].sum()
    facturas_vencidas = len(df_cobros[df_cobros['Dias_Mora'] > 0])
    deuda_vencida = df_cobros[df_cobros['Dias_Mora'] > 0]['Saldo_Pendiente'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Cartera Total en la Calle", f"${total_deuda:,.2f}")
    col2.metric("Monto Vencido Crítico 🔴", f"${deuda_vencida:,.2f}")
    col3.metric("Facturas Vencidas", facturas_vencidas)
    
    st.markdown("---")

    # 6. Filtros Interactivos
    st.subheader("Buscador de Clientes y Sucursales")
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        sucursal_seleccionada = st.selectbox("Filtrar por Sucursal:", ["Todas"] + list(df_cobros['Sucursal'].unique()))
    with col_filtro2:
        cliente_buscar = st.text_input("🔍 Buscar por nombre de cliente (Ej. Volcán):")

    df_filtrado = df_cobros.copy()
    
    if sucursal_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Sucursal'] == sucursal_seleccionada]
        
    if cliente_buscar:
        df_filtrado = df_filtrado[df_filtrado['Cliente'].str.contains(cliente_buscar, case=False, na=False)]

    # 7. Limpieza final de la tabla para la pantalla
    # Formateamos las fechas y el dinero para que se vea elegante
    df_filtrado['Fecha_Emision'] = pd.to_datetime(df_filtrado['Fecha_Emision']).dt.strftime('%d-%m-%Y')
    df_filtrado['Fecha_Vencimiento'] = df_filtrado['Fecha_Vencimiento'].dt.strftime('%d-%m-%Y')
    df_filtrado['Saldo_Pendiente'] = df_filtrado['Saldo_Pendiente'].apply(lambda x: f"${x:,.2f}")
    
    # Ordenamos las columnas para mostrar las más importantes primero
    columnas_mostrar = ['Alerta', 'Sucursal', 'Cliente', 'Numero_Factura', 'Fecha_Vencimiento', 'Dias_Mora', 'Saldo_Pendiente']
    
    st.dataframe(
        df_filtrado[columnas_mostrar], 
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error(f"Error interno: {e}")