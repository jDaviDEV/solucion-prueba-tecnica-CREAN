SELECT
	CASE
		WHEN grupo_edad = "18-25" THEN ABS(RANDOM()) % 8 + 18
		WHEN grupo_edad = "26-35" THEN ABS(RANDOM()) % 10 + 26
		WHEN grupo_edad = "36-49" THEN ABS(RANDOM()) % 14 + 36
		WHEN grupo_edad = "50-65" THEN ABS(RANDOM()) % 16 + 50
		WHEN grupo_edad = "65+" THEN ABS(RANDOM()) % 16 + 66
	END AS edad,
	CASE WHEN desc_segmento = "preferencial" THEN 1 ELSE 0 END AS seg_preferencial,
	CASE WHEN desc_segmento = "plus" THEN 1 ELSE 0 END AS seg_plus,
	CASE WHEN desc_segmento = "personal" THEN 1 ELSE 0 END AS seg_personal,
	COALESCE(ingresos_mensuales - total_egresos_mensuales, 0) AS flujo_de_caja,
	COALESCE(saldo_cuenta + saldo_bolsillo, 0) AS dinero_ahorrado,
	COALESCE(saldo_fiducuenta + saldo_inv_virtual, 0) AS dinero_invertido,
	CASE WHEN saldo_invesbot > 0 THEN 1 ELSE 0 END AS usa_invesbot
FROM tabla_maestra;