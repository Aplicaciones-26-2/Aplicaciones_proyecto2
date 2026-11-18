import pandas as pd

carpeta = "data/raw/Siniestros_viales/"

print("Leyendo el Excel, esto se demora unos minutos...")
hojas = pd.read_excel(carpeta + "SIGAT_ANUARIO_2024.xlsx", sheet_name=None)

for nombre, df in hojas.items():
    df.to_csv(f"{carpeta}SIGAT_ANUARIO_2024_{nombre}.csv.gz", index=False)
    print("Listo:", nombre, df.shape)