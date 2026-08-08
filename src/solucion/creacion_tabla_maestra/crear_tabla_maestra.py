import pandas as pd
from pandas import DataFrame
from pathlib import Path
from solucion.conexion_odbc.conexion import obtener_conexion
import logging
import sqlite3

log = logging.getLogger(__name__)

def crear_tabla_maestra():
  # Conexion a la base de datos
  conn = obtener_conexion()
  
  # Ruta donde estan todas las consultas para el analisis de los datos
  ruta_queries = Path(__file__).resolve().parents[2] / "recursos" / "queries" / "analisis"
  
  # Defino esta variable tipada para facilitar el desarrollo con autocompletado de funciones de pandas
  df_tabla_maestra: DataFrame
  
  # En este df cada registra es un cliente con toda su informacion financiera asociada, cada registro es el ultimo estado conocido
  # Del cliente
  log.info("ejecutando query de tabla maestra")
  df_tabla_maestra = pd.read_sql((ruta_queries / "crear_tabla_maestra.sql").read_text(encoding="utf-8"), conn)
  log.info("consulta terminada")
  conn.close()
  
  ruta_db = Path(__file__).resolve().parents[2] / "recursos" / "db" / "base_datos.db"
  
  log.info("Creando nueva base de datos limpia")
  conn_tabla_maestra = sqlite3.connect(ruta_db)
  log.info("Nueva base creada con exito")
  
  
  log.info(f"Creando tabla_maestra")
  df_tabla_maestra.to_sql(
      name="tabla_maestra",
      con=conn_tabla_maestra,
      if_exists="replace",
      index=False
  )
  log.info("Tabla creada con éxito")
  conn_tabla_maestra.close()
  
def ejecutar_creacion_tabla_maestra():
  crear_tabla_maestra()