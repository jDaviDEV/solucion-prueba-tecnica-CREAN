import pyodbc
import logging

log = logging.getLogger(__name__)

def obtener_conexion() -> pyodbc.Connection:
  try:
    log.info("Estableciendo conexion con la base de datos")
    conn = pyodbc.connect("DSN=CREAN;")
    log.info("Conexión exitosa")
    print("Conexión exitosa")
  except Exception as e:
    log.error(f"No se pudo establecer conexion con la base de datos: {e}", exc_info=True)
    print(f"La conexion a la base de datos ha fallado:\n{e}")
  
  return conn