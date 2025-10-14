"""
Módulo para análisis de datos RIPS
"""
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Tuple
from cargador_rips import CargadorRIPS


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
            "distribucion_edad": {
                "0-5": 0,
                "6-11": 0,
                "12-17": 0,
                "18-26": 0,
                "27-59": 0,
                "60+": 0
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

            # Edad
            fecha_nac = usuario.get("fechaNacimiento")
            if fecha_nac:
                edad = self.cargador.calcular_edad(fecha_nac)
                if edad is not None:
                    if edad <= 5:
                        grupo_edad = "0-5"
                    elif edad <= 11:
                        grupo_edad = "6-11"
                    elif edad <= 17:
                        grupo_edad = "12-17"
                    elif edad <= 26:
                        grupo_edad = "18-26"
                    elif edad <= 59:
                        grupo_edad = "27-59"
                    else:
                        grupo_edad = "60+"

                    resultado["distribucion_edad"][grupo_edad] += 1
                    resultado["distribucion_sexo_edad"][sexo][grupo_edad] += 1

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

        # Top 10 diagnósticos principales
        contador_diag = Counter([d["codigo"] for d in diagnosticos_principales])
        top_diagnosticos = []
        for codigo, cantidad in contador_diag.most_common(10):
            info = self.cargador.obtener_info_diagnostico(codigo)
            top_diagnosticos.append({
                **info,
                "cantidad": cantidad
            })

        return {
            "total_diagnosticos": len(diagnosticos_principales),
            "diagnosticos_unicos": len(contador_diag),
            "top_10_diagnosticos": top_diagnosticos,
            "diagnosticos_con_comorbilidades": len(comorbilidades),
            "comorbilidades_detalle": comorbilidades,
            "diagnosticos_por_grupo_edad": dict(diagnosticos_por_edad)
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
            "analisis_acudientes": self.analisis_acudientes(datos)
        }
