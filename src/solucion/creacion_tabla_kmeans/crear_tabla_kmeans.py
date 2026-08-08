import pandas as pd
from pandas import DataFrame
from pathlib import Path
from solucion.conexion_odbc.conexion import obtener_conexion
import logging
import sqlite3

log = logging.getLogger(__name__)

def crear_tabla_kmeans():
  # Conexion a la base de datos
  conn = obtener_conexion()
  
  # Ruta donde estan todas las consultas para el analisis de los datos
  ruta_queries = Path(__file__).resolve().parents[2] / "recursos" / "queries" / "analisis"
  
  # Defino esta variable tipada para facilitar el desarrollo con autocompletado de funciones de pandas
  df_tabla_kmeans: DataFrame
  
  # En este df cada registra es un cliente con toda su informacion financiera asociada, cada registro es el ultimo estado conocido
  # Del cliente
  log.info("ejecutando query de tabla kmeans")
  df_tabla_kmeans = pd.read_sql((ruta_queries / "crear_tabla_kmeans.sql").read_text(encoding="utf-8"), conn)
  log.info("consulta terminada")
  conn.close()
  
  ruta_db = Path(__file__).resolve().parents[2] / "recursos" / "db" / "base_datos.db"
  
  log.info("Creando nueva base de datos")
  conn_tabla_kmeans = sqlite3.connect(ruta_db)
  log.info("Nueva base creada con exito")
  
  
  log.info(f"Creando tabla_kmeans")
  df_tabla_kmeans.to_sql(
      name="tabla_kmeans",
      con=conn_tabla_kmeans,
      if_exists="replace",
      index=False
  )
  log.info("Tabla creada con éxito")
  conn_tabla_kmeans.close()
  
def ejecutar_creacion_tabla_kmeans():
  crear_tabla_kmeans()