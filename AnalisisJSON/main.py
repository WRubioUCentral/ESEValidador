"""
Script principal para análisis consolidado de archivos RIPS JSON
Resolución 2275 de 2023
Procesa TODOS los archivos JSON en la carpeta 'input' y genera UN SOLO REPORTE CONSOLIDADO
"""
import sys
from pathlib import Path

# Añadir directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cargador_rips import CargadorRIPS
from analizador_rips import AnalizadorRIPS
from generador_reportes import GeneradorReportes
from validador_calidad import ValidadorCalidadRIPS
from validador_avanzado import ValidadorAvanzadoRIPS
from consolidador_rips import ConsolidadorRIPS
from generador_tablas_especiales import GeneradorTablasEspeciales


def main():
    """Función principal"""
    print("=" * 80)
    print("ANALIZADOR CONSOLIDADO DE RIPS - RESOLUCIÓN 2275 DE 2023")
    print("=" * 80)
    print()

    # Configuración
    directorio_input = Path("input")
    directorio_output = Path("output")
    archivo_cie10 = "config/cie10_codigos.json"

    # Verificar que existe el directorio input
    if not directorio_input.exists():
        print(f"Error: No se encontró el directorio '{directorio_input}'")
        print("Por favor, crea la carpeta 'input' y coloca los archivos JSON RIPS")
        return

    # Crear directorio output si no existe
    directorio_output.mkdir(exist_ok=True)

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

    print()
    print("=" * 80)
    print("FASE 1: CARGA Y CONSOLIDACIÓN DE DATOS")
    print("=" * 80)
    print()

    # Consolidar todos los archivos RIPS
    consolidador = ConsolidadorRIPS(cargador)
    datos_consolidados = consolidador.cargar_multiples_rips(str(directorio_input))

    if not datos_consolidados:
        print("\nError: No se pudieron cargar los archivos RIPS")
        return

    print()
    print("=" * 80)
    print("FASE 2: ANÁLISIS CONSOLIDADO")
    print("=" * 80)
    print()

    # Estructuras para acumular datos consolidados
    total_usuarios = 0
    total_consultas = 0
    total_procedimientos = 0
    total_hospitalizaciones = 0
    total_recien_nacidos = 0
    diagnosticos_consolidados = {}
    procedimientos_consolidados = {}

    # Variables para análisis consolidado
    todos_usuarios_consolidados = []
    analisis_consolidado = {
        "informacion_general": {
            "total_archivos": len(datos_consolidados),
            "archivos_procesados": consolidador.archivos_procesados,
            "fecha_consolidacion": consolidador.obtener_datos_consolidados()["fecha_consolidacion"]
        },
        "analisis_demografico": {},
        "analisis_diagnosticos": {},
        "analisis_servicios": {},
        "analisis_procedimientos": {},
        "analisis_tipo_usuario": {},
        "analisis_incapacidades": {},
        "analisis_modalidad_diagnostico": {},
        "analisis_prestadores": {}
    }

    print("Analizando datos consolidados...")

    # Crear un único diccionario consolidado con todos los usuarios
    datos_rips_consolidado = {
        "numDocumentoIdObligado": "CONSOLIDADO",
        "numFactura": "CONSOLIDADO",
        "usuarios": []
    }

    # Consolidar usuarios de todos los archivos
    for rips in datos_consolidados:
        datos = rips["datos"]
        usuarios = cargador.extraer_usuarios(datos)
        datos_rips_consolidado["usuarios"].extend(usuarios)

        # Contadores
        total_usuarios += len(usuarios)
        for usuario in usuarios:
            consultas = cargador.extraer_consultas(usuario)
            procedimientos = cargador.extraer_procedimientos(usuario)
            servicios = usuario.get("servicios", {})

            total_consultas += len(consultas)
            total_procedimientos += len(procedimientos)
            total_hospitalizaciones += len(servicios.get("hospitalizacion", []))
            total_recien_nacidos += len(servicios.get("recienNacidos", []))

    print(f"  - Total usuarios consolidados: {total_usuarios}")
    print(f"  - Total consultas: {total_consultas}")
    print(f"  - Total procedimientos: {total_procedimientos}")
    print(f"  - Total hospitalizaciones: {total_hospitalizaciones}")
    print(f"  - Total recién nacidos: {total_recien_nacidos}")

    # Realizar análisis completo sobre datos consolidados
    analizador = AnalizadorRIPS(cargador)
    analisis_consolidado = analizador.generar_resumen_completo(datos_rips_consolidado)

    # Actualizar información general
    analisis_consolidado["informacion_general"] = {
        "total_archivos": len(datos_consolidados),
        "archivos_procesados": consolidador.archivos_procesados,
        "fecha_consolidacion": consolidador.obtener_datos_consolidados()["fecha_consolidacion"],
        "total_usuarios": total_usuarios,
        "total_consultas": total_consultas,
        "total_procedimientos": total_procedimientos,
        "total_hospitalizaciones": total_hospitalizaciones,
        "total_recien_nacidos": total_recien_nacidos
    }

    print("\n[OK] Análisis consolidado completado")

    print()
    print("=" * 80)
    print("FASE 3: VALIDACIÓN CONSOLIDADA")
    print("=" * 80)
    print()

    # Validación de calidad consolidada
    print("Validando calidad de datos consolidados...")
    validador = ValidadorCalidadRIPS()
    validacion = validador.validar_datos_completos(datos_rips_consolidado)
    print(f"[OK] Validación básica completada - Nivel de calidad: {validacion.get('calidad_datos')}")
    print(f"    Total de anomalías detectadas: {validacion.get('total_anomalias', 0)}")

    if validacion.get('total_anomalias', 0) > 0:
        por_sev = validacion.get('por_severidad', {})
        print(f"    - Alta: {por_sev.get('ALTA', 0)}, Media: {por_sev.get('MEDIA', 0)}, Baja: {por_sev.get('BAJA', 0)}")

    # Validación avanzada consolidada
    print("\nEjecutando validación avanzada consolidada...")
    validador_avanzado = ValidadorAvanzadoRIPS(cargador)
    analisis_avanzado = validador_avanzado.validar_y_analizar(datos_rips_consolidado)
    print(f"[OK] Validación avanzada completada")

    # Mostrar alertas críticas si existen
    alertas = analisis_avanzado.get("alertas", [])
    alertas_alta = [a for a in alertas if a.get("nivel") == "ALTA"]
    if alertas_alta:
        print(f"    [!] ALERTAS DE SEVERIDAD ALTA: {len(alertas_alta)}")
        for alerta in alertas_alta[:5]:  # Mostrar las primeras 5
            print(f"       - {alerta.get('tipo')}: {alerta.get('mensaje')}")

    # Mostrar indicadores clave
    indicadores = analisis_avanzado.get("indicadores_calidad", {})
    if indicadores and isinstance(indicadores, dict):
        oportunidad = indicadores.get('oportunidad_atencion', 0)
        completitud = indicadores.get('completitud_diagnosticos', 0)
        if isinstance(oportunidad, (int, float)) and isinstance(completitud, (int, float)):
            print(f"    Oportunidad en atención: {oportunidad:.1f}%")
            print(f"    Completitud de diagnósticos: {completitud:.1f}%")

    print()
    print("=" * 80)
    print("FASE 4: GENERACIÓN DE REPORTES CONSOLIDADOS")
    print("=" * 80)
    print()

    print("Generando reportes consolidados...")

    # Generar reporte consolidado tradicional
    generador = GeneradorReportes(nombre_archivo_json="CONSOLIDADO")

    ruta_excel = generador.generar_excel_completo(
        analisis_consolidado,
        datos_rips_consolidado,
        validacion,
        "informe_consolidado",
        analisis_avanzado
    )
    print(f"[OK] Reporte Excel Consolidado: {ruta_excel}")

    # Informe gerencial DOCX consolidado
    ruta_docx = generador.generar_informe_docx(
        analisis_consolidado,
        datos_rips_consolidado,
        validacion,
        "informe_gerencial_consolidado"
    )
    print(f"[OK] Informe Gerencial DOCX Consolidado: {ruta_docx}")

    # Generar Excel con tablas especiales AC, AP, AH, AN, USUARIOS, RESUMEN
    print("\nGenerando Excel con tablas especiales (AC, AP, AH, AN, USUARIOS, RESUMEN)...")
    generador_especial = GeneradorTablasEspeciales(cargador)
    ruta_excel_especial = str(directorio_output / "tablas_especiales_consolidado.xlsx")
    generador_especial.generar_tabla_ac_ap(datos_consolidados, ruta_excel_especial)
    print(f"[OK] Excel con tablas especiales: {ruta_excel_especial}")

    print()
    print("=" * 80)
    print("RESUMEN EJECUTIVO CONSOLIDADO")
    print("=" * 80)

    demo = analisis_consolidado["analisis_demografico"]
    diag = analisis_consolidado["analisis_diagnosticos"]
    serv = analisis_consolidado["analisis_servicios"]
    proc = analisis_consolidado.get("analisis_procedimientos", {})
    incap = analisis_consolidado.get("analisis_incapacidades", {})
    tipo_usuario_analisis = analisis_consolidado.get("analisis_tipo_usuario", {})

    print(f"\nARCHIVOS PROCESADOS: {len(datos_consolidados)}")
    for i, nombre in enumerate(consolidador.archivos_procesados, 1):
        print(f"  {i}. {nombre}")

    print(f"\nTOTAL DE USUARIOS: {demo['total_usuarios']}")
    print(f"Total de consultas: {serv['total_consultas']}")
    print(f"Total de procedimientos: {proc.get('total_procedimientos', 0)}")
    print(f"Total de hospitalizaciones: {total_hospitalizaciones}")
    print(f"Total de recién nacidos: {total_recien_nacidos}")
    print(f"Diagnósticos únicos: {diag['diagnosticos_unicos']}")
    print(f"Usuarios con incapacidad: {incap.get('total_con_incapacidad', 0)}")
    print(f"Nivel de calidad: {validacion.get('calidad_datos')}")

    print("\n--- DISTRIBUCIÓN POR SEXO ---")
    dist_sexo = demo.get("distribucion_sexo", {})
    for sexo, cantidad in dist_sexo.items():
        print(f"{sexo}: {cantidad}")

    print("\n--- DISTRIBUCIÓN POR RÉGIMEN ---")
    dist_regimen = tipo_usuario_analisis.get("distribucion_tipos", {})
    for tipo, info in dist_regimen.items():
        if isinstance(info, dict):
            print(f"{info.get('descripcion', tipo)}: {info.get('cantidad', 0)} usuarios")

    print("\n--- TOP 5 DIAGNÓSTICOS ---")
    todos_diag = diag.get("todos_diagnosticos", [])
    for i, d in enumerate(todos_diag[:5], 1):
        print(f"{i}. [{d['codigo']}] {d['nombre']} - Cantidad: {d['cantidad']}")

    print("\n--- TOP 5 PROCEDIMIENTOS CUPS ---")
    top_proc = proc.get("top_20_procedimientos", [])
    for i, p in enumerate(top_proc[:5], 1):
        print(f"{i}. {p['codigo']} - Cantidad: {p['cantidad']}")

    print()
    print("=" * 80)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print()
    print("Reportes generados:")
    print(f"  1. {ruta_excel}")
    print(f"  2. {ruta_docx}")
    print(f"  3. {ruta_excel_especial}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
