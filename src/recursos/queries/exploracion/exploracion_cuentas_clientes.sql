SELECT * FROM crean_aho_cte LIMIT 100;

SELECT DISTINCT producto FROM crean_aho_cte;

SELECT * FROM crean_aho_cte WHERE saldo IS NULL;

SELECT * FROM crean_aho_cte WHERE fecha is NULL;

SELECT  MAX(fecha) FROM crean_aho_cte;
SELECT  MIN(fecha) FROM crean_aho_cte;

SELECT COUNT(*) FROM crean_aho_cte;

SELECT
	fecha,
	CAST(numero_id AS TEXT) AS numero_id,
	producto,
	saldo
FROM crean_aho_cte;