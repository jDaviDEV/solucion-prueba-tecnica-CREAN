SELECT
  CAST(numero_id AS TEXT) as numero_id,
  grupo_edad,
  desc_genero,
  desc_segmento,
  desc_tipo_de_vivienda,
  ingresos_mensuales,
  total_egresos_mensuales,
  total_activos,
  total_pasivos,
  total_patrimonio
FROM clientes;
