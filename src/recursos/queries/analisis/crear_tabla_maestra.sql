WITH cte_crean_aho_cte AS (
    SELECT *
    FROM (
        SELECT
            numero_id,
            producto AS producto_cuenta,
            saldo AS saldo_cuenta,
            ROW_NUMBER() OVER (
                PARTITION BY numero_id
                ORDER BY fecha DESC
            ) AS rn
        FROM crean_aho_cte
    )
    WHERE rn = 1
),

cte_crean_bolsillos AS (
    SELECT *
    FROM (
        SELECT
            numero_id,
            producto AS producto_bolsillo,
            saldo AS saldo_bolsillo,
            ROW_NUMBER() OVER (
                PARTITION BY numero_id
                ORDER BY fecha DESC
            ) AS rn
        FROM crean_bolsillos
    )
    WHERE rn = 1
),

cte_crean_inv_virtual AS (
    SELECT *
    FROM (
        SELECT
            numero_id,
            producto AS producto_inv_virtual,
            saldo AS saldo_inv_virtual,
            ROW_NUMBER() OVER (
                PARTITION BY numero_id
                ORDER BY fecha DESC
            ) AS rn
        FROM crean_inv_virtual_cdt
    )
    WHERE rn = 1
),

cte_crean_fiducuenta AS (
    SELECT *
    FROM (
        SELECT
            numero_id,
            producto AS producto_fiducuenta,
            saldo AS saldo_fiducuenta,
            ROW_NUMBER() OVER (
                PARTITION BY numero_id
                ORDER BY fecha DESC
            ) AS rn
        FROM crean_fiducuenta
    )
    WHERE rn = 1
),

cte_invesbot AS (
    SELECT *
    FROM (
        SELECT
            numero_id,
            producto AS producto_invesbot,
            saldo AS saldo_invesbot,
            ROW_NUMBER() OVER (
                PARTITION BY numero_id
                ORDER BY fecha DESC
            ) AS rn
        FROM invesbot
    )
    WHERE rn = 1
)

SELECT
	clientes.numero_id,
	clientes.grupo_edad,
	clientes.desc_genero,
	clientes.desc_segmento,
	clientes.desc_tipo_de_vivienda,
	clientes.ingresos_mensuales,
	clientes.total_egresos_mensuales,
	clientes.total_activos,
	clientes.total_pasivos,
	clientes.total_patrimonio,
	cuentas_ahorro.producto_cuenta,
	cuentas_ahorro.saldo_cuenta,
	estimador_ingresos.producto AS producto_estimador,
	estimador_ingresos.estimador_ingreso,
	cuentas_bolsillo.producto_bolsillo,
	cuentas_bolsillo.saldo_bolsillo,
	cuentas_fiducuenta.producto_fiducuenta,
	cuentas_fiducuenta.saldo_fiducuenta,
	producto_invesbot.producto_invesbot,
	producto_invesbot.saldo_invesbot,
	producto_inv.producto_inv_virtual,
	producto_inv.saldo_inv_virtual,
	clientes.total_activos / clientes.total_pasivos AS liquidez,
	(clientes.ingresos_mensuales - clientes.total_egresos_mensuales) / clientes.ingresos_mensuales AS capacidad_de_ahorro,
	clientes.total_egresos_mensuales / clientes.ingresos_mensuales AS capacidad_endeudamiento,
	CASE
		WHEN 
			producto_inv.saldo_inv_virtual > 0 OR 
			producto_invesbot.saldo_invesbot > 0 OR 
			cuentas_fiducuenta.saldo_fiducuenta > 0 
		THEN 1 ELSE 0
	END AS invierte,
	(
		CASE WHEN producto_inv.saldo_inv_virtual IS NOT NULL THEN 1 ELSE 0 END +
		CASE WHEN producto_invesbot.saldo_invesbot IS NOT NULL THEN 1 ELSE 0 END +
		CASE WHEN cuentas_fiducuenta.saldo_fiducuenta IS NOT NULL THEN 1 ELSE 0 END 
	) AS cantidad_productos_inversion,
	COALESCE((COALESCE (producto_inv.saldo_inv_virtual, 0) + COALESCE(producto_invesbot.saldo_invesbot, 0) + COALESCE(cuentas_fiducuenta.saldo_fiducuenta,0)) / COALESCE(clientes.total_patrimonio,0),0) AS porcentaje_inversion
FROM clientes
LEFT JOIN cte_crean_aho_cte AS cuentas_ahorro ON clientes.numero_id = cuentas_ahorro.numero_id
LEFT JOIN estimador_ing AS estimador_ingresos ON clientes.numero_id = estimador_ingresos.numero_id
LEFT JOIN cte_crean_bolsillos AS cuentas_bolsillo ON clientes.numero_id = cuentas_bolsillo.numero_id
LEFT JOIN cte_crean_fiducuenta AS cuentas_fiducuenta ON clientes.numero_id = cuentas_fiducuenta.numero_id
LEFT JOIN cte_invesbot AS producto_invesbot ON clientes.numero_id = producto_invesbot.numero_id
LEFT JOIN cte_crean_inv_virtual AS producto_inv ON clientes.numero_id = producto_inv.numero_id
;