# 📊 Sistema Automatizado de Ingesta de Datos & Panel Financiero (ETL)

## 📌 Resumen Ejecutivo
Este proyecto es una solución integral de Inteligencia de Negocios diseñada para modernizar la gestión de cuentas por cobrar. El sistema extrae automáticamente información crítica de sistemas legacy (archivos `.dbf` tipo FoxPro), limpia los datos, y los consolida en una base de datos relacional moderna. El resultado final es un panel de control interactivo que permite a la gerencia tomar decisiones financieras en tiempo real sin requerir horas de procesamiento manual.

## 🏗️ Arquitectura del Pipeline (ETL)

El núcleo del proyecto es un pipeline de datos robusto construido en Python, estructurado en tres fases:

1. **Extract (Extracción):** Lectura automatizada de archivos crudos depositados por el sistema legacy en un directorio local seguro.
2. **Transform (Transformación):** Estandarización de cadenas de texto, limpieza de valores nulos y preparación de estructuras de datos utilizando Pandas.
3. **Load (Carga con Integridad Referencial):** 
   * Implementación de una **Staging Area** (`stg_customers`) temporal.
   * Ejecución de algoritmo **UPSERT** (Update + Insert) vía SQL puro. Esto garantiza que los clientes nuevos se agreguen y los existentes se actualicen, sin destruir el historial de llaves foráneas (`Foreign Keys`) atadas a la tabla de facturación transaccional.

## 🛡️ Características de Nivel de Producción
* **Orquestación Autónoma:** Script configurado para ejecutarse diariamente mediante el Programador de Tareas de Windows (vía `.bat` hacia entorno WSL).
* **Seguridad de Credenciales:** Aislamiento total de cadenas de conexión y variables de entorno utilizando `.env`, garantizando que ninguna contraseña ni dato sensible del cliente toque el control de versiones.
* **Manejo de Excepciones:** Bloques `try/except` que aseguran una finalización limpia ("Graceful Degradation") del script en caso de caída del servidor MySQL, protegiendo los datos contra corrupción.

## 💻 Stack Tecnológico
* **Lenguaje:** Python 3.10.12
* **Base de Datos:** MySQL (con SQLAlchemy y PyMySQL)
* **Procesamiento de Datos:** Pandas
* **Visualización:** Streamlit
* **Entorno & Control de Versiones:** WSL (Ubuntu), Git, GitHub

## 🚀 Instalación y Ejecución Local

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/frankdev07/quality_pint.git](https://github.com/frankdev07/quality_pint.git)