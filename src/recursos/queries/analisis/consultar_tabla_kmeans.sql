SELECT
	edad,
	seg_preferencial,
	seg_plus,
	seg_personal,
	flujo_de_caja,
	dinero_ahorrado,
	dinero_invertido,
	usa_invesbot
FROM tabla_kmeans
WHERE dinero_ahorrado >= 0;