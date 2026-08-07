# Solución a la prueba técnica Analítico I CREAN

## Crear una sola base de datos

Los datos están dispersos en distintas bases, lo cual resulta incomodo y poco práctico, ya que cada base solo tiene una tabla. Todas las bases comparten un mismo contexto, por lo que resulta apropiado unirlas.

Para facilitar el trabajo con las bases de datos se procede a consolidar toda la información en un solo archivo .db de sqlite3 que permita realizar consultar SQL
estableciendo una sola conexión de ODBC desde Python. Además también resulta útil para crear un DSN de ODBC Driver en windows para hacer Business Intelligence con Power BI al obtener datos de orígenes ODBC.

---

## Exploración de los datos

Ya que se tiene toda la información consolidada en solo archiv .db, se puede hacer una exploración de los datos utilizando la herramienta DB Browser for SQLite.

### tabla clientes
- El campo de numero_id se debe reemplazar a tipo texto ya que el valor entero es muy grande y algunas herramientas de visualización de datos llegan a su límite y reemplaza todos los id por un valor predeterminado.
  
- El campo desc_genero presenta valores nulos equivalentes al 0.011% de la población. Debido a su baja representatividad y con el fin de evitar imputaciones basadas en supuestos no observados, dichos registros fueron excluidos del análisis.
<br>
<br>
- El campo desc_tipo_de_vivienda presenta un 68.79% de valores nulos. Debido a que existe la categoría de negocio "NO INFORMA" y los registros nulos representan ausencia de información reportada por el cliente, los valores nulos fueron homologados a dicha categoría. No se consideró la eliminación de registros debido a la alta proporción de casos afectados ni la imputación hacia categorías como "PROPIA" o "ARRENDADA", ya que esto introduciría información no observada y potenciales sesgos en el análisis.
<br>
<br>
- Los campos ingresos_mensuales, total_egresos_mensuales, total_activos, total_pasivos y total_patrimonio presentan valores nulos, que no representan una cifra significativa en la población de los datos, por lo que se pueden eliminar esos registros sin afectar el modelo.

### cantidad de datos nulos
| total_clientes | # nulos_ingresos | # nulos_egresos | # nulos_activos | # nulos_pasivos | # nulos_patrimonio |
 :---: | :---: | :---: | :---: | :---: |:---: |
|860231| 249 | 249 |249 |249 |260 |

### porcentaje de datos nulos

| total_clientes | % nulos_ingresos | % nulos_egresos | % nulos_activos | % nulos_pasivos | % nulos_patrimonio |
| :---: | :---: | :---: | :---: | :---: |:---: |
|860231| 0.029 | 0.029 | 0.029 | 0.029 | 0.03 |

NOTA: Tras eliminar los registros con esos campos nulos, nos queda un dataset de 859878 registros de clientes.

#### Query empleado para obtener estos datos:
```SQL
WITH num_clientes_nulos AS (
SELECT
  COUNT(*) total_clientes,
	CAST(SUM(CASE WHEN desc_tipo_de_vivienda IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_vivienda",
	CAST(SUM(CASE WHEN desc_genero IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_genero",
  CAST(SUM(CASE WHEN ingresos_mensuales IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_ingresos",
	CAST(SUM(CASE WHEN total_egresos_mensuales IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_egresos",
  CAST(SUM(CASE WHEN total_activos IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_activos",
	CAST(SUM(CASE WHEN total_pasivos IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_pasivos",
	CAST(SUM(CASE WHEN total_patrimonio IS NULL THEN 1 ELSE 0 END) AS REAL) AS "# nulos_patrimonio"
FROM clientes )
SELECT
	total_clientes,
	"# nulos_vivienda",
	CAST(("# nulos_vivienda" / "total_clientes") * 100.0 AS REAL) AS "% nulos_vivienda",
	"# nulos_genero",
	CAST(("# nulos_genero" / "total_clientes") * 100.0 AS REAL) AS "% nulos_genero",
	"# nulos_ingresos",
	CAST(("# nulos_ingresos" / "total_clientes") * 100.0 AS REAL) AS "% nulos_ingresos",
	"# nulos_egresos",
	CAST(("# nulos_egresos" / "total_clientes") * 100.0 AS REAL) AS "% nulos_egresos",
	"# nulos_activos",
	CAST(("# nulos_activos" / "total_clientes") * 100.0 AS REAL) AS "% nulos_activos",
	"# nulos_pasivos",
	CAST(("# nulos_pasivos" / "total_clientes") * 100.0 AS REAL) AS "% nulos_pasivos",
	"# nulos_patrimonio",
	CAST(("# nulos_patrimonio" / "total_clientes") * 100.0 AS REAL) AS "% nulos_patrimonio"
FROM num_clientes_nulos;
```

### Otras tablas
- crean_aho_cte
- crean_bolsillos
- crean_fiducuenta
- crean_inv_virtual_cdt
- estimador_ing
- invesbot

Dentro de estas tablas también es necesario cambiar el tipo de dato del campo numero_id por tipo texto. Estas tablas no tiene valores nulos, pero se observa que las fechas no son continuas, lo que complica la creación de un modelo predictivo.

---