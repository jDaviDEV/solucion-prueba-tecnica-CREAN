SELECT * FROM crean_bolsillos LIMIT 100;

SELECT DISTINCT fecha FROM crean_bolsillos ORDER BY FECHA DESC;

SELECT * FROM crean_bolsillos WHERE numero_id IS NULL;
SELECT DISTINCT producto FROM crean_bolsillos;
SELECT saldo FROM crean_bolsillos WHERE SALDO IS NULL;