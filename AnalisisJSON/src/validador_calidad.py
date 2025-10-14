"""
Módulo para validar la calidad de datos RIPS según Resolución 2275 de 2023
"""
from typing import Dict, List, Any
from datetime import datetime
import re


class ValidadorCalidadRIPS:
    """Clase para validar la calidad de datos RIPS"""

    def __init__(self):
        """Inicializa el validador con las reglas de validación"""
        self.anomalias = []
        self.campos_obligatorios_consulta = [
            "num_factura",
            "cod_prestador",
            "tipo_documento_identificacion",
            "num_documento_identificacion",
            "fecha_consulta",
            "num_autorizacion",
            "cod_consulta",
            "finalidad_consulta",
            "causa_externa",
            "diagnostico_principal",
            "tipo_diagnostico_principal"
        ]

    def validar_datos_completos(self, datos_rips: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida que los datos estén completos según la Resolución 2275

        Args:
            datos_rips: Datos RIPS a validar

        Returns:
            Diccionario con el resultado de la validación
        """
        self.anomalias = []
        consultas = datos_rips.get("consultas", [])

        for idx, consulta in enumerate(consultas, 1):
            self._validar_campos_obligatorios(consulta, idx)
            self._validar_formato_documento(consulta, idx)
            self._validar_fecha(consulta, idx)
            self._validar_edad_coherencia(consulta, idx)
            self._validar_diagnosticos(consulta, idx)
            self._validar_relacion_acudiente(consulta, idx)
            self._validar_valores_numericos(consulta, idx)
            self._validar_codigos_validos(consulta, idx)

        return self._generar_reporte_validacion()

    def _validar_campos_obligatorios(self, consulta: Dict[str, Any], idx: int):
        """Valida que existan todos los campos obligatorios"""
        for campo in self.campos_obligatorios_consulta:
            valor = consulta.get(campo)
            if valor is None or valor == "" or valor == "null":
                self.anomalias.append({
                    "tipo": "CAMPO_OBLIGATORIO_FALTANTE",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": campo,
                    "descripcion": f"El campo '{campo}' es obligatorio y está vacío o nulo",
                    "valor_actual": str(valor),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

    def _validar_formato_documento(self, consulta: Dict[str, Any], idx: int):
        """Valida el formato del número de documento"""
        tipo_doc = consulta.get("tipo_documento_identificacion")
        num_doc = consulta.get("num_documento_identificacion")

        if num_doc:
            # El documento debe ser numérico
            if not str(num_doc).isdigit():
                self.anomalias.append({
                    "tipo": "FORMATO_DOCUMENTO_INVALIDO",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": "num_documento_identificacion",
                    "descripcion": f"El número de documento debe ser numérico",
                    "valor_actual": str(num_doc),
                    "documento_paciente": num_doc
                })

            # Validar longitud según tipo de documento
            longitud = len(str(num_doc))
            if tipo_doc == "CC" and (longitud < 6 or longitud > 10):
                self.anomalias.append({
                    "tipo": "LONGITUD_DOCUMENTO_INVALIDA",
                    "severidad": "MEDIA",
                    "registro": idx,
                    "campo": "num_documento_identificacion",
                    "descripcion": f"La CC debe tener entre 6 y 10 dígitos",
                    "valor_actual": str(num_doc),
                    "documento_paciente": num_doc
                })

    def _validar_fecha(self, consulta: Dict[str, Any], idx: int):
        """Valida el formato y coherencia de las fechas"""
        fecha_consulta = consulta.get("fecha_consulta")

        if fecha_consulta:
            try:
                # Formato esperado: YYYY-MM-DD HH:MM o YYYY-MM-DD
                if " " in str(fecha_consulta):
                    fecha_obj = datetime.strptime(str(fecha_consulta), "%Y-%m-%d %H:%M")
                else:
                    fecha_obj = datetime.strptime(str(fecha_consulta), "%Y-%m-%d")

                # La fecha no debe ser futura
                if fecha_obj > datetime.now():
                    self.anomalias.append({
                        "tipo": "FECHA_FUTURA",
                        "severidad": "ALTA",
                        "registro": idx,
                        "campo": "fecha_consulta",
                        "descripcion": "La fecha de consulta no puede ser futura",
                        "valor_actual": str(fecha_consulta),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

                # La fecha no debe ser muy antigua (más de 10 años)
                años_diferencia = (datetime.now() - fecha_obj).days / 365
                if años_diferencia > 10:
                    self.anomalias.append({
                        "tipo": "FECHA_MUY_ANTIGUA",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "fecha_consulta",
                        "descripcion": f"La fecha de consulta es muy antigua ({años_diferencia:.1f} años)",
                        "valor_actual": str(fecha_consulta),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

            except ValueError:
                self.anomalias.append({
                    "tipo": "FORMATO_FECHA_INVALIDO",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": "fecha_consulta",
                    "descripcion": "El formato de fecha es inválido (esperado: YYYY-MM-DD o YYYY-MM-DD HH:MM)",
                    "valor_actual": str(fecha_consulta),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

    def _validar_edad_coherencia(self, consulta: Dict[str, Any], idx: int):
        """Valida la coherencia de la edad"""
        edad = consulta.get("edad")
        tipo_doc = consulta.get("tipo_documento_identificacion")
        sexo = consulta.get("sexo")

        if edad is not None:
            try:
                edad_num = int(edad)

                # Edad debe ser positiva
                if edad_num < 0:
                    self.anomalias.append({
                        "tipo": "EDAD_NEGATIVA",
                        "severidad": "ALTA",
                        "registro": idx,
                        "campo": "edad",
                        "descripcion": "La edad no puede ser negativa",
                        "valor_actual": str(edad),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

                # Edad no debe exceder 120 años
                if edad_num > 120:
                    self.anomalias.append({
                        "tipo": "EDAD_EXCESIVA",
                        "severidad": "ALTA",
                        "registro": idx,
                        "campo": "edad",
                        "descripcion": "La edad excede los 120 años",
                        "valor_actual": str(edad),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

                # Coherencia entre tipo de documento y edad
                if tipo_doc == "RC" and edad_num > 7:
                    self.anomalias.append({
                        "tipo": "INCOHERENCIA_TIPO_DOC_EDAD",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "tipo_documento_identificacion",
                        "descripcion": f"Registro Civil (RC) no coherente con edad {edad_num} años (debe ser ≤7 años)",
                        "valor_actual": f"{tipo_doc} - {edad_num} años",
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

                if tipo_doc == "TI" and (edad_num < 7 or edad_num > 17):
                    self.anomalias.append({
                        "tipo": "INCOHERENCIA_TIPO_DOC_EDAD",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "tipo_documento_identificacion",
                        "descripcion": f"Tarjeta de Identidad (TI) no coherente con edad {edad_num} años (debe estar entre 7 y 17 años)",
                        "valor_actual": f"{tipo_doc} - {edad_num} años",
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

                if tipo_doc == "CC" and edad_num < 18:
                    self.anomalias.append({
                        "tipo": "INCOHERENCIA_TIPO_DOC_EDAD",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "tipo_documento_identificacion",
                        "descripcion": f"Cédula de Ciudadanía (CC) no coherente con edad {edad_num} años (debe ser ≥18 años)",
                        "valor_actual": f"{tipo_doc} - {edad_num} años",
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })

            except (ValueError, TypeError):
                self.anomalias.append({
                    "tipo": "FORMATO_EDAD_INVALIDO",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": "edad",
                    "descripcion": "La edad debe ser un número entero",
                    "valor_actual": str(edad),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

        # Validar sexo
        if sexo and sexo not in ["F", "M"]:
            self.anomalias.append({
                "tipo": "VALOR_SEXO_INVALIDO",
                "severidad": "ALTA",
                "registro": idx,
                "campo": "sexo",
                "descripcion": "El sexo debe ser 'F' o 'M'",
                "valor_actual": str(sexo),
                "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
            })

    def _validar_diagnosticos(self, consulta: Dict[str, Any], idx: int):
        """Valida diagnósticos y su coherencia"""
        diag_principal = consulta.get("diagnostico_principal")
        tipo_diag = consulta.get("tipo_diagnostico_principal")
        edad = consulta.get("edad")
        sexo = consulta.get("sexo")

        # Diagnóstico principal debe tener formato válido (letra + números)
        if diag_principal:
            if not re.match(r'^[A-Z][0-9]{2,3}[0-9A-Z]?$', str(diag_principal)):
                self.anomalias.append({
                    "tipo": "FORMATO_DIAGNOSTICO_INVALIDO",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": "diagnostico_principal",
                    "descripcion": "El código de diagnóstico debe seguir el formato CIE-10 (ej: Z719, A001)",
                    "valor_actual": str(diag_principal),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

        # Tipo de diagnóstico debe ser válido
        if tipo_diag and tipo_diag not in ["1", "2", "3", "4"]:
            self.anomalias.append({
                "tipo": "TIPO_DIAGNOSTICO_INVALIDO",
                "severidad": "MEDIA",
                "registro": idx,
                "campo": "tipo_diagnostico_principal",
                "descripcion": "El tipo de diagnóstico debe ser: 1=Impresión diagnóstica, 2=Confirmado nuevo, 3=Confirmado repetido, 4=No aplica",
                "valor_actual": str(tipo_diag),
                "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
            })

        # Validar coherencia diagnóstico-sexo (embarazo en hombres, etc.)
        if diag_principal and sexo == "M":
            # Códigos relacionados con embarazo (Z3x, O00-O99)
            if str(diag_principal).startswith(('Z3', 'O')):
                self.anomalias.append({
                    "tipo": "INCOHERENCIA_DIAGNOSTICO_SEXO",
                    "severidad": "ALTA",
                    "registro": idx,
                    "campo": "diagnostico_principal",
                    "descripcion": f"Diagnóstico relacionado con embarazo/parto asignado a paciente masculino",
                    "valor_actual": f"{diag_principal} - Sexo: {sexo}",
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

    def _validar_relacion_acudiente(self, consulta: Dict[str, Any], idx: int):
        """Valida la coherencia en la relación con acudientes"""
        edad = consulta.get("edad")
        cod_acudiente = consulta.get("cod_acudiente")

        try:
            edad_num = int(edad) if edad else None

            # Menores de 18 deberían tener acudiente
            if edad_num is not None and edad_num < 18 and not cod_acudiente:
                self.anomalias.append({
                    "tipo": "MENOR_SIN_ACUDIENTE",
                    "severidad": "MEDIA",
                    "registro": idx,
                    "campo": "cod_acudiente",
                    "descripcion": f"Menor de edad ({edad_num} años) sin acudiente registrado",
                    "valor_actual": "Sin acudiente",
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

            # Mayores de 18 no deberían tener acudiente (salvo excepciones)
            if edad_num is not None and edad_num >= 18 and cod_acudiente:
                self.anomalias.append({
                    "tipo": "MAYOR_CON_ACUDIENTE",
                    "severidad": "BAJA",
                    "registro": idx,
                    "campo": "cod_acudiente",
                    "descripcion": f"Mayor de edad ({edad_num} años) con acudiente registrado (verificar si aplica)",
                    "valor_actual": str(cod_acudiente),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

        except (ValueError, TypeError):
            pass

    def _validar_valores_numericos(self, consulta: Dict[str, Any], idx: int):
        """Valida que los valores numéricos tengan formato correcto"""
        valor_consulta = consulta.get("valor_consulta")
        copago = consulta.get("valor_cuota_moderadora")

        # Valores deben ser numéricos y no negativos
        if valor_consulta is not None:
            try:
                valor_num = float(valor_consulta)
                if valor_num < 0:
                    self.anomalias.append({
                        "tipo": "VALOR_NEGATIVO",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "valor_consulta",
                        "descripcion": "El valor de la consulta no puede ser negativo",
                        "valor_actual": str(valor_consulta),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })
            except (ValueError, TypeError):
                self.anomalias.append({
                    "tipo": "FORMATO_VALOR_INVALIDO",
                    "severidad": "MEDIA",
                    "registro": idx,
                    "campo": "valor_consulta",
                    "descripcion": "El valor de la consulta debe ser numérico",
                    "valor_actual": str(valor_consulta),
                    "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                })

        if copago is not None:
            try:
                copago_num = float(copago)
                if copago_num < 0:
                    self.anomalias.append({
                        "tipo": "VALOR_NEGATIVO",
                        "severidad": "MEDIA",
                        "registro": idx,
                        "campo": "valor_cuota_moderadora",
                        "descripcion": "El copago no puede ser negativo",
                        "valor_actual": str(copago),
                        "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
                    })
            except (ValueError, TypeError):
                pass

    def _validar_codigos_validos(self, consulta: Dict[str, Any], idx: int):
        """Valida que los códigos cumplan con los dominios establecidos"""
        finalidad = consulta.get("finalidad_consulta")
        causa = consulta.get("causa_externa")
        zona = consulta.get("zona_territorial_residencia")

        # Validar finalidad de consulta
        finalidades_validas = ["01", "02", "03", "04", "05", "06", "10", "11", "12", "13", "14", "15", "16", "17"]
        if finalidad and finalidad not in finalidades_validas:
            self.anomalias.append({
                "tipo": "CODIGO_FINALIDAD_INVALIDO",
                "severidad": "ALTA",
                "registro": idx,
                "campo": "finalidad_consulta",
                "descripcion": f"El código de finalidad '{finalidad}' no es válido",
                "valor_actual": str(finalidad),
                "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
            })

        # Validar causa externa
        causas_validas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "26", "38"]
        if causa and causa not in causas_validas:
            self.anomalias.append({
                "tipo": "CODIGO_CAUSA_INVALIDO",
                "severidad": "ALTA",
                "registro": idx,
                "campo": "causa_externa",
                "descripcion": f"El código de causa externa '{causa}' no es válido",
                "valor_actual": str(causa),
                "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
            })

        # Validar zona territorial
        zonas_validas = ["01", "02"]
        if zona and zona not in zonas_validas:
            self.anomalias.append({
                "tipo": "CODIGO_ZONA_INVALIDO",
                "severidad": "MEDIA",
                "registro": idx,
                "campo": "zona_territorial_residencia",
                "descripcion": f"El código de zona territorial '{zona}' no es válido (01=Urbana, 02=Rural)",
                "valor_actual": str(zona),
                "documento_paciente": consulta.get("num_documento_identificacion", "N/A")
            })

    def _generar_reporte_validacion(self) -> Dict[str, Any]:
        """Genera el reporte de validación con estadísticas"""
        # Contar por severidad
        severidades = {"ALTA": 0, "MEDIA": 0, "BAJA": 0}
        tipos = {}

        for anomalia in self.anomalias:
            sev = anomalia.get("severidad", "MEDIA")
            severidades[sev] = severidades.get(sev, 0) + 1

            tipo = anomalia.get("tipo", "OTRO")
            tipos[tipo] = tipos.get(tipo, 0) + 1

        # Top 10 anomalías más frecuentes
        top_anomalias = sorted(tipos.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total_anomalias": len(self.anomalias),
            "por_severidad": severidades,
            "por_tipo": tipos,
            "top_10_anomalias": [{"tipo": t, "cantidad": c} for t, c in top_anomalias],
            "detalle_anomalias": self.anomalias,
            "calidad_datos": self._calcular_calidad()
        }

    def _calcular_calidad(self) -> str:
        """Calcula el nivel de calidad de los datos"""
        total = len(self.anomalias)

        if total == 0:
            return "EXCELENTE"
        elif total <= 5:
            return "BUENA"
        elif total <= 15:
            return "REGULAR"
        elif total <= 30:
            return "DEFICIENTE"
        else:
            return "CRÍTICA"
