SELECT * FROM clientes
	WHERE desc_tipo_de_vivienda = "NO INFORMA"
LIMIT 100;

SELECT * FROM clientes
	WHERE total_patrimonio IS NULL
;

SELECT DISTINCT desc_genero FROM clientes;
SELECT DISTINCT grupo_edad FROM clientes;
SELECT DISTINCT desc_segmento FROM clientes;
SELECT DISTINCT desc_tipo_de_vivienda FROM clientes;

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

SELECT numero_id, COUNT(*) AS cantidad
FROM clientes
GROUP BY numero_id
HAVING COUNT(*) > 1;