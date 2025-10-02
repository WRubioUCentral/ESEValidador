# generador_csv.py
import os
import csv

def generar_csv(nombre_archivo, lista_errores):
    carpeta_errores = os.path.join(os.path.dirname(nombre_archivo), "errores")
    os.makedirs(carpeta_errores, exist_ok=True)

    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    nombre_salida = os.path.join(carpeta_errores, f"{base}_errores.csv")

    with open(nombre_salida, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["usuario", "dato_erroneo", "codigo", "explicacion"])
        escritor.writeheader()
        for error in lista_errores:
            escritor.writerow(error)
