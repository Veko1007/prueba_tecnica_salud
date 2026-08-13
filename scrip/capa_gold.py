CREATE VIEW gold_analisis_epidemiologico AS
SELECT 
    fc.id_encuentro,
    fc.fec_registro,
    fc.diag_principal_cie10 AS diagnostico,
    ds.nom_sede,
    ds.nivel_complejidad,
    dp.genero,
    dp.estrato_socioec,
    fc.vr_facturado
FROM HCE_ENCUENTROS fc
INNER JOIN PAC_REGISTRO dp ON fc.pac_id = dp.pac_id
INNER JOIN RED_SEDES ds ON fc.id_sede = ds.id_sede;
