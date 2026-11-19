import pandas as pd

carpeta = "data/raw/Siniestros_viales/SIGAT_ANUARIO_2024.xlsx"

df = pd.read_excel(carpeta, sheet_name=0)

df.to_csv(carpeta.replace(".xlsx", ".csv.gz"), index=False)