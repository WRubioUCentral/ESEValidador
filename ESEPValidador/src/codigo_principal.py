# codigo_principal.py
"""
Módulo principal para validar archivos ESE según Resolución 202 de 2021
Genera reportes de errores directamente en formato Excel
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al sys.path
# para que Python pueda encontrar el módulo 'config'
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from validador_completo import validar_archivo_ese
from config.config import INPUT_DIR  # Importar la ruta desde config
from generador_excel import generar_reporte_excel

CARPETA_BASE = INPUT_DIR  # Usar la ruta configurada

def procesar_documentos():
    """
    Procesa todos los archivos Excel en la carpeta INPUT_DIR
    y genera reportes de validación según Resolución 202 de 2021
    """
    archivos_procesados = 0
    archivos_con_errores = 0

    print(f"\n{'='*80}")
    print(f"VALIDADOR ESE - RESOLUCIÓN 202 DE 2021")
    print(f"{'='*80}")
    print(f"Carpeta de entrada: {CARPETA_BASE}")
    print(f"{'='*80}\n")

    for archivo in os.listdir(CARPETA_BASE):
        if archivo.endswith(".xlsx") or archivo.endswith(".xls"):
            ruta = os.path.join(CARPETA_BASE, archivo)
            print(f"Procesando: {archivo}...")

            try:
                df = pd.read_excel(ruta, header=None)
                df = df.iloc[1:]  # Omitir la primera fila que contiene los títulos de las columnas

                fecha_corte = pd.Timestamp("2025-09-30")

                # Aplicar validaciones según Resolución 202 de 2021
                resultado_validacion = validar_archivo_ese(df, fecha_corte)
                errores = resultado_validacion['errores']
                warnings = resultado_validacion.get('warnings', [])

                archivos_procesados += 1

                # Generar Excel con los errores detectados
                if errores or warnings:
                    generar_reporte_excel(ruta, errores, warnings)
                    archivos_con_errores += 1
                else:
                    print(f"  ✓ Sin errores detectados en {archivo}")

            except Exception as e:
                print(f"  ✗ Error al procesar {archivo}: {str(e)}")

    print(f"\n{'='*80}")
    print(f"RESUMEN DE PROCESAMIENTO")
    print(f"{'='*80}")
    print(f"Archivos procesados: {archivos_procesados}")
    print(f"Archivos con errores: {archivos_con_errores}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    procesar_documentos()