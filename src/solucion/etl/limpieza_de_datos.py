import pandas as pd
from pandas import DataFrame
from pathlib import Path
from solucion.conexion_odbc.conexion import obtener_conexion
import logging
import sqlite3

log = logging.getLogger(__name__)

def limpiar_datos() -> dict:
  # Conexion a la base de datos
  # He creado un DSN de ODBC en Windows que apunta al archivo base_datos.db de sqlite3
  conn = obtener_conexion()

  # Ruta donde estan todas las consultas para las etl
  ruta_queries = Path(__file__).resolve().parents[2] / "recursos" / "queries" / "etl"

  # Defino esta variable tipada para facilitar el desarrollo con autocompletado de funciones de pandas
  df_clientes: DataFrame

  # Crear un dataframe que contenga todos los clientes
  log.info("Creando dataframe con los datos del cliente")
  df_clientes = pd.read_sql((ruta_queries / "extraccion_clientes.sql").read_text(encoding="utf-8"), conn)
  log.info("Se ha creaqdo el dataframe: df_clientes")

  # Eliminar registros con datos nulos
  log.info("Eliminando registros con datos nulos en df_clientes")
  df_clientes = df_clientes.dropna(subset=["desc_genero","ingresos_mensuales","total_egresos_mensuales","total_activos","total_pasivos","total_patrimonio"])
  log.info("Se han eliminado los registros con datos nulos en df_clientes")
  
  # Reemplazar nulos en desc_tipo_de_vivienda
  log.info("Reemplazando campos nulos desc_tipo_de_vivienda en df_clientes")
  df_clientes["desc_tipo_de_vivienda"] = df_clientes["desc_tipo_de_vivienda"].fillna("NO INFORMA")
  log.info("Se ha reemplazado los campos nulos correctamente")
  
  # Eliminar registros duplicados y conservar el primero
  df_clientes = df_clientes.drop_duplicates(subset=["numero_id"], keep="first")

  # Nuevos df de las otras tablas con el campo numero id como formato texto
  log.info("Creando dataframes con los datos de cuentas, bolsillos, fiducuentas, inversiones virtuales, estimador e invesbot")
  df_crean_aho_cte = pd.read_sql((ruta_queries / "extraccion_crean_aho_cte.sql").read_text(encoding="utf-8"), conn)
  df_crean_bolsillo = pd.read_sql((ruta_queries / "extraccion_crean_bolsillo.sql").read_text(encoding="utf-8"), conn)
  df_crean_fiducuenta = pd.read_sql((ruta_queries / "extraccion_crean_fiducuenta.sql").read_text(encoding="utf-8"), conn)
  df_crean_inv_virtual_cdt = pd.read_sql((ruta_queries / "extraccion_crean_inv_virtual_cdt.sql").read_text(encoding="utf-8"), conn)
  df_estimador = pd.read_sql((ruta_queries / "extraccion_estimador.sql").read_text(encoding="utf-8"), conn)
  df_invesbot = pd.read_sql((ruta_queries / "extraccion_invesbot.sql").read_text(encoding="utf-8"), conn)
  conn.close()
  log.info("Dataframes creados correctamente")
  
  return dict({
    "clientes": df_clientes,
    "crean_aho_cte": df_crean_aho_cte,
    "crean_bolsillos": df_crean_bolsillo,
    "crean_inv_virtual_cdt": df_crean_inv_virtual_cdt,
    "crean_fiducuenta": df_crean_fiducuenta,
    "invesbot": df_invesbot,
    "estimador_ing": df_estimador
  })

def crear_base_datos_limpia() -> None:
  dict_de_df = limpiar_datos()
  
  ruta_db = Path(__file__).resolve().parents[2] / "recursos" / "db" / "base_datos.db"

  # Si ya existe el archivo, entonces lo eliminamos
  if ruta_db.exists():
    ruta_db.unlink()
  
  log.info("Creando nueva base de datos limpia")
  conn_limpia = sqlite3.connect(ruta_db)
  log.info("Nueva base creada con exito")
  
  for nombre_tabla, df in dict_de_df.items():
    log.info(f"Creando tabla {nombre_tabla}")
    df.to_sql(
        name=nombre_tabla,
        con=conn_limpia,
        if_exists="replace",
        index=False
    )
    log.info("Tabla creada con éxito")
  conn_limpia.close()

def ejecutar_limpieza():
  crear_base_datos_limpia()