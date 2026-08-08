import pandas as pd
from pandas import DataFrame
from pathlib import Path
from solucion.conexion_odbc.conexion import obtener_conexion
import logging
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import sqlite3

log = logging.getLogger(__name__)

def crear_cluster():
  # Conexion a la base de datos
  conn = obtener_conexion()
  
  # Ruta donde estan todas las consultas para el analisis de los datos
  ruta_queries = Path(__file__).resolve().parents[2] / "recursos" / "queries" / "analisis"
  
  # Defino esta variable tipada para facilitar el desarrollo con autocompletado de funciones de pandas
  df_tabla_kmeans: DataFrame
  
  # En este df cada registra es un cliente con toda su informacion financiera asociada, cada registro es el ultimo estado conocido
  # Del cliente
  log.info("ejecutando consulta a tabla kmeans")
  df_tabla_kmeans = pd.read_sql((ruta_queries / "consultar_tabla_kmeans.sql").read_text(encoding="utf-8"), conn)
  log.info("consulta terminada")
  conn.close()
  
  # Tomar una muestra del dataframe
  df_muestra = df_tabla_kmeans.sample(
    n=100000,
    random_state=10
  )
  
  df_muestra_copy = df_muestra.copy()
  

  variables_financieras_positivas = [
      "dinero_ahorrado",
      "dinero_invertido"
  ]
  
  df_muestra[variables_financieras_positivas] = np.log1p(
    df_muestra[variables_financieras_positivas]
  )
  
  def signed_log(x):
    """
    Transformación logarítmica que conserva el signo.

    Ejemplo:
        -1,000,000 -> valor negativo transformado
         0         -> 0
         1,000,000 -> valor positivo transformado
    """
    return np.sign(x) * np.log1p(np.abs(x))


  df_muestra["flujo_de_caja"] = signed_log(
    df_muestra["flujo_de_caja"]
  )
  
  scaler = StandardScaler()
  
  df_muestra_escalada = scaler.fit_transform(df_muestra)
  
  modelo = KMeans(
    n_clusters=4,
    random_state=10,
    n_init="auto"
  )

  modelo.fit(df_muestra_escalada)
  
  df_muestra_copy["cluster"] = modelo.labels_
  
  perfil_clusters = (
      df_muestra_copy
      .groupby("cluster")
      .agg(
          cantidad_clientes=("cluster", "count"),
  
          edad_promedio=("edad", "mean"),
  
          flujo_caja_promedio=("flujo_de_caja", "mean"),
  
          ahorro_promedio=("dinero_ahorrado", "mean"),
  
          inversion_promedio=("dinero_invertido", "mean"),
  
          invesbot_pct=("usa_invesbot", "mean"),
  
          preferencial_pct=("seg_preferencial", "mean"),
  
          plus_pct=("seg_plus", "mean"),
  
          personal_pct=("seg_personal", "mean")
      )
      .reset_index()
    )
    
  print(perfil_clusters)

  ruta_db = Path(__file__).resolve().parents[2] / "recursos" / "db" / "base_datos.db"
    
  log.info("Creando nueva base de datos")
  conn_tabla_muestra_kmeans = sqlite3.connect(ruta_db)
  log.info("Nueva base creada con exito")
  
  
  log.info(f"Creando tabla_muestra_kmeans")
  df_muestra_copy.to_sql(
      name="tabla_muestra_kmeans",
      con=conn_tabla_muestra_kmeans,
      if_exists="replace",
      index=False
  )
  log.info("Tabla creada con éxito")
  conn_tabla_muestra_kmeans.close()
  

def ejecutar_creacion_cluster():
  crear_cluster()