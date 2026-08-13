import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import os

np.random.seed(42)
PARAMS ={
    "vol_sedes": 82,
    "vol_pacientes": 100000,
    "vol_encuentros": 50000,
    "fecha_inicio": datetime(2023, 1, 1),
    "fecha_fin": datetime(2024, 1, 1)
}


os.makedirs("datos_salud", exist_ok=True)

def inyectar_nulos(serie, porcentaje=0.05):
    mascara =  np.random.rand(len (serie) ) < porcentaje
    serie[mascara] = np.nan
    return serie

print("...")


ids_sedes = np.arange(1, PARAMS["vol_sedes"] +  1)
tipos_sede = np.random.choice(['Hospital', 'Clinica','Centro Medico','Diagnostico'], PARAMS["vol_sedes"])

df_sedes = pd.DataFrame({
    'id_sede': ids_sedes,
    'nom_sede': [f"Sede_{i}" for i in ids_sedes],
    'tip_sede': tipos_sede,
    'cap_camas_gen': np.random.randint(10, 100, PARAMS["vol_sedes"]),
    'cap_camas_uci': np.random.randint(0, 20, PARAMS["vol_sedes"]),
    'nivel_complejidad': np.random.choice(['Baja', 'Media', 'Alta'], PARAMS["vol_sedes"])
})

df_sedes.to_csv("datos_salud/RED_SEDES.csv", index=False)
print("RED_SEDES generado")


ids_pacientes = np.arange(1, PARAMS["vol_pacientes"] + 1)
df_pacientes = pd.DataFrame({
    'pac_id': ids_pacientes,
    'tip_doc': np.random.choice(['CC', 'TI', 'CE'], PARAMS["vol_pacientes"]),
    'num_doc_hash': [f"HASH_{np.random.randint(100000, 999999)}" for _ in range(PARAMS["vol_pacientes"])],
    'fec_nac': [PARAMS["fecha_inicio"] - timedelta(days=np.random.randint(1000, 25000)) for _ in range(PARAMS["vol_pacientes"])],
    'genero': np.random.choice(['M', 'F', 'Otro'], PARAMS["vol_pacientes"]),
    'estrato_socioec': np.random.randint(1, 7, PARAMS["vol_pacientes"])
})

idx_anomalos = np.random.choice(df_pacientes.index, 10)
df_pacientes.loc[idx_anomalos, 'fec_nac'] = datetime(2050, 1, 1)


df_pacientes['estrato_socioec'] = inyectar_nulos(df_pacientes['estrato_socioec'], 0.05)

df_pacientes.to_csv("datos_salud/PAC_REGISTRO.csv", index=False)
print("df_pacientes generado")

dias_rango = (PARAMS["fecha_fin"] - PARAMS["fecha_inicio"]).days
fechas_registro = [PARAMS["fecha_inicio"] + timedelta(days=np.random.randint(0, dias_rango)) for _ in range(PARAMS["vol_encuentros"])]

df_encuentros = pd.DataFrame({
    'id_encuentro': np.arange(1, PARAMS["vol_encuentros"] + 1),
    'pac_id': np.random.choice(ids_pacientes, PARAMS["vol_encuentros"]),
    'id_sede': np.random.choice(ids_sedes, PARAMS["vol_encuentros"]),
    'fec_registro': fechas_registro,
    'diag_principal_cie10': np.random.choice(['J00', 'A09', 'E11', 'I10', 'U071'], PARAMS["vol_encuentros"]),
    'vr_facturado': np.random.normal(50000, 15000, PARAMS["vol_encuentros"])
})


idx_anomalos_fact = np.random.choice(df_encuentros.index, 50)
df_encuentros.loc[idx_anomalos_fact, 'vr_facturado'] = -1000

df_encuentros.to_csv("datos_salud/HCE_ENCUENTROS.csv", index=False)
print("HCE_ENCUENTROS generado")
