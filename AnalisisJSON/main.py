"""
Script principal para análisis de archivos RIPS JSON
Resolución 2275 de 2023
Procesa TODOS los archivos JSON en la carpeta 'input'
"""
import sys
from pathlib import Path

# Añadir directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cargador_rips import CargadorRIPS
from analizador_rips import AnalizadorRIPS
from generador_reportes import GeneradorReportes
from validador_calidad import ValidadorCalidadRIPS


def procesar_archivo(archivo_rips: str, cargador: CargadorRIPS, archivo_num: int, total_archivos: int):
    """
    Procesa un archivo RIPS individual

    Args:
        archivo_rips: Ruta al archivo JSON
        cargador: Instancia del cargador RIPS
        archivo_num: Número de archivo actual
        total_archivos: Total de archivos a procesar

    Returns:
        True si se procesó exitosamente, False en caso de error
    """
    print()
    print("=" * 80)
    print(f"PROCESANDO ARCHIVO {archivo_num} DE {total_archivos}")
    print("=" * 80)
    print(f"Archivo: {archivo_rips}")
    print()

    try:
        # Cargar datos RIPS
        print("Cargando datos RIPS...")
        datos_rips = cargador.cargar_json(archivo_rips)
        print("[OK] Datos RIPS cargados exitosamente")
        print()

        # Análisis
        print("Ejecutando análisis...")
        analizador = AnalizadorRIPS(cargador)
        analisis_completo = analizador.generar_resumen_completo(datos_rips)
        print("[OK] Análisis completado")
        print()

        # Validación de calidad de datos
        print("Validando calidad de datos...")
        validador = ValidadorCalidadRIPS()
        validacion = validador.validar_datos_completos(datos_rips)
        print(f"[OK] Validación completada - Nivel de calidad: {validacion.get('calidad_datos')}")
        print(f"    Total de anomalías detectadas: {validacion.get('total_anomalias', 0)}")
        if validacion.get('total_anomalias', 0) > 0:
            por_sev = validacion.get('por_severidad', {})
            print(f"    - Alta: {por_sev.get('ALTA', 0)}, Media: {por_sev.get('MEDIA', 0)}, Baja: {por_sev.get('BAJA', 0)}")
        print()

        # Generar reportes en carpeta específica
        print("Generando reportes...")
        generador = GeneradorReportes(nombre_archivo_json=archivo_rips)

        # Reporte Excel completo con múltiples hojas
        ruta_excel = generador.generar_excel_completo(analisis_completo, datos_rips, validacion, "informe_completo")
        print(f"[OK] Reporte Excel: {ruta_excel}")

        # Informe gerencial en DOCX con gráficos
        ruta_docx = generador.generar_informe_docx(analisis_completo, datos_rips, validacion, "informe_gerencial")
        print(f"[OK] Informe Gerencial DOCX: {ruta_docx}")

        # Mostrar resumen ejecutivo
        print()
        print("-" * 80)
        print("RESUMEN EJECUTIVO")
        print("-" * 80)

        demo = analisis_completo["analisis_demografico"]
        diag = analisis_completo["analisis_diagnosticos"]
        serv = analisis_completo["analisis_servicios"]

        print(f"\nTotal de usuarios: {demo['total_usuarios']}")
        print(f"Total de consultas: {serv['total_consultas']}")
        print(f"Diagnósticos únicos: {diag['diagnosticos_unicos']}")
        print(f"Nivel de calidad: {validacion.get('calidad_datos')}")

        print("\n--- TOP 3 DIAGNÓSTICOS ---")
        for i, d in enumerate(diag["top_10_diagnosticos"][:3], 1):
            print(f"{i}. [{d['codigo']}] {d['nombre']} - Cantidad: {d['cantidad']}")

        print()
        print("[OK] Archivo procesado exitosamente")
        return True

    except Exception as e:
        print(f"\n[ERROR] al procesar archivo: {str(e)}")
        print(f"        El archivo {archivo_rips} sera omitido")
        return False


def main():
    """Función principal"""
    print("=" * 80)
    print("ANALIZADOR MASIVO DE RIPS - RESOLUCIÓN 2275 DE 2023")
    print("=" * 80)
    print()

    # Configuración
    directorio_input = Path("input")
    archivo_cie10 = "config/cie10_codigos.json"

    # Verificar que existe el directorio input
    if not directorio_input.exists():
        print(f"Error: No se encontró el directorio '{directorio_input}'")
        print("Por favor, crea la carpeta 'input' y coloca los archivos JSON RIPS")
        return

    # Buscar todos los archivos JSON en la carpeta input
    archivos_json = list(directorio_input.glob("*.json"))

    if not archivos_json:
        print(f"Error: No se encontraron archivos JSON en la carpeta '{directorio_input}'")
        print("Por favor, coloca al menos un archivo JSON RIPS en la carpeta 'input'")
        return

    print(f"Se encontraron {len(archivos_json)} archivo(s) JSON para procesar:")
    for i, archivo in enumerate(archivos_json, 1):
        print(f"  {i}. {archivo.name}")
    print()

    # Inicializar componentes
    print("Cargando códigos CIE-10...")
    try:
        cargador = CargadorRIPS(archivo_cie10)
        print(f"[OK] Cargados {len(cargador.codigos_cie10)} códigos CIE-10")
    except Exception as e:
        print(f"Error al cargar códigos CIE-10: {str(e)}")
        return

    # Procesar cada archivo
    archivos_exitosos = 0
    archivos_fallidos = 0

    for i, archivo in enumerate(archivos_json, 1):
        exito = procesar_archivo(str(archivo), cargador, i, len(archivos_json))
        if exito:
            archivos_exitosos += 1
        else:
            archivos_fallidos += 1

    # Resumen final
    """
    print()
    print("=" * 80)
    print("RESUMEN FINAL DEL PROCESO")
    print("=" * 80)
    print(f"\nTotal de archivos procesados: {len(archivos_json)}")
    print(f"  [OK] Exitosos: {archivos_exitosos}")
    if archivos_fallidos > 0:
        print(f"  [X] Fallidos: {archivos_fallidos}")
    print()
    print(f"Los reportes se generaron en carpetas individuales dentro de 'output/'")
    print()
    print("=" * 80)
    print("Proceso completado exitosamente")
    print("=" * 80)
    """


if __name__ == "__main__":
    main()
