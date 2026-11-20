import pandas as pd

carpeta = "data/raw/Siniestros_viales/"

hojas = pd.read_excel(carpeta + "SIGAT_ANUARIO_2024.xlsx", sheet_name=None)

for nombre, df in hojas.items():
    df.to_csv(carpeta + "SIGAT_ANUARIO_2024_" + nombre + ".csv.gz", index=False)
