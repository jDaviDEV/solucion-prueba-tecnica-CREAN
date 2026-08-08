from solucion.etl.limpieza_de_datos import ejecutar_limpieza
from solucion.creacion_tabla_maestra.crear_tabla_maestra import ejecutar_creacion_tabla_maestra
from solucion.creacion_tabla_kmeans.crear_tabla_kmeans import ejecutar_creacion_tabla_kmeans
from solucion.analisis_de_cluster.cluster import ejecutar_creacion_cluster
from solucion.logging_config import Logger

log = Logger().get_logger()

def main():
  
  log.info("Iniciando ejecución")
  ejecutar_limpieza()
  ejecutar_creacion_tabla_maestra()
  ejecutar_creacion_tabla_kmeans()
  ejecutar_creacion_cluster()
  log.info("Ejecución finalizada correctamente")

if __name__ == "__main__":
  main()