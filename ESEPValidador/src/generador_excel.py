# generador_excel.py
"""
Módulo para generar reportes de errores en formato Excel con:
1. Hoja de errores detallados
2. Hoja de tabla de frecuencia/distribución de errores
"""
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

def generar_reporte_excel(nombre_archivo, lista_errores, lista_warnings=None):
    """
    Genera un archivo Excel con dos hojas:
    - Errores: Lista detallada de errores encontrados
    - Distribución: Tabla de frecuencia de errores por código

    Args:
        nombre_archivo: Ruta del archivo original validado
        lista_errores: Lista de diccionarios con errores encontrados
        lista_warnings: Lista de diccionarios con advertencias (opcional)
    """
    # Determinar la carpeta de salida
    from config.config import OUTPUT_DIR

    # Crear carpeta output si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generar nombre del archivo de salida
    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_salida = os.path.join(OUTPUT_DIR, f"{base}_reporte_errores_{timestamp}.xlsx")

    # Crear el archivo Excel con múltiples hojas
    with pd.ExcelWriter(nombre_salida, engine='openpyxl') as writer:

        # HOJA 1: Errores Detallados
        if lista_errores:
            df_errores = pd.DataFrame(lista_errores)
            df_errores = df_errores[["codigo", "usuario", "dato_erroneo", "explicacion"]]
            df_errores.columns = ["Código Error", "ID Usuario", "Dato Erróneo", "Explicación"]
            df_errores.to_excel(writer, sheet_name='Errores', index=False)

            # Ajustar ancho de columnas
            worksheet_errores = writer.sheets['Errores']
            worksheet_errores.column_dimensions['A'].width = 15
            worksheet_errores.column_dimensions['B'].width = 20
            worksheet_errores.column_dimensions['C'].width = 25
            worksheet_errores.column_dimensions['D'].width = 80

        # HOJA 2: Distribución/Frecuencia de Errores
        if lista_errores:
            df_distribucion = pd.DataFrame(lista_errores)
            distribucion = df_distribucion.groupby(['codigo', 'explicacion']).size().reset_index(name='frecuencia')
            distribucion = distribucion.sort_values('frecuencia', ascending=False)
            distribucion.columns = ["Código Error", "Descripción", "Frecuencia"]

            # Agregar porcentaje
            total_errores = distribucion['Frecuencia'].sum()
            distribucion['Porcentaje'] = (distribucion['Frecuencia'] / total_errores * 100).round(2)
            distribucion['Porcentaje'] = distribucion['Porcentaje'].astype(str) + '%'

            distribucion.to_excel(writer, sheet_name='Distribución de Errores', index=False)

            # Ajustar ancho de columnas
            worksheet_dist = writer.sheets['Distribución de Errores']
            worksheet_dist.column_dimensions['A'].width = 15
            worksheet_dist.column_dimensions['B'].width = 80
            worksheet_dist.column_dimensions['C'].width = 12
            worksheet_dist.column_dimensions['D'].width = 12

        # HOJA 3: Advertencias (si existen)
        if lista_warnings:
            df_warnings = pd.DataFrame(lista_warnings)
            df_warnings = df_warnings[["codigo", "usuario", "dato_erroneo", "explicacion"]]
            df_warnings.columns = ["Código Warning", "ID Usuario", "Dato Advertencia", "Explicación"]
            df_warnings.to_excel(writer, sheet_name='Advertencias', index=False)

            # Ajustar ancho de columnas
            worksheet_warnings = writer.sheets['Advertencias']
            worksheet_warnings.column_dimensions['A'].width = 15
            worksheet_warnings.column_dimensions['B'].width = 20
            worksheet_warnings.column_dimensions['C'].width = 25
            worksheet_warnings.column_dimensions['D'].width = 80

        # HOJA 4: Resumen
        resumen_data = {
            'Métrica': [
                'Archivo Validado',
                'Fecha de Validación',
                'Total de Errores',
                'Errores Únicos',
                'Total de Advertencias'
            ],
            'Valor': [
                os.path.basename(nombre_archivo),
                timestamp,
                len(lista_errores) if lista_errores else 0,
                len(set([e['codigo'] for e in lista_errores])) if lista_errores else 0,
                len(lista_warnings) if lista_warnings else 0
            ]
        }
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)

        # Ajustar ancho de columnas
        worksheet_resumen = writer.sheets['Resumen']
        worksheet_resumen.column_dimensions['A'].width = 25
        worksheet_resumen.column_dimensions['B'].width = 40

    print(f"\n{'='*80}")
    print(f"REPORTE DE VALIDACIÓN GENERADO")
    print(f"{'='*80}")
    print(f"Archivo: {nombre_salida}")
    print(f"Total de errores: {len(lista_errores) if lista_errores else 0}")
    print(f"Total de advertencias: {len(lista_warnings) if lista_warnings else 0}")
    print(f"{'='*80}\n")

    return nombre_salida
