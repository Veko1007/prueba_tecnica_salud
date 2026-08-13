SELECT 
    nom_sede,
    diagnostico,
    genero,
    COUNT(id_encuentro) AS total_consultas,
    SUM(vr_facturado) AS total_facturado
FROM gold_analisis_epidemiologico
GROUP BY 
