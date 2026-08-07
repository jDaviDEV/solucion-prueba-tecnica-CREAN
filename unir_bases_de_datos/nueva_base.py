"""
IMPORTANTE: Este script de python fue usado unicamente para unir
las bases de datos en una sola base, y asi crear un DSN en el ODBC Driver
de windows para facilitar el trabajo en el proyecto.

Si ya cuentas con el archivo base_datos.db, no ejecutes este script.
"""

import sqlite3
from pathlib import Path

# Carpeta donde están las bases
ruta_db = Path(__file__).resolve().parents[1] / "src" / "recursos" / "db"

# Base consolidada
archivo_destino = ruta_db / "base_datos.db"

# Si existe una consolidación previa, la eliminamos
if archivo_destino.exists():
    archivo_destino.unlink()

# Crear nueva base
conn_dest = sqlite3.connect(archivo_destino)
cur_dest = conn_dest.cursor()

# Recorrer todas las bases
for archivo_db in ruta_db.glob("*.db"):

    if archivo_db.name == "base_datos.db":
        continue

    print(f"Procesando {archivo_db.name}")

    conn_src = sqlite3.connect(archivo_db)
    cur_src = conn_src.cursor()

    # Obtener definición de la tabla
    cur_src.execute("""
        SELECT name, sql
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tabla = cur_src.fetchone()

    if not tabla:
        conn_src.close()
        continue

    nombre_tabla, create_sql = tabla

    print(f"  Copiando tabla: {nombre_tabla}")

    # Crear tabla en la base consolidada
    cur_dest.execute(create_sql)

    # Copiar datos
    filas = cur_src.execute(
        f"SELECT * FROM {nombre_tabla}"
    ).fetchall()

    if filas:

        placeholders = ",".join(
            ["?"] * len(filas[0])
        )

        cur_dest.executemany(
            f"INSERT INTO {nombre_tabla} VALUES ({placeholders})",
            filas
        )

    conn_src.close()

conn_dest.commit()
conn_dest.close()

print("\nBase consolidada creada:", archivo_destino)