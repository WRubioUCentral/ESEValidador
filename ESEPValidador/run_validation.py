#!/usr/bin/env python3
"""
Script principal para ejecutar validaciones ESE
"""

import sys
import os
from pathlib import Path
import argparse

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from validador_completo import validar_archivo_ese
import pandas as pd


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Validador de archivos ESE')
    parser.add_argument('archivo', help='Ruta al archivo ESE a validar')
    parser.add_argument('--fecha-corte', default='2023-12-31', 
                       help='Fecha de corte para validaciones (formato YYYY-MM-DD)')
    parser.add_argument('--output', '-o', help='Archivo de salida para los resultados')
    parser.add_argument('--formato', choices=['csv', 'xlsx'], default='csv',
                       help='Formato del archivo de salida')
    
    args = parser.parse_args()
    
    try:
        # Cargar el archivo
        print(f"Cargando archivo: {args.archivo}")
        if args.archivo.endswith('.xlsx'):
            df = pd.read_excel(args.archivo)
        else:
            df = pd.read_csv(args.archivo)
        
        print(f"Archivo cargado: {len(df)} registros")
        
        # Validar
        print(f"Iniciando validación con fecha de corte: {args.fecha_corte}")
        resultados = validar_archivo_ese(df, args.fecha_corte)
        
        # Mostrar resumen
        print("\n" + "="*50)
        print("RESUMEN DE VALIDACIÓN")
        print("="*50)
        print(f"Total de errores: {resultados['total_errores']}")
        print(f"Total de warnings: {resultados['total_warnings']}")
        
        if resultados['total_errores'] > 0:
            print(f"\nPrimeros 5 errores:")
            for i, error in enumerate(resultados['errores'][:5]):
                print(f"{i+1}. Usuario: {error['usuario']} - {error['codigo']}: {error['explicacion']}")
        
        if resultados['total_warnings'] > 0:
            print(f"\nPrimeros 5 warnings:")
            for i, warning in enumerate(resultados['warnings'][:5]):
                print(f"{i+1}. Usuario: {warning['usuario']} - {warning['codigo']}: {warning['explicacion']}")
        
        # Guardar resultados si se especifica archivo de salida
        if args.output:
            print(f"\nGuardando resultados en: {args.output}")
            
            # Crear DataFrame con errores
            errores_df = pd.DataFrame(resultados['errores'])
            warnings_df = pd.DataFrame(resultados['warnings'])
            
            if args.formato == 'xlsx':
                with pd.ExcelWriter(args.output) as writer:
                    errores_df.to_excel(writer, sheet_name='Errores', index=False)
                    warnings_df.to_excel(writer, sheet_name='Warnings', index=False)
            else:
                errores_df.to_csv(args.output.replace('.csv', '_errores.csv'), index=False)
                warnings_df.to_csv(args.output.replace('.csv', '_warnings.csv'), index=False)
            
            print("Resultados guardados exitosamente")
        
        print("\nValidación completada")
        
    except Exception as e:
        print(f"Error durante la validación: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()