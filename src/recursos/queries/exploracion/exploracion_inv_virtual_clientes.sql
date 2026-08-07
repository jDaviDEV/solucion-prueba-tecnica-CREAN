SELECT * FROM crean_inv_virtual_cdt LIMIT 100;

SELECT DISTINCT fecha FROM crean_inv_virtual_cdt ORDER BY FECHA DESC;

SELECT * FROM crean_inv_virtual_cdt WHERE numero_id IS NULL;
SELECT DISTINCT producto FROM crean_inv_virtual_cdt;
SELECT saldo FROM crean_inv_virtual_cdt WHERE SALDO IS NULL;

SELECT COUNT(*) FROM crean_inv_virtual_cdt;