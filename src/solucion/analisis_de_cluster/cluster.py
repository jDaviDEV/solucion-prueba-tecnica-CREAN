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
  
  # Escalar los datos de la muestra
  scaler = StandardScaler()
  
  df_muestra_escalada = scaler.fit_transform(df_muestra)
  
  # Entrenar Kmeans
  modelo = KMeans(
    n_clusters = 5,
    random_state = 10,
    n_init = "auto"
  )
  
  modelo.fit(df_muestra_escalada)
  
  df_muestra["cluster"] = modelo.labels_
  
  # perfil_jovenes = df_muestra[
  #   df_muestra["edad_18-25"] == 1
  # ].groupby("cluster").agg(
  #   cantidad_clientes=("cluster", "size"),
  #   ingresos_promedio=("ingresos_mensuales", "mean"),
  #   patrimonio_promedio=("total_patrimonio", "mean"),
  #   ahorro_promedio=("saldo_cuenta", "mean"),
  #   bolsillos_promedio=("saldo_bolsillo", "mean"),
  #   invesbot_promedio=("saldo_invesbot", "mean"),
  #   inv_virtual=("saldo_inv_virtual", "mean"),
  #   fiducuenta=("saldo_fiducuenta", "mean")
  # ).reset_index()
  
  # perfil_adulto_joven = df_muestra[
  #   df_muestra["edad_26-35"] == 1
  # ].groupby("cluster").agg(
  #   cantidad_clientes=("cluster", "size"),
  #   ingresos_promedio=("ingresos_mensuales", "mean"),
  #   patrimonio_promedio=("total_patrimonio", "mean"),
  #   ahorro_promedio=("saldo_cuenta", "mean"),
  #   bolsillos_promedio=("saldo_bolsillo", "mean"),
  #   invesbot_promedio=("saldo_invesbot", "mean"),
  #   inv_virtual=("saldo_inv_virtual", "mean"),
  #   fiducuenta=("saldo_fiducuenta", "mean")
  # ).reset_index()
  
  # perfil_mediana_edad = df_muestra[
  #   df_muestra["edad_36-49"] == 1
  # ].groupby("cluster").agg(
  #   cantidad_clientes=("cluster", "size"),
  #   ingresos_promedio=("ingresos_mensuales", "mean"),
  #   patrimonio_promedio=("total_patrimonio", "mean"),
  #   ahorro_promedio=("saldo_cuenta", "mean"),
  #   bolsillos_promedio=("saldo_bolsillo", "mean"),
  #   invesbot_promedio=("saldo_invesbot", "mean"),
  #   inv_virtual=("saldo_inv_virtual", "mean"),
  #   fiducuenta=("saldo_fiducuenta", "mean")
  # ).reset_index()
  
  # perfil_adulto_mayor = df_muestra[
  #   df_muestra["edad_50-65"] == 1
  # ].groupby("cluster").agg(
  #   cantidad_clientes=("cluster", "size"),
  #   ingresos_promedio=("ingresos_mensuales", "mean"),
  #   patrimonio_promedio=("total_patrimonio", "mean"),
  #   ahorro_promedio=("saldo_cuenta", "mean"),
  #   bolsillos_promedio=("saldo_bolsillo", "mean"),
  #   invesbot_promedio=("saldo_invesbot", "mean"),
  #   inv_virtual=("saldo_inv_virtual", "mean"),
  #   fiducuenta=("saldo_fiducuenta", "mean")
  # ).reset_index()
  
  # perfil_ancianos = df_muestra[
  #   df_muestra["edad_65+"] == 1
  # ].groupby("cluster").agg(
  #   cantidad_clientes=("cluster", "size"),
  #   ingresos_promedio=("ingresos_mensuales", "mean"),
  #   patrimonio_promedio=("total_patrimonio", "mean"),
  #   ahorro_promedio=("saldo_cuenta", "mean"),
  #   bolsillos_promedio=("saldo_bolsillo", "mean"),
  #   invesbot_promedio=("saldo_invesbot", "mean"),
  #   inv_virtual=("saldo_inv_virtual", "mean"),
  #   fiducuenta=("saldo_fiducuenta", "mean")
  # ).reset_index()
        
  # print("perfil jovenes\n")
  # print(perfil_jovenes)
  # print("perfil adulto joven\n")
  # print(perfil_adulto_joven)
  # print("perfil mediana edad\n")
  # print(perfil_mediana_edad)
  # print("perfil adulto mayor\n")
  # print(perfil_adulto_mayor)
  # print("perfil ancianos\n")
  # print(perfil_ancianos)
  
  ruta_db = Path(__file__).resolve().parents[2] / "recursos" / "db" / "base_datos.db"
    
  log.info("Creando nueva base de datos")
  conn_tabla_muestra_kmeans = sqlite3.connect(ruta_db)
  log.info("Nueva base creada con exito")
  
  
  log.info(f"Creando tabla_muestra_kmeans")
  df_muestra.to_sql(
      name="tabla_muestra_kmeans",
      con=conn_tabla_muestra_kmeans,
      if_exists="replace",
      index=False
  )
  log.info("Tabla creada con éxito")
  conn_tabla_muestra_kmeans.close()
  

def ejecutar_creacion_cluster():
  crear_cluster()