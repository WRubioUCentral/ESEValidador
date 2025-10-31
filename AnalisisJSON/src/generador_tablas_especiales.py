"""
Módulo para generar Excel con tablas especiales AC, AP, AH, AN, USUARIOS y RESUMEN
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
from typing import Dict, List, Any
from src.cargador_rips import CargadorRIPS


class GeneradorTablasEspeciales:
    """Genera Excel con tablas especiales para análisis RIPS"""

    def __init__(self, cargador: CargadorRIPS):
        """
        Inicializa el generador

        Args:
            cargador: Instancia de CargadorRIPS
        """
        self.cargador = cargador

        # Estilos para encabezados
        self.header_font = Font(bold=True, color="FFFFFF", size=10)
        self.header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        self.header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # Bordes
        thin_border = Side(style="thin", color="000000")
        self.border = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)

        # Mapeos de códigos
        self.tipos_usuario = {
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

        self.regimenes = {
            "01": "Contributivo",
            "02": "Contributivo",
            "03": "Contributivo",
            "04": "Subsidiado",
            "05": "No asegurado",
            "06": "Especial",
            "07": "Especial",
            "08": "Especial",
            "09": "Especial"
        }

    def _aplicar_estilo_encabezado(self, ws, row_num: int, columnas: int):
        """Aplica estilo a la fila de encabezado"""
        for col in range(1, columnas + 1):
            cell = ws.cell(row=row_num, column=col)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = self.header_alignment
            cell.border = self.border

    def _aplicar_bordes(self, ws, start_row: int, end_row: int, columnas: int):
        """Aplica bordes a un rango de celdas"""
        for row in range(start_row, end_row + 1):
            for col in range(1, columnas + 1):
                ws.cell(row=row, column=col).border = self.border

    def _ajustar_columnas(self, ws):
        """Ajusta el ancho de las columnas"""
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

    def _obtener_regimen(self, tipo_usuario: str) -> str:
        """Obtiene el régimen a partir del tipo de usuario"""
        return self.regimenes.get(tipo_usuario, "Desconocido")

    def _calcular_edad_con_unidad(self, fecha_nacimiento: str, fecha_referencia: str = None):
        """
        Calcula edad y determina la unidad de medida apropiada

        Returns:
            tuple: (edad, unidad) donde unidad es 1=Años, 2=Meses, 3=Días
        """
        try:
            fn = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            if fecha_referencia:
                if " " in fecha_referencia:
                    fecha_referencia = fecha_referencia.split(" ")[0]
                fr = datetime.strptime(fecha_referencia, "%Y-%m-%d")
            else:
                fr = datetime.now()

            # Calcular diferencia en días
            dias_total = (fr - fn).days

            if dias_total < 30:  # Menos de un mes
                return dias_total, "3"  # Días
            elif dias_total < 365:  # Menos de un año
                meses = dias_total // 30
                return meses, "2"  # Meses
            else:  # Un año o más
                edad = fr.year - fn.year
                if (fr.month, fr.day) < (fn.month, fn.day):
                    edad -= 1
                return edad, "1"  # Años
        except:
            return None, None

    def _extraer_mes(self, fecha_str: str) -> str:
        """Extrae el mes de una fecha"""
        try:
            if " " in fecha_str:
                fecha_str = fecha_str.split(" ")[0]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha.strftime("%Y-%m")
        except:
            return ""

    def generar_tabla_ac_ap(self, datos_consolidados: List[Dict[str, Any]], nombre_archivo: str):
        """
        Genera Excel con tablas AC (Consultas) y AP (Procedimientos)

        Args:
            datos_consolidados: Lista con datos de todos los RIPS
            nombre_archivo: Nombre del archivo Excel a generar
        """
        wb = Workbook()
        wb.remove(wb.active)  # Remover hoja por defecto

        # Tabla AC - Consultas
        ws_ac = wb.create_sheet("AC")
        encabezados_ac = [
            "Número de la factura",
            "Código del prestador de servicios de salud",
            "Tipo de identificación del usuario",
            "Número de identificación del usuario en el sistema",
            "Fecha del procedimiento",
            "Número de Autorización",
            "Código del procedimiento",
            "NOMBRE CUPS",
            "Ambito de realización del procedimiento",
            "Finalidad del procedimiento",
            "Personal que atiende",
            "Diagnóstivo principal",
            "Código del diagnóstico relacionado",
            "Complicación",
            "Forma de realización del acto quirúrgico",
            "Valor del Procedimiento",
            "EPS",
            "MUNICIPIO",
            "REGIMEN",
            "Edad",
            "Unidad de medida de la Edad",
            "SEXO",
            "MES"
        ]

        ws_ac.append(encabezados_ac)
        self._aplicar_estilo_encabezado(ws_ac, 1, len(encabezados_ac))

        row_ac = 2

        # Tabla AP - Procedimientos
        ws_ap = wb.create_sheet("AP")
        encabezados_ap = encabezados_ac.copy()  # Mismos encabezados

        ws_ap.append(encabezados_ap)
        self._aplicar_estilo_encabezado(ws_ap, 1, len(encabezados_ap))

        row_ap = 2

        # Procesar todos los RIPS
        for rips in datos_consolidados:
            datos = rips["datos"]
            num_factura = datos.get("numFactura", "")
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")
                tipo_usuario = usuario.get("tipoUsuario", "")
                fecha_nacimiento = usuario.get("fechaNacimiento", "")
                sexo = usuario.get("codSexo", "")
                cod_municipio = usuario.get("codMunicipioResidencia", "")
                regimen = self._obtener_regimen(tipo_usuario)

                # Procesar CONSULTAS para Tabla AC
                consultas = self.cargador.extraer_consultas(usuario)
                for consulta in consultas:
                    fecha_atencion = consulta.get("fechaInicioAtencion", "")
                    edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento, fecha_atencion)
                    mes = self._extraer_mes(fecha_atencion)

                    fila_ac = [
                        num_factura,
                        consulta.get("codPrestador", ""),
                        tipo_doc,
                        num_doc,
                        fecha_atencion,
                        consulta.get("numAutorizacion", ""),
                        consulta.get("codConsulta", ""),
                        "",  # NOMBRE CUPS - se puede agregar diccionario
                        consulta.get("modalidadGrupoServicioTecSal", ""),
                        consulta.get("finalidadTecnologiaSalud", ""),
                        "",  # Personal que atiende - no disponible en consultas
                        consulta.get("codDiagnosticoPrincipal", ""),
                        consulta.get("codDiagnosticoRelacionado1", ""),
                        "",  # Complicación - no aplica en consultas
                        "",  # Forma de realización - no aplica en consultas
                        consulta.get("vrServicio", 0),
                        tipo_usuario,
                        cod_municipio,
                        regimen,
                        edad,
                        unidad_edad,
                        sexo,
                        mes
                    ]
                    ws_ac.append(fila_ac)
                    row_ac += 1

                # Procesar PROCEDIMIENTOS para Tabla AP
                procedimientos = self.cargador.extraer_procedimientos(usuario)
                for proc in procedimientos:
                    fecha_atencion = proc.get("fechaInicioAtencion", "")
                    edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento, fecha_atencion)
                    mes = self._extraer_mes(fecha_atencion)

                    fila_ap = [
                        num_factura,
                        proc.get("codPrestador", ""),
                        tipo_doc,
                        num_doc,
                        fecha_atencion,
                        proc.get("numAutorizacion", ""),
                        proc.get("codProcedimiento", ""),
                        "",  # NOMBRE CUPS
                        proc.get("modalidadGrupoServicioTecSal", ""),
                        proc.get("finalidadTecnologiaSalud", ""),
                        "",  # Personal que atiende
                        proc.get("codDiagnosticoPrincipal", ""),
                        proc.get("codDiagnosticoRelacionado", ""),
                        proc.get("codComplicacion", ""),
                        "",  # Forma de realización
                        proc.get("vrServicio", 0),
                        tipo_usuario,
                        cod_municipio,
                        regimen,
                        edad,
                        unidad_edad,
                        sexo,
                        mes
                    ]
                    ws_ap.append(fila_ap)
                    row_ap += 1

        # Aplicar bordes y ajustar columnas
        if row_ac > 2:
            self._aplicar_bordes(ws_ac, 2, row_ac - 1, len(encabezados_ac))
        self._ajustar_columnas(ws_ac)

        if row_ap > 2:
            self._aplicar_bordes(ws_ap, 2, row_ap - 1, len(encabezados_ap))
        self._ajustar_columnas(ws_ap)

        # Crear hojas AH, AN, USUARIOS, RESUMEN (por ahora vacías)
        self._crear_tabla_ah(wb, datos_consolidados)
        self._crear_tabla_an(wb, datos_consolidados)
        self._crear_tabla_usuarios(wb, datos_consolidados)
        self._crear_tabla_resumen(wb, datos_consolidados)

        # Guardar archivo
        wb.save(nombre_archivo)
        print(f"\nExcel con tablas especiales generado: {nombre_archivo}")
        print(f"  - Tabla AC: {row_ac - 2} consultas")
        print(f"  - Tabla AP: {row_ap - 2} procedimientos")

    def _crear_tabla_ah(self, wb: Workbook, datos_consolidados: List[Dict[str, Any]]):
        """Crea la tabla AH - Hospitalizaciones"""
        ws = wb.create_sheet("AH")

        encabezados = [
            "FACTURA", "CODIGO MUNICIPIO", "TP DOC", "DOCUMENTO",
            "VIA DE INGRESO", "FECHA DE INGRESO", "HORA DE INGRESO",
            "AUTORIZACION", "CAUSA EXTERNA", "DIAGNOSTICO INGRESO",
            "DIAGNOSTICO EGRESO", "DIAGNOSTICO 2", "DIAGNOSTICO 3",
            "DIAGNOSTICO 4", "DIAGNOSTICO 5", "ESTADO AL EGRESO",
            "DX MUERTE", "FECHA EGRESO", "HORA EGRESO", "EPS",
            "MUNICIPIO", "REGIMEN", "Edad", "Unidad de medida de la Edad",
            "SEXO", "MES"
        ]

        ws.append(encabezados)
        self._aplicar_estilo_encabezado(ws, 1, len(encabezados))

        row = 2

        # Procesar hospitalizaciones
        for rips in datos_consolidados:
            datos = rips["datos"]
            num_factura = datos.get("numFactura", "")
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                servicios = usuario.get("servicios", {})
                hospitalizaciones = servicios.get("hospitalizacion", [])

                if not hospitalizaciones:
                    continue

                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")
                tipo_usuario = usuario.get("tipoUsuario", "")
                fecha_nacimiento = usuario.get("fechaNacimiento", "")
                sexo = usuario.get("codSexo", "")
                cod_municipio = usuario.get("codMunicipioResidencia", "")
                regimen = self._obtener_regimen(tipo_usuario)

                for hosp in hospitalizaciones:
                    fecha_ingreso = hosp.get("fechaInicioAtencion", "")
                    edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento, fecha_ingreso)
                    mes = self._extraer_mes(fecha_ingreso)

                    # Extraer hora de la fecha
                    hora_ingreso = ""
                    hora_egreso = ""
                    if " " in fecha_ingreso:
                        hora_ingreso = fecha_ingreso.split(" ")[1] if len(fecha_ingreso.split(" ")) > 1 else ""

                    fecha_egreso = hosp.get("fechaEgreso", "")
                    if " " in fecha_egreso:
                        hora_egreso = fecha_egreso.split(" ")[1] if len(fecha_egreso.split(" ")) > 1 else ""

                    fila = [
                        num_factura,
                        cod_municipio,
                        tipo_doc,
                        num_doc,
                        hosp.get("viaIngresoServicioSalud", ""),
                        fecha_ingreso.split(" ")[0] if " " in fecha_ingreso else fecha_ingreso,
                        hora_ingreso,
                        hosp.get("numAutorizacion", ""),
                        hosp.get("causaMotivoAtencion", ""),
                        hosp.get("codDiagnosticoPrincipalIngreso", ""),
                        hosp.get("codDiagnosticoPrincipalEgreso", ""),
                        hosp.get("codDiagnosticoRelacionado1Egreso", ""),
                        hosp.get("codDiagnosticoRelacionado2Egreso", ""),
                        hosp.get("codDiagnosticoRelacionado3Egreso", ""),
                        "",  # Diagnostico 5
                        hosp.get("estadoSalidaPaciente", ""),
                        hosp.get("codDiagnosticoCausaMuerte", ""),
                        fecha_egreso.split(" ")[0] if " " in fecha_egreso else fecha_egreso,
                        hora_egreso,
                        tipo_usuario,
                        cod_municipio,
                        regimen,
                        edad,
                        unidad_edad,
                        sexo,
                        mes
                    ]
                    ws.append(fila)
                    row += 1

        if row > 2:
            self._aplicar_bordes(ws, 2, row - 1, len(encabezados))
        self._ajustar_columnas(ws)

    def _crear_tabla_an(self, wb: Workbook, datos_consolidados: List[Dict[str, Any]]):
        """Crea la tabla AN - Recién nacidos"""
        ws = wb.create_sheet("AN")

        encabezados = [
            "Número de la factura",
            "Código del prestador de servicios de salud",
            "Tipo de identificación del usuario",
            "Número de identificación del usuario en el sistema",
            "FECHA DE PARTO",
            "HORA DE O",
            "SEMANAS DE GESTACION",
            "ASISTIO A CONTROLES",
            "SEXO DEL RN",
            "PESO RN",
            "DX",
            "EPS",
            "MUNICIPIO",
            "REGIMEN",
            "Edad",
            "Unidad de medida de la Edad",
            "SEXO",
            "MES"
        ]

        ws.append(encabezados)
        self._aplicar_estilo_encabezado(ws, 1, len(encabezados))

        row = 2

        # Procesar recién nacidos
        for rips in datos_consolidados:
            datos = rips["datos"]
            num_factura = datos.get("numFactura", "")
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                servicios = usuario.get("servicios", {})
                recien_nacidos = servicios.get("recienNacidos", [])

                if not recien_nacidos:
                    continue

                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")
                tipo_usuario = usuario.get("tipoUsuario", "")
                fecha_nacimiento = usuario.get("fechaNacimiento", "")
                sexo = usuario.get("codSexo", "")
                cod_municipio = usuario.get("codMunicipioResidencia", "")
                regimen = self._obtener_regimen(tipo_usuario)

                for rn in recien_nacidos:
                    fecha_parto = rn.get("fechaParto", "")
                    edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento, fecha_parto)
                    mes = self._extraer_mes(fecha_parto)

                    hora_parto = ""
                    if " " in fecha_parto:
                        hora_parto = fecha_parto.split(" ")[1] if len(fecha_parto.split(" ")) > 1 else ""

                    fila = [
                        num_factura,
                        rn.get("codPrestador", ""),
                        tipo_doc,
                        num_doc,
                        fecha_parto.split(" ")[0] if " " in fecha_parto else fecha_parto,
                        hora_parto,
                        rn.get("edadGestacional", ""),
                        rn.get("consultasPrenatales", ""),
                        rn.get("sexo", ""),
                        rn.get("peso", ""),
                        rn.get("codDiagnosticoPrincipal", ""),
                        tipo_usuario,
                        cod_municipio,
                        regimen,
                        edad,
                        unidad_edad,
                        sexo,
                        mes
                    ]
                    ws.append(fila)
                    row += 1

        if row > 2:
            self._aplicar_bordes(ws, 2, row - 1, len(encabezados))
        self._ajustar_columnas(ws)

    def _crear_tabla_usuarios(self, wb: Workbook, datos_consolidados: List[Dict[str, Any]]):
        """Crea la tabla USUARIOS"""
        ws = wb.create_sheet("USUARIOS")

        encabezados = [
            "Tipo de Identificación del Usuario",
            "Número de Identifiación del Usuario en el Sistema",
            "Código Entidad Administradora",
            "Tipo de Usuario",
            "Primer Apellido del usuario",
            "Segundo apellido del usuario",
            "Primer nombre del usuario",
            "Segundo nombre del usuario",
            "Edad",
            "Unidad de medida de la Edad",
            "Sexo",
            "Código del departamento de residencia habitual",
            "Código de municipios de residencia habitual",
            "Zona de residencia habitual",
            "EPS",
            "MES",
            "REGIMEN",
            "SEDE"
        ]

        ws.append(encabezados)
        self._aplicar_estilo_encabezado(ws, 1, len(encabezados))

        row = 2
        usuarios_procesados = set()  # Para evitar duplicados

        for rips in datos_consolidados:
            datos = rips["datos"]
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")

                # Evitar duplicados
                clave_usuario = f"{tipo_doc}-{num_doc}"
                if clave_usuario in usuarios_procesados:
                    continue
                usuarios_procesados.add(clave_usuario)

                tipo_usuario = usuario.get("tipoUsuario", "")
                fecha_nacimiento = usuario.get("fechaNacimiento", "")
                edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento)
                regimen = self._obtener_regimen(tipo_usuario)

                # Extraer mes de la primera consulta o procedimiento
                mes = ""
                servicios = usuario.get("servicios", {})
                consultas = servicios.get("consultas", [])
                if consultas:
                    mes = self._extraer_mes(consultas[0].get("fechaInicioAtencion", ""))

                # Extraer departamento del código de municipio (primeros 2 dígitos)
                cod_municipio = usuario.get("codMunicipioResidencia", "")
                cod_departamento = cod_municipio[:2] if len(cod_municipio) >= 2 else ""

                fila = [
                    tipo_doc,
                    num_doc,
                    "",  # Código Entidad Administradora - no disponible
                    tipo_usuario,
                    usuario.get("primerApellido", ""),
                    usuario.get("segundoApellido", ""),
                    usuario.get("primerNombre", ""),
                    usuario.get("segundoNombre", ""),
                    edad,
                    unidad_edad,
                    usuario.get("codSexo", ""),
                    cod_departamento,
                    cod_municipio,
                    usuario.get("codZonaTerritorialResidencia", ""),
                    tipo_usuario,
                    mes,
                    regimen,
                    ""  # SEDE - no disponible
                ]
                ws.append(fila)
                row += 1

        if row > 2:
            self._aplicar_bordes(ws, 2, row - 1, len(encabezados))
        self._ajustar_columnas(ws)

    def _crear_tabla_resumen(self, wb: Workbook, datos_consolidados: List[Dict[str, Any]]):
        """Crea la tabla RESUMEN con indicadores por usuario"""
        ws = wb.create_sheet("RESUMEN")

        encabezados = [
            "Tipo de Identificación del Usuario",
            "Número de Identifiación del Usuario en el Sistema",
            "Código Entidad Administradora",
            "Tipo de Usuario",
            "Primer Apellido del usuario",
            "Segundo apellido del usuario",
            "Primer nombre del usuario",
            "Segundo nombre del usuario",
            "Edad",
            "Unidad de medida de la Edad",
            "Sexo",
            "Código del departamento de residencia habitual",
            "Código de municipios de residencia habitual",
            "Zona de residencia habitual",
            "EPS",
            "MES",
            "REGIMEN",
            "SEDE",
            "CCU",
            "ODONTOLOGIA PRIMERA VEZ",
            "ODONTOLOGIA CONTROL",
            "PLACA BACTERIANA",
            "FLUOR",
            "DETARTRAJE",
            "SELLANTES",
            "VALORACIÓN INTEGRAL",
            "Primera Infancia",
            "Infancia",
            "Adolescencia",
            "Juventud",
            "Adultez",
            "Vejez",
            "AGUDEZA VISUAL",
            "PLANIFICACION FAMILIAR",
            "FECHA SUMINISTRO",
            "SUMINISTRO DE METODO",
            "SANGRE OCULTA",
            "COLESTEROL HDL",
            "COLESTEROL LDL",
            "COLESTEROL TOTAL",
            "GLICEMIA",
            "CREATININA",
            "TRIGLICERIDOS"
        ]

        ws.append(encabezados)
        self._aplicar_estilo_encabezado(ws, 1, len(encabezados))

        row = 2

        # Códigos CUPS para identificar procedimientos específicos
        codigos_cups = {
            "CCU": ["879101", "879102"],  # Citología cervicouterina
            "ODONTOLOGIA_PRIMERA": ["890201"],  # Primera vez por odontología
            "ODONTOLOGIA_CONTROL": ["890202"],  # Control por odontología
            "PLACA_BACTERIANA": ["997101"],  # Índice de placa bacteriana
            "FLUOR": ["997310"],  # Aplicación de flúor
            "DETARTRAJE": ["997302"],  # Detartraje supragingival
            "SELLANTES": ["997311"],  # Aplicación de sellantes
            "VALORACION_INTEGRAL": ["890201", "890301"],  # Consultas integrales
            "AGUDEZA_VISUAL": ["950101"],  # Agudeza visual
            "PLANIFICACION": ["990201"],  # Planificación familiar
        }

        # Códigos de laboratorio
        codigos_lab = {
            "SANGRE_OCULTA": ["902222"],
            "COLESTEROL_HDL": ["903815"],
            "COLESTEROL_LDL": ["903816"],
            "COLESTEROL_TOTAL": ["903814"],
            "GLICEMIA": ["903841"],
            "CREATININA": ["903895"],
            "TRIGLICERIDOS": ["903818"]
        }

        usuarios_procesados = {}

        # Primera pasada: recolectar información de usuarios
        for rips in datos_consolidados:
            datos = rips["datos"]
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")
                clave_usuario = f"{tipo_doc}-{num_doc}"

                if clave_usuario not in usuarios_procesados:
                    tipo_usuario = usuario.get("tipoUsuario", "")
                    fecha_nacimiento = usuario.get("fechaNacimiento", "")
                    edad, unidad_edad = self._calcular_edad_con_unidad(fecha_nacimiento)
                    regimen = self._obtener_regimen(tipo_usuario)

                    # Determinar curso de vida
                    curso_vida = self._determinar_curso_vida(edad, unidad_edad)

                    # Extraer mes
                    mes = ""
                    servicios = usuario.get("servicios", {})
                    consultas = servicios.get("consultas", [])
                    if consultas:
                        mes = self._extraer_mes(consultas[0].get("fechaInicioAtencion", ""))

                    cod_municipio = usuario.get("codMunicipioResidencia", "")
                    cod_departamento = cod_municipio[:2] if len(cod_municipio) >= 2 else ""

                    usuarios_procesados[clave_usuario] = {
                        "tipo_doc": tipo_doc,
                        "num_doc": num_doc,
                        "tipo_usuario": tipo_usuario,
                        "primer_apellido": usuario.get("primerApellido", ""),
                        "segundo_apellido": usuario.get("segundoApellido", ""),
                        "primer_nombre": usuario.get("primerNombre", ""),
                        "segundo_nombre": usuario.get("segundoNombre", ""),
                        "edad": edad,
                        "unidad_edad": unidad_edad,
                        "sexo": usuario.get("codSexo", ""),
                        "cod_departamento": cod_departamento,
                        "cod_municipio": cod_municipio,
                        "zona": usuario.get("codZonaTerritorialResidencia", ""),
                        "regimen": regimen,
                        "mes": mes,
                        "curso_vida": curso_vida,
                        "procedimientos": {},
                        "laboratorios": {}
                    }

                # Recolectar procedimientos
                procedimientos = self.cargador.extraer_procedimientos(usuario)
                for proc in procedimientos:
                    cod_proc = proc.get("codProcedimiento", "")
                    if cod_proc:
                        if cod_proc not in usuarios_procesados[clave_usuario]["procedimientos"]:
                            usuarios_procesados[clave_usuario]["procedimientos"][cod_proc] = 0
                        usuarios_procesados[clave_usuario]["procedimientos"][cod_proc] += 1

        # Segunda pasada: generar filas
        for clave, datos_usuario in usuarios_procesados.items():
            # Verificar procedimientos específicos
            tiene_ccu = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["CCU"])
            tiene_odonto_pv = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["ODONTOLOGIA_PRIMERA"])
            tiene_odonto_ctrl = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["ODONTOLOGIA_CONTROL"])
            tiene_placa = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["PLACA_BACTERIANA"])
            tiene_fluor = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["FLUOR"])
            tiene_detartraje = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["DETARTRAJE"])
            tiene_sellantes = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["SELLANTES"])
            tiene_valoracion = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["VALORACION_INTEGRAL"])
            tiene_agudeza = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["AGUDEZA_VISUAL"])
            tiene_planif = any(cod in datos_usuario["procedimientos"] for cod in codigos_cups["PLANIFICACION"])

            # Laboratorios
            tiene_sangre = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["SANGRE_OCULTA"])
            tiene_hdl = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["COLESTEROL_HDL"])
            tiene_ldl = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["COLESTEROL_LDL"])
            tiene_col_total = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["COLESTEROL_TOTAL"])
            tiene_glicemia = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["GLICEMIA"])
            tiene_creatinina = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["CREATININA"])
            tiene_trigli = any(cod in datos_usuario["procedimientos"] for cod in codigos_lab["TRIGLICERIDOS"])

            fila = [
                datos_usuario["tipo_doc"],
                datos_usuario["num_doc"],
                "",  # Código Entidad Administradora
                datos_usuario["tipo_usuario"],
                datos_usuario["primer_apellido"],
                datos_usuario["segundo_apellido"],
                datos_usuario["primer_nombre"],
                datos_usuario["segundo_nombre"],
                datos_usuario["edad"],
                datos_usuario["unidad_edad"],
                datos_usuario["sexo"],
                datos_usuario["cod_departamento"],
                datos_usuario["cod_municipio"],
                datos_usuario["zona"],
                datos_usuario["tipo_usuario"],
                datos_usuario["mes"],
                datos_usuario["regimen"],
                "",  # SEDE
                "SI" if tiene_ccu else "NO",
                "SI" if tiene_odonto_pv else "NO",
                "SI" if tiene_odonto_ctrl else "NO",
                "SI" if tiene_placa else "NO",
                "SI" if tiene_fluor else "NO",
                "SI" if tiene_detartraje else "NO",
                "SI" if tiene_sellantes else "NO",
                "SI" if tiene_valoracion else "NO",
                "SI" if datos_usuario["curso_vida"] == "Primera Infancia" else "NO",
                "SI" if datos_usuario["curso_vida"] == "Infancia" else "NO",
                "SI" if datos_usuario["curso_vida"] == "Adolescencia" else "NO",
                "SI" if datos_usuario["curso_vida"] == "Juventud" else "NO",
                "SI" if datos_usuario["curso_vida"] == "Adultez" else "NO",
                "SI" if datos_usuario["curso_vida"] == "Vejez" else "NO",
                "SI" if tiene_agudeza else "NO",
                "SI" if tiene_planif else "NO",
                datos_usuario["mes"],  # FECHA SUMINISTRO
                "SI" if tiene_planif else "NO",
                "SI" if tiene_sangre else "NO",
                "SI" if tiene_hdl else "NO",
                "SI" if tiene_ldl else "NO",
                "SI" if tiene_col_total else "NO",
                "SI" if tiene_glicemia else "NO",
                "SI" if tiene_creatinina else "NO",
                "SI" if tiene_trigli else "NO"
            ]
            ws.append(fila)
            row += 1

        if row > 2:
            self._aplicar_bordes(ws, 2, row - 1, len(encabezados))
        self._ajustar_columnas(ws)

    def _determinar_curso_vida(self, edad, unidad_edad) -> str:
        """Determina el curso de vida según Resolución 3280 de 2018"""
        if not edad or not unidad_edad:
            return "Desconocido"

        # Convertir todo a años para facilitar la clasificación
        if unidad_edad == "3":  # Días
            edad_anos = edad / 365
        elif unidad_edad == "2":  # Meses
            edad_anos = edad / 12
        else:  # Años
            edad_anos = edad

        if edad_anos < 6:
            return "Primera Infancia"
        elif edad_anos < 12:
            return "Infancia"
        elif edad_anos < 18:
            return "Adolescencia"
        elif edad_anos < 29:
            return "Juventud"
        elif edad_anos < 60:
            return "Adultez"
        else:
            return "Vejez"
