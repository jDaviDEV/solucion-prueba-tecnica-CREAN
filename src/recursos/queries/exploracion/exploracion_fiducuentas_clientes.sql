SELECT * FROM crean_fiducuenta LIMIT 100;

SELECT DISTINCT fecha FROM crean_fiducuenta ORDER BY FECHA DESC;

SELECT * FROM crean_fiducuenta WHERE numero_id IS NULL;
SELECT DISTINCT producto FROM crean_fiducuenta;
SELECT saldo FROM crean_fiducuenta WHERE SALDO IS NULL;