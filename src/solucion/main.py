from solucion.etl.limpieza_de_datos import ejecutar_limpieza
from solucion.logging_config import Logger

log = Logger().get_logger()

def main():
  
  log.info("Iniciando ejecución")
  ejecutar_limpieza()
  log.info("Ejecución finalizada correctamente")

if __name__ == "__main__":
  main()