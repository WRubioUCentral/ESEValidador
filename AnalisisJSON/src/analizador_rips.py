"""
Módulo para análisis de datos RIPS
"""
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Tuple
from cargador_rips import CargadorRIPS
from catalogos_rips import (
    CODIGOS_GESTACION,
    PREFIJOS_GESTACION,
    FINALIDADES_SALUD_MATERNA,
    PROCEDIMIENTOS_PRIORITARIOS,
    CODIGOS_ENFERMEDADES_CRONICAS,
    PREFIJOS_ENFERMEDADES_CRONICAS
)


class AnalizadorRIPS:
    """Clase para análisis de datos RIPS"""

    def __init__(self, cargador: CargadorRIPS):
        """
        Inicializa el analizador

        Args:
            cargador: Instancia de CargadorRIPS
        """
        self.cargador = cargador

    def analisis_demografico(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis demográfico de los usuarios

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis demográfico
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        resultado = {
            "total_usuarios": len(usuarios),
            "distribucion_sexo": Counter(),
            "distribucion_tipo_documento": Counter(),
            "distribucion_zona_territorial": Counter(),
            "distribucion_ruta_vida": {
                "Primera infancia (0-5)": 0,
                "Infancia (6-11)": 0,
                "Adolescencia (12-17)": 0,
                "Juventud (18-28)": 0,
                "Adultez (29-59)": 0,
                "Vejez (60+)": 0
            },
            "usuarios_por_municipio": Counter(),
            "distribucion_sexo_edad": defaultdict(lambda: defaultdict(int))
        }

        for usuario in usuarios:
            # Sexo
            sexo = usuario.get("codSexo", "No especificado")
            resultado["distribucion_sexo"][sexo] += 1

            # Tipo de documento
            tipo_doc = usuario.get("tipoDocumentoIdentificacion", "No especificado")
            resultado["distribucion_tipo_documento"][tipo_doc] += 1

            # Zona territorial
            zona = usuario.get("codZonaTerritorialResidencia", "No especificado")
            resultado["distribucion_zona_territorial"][zona] += 1

            # Municipio
            municipio = usuario.get("codMunicipioResidencia", "No especificado")
            resultado["usuarios_por_municipio"][municipio] += 1

            # Ruta de Vida (Resolución 3280 de 2018)
            fecha_nac = usuario.get("fechaNacimiento")
            if fecha_nac:
                edad = self.cargador.calcular_edad(fecha_nac)
                if edad is not None:
                    if edad <= 5:
                        ruta_vida = "Primera infancia (0-5)"
                    elif edad <= 11:
                        ruta_vida = "Infancia (6-11)"
                    elif edad <= 17:
                        ruta_vida = "Adolescencia (12-17)"
                    elif edad <= 28:
                        ruta_vida = "Juventud (18-28)"
                    elif edad <= 59:
                        ruta_vida = "Adultez (29-59)"
                    else:
                        ruta_vida = "Vejez (60+)"

                    resultado["distribucion_ruta_vida"][ruta_vida] += 1
                    resultado["distribucion_sexo_edad"][sexo][ruta_vida] += 1

        return resultado

    def analisis_diagnosticos(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de diagnósticos con información CIE-10

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de diagnósticos
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        diagnosticos_principales = []
        comorbilidades = []
        diagnosticos_por_edad = defaultdict(lambda: defaultdict(int))
        diagnosticos_por_sexo = defaultdict(int)

        for usuario in usuarios:
            sexo = usuario.get("codSexo", "No especificado")
            edad = None
            fecha_nac = usuario.get("fechaNacimiento")
            if fecha_nac:
                edad = self.cargador.calcular_edad(fecha_nac)

            consultas = self.cargador.extraer_consultas(usuario)

            for consulta in consultas:
                # Diagnóstico principal
                cod_principal = consulta.get("codDiagnosticoPrincipal")
                if cod_principal:
                    info_diag = self.cargador.obtener_info_diagnostico(cod_principal)
                    diagnosticos_principales.append({
                        **info_diag,
                        "finalidad": consulta.get("finalidadTecnologiaSalud"),
                        "causa": consulta.get("causaMotivoAtencion"),
                        "tipo": consulta.get("tipoDiagnosticoPrincipal")
                    })

                    diagnosticos_por_sexo[f"{cod_principal}_{sexo}"] += 1

                    if edad is not None:
                        if edad <= 17:
                            grupo = "Niños y adolescentes (0-17)"
                        elif edad <= 59:
                            grupo = "Adultos (18-59)"
                        else:
                            grupo = "Adultos mayores (60+)"
                        diagnosticos_por_edad[grupo][cod_principal] += 1

                # Diagnósticos relacionados (comorbilidades)
                relacionados = []
                for i in range(1, 4):
                    cod_rel = consulta.get(f"codDiagnosticoRelacionado{i}")
                    if cod_rel:
                        relacionados.append(cod_rel)

                if relacionados:
                    comorbilidades.append({
                        "diagnostico_principal": cod_principal,
                        "info_principal": self.cargador.obtener_info_diagnostico(cod_principal),
                        "relacionados": [
                            self.cargador.obtener_info_diagnostico(cod)
                            for cod in relacionados
                        ]
                    })

        # TODOS los diagnósticos principales (ordenados por cantidad)
        contador_diag = Counter([d["codigo"] for d in diagnosticos_principales])
        todos_diagnosticos = []
        for codigo, cantidad in contador_diag.most_common():
            info = self.cargador.obtener_info_diagnostico(codigo)
            todos_diagnosticos.append({
                **info,
                "cantidad": cantidad,
                "porcentaje": (cantidad / len(diagnosticos_principales) * 100) if diagnosticos_principales else 0
            })

        # Análisis detallado de comorbilidades
        analisis_comorbilidad = self._analizar_comorbilidades_detallado(comorbilidades)

        return {
            "total_diagnosticos": len(diagnosticos_principales),
            "diagnosticos_unicos": len(contador_diag),
            "todos_diagnosticos": todos_diagnosticos,
            "diagnosticos_con_comorbilidades": len(comorbilidades),
            "comorbilidades_detalle": comorbilidades,
            "analisis_comorbilidad_detallado": analisis_comorbilidad,
            "diagnosticos_por_grupo_edad": dict(diagnosticos_por_edad)
        }

    def _analizar_comorbilidades_detallado(self, comorbilidades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Análisis detallado de comorbilidades

        Args:
            comorbilidades: Lista de comorbilidades detectadas

        Returns:
            Diccionario con análisis detallado de comorbilidades
        """
        if not comorbilidades:
            return {
                "total_pacientes_con_comorbilidades": 0,
                "combinaciones_mas_frecuentes": [],
                "diagnostico_principal_con_mas_comorbilidades": None,
                "promedio_comorbilidades_por_paciente": 0
            }

        # Contar combinaciones de diagnósticos
        combinaciones = []
        diagnosticos_principales_comorbilidad = Counter()
        total_comorbilidades = 0

        for combo in comorbilidades:
            principal = combo.get("diagnostico_principal")
            relacionados = combo.get("relacionados", [])

            diagnosticos_principales_comorbilidad[principal] += 1
            total_comorbilidades += len(relacionados)

            # Crear cadena de combinación
            codigos_relacionados = [r.get("codigo") for r in relacionados if r.get("codigo")]
            if codigos_relacionados:
                combinacion = f"{principal} + {', '.join(codigos_relacionados)}"
                combinaciones.append(combinacion)

        # Combinaciones más frecuentes
        contador_combinaciones = Counter(combinaciones)
        combinaciones_frecuentes = []
        for comb, cantidad in contador_combinaciones.most_common(10):
            combinaciones_frecuentes.append({
                "combinacion": comb,
                "frecuencia": cantidad
            })

        # Diagnóstico principal con más comorbilidades
        diag_mas_comorbilidades = None
        if diagnosticos_principales_comorbilidad:
            codigo_mas_comun = diagnosticos_principales_comorbilidad.most_common(1)[0][0]
            info_diag = self.cargador.obtener_info_diagnostico(codigo_mas_comun)
            diag_mas_comorbilidades = {
                **info_diag,
                "cantidad_pacientes": diagnosticos_principales_comorbilidad[codigo_mas_comun]
            }

        promedio = total_comorbilidades / len(comorbilidades) if comorbilidades else 0

        return {
            "total_pacientes_con_comorbilidades": len(comorbilidades),
            "combinaciones_mas_frecuentes": combinaciones_frecuentes,
            "diagnostico_principal_con_mas_comorbilidades": diag_mas_comorbilidades,
            "promedio_comorbilidades_por_paciente": round(promedio, 2),
            "total_comorbilidades_registradas": total_comorbilidades
        }

    def analisis_servicios(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de servicios prestados

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de servicios
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        resultado = {
            "total_consultas": 0,
            "usuarios_multiples_consultas": [],
            "distribucion_modalidad": Counter(),
            "distribucion_finalidad": Counter(),
            "distribucion_causa_atencion": Counter(),
            "consultas_por_fecha": Counter(),
            "servicios_sin_autorizacion": 0,
            "total_valor_servicios": 0,
            "total_copagos": 0
        }

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)
            resultado["total_consultas"] += len(consultas)

            if len(consultas) > 1:
                resultado["usuarios_multiples_consultas"].append({
                    "documento": usuario.get("numDocumentoIdentificacion"),
                    "tipo_documento": usuario.get("tipoDocumentoIdentificacion"),
                    "cantidad_consultas": len(consultas),
                    "fechas": list(set([c.get("fechaInicioAtencion") for c in consultas]))
                })

            for consulta in consultas:
                # Modalidad
                modalidad = consulta.get("modalidadGrupoServicioTecSal", "No especificado")
                resultado["distribucion_modalidad"][modalidad] += 1

                # Finalidad
                finalidad = consulta.get("finalidadTecnologiaSalud", "No especificado")
                resultado["distribucion_finalidad"][finalidad] += 1

                # Causa de atención
                causa = consulta.get("causaMotivoAtencion", "No especificado")
                resultado["distribucion_causa_atencion"][causa] += 1

                # Fecha
                fecha = consulta.get("fechaInicioAtencion", "")[:10]  # Solo YYYY-MM-DD
                if fecha:
                    resultado["consultas_por_fecha"][fecha] += 1

                # Autorización
                if not consulta.get("numAutorizacion"):
                    resultado["servicios_sin_autorizacion"] += 1

                # Valores
                resultado["total_valor_servicios"] += consulta.get("vrServicio", 0)
                resultado["total_copagos"] += consulta.get("valorPagoModerador", 0)

        return resultado

    def analisis_acudientes(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de relación paciente-acudiente

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de acudientes
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        acudientes = defaultdict(list)
        menores_con_acudiente = []

        for usuario in usuarios:
            doc_usuario = usuario.get("numDocumentoIdentificacion")
            edad = None
            fecha_nac = usuario.get("fechaNacimiento")
            if fecha_nac:
                edad = self.cargador.calcular_edad(fecha_nac)

            consultas = self.cargador.extraer_consultas(usuario)

            for consulta in consultas:
                doc_acudiente = consulta.get("numDocumentoIdentificacion")

                if doc_acudiente and doc_acudiente != doc_usuario:
                    acudientes[doc_acudiente].append({
                        "paciente": doc_usuario,
                        "tipo_doc_paciente": usuario.get("tipoDocumentoIdentificacion"),
                        "edad_paciente": edad,
                        "sexo_paciente": usuario.get("codSexo")
                    })

                    if edad is not None and edad < 18:
                        menores_con_acudiente.append({
                            "paciente": doc_usuario,
                            "edad": edad,
                            "acudiente": doc_acudiente
                        })

        return {
            "total_acudientes": len(acudientes),
            "acudientes_detalle": dict(acudientes),
            "menores_con_acudiente": menores_con_acudiente,
            "total_menores_con_acudiente": len(menores_con_acudiente)
        }

    def analisis_poblacion_gestante(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis completo y detallado de la población gestante
        Incluye: controles prenatales, riesgo obstétrico, complicaciones

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis exhaustivo de población gestante
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        gestantes = []
        diagnosticos_gestantes = Counter()
        servicios_gestantes = Counter()
        edad_gestantes = []
        gestantes_con_control = 0
        gestantes_alto_riesgo = 0
        gestantes_con_complicaciones = 0

        # Códigos de alto riesgo obstétrico
        codigos_alto_riesgo = ["O10", "O11", "O13", "O14", "O15", "O24", "O30", "O35", "O36", "O40", "O42", "O43", "O44", "O45"]

        # Códigos de complicaciones
        codigos_complicaciones = ["O20", "O46", "O60", "O67", "O68", "O70", "O71", "O72", "O85", "O86", "O88"]

        for usuario in usuarios:
            sexo = usuario.get("codSexo")
            if sexo != "F":  # Solo mujeres pueden estar gestantes
                continue

            edad = None
            fecha_nac = usuario.get("fechaNacimiento")
            if fecha_nac:
                edad = self.cargador.calcular_edad(fecha_nac)

            consultas = self.cargador.extraer_consultas(usuario)
            es_gestante = False

            diagnosticos_usuario = []
            servicios_usuario = []
            controles_prenatales = 0
            tiene_alto_riesgo = False
            tiene_complicaciones = False
            fechas_controles = []

            for consulta in consultas:
                # Verificar diagnósticos relacionados con gestación
                diag_principal = consulta.get("codDiagnosticoPrincipal", "")
                finalidad = consulta.get("finalidadTecnologiaSalud", "")
                cod_consulta = consulta.get("codConsulta", "")

                # Identificar gestante
                if any(diag_principal.startswith(cod) for cod in PREFIJOS_GESTACION) or finalidad in FINALIDADES_SALUD_MATERNA:
                    es_gestante = True
                    diagnosticos_usuario.append(diag_principal)
                    servicios_usuario.append(finalidad)

                    # Contar controles prenatales
                    if finalidad == "15" or cod_consulta in ["890301", "890302"]:
                        controles_prenatales += 1
                        fechas_controles.append(consulta.get("fechaInicioAtencion", ""))

                    # Identificar alto riesgo
                    if any(diag_principal.startswith(codigo) for codigo in codigos_alto_riesgo):
                        tiene_alto_riesgo = True

                    # Identificar complicaciones
                    if any(diag_principal.startswith(codigo) for codigo in codigos_complicaciones):
                        tiene_complicaciones = True

            if es_gestante:
                # Clasificar riesgo por edad
                riesgo_por_edad = "Normal"
                if edad:
                    if edad < 18:
                        riesgo_por_edad = "Alto riesgo (adolescente)"
                    elif edad >= 35:
                        riesgo_por_edad = "Alto riesgo (edad materna avanzada)"

                gestante_data = {
                    "documento": usuario.get("numDocumentoIdentificacion"),
                    "tipo_documento": usuario.get("tipoDocumentoIdentificacion"),
                    "edad": edad,
                    "municipio": usuario.get("codMunicipioResidencia"),
                    "zona": usuario.get("codZonaTerritorialResidencia"),
                    "diagnosticos": diagnosticos_usuario,
                    "servicios": servicios_usuario,
                    "controles_prenatales": controles_prenatales,
                    "tiene_alto_riesgo": tiene_alto_riesgo,
                    "tiene_complicaciones": tiene_complicaciones,
                    "riesgo_por_edad": riesgo_por_edad,
                    "fechas_controles": fechas_controles,
                }

                gestantes.append(gestante_data)

                if edad:
                    edad_gestantes.append(edad)

                if controles_prenatales > 0:
                    gestantes_con_control += 1

                if tiene_alto_riesgo:
                    gestantes_alto_riesgo += 1

                if tiene_complicaciones:
                    gestantes_con_complicaciones += 1

                for diag in diagnosticos_usuario:
                    diagnosticos_gestantes[diag] += 1

                for serv in servicios_usuario:
                    servicios_gestantes[serv] += 1

        # Distribución por grupo de edad
        distribucion_edad_gestantes = {
            "Adolescentes (10-17)": 0,
            "Jóvenes (18-28)": 0,
            "Adultas (29-40)": 0,
            "Mayores de 40": 0
        }

        gestantes_sin_control = 0

        for gestante in gestantes:
            edad = gestante["edad"]
            if edad:
                if edad <= 17:
                    distribucion_edad_gestantes["Adolescentes (10-17)"] += 1
                elif edad <= 28:
                    distribucion_edad_gestantes["Jóvenes (18-28)"] += 1
                elif edad <= 40:
                    distribucion_edad_gestantes["Adultas (29-40)"] += 1
                else:
                    distribucion_edad_gestantes["Mayores de 40"] += 1

            if gestante["controles_prenatales"] == 0:
                gestantes_sin_control += 1

        # Top diagnósticos en gestantes
        top_diagnosticos_gestantes = []
        for codigo, cantidad in diagnosticos_gestantes.most_common(15):
            info = self.cargador.obtener_info_diagnostico(codigo)
            nombre_especifico = CODIGOS_GESTACION.get(codigo[:3], info.get("nombre", ""))
            top_diagnosticos_gestantes.append({
                **info,
                "nombre_especifico": nombre_especifico,
                "cantidad": cantidad,
                "porcentaje": (cantidad / len(gestantes) * 100) if gestantes else 0
            })

        # Distribución de controles prenatales
        distribucion_controles = {
            "Sin control": 0,
            "1-3 controles": 0,
            "4-6 controles": 0,
            "7+ controles (adecuado)": 0
        }

        for gestante in gestantes:
            controles = gestante["controles_prenatales"]
            if controles == 0:
                distribucion_controles["Sin control"] += 1
            elif controles <= 3:
                distribucion_controles["1-3 controles"] += 1
            elif controles <= 6:
                distribucion_controles["4-6 controles"] += 1
            else:
                distribucion_controles["7+ controles (adecuado)"] += 1

        return {
            "total_gestantes": len(gestantes),
            "gestantes_detalle": gestantes,
            "distribucion_edad_gestantes": distribucion_edad_gestantes,
            "top_diagnosticos_gestantes": top_diagnosticos_gestantes,
            "servicios_mas_frecuentes": dict(servicios_gestantes),
            "edad_promedio": round(sum(edad_gestantes) / len(edad_gestantes), 1) if edad_gestantes else 0,
            "edad_minima": min(edad_gestantes) if edad_gestantes else 0,
            "edad_maxima": max(edad_gestantes) if edad_gestantes else 0,
            "gestantes_adolescentes": distribucion_edad_gestantes["Adolescentes (10-17)"],
            "gestantes_con_control_prenatal": gestantes_con_control,
            "gestantes_sin_control": gestantes_sin_control,
            "gestantes_alto_riesgo": gestantes_alto_riesgo,
            "gestantes_con_complicaciones": gestantes_con_complicaciones,
            "distribucion_controles": distribucion_controles,
            "porcentaje_cobertura_control": (gestantes_con_control / len(gestantes) * 100) if gestantes else 0,
            "porcentaje_alto_riesgo": (gestantes_alto_riesgo / len(gestantes) * 100) if gestantes else 0,
            "porcentaje_complicaciones": (gestantes_con_complicaciones / len(gestantes) * 100) if gestantes else 0,
        }

    def analisis_procedimientos(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis completo de procedimientos CUPS realizados

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de procedimientos
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        procedimientos_cups = Counter()
        procedimientos_por_finalidad = Counter()
        procedimientos_por_via_ingreso = Counter()
        procedimientos_con_complicacion = []
        procedimientos_con_mipres = 0
        total_valor_procedimientos = 0
        procedimientos_sin_autorizacion = 0

        for usuario in usuarios:
            procedimientos = self.cargador.extraer_procedimientos(usuario)

            for proc in procedimientos:
                cod_proc = proc.get("codProcedimiento", "")
                if cod_proc:
                    procedimientos_cups[cod_proc] += 1

                finalidad = proc.get("finalidadTecnologiaSalud", "")
                if finalidad:
                    procedimientos_por_finalidad[finalidad] += 1

                via_ingreso = proc.get("viaIngresoServicioSalud", "")
                if via_ingreso:
                    procedimientos_por_via_ingreso[via_ingreso] += 1

                # Complicaciones
                cod_complicacion = proc.get("codComplicacion")
                if cod_complicacion:
                    procedimientos_con_complicacion.append({
                        "documento": usuario.get("numDocumentoIdentificacion"),
                        "procedimiento": cod_proc,
                        "complicacion": cod_complicacion,
                        "fecha": proc.get("fechaInicioAtencion")
                    })

                # MIPRES
                if proc.get("idMIPRES"):
                    procedimientos_con_mipres += 1

                # Valor
                valor = proc.get("vrServicio", 0)
                if valor:
                    total_valor_procedimientos += valor

                # Autorización
                if not proc.get("numAutorizacion"):
                    procedimientos_sin_autorizacion += 1

        # Top 20 procedimientos más frecuentes
        top_procedimientos = []
        total_proc = sum(procedimientos_cups.values())
        for codigo, cantidad in procedimientos_cups.most_common(20):
            top_procedimientos.append({
                "codigo": codigo,
                "cantidad": cantidad,
                "porcentaje": (cantidad / total_proc * 100) if total_proc > 0 else 0
            })

        return {
            "total_procedimientos": total_proc,
            "procedimientos_unicos": len(procedimientos_cups),
            "top_20_procedimientos": top_procedimientos,
            "distribucion_finalidad": dict(procedimientos_por_finalidad),
            "distribucion_via_ingreso": dict(procedimientos_por_via_ingreso),
            "total_complicaciones": len(procedimientos_con_complicacion),
            "detalle_complicaciones": procedimientos_con_complicacion,
            "procedimientos_con_mipres": procedimientos_con_mipres,
            "procedimientos_sin_autorizacion": procedimientos_sin_autorizacion,
            "total_valor_procedimientos": total_valor_procedimientos,
            "valor_promedio_procedimiento": (total_valor_procedimientos / total_proc) if total_proc > 0 else 0
        }

    def analisis_tipo_usuario(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis por tipo de usuario (régimen)

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis por tipo de usuario
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        distribucion_tipo_usuario = Counter()
        servicios_por_tipo = defaultdict(int)
        valor_por_tipo = defaultdict(float)

        tipos_usuario_desc = {
            "01": "Contributivo cotizante",
            "02": "Contributivo beneficiario",
            "03": "Contributivo adicional",
            "04": "Subsidiado",
            "05": "No asegurado",
            "06": "Especial o excepción cotizante",
            "07": "Especial o excepción beneficiario",
            "08": "Personas privadas de la libertad",
            "09": "Víctimas de eventos catastróficos"
        }

        for usuario in usuarios:
            tipo = usuario.get("tipoUsuario", "No especificado")
            distribucion_tipo_usuario[tipo] += 1

            consultas = self.cargador.extraer_consultas(usuario)
            procedimientos = self.cargador.extraer_procedimientos(usuario)

            total_servicios = len(consultas) + len(procedimientos)
            servicios_por_tipo[tipo] += total_servicios

            # Valor total
            for consulta in consultas:
                valor_por_tipo[tipo] += consulta.get("vrServicio", 0)

            for proc in procedimientos:
                valor_por_tipo[tipo] += proc.get("vrServicio", 0)

        resultado = {
            "distribucion_tipo_usuario": dict(distribucion_tipo_usuario),
            "servicios_por_tipo": dict(servicios_por_tipo),
            "valor_por_tipo": dict(valor_por_tipo),
            "descripciones_tipo": tipos_usuario_desc
        }

        return resultado

    def analisis_incapacidades(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de usuarios con incapacidad

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de incapacidades
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        usuarios_con_incapacidad = []
        total_con_incapacidad = 0
        diagnosticos_incapacidad = Counter()
        incapacidad_por_edad = defaultdict(int)
        incapacidad_por_sexo = Counter()

        for usuario in usuarios:
            incapacidad = usuario.get("incapacidad", "NO")

            if incapacidad == "SI" or incapacidad == "S":
                total_con_incapacidad += 1

                doc = usuario.get("numDocumentoIdentificacion")
                sexo = usuario.get("codSexo")
                edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento"))

                incapacidad_por_sexo[sexo] += 1

                if edad:
                    if edad <= 17:
                        grupo_edad = "Menor de edad"
                    elif edad <= 28:
                        grupo_edad = "Joven (18-28)"
                    elif edad <= 59:
                        grupo_edad = "Adulto (29-59)"
                    else:
                        grupo_edad = "Adulto mayor (60+)"

                    incapacidad_por_edad[grupo_edad] += 1

                # Obtener diagnósticos
                consultas = self.cargador.extraer_consultas(usuario)
                diagnosticos_usuario = []
                for consulta in consultas:
                    diag = consulta.get("codDiagnosticoPrincipal")
                    if diag:
                        diagnosticos_incapacidad[diag] += 1
                        diagnosticos_usuario.append(diag)

                usuarios_con_incapacidad.append({
                    "documento": doc,
                    "sexo": sexo,
                    "edad": edad,
                    "diagnosticos": diagnosticos_usuario
                })

        # Top diagnósticos asociados a incapacidad
        top_diagnosticos_incapacidad = []
        for codigo, cantidad in diagnosticos_incapacidad.most_common(10):
            info = self.cargador.obtener_info_diagnostico(codigo)
            top_diagnosticos_incapacidad.append({
                **info,
                "cantidad": cantidad
            })

        total_usuarios = len(usuarios)
        return {
            "total_con_incapacidad": total_con_incapacidad,
            "porcentaje_incapacidad": (total_con_incapacidad / total_usuarios * 100) if total_usuarios > 0 else 0,
            "usuarios_con_incapacidad": usuarios_con_incapacidad,
            "distribucion_por_edad": dict(incapacidad_por_edad),
            "distribucion_por_sexo": dict(incapacidad_por_sexo),
            "top_diagnosticos_incapacidad": top_diagnosticos_incapacidad
        }

    def analisis_modalidad_diagnostico(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de modalidad de atención y tipo de diagnóstico

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de modalidad y tipo diagnóstico
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        distribucion_modalidad = Counter()
        distribucion_tipo_diagnostico = Counter()
        distribucion_grupo_servicios = Counter()

        tipos_diagnostico_desc = {
            "01": "Impresión diagnóstica",
            "02": "Confirmado nuevo",
            "03": "Confirmado repetido"
        }

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)

            for consulta in consultas:
                modalidad = consulta.get("modalidadGrupoServicioTecSal", "")
                if modalidad:
                    distribucion_modalidad[modalidad] += 1

                tipo_diag = consulta.get("tipoDiagnosticoPrincipal", "")
                if tipo_diag:
                    distribucion_tipo_diagnostico[tipo_diag] += 1

                grupo = consulta.get("grupoServicios", "")
                if grupo:
                    distribucion_grupo_servicios[grupo] += 1

        # Calcular porcentajes para tipo de diagnóstico
        total_diagnosticos = sum(distribucion_tipo_diagnostico.values())
        tipo_diagnostico_detalle = {}
        for tipo, cantidad in distribucion_tipo_diagnostico.items():
            tipo_diagnostico_detalle[tipo] = {
                "descripcion": tipos_diagnostico_desc.get(tipo, "No especificado"),
                "cantidad": cantidad,
                "porcentaje": (cantidad / total_diagnosticos * 100) if total_diagnosticos > 0 else 0
            }

        return {
            "distribucion_modalidad": dict(distribucion_modalidad),
            "distribucion_tipo_diagnostico": dict(distribucion_tipo_diagnostico),
            "tipo_diagnostico_detalle": tipo_diagnostico_detalle,
            "distribucion_grupo_servicios": dict(distribucion_grupo_servicios)
        }

    def analisis_prestadores(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análisis de prestadores de servicios

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con análisis de prestadores
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        prestadores = Counter()
        servicios_por_prestador = defaultdict(lambda: {"consultas": 0, "procedimientos": 0})
        valor_por_prestador = defaultdict(float)

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)
            procedimientos = self.cargador.extraer_procedimientos(usuario)

            for consulta in consultas:
                prestador = consulta.get("codPrestador")
                if prestador:
                    prestadores[prestador] += 1
                    servicios_por_prestador[prestador]["consultas"] += 1
                    valor_por_prestador[prestador] += consulta.get("vrServicio", 0)

            for proc in procedimientos:
                prestador = proc.get("codPrestador")
                if prestador:
                    prestadores[prestador] += 1
                    servicios_por_prestador[prestador]["procedimientos"] += 1
                    valor_por_prestador[prestador] += proc.get("vrServicio", 0)

        # Top 10 prestadores
        top_prestadores = []
        for prestador, total_servicios in prestadores.most_common(10):
            top_prestadores.append({
                "codigo_prestador": prestador,
                "total_servicios": total_servicios,
                "consultas": servicios_por_prestador[prestador]["consultas"],
                "procedimientos": servicios_por_prestador[prestador]["procedimientos"],
                "valor_total": valor_por_prestador[prestador]
            })

        return {
            "total_prestadores": len(prestadores),
            "top_10_prestadores": top_prestadores,
            "distribucion_prestadores": dict(prestadores)
        }

    def generar_resumen_completo(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Genera un resumen completo de todos los análisis

        Args:
            datos: Datos RIPS

        Returns:
            Diccionario con todos los análisis
        """
        return {
            "informacion_general": {
                "num_factura": datos.get("numFactura"),
                "num_documento_obligado": datos.get("numDocumentoIdObligado"),
                "tipo_nota": datos.get("tipoNota"),
                "num_nota": datos.get("numNota")
            },
            "analisis_demografico": self.analisis_demografico(datos),
            "analisis_diagnosticos": self.analisis_diagnosticos(datos),
            "analisis_servicios": self.analisis_servicios(datos),
            "analisis_acudientes": self.analisis_acudientes(datos),
            "analisis_poblacion_gestante": self.analisis_poblacion_gestante(datos),
            "analisis_procedimientos": self.analisis_procedimientos(datos),
            "analisis_tipo_usuario": self.analisis_tipo_usuario(datos),
            "analisis_incapacidades": self.analisis_incapacidades(datos),
            "analisis_modalidad_diagnostico": self.analisis_modalidad_diagnostico(datos),
            "analisis_prestadores": self.analisis_prestadores(datos)
        }
