import os
import pandas as pd

# Carpeta donde buscar los archivos CSV
carpeta = "data/input/errores"

# Carpeta destino para los archivos XLSX generados
carpeta_destino = "data/output"
os.makedirs(carpeta_destino, exist_ok=True)

for archivo in os.listdir(carpeta):
    if archivo.lower().endswith('.csv'):
        ruta_csv = os.path.join(carpeta, archivo)
        nombre_base = os.path.splitext(archivo)[0]
        ruta_xlsx = os.path.join(carpeta_destino, f"{nombre_base}.xlsx")
        try:
            df = pd.read_csv(ruta_csv, dtype=str, encoding='utf-8')
        except Exception:
            df = pd.read_csv(ruta_csv, dtype=str, encoding='latin1')
        df.to_excel(ruta_xlsx, index=False)
        print(f"Convertido: {archivo} -> xlsx_generados/{nombre_base}.xlsx")