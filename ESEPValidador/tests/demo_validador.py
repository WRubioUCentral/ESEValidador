# demo_validador.py
import pandas as pd
from validador_completo import validar_archivo_ese
from datetime import datetime

def crear_datos_ejemplo():
    """Crea datos de ejemplo para demostrar las validaciones"""
    datos = {
        # Columnas básicas (0-10)
        'tipo_registro': [2, 2, 2, 1],  # Error en el último
        'consecutivo': [1, 2, 3, 4],
        'codigo_ips': [12345, 999, 67890, None],  # Error en el último
        'tipo_id': ['CC', 'TI', 'CE', 'XX'],  # Error en el último
        'numero_id': ['12345678', '1234567890123', 'ABC', '123456789012345'],  # Errores en algunos
        'primer_apellido': ['GARCIA', 'LOPEZ', 'MARTINEZ', 'RODRIGUEZ'],
        'segundo_apellido': ['PEREZ', 'NONE', 'GOMEZ', 'SILVA'],
        'primer_nombre': ['JUAN', 'MARIA', 'CARLOS', 'ANA'],
        'segundo_nombre': ['CARLOS', 'NONE', 'ALBERTO', 'LUCIA'],
        'fecha_nacimiento': ['1990-05-15', '2010-03-20', '1985-12-10', '2025-01-01'],  # Error en el último
        'sexo': ['M', 'F', 'M', 'X'],  # Error en el último
        'etnia': [6, 1, 3, 2],
        'ocupacion': [1234, 9998, 5678, 9999],
        'nivel_educativo': [12, 5, 8, 15],  # Error en el último
        'gestante': [0, 1, 0, 2],  # Posibles errores según sexo/edad
        'sifilis_gestacional': [0, 0, 0, 1],  # Error en el último
        'mini_mental': [0, 21, 5, 4],
        'hipotiroidismo': [0, 0, 0, 1],  # Error en el último
        'sintomatico_resp': [2, 21, 1, 2],
        'consumo_tabaco': [98, 99, 15, 98],
        'lepra': [21, 21, 21, 0],  # Error en el último
        'obesidad': [21, 21, 21, 5],  # Error en el último
        'tacto_rectal': [0, 0, 4, 5],
        'acido_folico': [0, 1, 2, 5],  # Error en el último
    }
    
    # Agregar más columnas hasta llegar a las necesarias
    for i in range(24, 120):
        datos[f'columna_{i}'] = [0] * 4
    
    # Columnas específicas de peso y talla
    datos['fecha_peso'] = ['2023-01-15', '2023-02-20', '2023-03-10', '1800-01-01']
    datos['peso'] = [70.5, 25.0, 80.2, 999]
    datos['fecha_talla'] = ['2023-01-15', '2023-02-20', '2023-03-10', '1800-01-01']
    datos['talla'] = [175, 120, 180, 999]
    
    return pd.DataFrame(datos)

def main():
    """Función principal de demostración"""
    print("=== DEMO DEL VALIDADOR ESE ===\n")
    
    # Crear datos de ejemplo
    df = crear_datos_ejemplo()
    fecha_corte = '2025-8-01'
    
    print(f"Datos de ejemplo creados: {len(df)} registros")
    print(f"Fecha de corte: {fecha_corte}\n")
    
    # Ejecutar validaciones
    print("Ejecutando validaciones...")
    resultados = validar_archivo_ese(df, fecha_corte)
    
    # Mostrar resultados
    print(f"\n=== RESULTADOS ===")
    print(f"Total de errores: {resultados['total_errores']}")
    print(f"Total de warnings: {resultados['total_warnings']}\n")
    
    # Mostrar errores
    if resultados['errores']:
        print("=== ERRORES ENCONTRADOS ===")
        for i, error in enumerate(resultados['errores'][:10], 1):  # Mostrar solo los primeros 10
            print(f"{i}. Usuario: {error['usuario']}")
            print(f"   Código: {error['codigo']}")
            print(f"   Dato erróneo: {error['dato_erroneo']}")
            print(f"   Explicación: {error['explicacion']}\n")
        
        if len(resultados['errores']) > 10:
            print(f"... y {len(resultados['errores']) - 10} errores más\n")
    
    # Mostrar warnings
    if resultados['warnings']:
        print("=== WARNINGS ENCONTRADOS ===")
        for i, warning in enumerate(resultados['warnings'][:5], 1):  # Mostrar solo los primeros 5
            print(f"{i}. Usuario: {warning['usuario']}")
            print(f"   Código: {warning['codigo']}")
            print(f"   Dato erróneo: {warning['dato_erroneo']}")
            print(f"   Explicación: {warning['explicacion']}\n")
        
        if len(resultados['warnings']) > 5:
            print(f"... y {len(resultados['warnings']) - 5} warnings más\n")
    
    # Resumen por tipo de error
    print("=== RESUMEN POR TIPO DE ERROR ===")
    errores_por_codigo = {}
    for error in resultados['errores']:
        codigo = error['codigo']
        errores_por_codigo[codigo] = errores_por_codigo.get(codigo, 0) + 1
    
    for codigo, cantidad in sorted(errores_por_codigo.items()):
        print(f"{codigo}: {cantidad} ocurrencias")
    
    print(f"\nValidación completada. Total de registros procesados: {len(df)}")

if __name__ == "__main__":
    main()