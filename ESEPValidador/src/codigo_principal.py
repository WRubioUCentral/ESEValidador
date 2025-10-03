# codigo_principal.py
import os
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al sys.path
# para que Python pueda encontrar el módulo 'config'
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from validador_completo import validar_archivo_ese
from config.config import INPUT_DIR # Importar la ruta desde config
from generador_csv import generar_csv

CARPETA_BASE = INPUT_DIR # Usar la ruta configurada

def procesar_documentos():
    for archivo in os.listdir(CARPETA_BASE):
        if archivo.endswith(".xlsx"):
            ruta = os.path.join(CARPETA_BASE, archivo)
            df = pd.read_excel(ruta, header=None)
            df = df.iloc[1:]  # Omitir la primera fila que contiene los títulos de las columnas

            fecha_corte = pd.Timestamp("2025-08-31")
            
            # Aplicar validaciones
            resultado_validacion = validar_archivo_ese(df, fecha_corte)
            errores = resultado_validacion['errores']

            # Generar CSV con los errores detectados
            if errores:
                generar_csv(ruta, errores)

if __name__ == "__main__":
    procesar_documentos()