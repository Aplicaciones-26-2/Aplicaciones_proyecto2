import pandas as pd

excel = "data/raw/Siniestros_viales/SIGAT_ANUARIO_2024.xlsx"

print("Leyendo el Excel, esto se demora unos minutos...")
archivo = pd.read_excel(excel, sheet_name=0)

archivo.to_csv(excel.replace(".xlsx", ".csv.gz"), index=False)
print("Listo:", archivo.shape)
    