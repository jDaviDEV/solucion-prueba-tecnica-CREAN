SELECT * FROM invesbot LIMIT 100;

SELECT COUNT(*) FROM invesbot;
SELECT DISTINCT fecha FROM invesbot ORDER BY fecha DESC;
SELECT * FROM invesbot WHERE saldo IS NULL;
SELECT DISTINCT producto FROM invesbot;
SELECT * FROM invesbot WHERE numero_id IS NULL;