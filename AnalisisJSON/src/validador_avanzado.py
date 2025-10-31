"""
Sistema avanzado de validación de calidad y alertas para RIPS
Resolución 2275 de 2023
"""
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from catalogos_rips import (
    UMBRALES_ALERTAS,
    CODIGOS_ENFERMEDADES_CRONICAS,
    PREFIJOS_ENFERMEDADES_CRONICAS,
    CODIGOS_EVENTOS_SALUD_PUBLICA,
    GRUPOS_RIESGO,
    PROCEDIMIENTOS_PRIORITARIOS
)


class ValidadorAvanzadoRIPS:
    """Validador avanzado con sistema de alertas para RIPS"""

    def __init__(self, cargador):
        """
        Inicializa el validador avanzado

        Args:
            cargador: Instancia de CargadorRIPS
        """
        self.cargador = cargador
        self.alertas = []

    def validar_y_analizar(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza validación completa y análisis de calidad de datos

        Args:
            datos: Datos RIPS completos

        Returns:
            Diccionario con validaciones, alertas e indicadores
        """
        usuarios = self.cargador.extraer_usuarios(datos)

        resultado = {
            "validaciones": self._validar_datos(usuarios),
            "alertas": self._generar_alertas(datos, usuarios),
            "indicadores_calidad": self._calcular_indicadores_calidad(datos, usuarios),
            "analisis_morbilidad": self._analizar_morbilidad_especifica(usuarios),
            "analisis_oportunidad": self._analizar_oportunidad_atencion(usuarios),
            "grupos_riesgo": self._identificar_grupos_riesgo(usuarios),
            "eventos_salud_publica": self._identificar_eventos_salud_publica(usuarios),
        }

        return resultado

    def _validar_datos(self, usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validación exhaustiva de calidad de datos"""
        validaciones = {
            "total_usuarios": len(usuarios),
            "usuarios_sin_fecha_nacimiento": 0,
            "usuarios_sin_documento": 0,
            "consultas_sin_diagnostico": 0,
            "consultas_sin_fecha": 0,
            "valores_servicio_cero": 0,
            "total_consultas": 0,
            "diagnosticos_invalidos": [],
            "inconsistencias_edad_diagnostico": [],
            "inconsistencias_sexo_diagnostico": [],
        }

        for usuario in usuarios:
            # Validar datos personales
            if not usuario.get("fechaNacimiento"):
                validaciones["usuarios_sin_fecha_nacimiento"] += 1

            if not usuario.get("numDocumentoIdentificacion"):
                validaciones["usuarios_sin_documento"] += 1

            consultas = self.cargador.extraer_consultas(usuario)
            validaciones["total_consultas"] += len(consultas)

            sexo = usuario.get("codSexo")
            edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento")) if usuario.get("fechaNacimiento") else None

            for consulta in consultas:
                # Validar diagnóstico
                diag_principal = consulta.get("codDiagnosticoPrincipal")
                if not diag_principal:
                    validaciones["consultas_sin_diagnostico"] += 1

                # Validar fecha
                if not consulta.get("fechaInicioAtencion"):
                    validaciones["consultas_sin_fecha"] += 1

                # Validar valor
                if consulta.get("vrServicio", 0) == 0:
                    validaciones["valores_servicio_cero"] += 1

                # Validar coherencia diagnóstico-sexo (embarazo en hombres)
                if diag_principal and sexo == "M":
                    if diag_principal.startswith("O") or diag_principal.startswith("Z3"):
                        validaciones["inconsistencias_sexo_diagnostico"].append({
                            "documento": usuario.get("numDocumentoIdentificacion"),
                            "diagnostico": diag_principal,
                            "problema": "Diagnóstico de embarazo en paciente masculino"
                        })

                # Validar coherencia diagnóstico-edad
                if diag_principal and edad is not None:
                    if self._validar_coherencia_edad_diagnostico(diag_principal, edad):
                        validaciones["inconsistencias_edad_diagnostico"].append({
                            "documento": usuario.get("numDocumentoIdentificacion"),
                            "edad": edad,
                            "diagnostico": diag_principal
                        })

        # Calcular porcentajes
        validaciones["porcentaje_sin_fecha_nacimiento"] = (
            validaciones["usuarios_sin_fecha_nacimiento"] / validaciones["total_usuarios"] * 100
            if validaciones["total_usuarios"] > 0 else 0
        )

        validaciones["porcentaje_sin_diagnostico"] = (
            validaciones["consultas_sin_diagnostico"] / validaciones["total_consultas"] * 100
            if validaciones["total_consultas"] > 0 else 0
        )

        validaciones["porcentaje_valores_cero"] = (
            validaciones["valores_servicio_cero"] / validaciones["total_consultas"] * 100
            if validaciones["total_consultas"] > 0 else 0
        )

        return validaciones

    def _validar_coherencia_edad_diagnostico(self, diagnostico: str, edad: int) -> bool:
        """Valida coherencia entre edad y diagnóstico"""
        # Embarazo en menores de 10 o mayores de 55 (alerta)
        if diagnostico.startswith("O") or diagnostico.startswith("Z3"):
            if edad < 10 or edad > 55:
                return True

        # Enfermedades propias de la infancia en adultos
        if diagnostico in ["P00", "P01", "P02", "P03", "P04", "P05"]:  # Códigos perinatales
            if edad > 1:
                return True

        return False

    def _generar_alertas(self, datos: Dict[str, Any], usuarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Genera alertas automáticas según umbrales definidos"""
        alertas = []

        # Calcular métricas para alertas
        total_consultas = sum(len(self.cargador.extraer_consultas(u)) for u in usuarios)
        consultas_sin_autorizacion = 0
        gestantes_adolescentes = 0
        total_gestantes = 0
        pacientes_comorbilidad_alta = 0

        # Listas de usuarios afectados para cada alerta
        usuarios_sin_autorizacion = []
        usuarios_gestantes_adolescentes = []
        usuarios_comorbilidad_alta = []

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)

            # Variable para tracking si este usuario tiene consultas sin autorización
            usuario_sin_autorizacion = False

            # Contar servicios sin autorización
            for consulta in consultas:
                if not consulta.get("numAutorizacion"):
                    consultas_sin_autorizacion += 1
                    if not usuario_sin_autorizacion:
                        usuarios_sin_autorizacion.append({
                            "tipo_documento": usuario.get("tipoDocumentoIdentificacion"),
                            "documento": usuario.get("numDocumentoIdentificacion"),
                            "nombre_completo": f"{usuario.get('primerNombre', '')} {usuario.get('segundoNombre', '')} {usuario.get('primerApellido', '')} {usuario.get('segundoApellido', '')}".strip(),
                            "municipio": usuario.get("codMunicipioResidencia")
                        })
                        usuario_sin_autorizacion = True

                # Identificar gestantes adolescentes
                diag = consulta.get("codDiagnosticoPrincipal", "")
                if diag.startswith("O") or diag.startswith("Z3"):
                    total_gestantes += 1
                    edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento"))
                    if edad and edad < 18:
                        gestantes_adolescentes += 1
                        usuarios_gestantes_adolescentes.append({
                            "tipo_documento": usuario.get("tipoDocumentoIdentificacion"),
                            "documento": usuario.get("numDocumentoIdentificacion"),
                            "nombre_completo": f"{usuario.get('primerNombre', '')} {usuario.get('segundoNombre', '')} {usuario.get('primerApellido', '')} {usuario.get('segundoApellido', '')}".strip(),
                            "municipio": usuario.get("codMunicipioResidencia"),
                            "edad": edad
                        })

            # Contar comorbilidades
            comorbilidades_usuario = 0
            for consulta in consultas:
                for i in range(1, 4):
                    if consulta.get(f"codDiagnosticoRelacionado{i}"):
                        comorbilidades_usuario += 1
            if comorbilidades_usuario >= 3:
                pacientes_comorbilidad_alta += 1
                usuarios_comorbilidad_alta.append({
                    "tipo_documento": usuario.get("tipoDocumentoIdentificacion"),
                    "documento": usuario.get("numDocumentoIdentificacion"),
                    "nombre_completo": f"{usuario.get('primerNombre', '')} {usuario.get('segundoNombre', '')} {usuario.get('primerApellido', '')} {usuario.get('segundoApellido', '')}".strip(),
                    "municipio": usuario.get("codMunicipioResidencia"),
                    "comorbilidades_total": comorbilidades_usuario
                })

        # Generar alertas según umbrales
        porcentaje_sin_autorizacion = (consultas_sin_autorizacion / total_consultas * 100) if total_consultas > 0 else 0
        if porcentaje_sin_autorizacion > UMBRALES_ALERTAS["servicios_sin_autorizacion"]:
            alertas.append({
                "nivel": "ALTA",
                "tipo": "Administrativo",
                "categoria": "Autorizaciones",
                "mensaje": f"Alto porcentaje de servicios sin autorización: {porcentaje_sin_autorizacion:.1f}%",
                "valor_actual": porcentaje_sin_autorizacion,
                "umbral": UMBRALES_ALERTAS["servicios_sin_autorizacion"],
                "recomendacion": "Revisar procesos de autorización previa de servicios",
                "usuarios_afectados": usuarios_sin_autorizacion
            })

        porcentaje_gestantes_adolescentes = (gestantes_adolescentes / total_gestantes * 100) if total_gestantes > 0 else 0
        if porcentaje_gestantes_adolescentes > UMBRALES_ALERTAS["gestantes_adolescentes"]:
            alertas.append({
                "nivel": "MEDIA",
                "tipo": "Salud Pública",
                "categoria": "Salud Materna",
                "mensaje": f"Alto porcentaje de gestantes adolescentes: {porcentaje_gestantes_adolescentes:.1f}%",
                "valor_actual": gestantes_adolescentes,
                "total": total_gestantes,
                "recomendacion": "Fortalecer programas de salud sexual y reproductiva en adolescentes",
                "usuarios_afectados": usuarios_gestantes_adolescentes
            })

        porcentaje_comorbilidad = (pacientes_comorbilidad_alta / len(usuarios) * 100) if usuarios else 0
        if porcentaje_comorbilidad > UMBRALES_ALERTAS["comorbilidades_altas"]:
            alertas.append({
                "nivel": "MEDIA",
                "tipo": "Clínico",
                "categoria": "Comorbilidades",
                "mensaje": f"Alto porcentaje de pacientes con múltiples comorbilidades: {porcentaje_comorbilidad:.1f}%",
                "valor_actual": pacientes_comorbilidad_alta,
                "recomendacion": "Implementar programas de atención integral para pacientes crónicos complejos",
                "usuarios_afectados": usuarios_comorbilidad_alta
            })

        # Detectar posibles brotes epidemiológicos
        brote_detectado = self._detectar_brote_epidemiologico(usuarios)
        if brote_detectado:
            alertas.append(brote_detectado)

        return alertas

    def _detectar_brote_epidemiologico(self, usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detecta posibles brotes epidemiológicos"""
        diagnosticos_por_fecha = defaultdict(lambda: defaultdict(int))

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)
            for consulta in consultas:
                diag = consulta.get("codDiagnosticoPrincipal", "")
                fecha = consulta.get("fechaInicioAtencion", "")[:10]  # Solo fecha

                if diag and fecha:
                    # Buscar enfermedades de interés en salud pública
                    if diag[:3] in CODIGOS_EVENTOS_SALUD_PUBLICA or diag[:4] in CODIGOS_EVENTOS_SALUD_PUBLICA:
                        diagnosticos_por_fecha[fecha][diag] += 1

        # Buscar picos significativos
        for fecha, diagnosticos in diagnosticos_por_fecha.items():
            for diag, cantidad in diagnosticos.items():
                if cantidad >= 3:  # Umbral: 3 o más casos del mismo diagnóstico en un día
                    return {
                        "nivel": "CRÍTICA",
                        "tipo": "Salud Pública",
                        "categoria": "Brote Epidemiológico",
                        "mensaje": f"Posible brote de {diag} detectado el {fecha}",
                        "casos": cantidad,
                        "fecha": fecha,
                        "diagnostico": diag,
                        "recomendacion": "Notificar a autoridades de salud pública. Investigación epidemiológica de campo."
                    }

        return None

    def _calcular_indicadores_calidad(self, datos: Dict[str, Any], usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula indicadores de calidad según Resolución 202 de 2021"""

        # Contadores para indicadores
        total_consultas = 0
        consultas_con_diagnostico = 0
        consultas_con_autorizacion = 0
        consultas_completas = 0  # Con todos los campos requeridos

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)
            total_consultas += len(consultas)

            for consulta in consultas:
                # Completitud de diagnósticos
                if consulta.get("codDiagnosticoPrincipal"):
                    consultas_con_diagnostico += 1

                # Cobertura de autorizaciones
                if consulta.get("numAutorizacion"):
                    consultas_con_autorizacion += 1

                # Calidad de registro (campos completos)
                campos_requeridos = [
                    "fechaInicioAtencion",
                    "codDiagnosticoPrincipal",
                    "codConsulta",
                    "finalidadTecnologiaSalud",
                    "vrServicio"
                ]
                if all(consulta.get(campo) for campo in campos_requeridos):
                    consultas_completas += 1

        # Calcular porcentajes
        oportunidad_atencion = 100.0  # Por defecto 100% si no hay demoras detectadas
        completitud_diagnosticos = (consultas_con_diagnostico / total_consultas * 100) if total_consultas > 0 else 100.0
        cobertura_autorizaciones = (consultas_con_autorizacion / total_consultas * 100) if total_consultas > 0 else 100.0
        calidad_registro = (consultas_completas / total_consultas * 100) if total_consultas > 0 else 100.0

        # Cobertura de programas
        gestantes_con_control = 0
        total_gestantes = 0
        menores_con_control = 0
        total_menores = 0

        for usuario in usuarios:
            edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento"))
            consultas = self.cargador.extraer_consultas(usuario)

            # Gestantes
            es_gestante = False
            tiene_control_prenatal = False

            for consulta in consultas:
                diag = consulta.get("codDiagnosticoPrincipal", "")
                finalidad = consulta.get("finalidadTecnologiaSalud", "")
                cod_consulta = consulta.get("codConsulta", "")

                if diag.startswith("O") or diag.startswith("Z3"):
                    es_gestante = True
                    if finalidad == "15" or cod_consulta in ["890301", "890302"]:
                        tiene_control_prenatal = True

            if es_gestante:
                total_gestantes += 1
                if tiene_control_prenatal:
                    gestantes_con_control += 1

            # Menores de 10 años
            if edad and edad < 10:
                total_menores += 1
                for consulta in consultas:
                    finalidad = consulta.get("finalidadTecnologiaSalud", "")
                    if finalidad == "13":  # Control de crecimiento y desarrollo
                        menores_con_control += 1
                        break

        indicadores = {
            # Indicadores principales para la hoja de Excel
            "oportunidad_atencion": oportunidad_atencion,
            "completitud_diagnosticos": completitud_diagnosticos,
            "cobertura_autorizaciones": cobertura_autorizaciones,
            "calidad_registro": calidad_registro,

            # Detalles adicionales
            "total_consultas": total_consultas,
            "consultas_con_diagnostico": consultas_con_diagnostico,
            "consultas_con_autorizacion": consultas_con_autorizacion,
            "consultas_completas": consultas_completas,

            # Cobertura de programas
            "cobertura_programas": {
                "cobertura_control_prenatal": {
                    "porcentaje": (gestantes_con_control / total_gestantes * 100) if total_gestantes > 0 else 0,
                    "numerador": gestantes_con_control,
                    "denominador": total_gestantes
                },
                "cobertura_crecimiento_desarrollo": {
                    "porcentaje": (menores_con_control / total_menores * 100) if total_menores > 0 else 0,
                    "numerador": menores_con_control,
                    "denominador": total_menores
                }
            }
        }

        return indicadores

    def _analizar_morbilidad_especifica(self, usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análisis detallado de morbilidad específica"""
        morbilidad = {
            "enfermedades_cronicas": Counter(),
            "eventos_salud_publica": Counter(),
            "causas_externas": Counter(),
            "total_pacientes_cronicos": 0,
            "prevalencia_diabetes": 0,
            "prevalencia_hipertension": 0,
            "prevalencia_cancer": 0,
        }

        pacientes_con_ecnt = set()

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)
            doc = usuario.get("numDocumentoIdentificacion")

            for consulta in consultas:
                diag = consulta.get("codDiagnosticoPrincipal", "")

                if not diag:
                    continue

                # Enfermedades crónicas
                if diag[:3] in PREFIJOS_ENFERMEDADES_CRONICAS or diag[:4] in PREFIJOS_ENFERMEDADES_CRONICAS:
                    morbilidad["enfermedades_cronicas"][diag] += 1
                    pacientes_con_ecnt.add(doc)

                    # Contar específicas
                    if diag.startswith("E1"):  # Diabetes
                        morbilidad["prevalencia_diabetes"] += 1
                    elif diag.startswith("I1"):  # Hipertensión
                        morbilidad["prevalencia_hipertension"] += 1
                    elif diag.startswith("C"):  # Cáncer
                        morbilidad["prevalencia_cancer"] += 1

                # Eventos de salud pública
                if diag[:3] in CODIGOS_EVENTOS_SALUD_PUBLICA or diag[:4] in CODIGOS_EVENTOS_SALUD_PUBLICA:
                    morbilidad["eventos_salud_publica"][diag] += 1

        morbilidad["total_pacientes_cronicos"] = len(pacientes_con_ecnt)
        morbilidad["porcentaje_pacientes_cronicos"] = (
            len(pacientes_con_ecnt) / len(usuarios) * 100 if usuarios else 0
        )

        return morbilidad

    def _analizar_oportunidad_atencion(self, usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análisis de oportunidad en la atención"""
        oportunidad = {
            "consultas_urgentes": 0,
            "consultas_programadas": 0,
            "tiempo_promedio_atencion": None,
            "consultas_por_dia_semana": Counter(),
            "consultas_por_mes": Counter(),
        }

        for usuario in usuarios:
            consultas = self.cargador.extraer_consultas(usuario)

            for consulta in consultas:
                causa = consulta.get("causaMotivoAtencion", "")

                # Clasificar por urgencia
                if causa in ["01", "02", "05", "07", "08"]:  # Accidentes, agresiones
                    oportunidad["consultas_urgentes"] += 1
                else:
                    oportunidad["consultas_programadas"] += 1

                # Distribución temporal
                fecha = consulta.get("fechaInicioAtencion")
                if fecha:
                    try:
                        dt = datetime.strptime(fecha[:10], "%Y-%m-%d")
                        dia_semana = dt.strftime("%A")
                        mes = dt.strftime("%Y-%m")

                        oportunidad["consultas_por_dia_semana"][dia_semana] += 1
                        oportunidad["consultas_por_mes"][mes] += 1
                    except:
                        pass

        return oportunidad

    def _identificar_grupos_riesgo(self, usuarios: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Identifica pacientes en grupos de riesgo específicos"""
        grupos = {
            "gestantes_adolescentes": [],
            "gestantes_edad_avanzada": [],
            "adultos_mayores_fragiles": [],
            "pacientes_multimorbidos": [],
            "menores_desnutridos": [],
            "pacientes_oncologicos": [],
        }

        for usuario in usuarios:
            doc = usuario.get("numDocumentoIdentificacion")
            edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento"))
            sexo = usuario.get("codSexo")

            if not edad:
                continue

            consultas = self.cargador.extraer_consultas(usuario)

            # Identificar condiciones
            es_gestante = False
            tiene_cancer = False
            tiene_desnutricion = False
            num_comorbilidades = 0

            diagnosticos_usuario = []

            for consulta in consultas:
                diag = consulta.get("codDiagnosticoPrincipal", "")
                diagnosticos_usuario.append(diag)

                if diag.startswith("O") or diag.startswith("Z3"):
                    es_gestante = True

                if diag.startswith("C"):
                    tiene_cancer = True

                if diag.startswith("E4"):  # Desnutrición
                    tiene_desnutricion = True

                # Contar comorbilidades
                for i in range(1, 4):
                    if consulta.get(f"codDiagnosticoRelacionado{i}"):
                        num_comorbilidades += 1

            # Clasificar en grupos de riesgo
            if es_gestante and sexo == "F":
                if edad < 18:
                    grupos["gestantes_adolescentes"].append({
                        "documento": doc,
                        "edad": edad,
                        "diagnosticos": diagnosticos_usuario
                    })
                elif edad >= 40:
                    grupos["gestantes_edad_avanzada"].append({
                        "documento": doc,
                        "edad": edad,
                        "diagnosticos": diagnosticos_usuario
                    })

            if edad >= 75:
                grupos["adultos_mayores_fragiles"].append({
                    "documento": doc,
                    "edad": edad,
                    "diagnosticos": diagnosticos_usuario
                })

            if num_comorbilidades >= 3:
                grupos["pacientes_multimorbidos"].append({
                    "documento": doc,
                    "edad": edad,
                    "comorbilidades": num_comorbilidades,
                    "diagnosticos": diagnosticos_usuario
                })

            if tiene_desnutricion and edad < 10:
                grupos["menores_desnutridos"].append({
                    "documento": doc,
                    "edad": edad,
                    "diagnosticos": diagnosticos_usuario
                })

            if tiene_cancer:
                grupos["pacientes_oncologicos"].append({
                    "documento": doc,
                    "edad": edad,
                    "diagnosticos": diagnosticos_usuario
                })

        # Agregar conteos (usar list() para evitar modificar dict durante iteración)
        for grupo in list(grupos.keys()):
            grupos[f"{grupo}_count"] = len(grupos[grupo])

        return grupos

    def _identificar_eventos_salud_publica(self, usuarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identifica eventos de interés en salud pública"""
        eventos = {
            "total_eventos": 0,
            "eventos_por_tipo": Counter(),
            "eventos_detalle": [],
            "requiere_notificacion": [],
        }

        for usuario in usuarios:
            doc = usuario.get("numDocumentoIdentificacion")
            edad = self.cargador.calcular_edad(usuario.get("fechaNacimiento"))

            consultas = self.cargador.extraer_consultas(usuario)

            for consulta in consultas:
                diag = consulta.get("codDiagnosticoPrincipal", "")
                fecha = consulta.get("fechaInicioAtencion", "")[:10]

                # Verificar si es evento de salud pública
                if diag[:3] in CODIGOS_EVENTOS_SALUD_PUBLICA:
                    evento_nombre = CODIGOS_EVENTOS_SALUD_PUBLICA.get(diag[:3], "Evento no clasificado")

                    eventos["total_eventos"] += 1
                    eventos["eventos_por_tipo"][diag] += 1

                    evento_detalle = {
                        "documento": doc,
                        "edad": edad,
                        "diagnostico": diag,
                        "nombre_evento": evento_nombre,
                        "fecha": fecha,
                    }

                    eventos["eventos_detalle"].append(evento_detalle)

                    # Eventos que requieren notificación inmediata
                    if diag[:3] in ["A00", "A15", "A33", "A35", "A80", "A82", "A90", "A91", "B05", "B50", "B51"]:
                        eventos["requiere_notificacion"].append(evento_detalle)

        return eventos
