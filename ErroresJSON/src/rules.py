"""
Reglas de validación específicas para cada tipo de archivo RIPS
según Resolución 2275 de 2023 y Resolución 3280 de 2018
"""
from typing import List, Dict, Any
from .validators import (
    BaseValidator, DateValidator, NumericValidator, LengthValidator,
    CodeValidator, TextValidator
)
from .models import AFRecord, USRecord, ACRecord, APRecord, ATRecord, AHRecord, AMRecord, ANRecord, CTRecord


class ValidationError:
    """Representa un error de validación"""

    def __init__(self, file_name: str, line_number: int, field_name: str, error_description: str, regulation: str, suggested_fix: str):
        self.file_name = file_name
        self.line_number = line_number
        self.field_name = field_name
        self.error_description = error_description
        self.regulation = regulation
        self.suggested_fix = suggested_fix

    def to_dict(self) -> Dict[str, Any]:
        return {
            'nombre_documento': self.file_name,
            'numero_linea': self.line_number,
            'nombre_campo': self.field_name,
            'descripcion_error': self.error_description,
            'regla_normativa': self.regulation,
            'correccion_recomendada': self.suggested_fix
        }


class AFValidator:
    """Validador para archivo de Transacciones (AF)"""

    @staticmethod
    def validate(record: AFRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro AF"""
        errors = []

        # 1. Código del prestador (12 dígitos)
        valid, msg = LengthValidator.validate_length(record.cod_prestador, "cod_prestador", 12, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_prestador", msg, "Res. 2275/2023", "Verificar código habilitación del prestador"))

        valid, msg = NumericValidator.validate_integer(record.cod_prestador, "cod_prestador", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_prestador", msg, "Res. 2275/2023", "El código debe ser numérico"))

        # 2. Nombre del prestador (60 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.nombre_prestador, "nombre_prestador", 60, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "nombre_prestador", msg, "Res. 2275/2023", "Reducir longitud del nombre"))

        # 3. Tipo de documento del prestador
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento_prestador, "tipo_documento_prestador")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento_prestador", msg, "Res. 2275/2023", "Usar: CC, NI, CE, etc."))

        # 4. Número de documento del prestador (20 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.num_documento_prestador, "num_documento_prestador", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_documento_prestador", msg, "Res. 2275/2023", "Verificar número de documento"))

        # 5. Número de factura (20 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.num_factura, "num_factura", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_factura", msg, "Res. 2275/2023", "Verificar número de factura"))

        # 6. Fecha de expedición
        valid, msg, _ = DateValidator.validate_format(record.fecha_expedicion, "fecha_expedicion", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_expedicion", msg, "Res. 2275/2023", "Formato: DD/MM/YYYY"))

        # 7. Fecha inicio
        valid, msg, _ = DateValidator.validate_format(record.fecha_inicio, "fecha_inicio", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_inicio", msg, "Res. 2275/2023", "Formato: DD/MM/YYYY"))

        # 8. Fecha final
        valid, msg, _ = DateValidator.validate_format(record.fecha_final, "fecha_final", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_final", msg, "Res. 2275/2023", "Formato: DD/MM/YYYY"))

        # Validar rango de fechas
        valid, msg = DateValidator.validate_date_range(record.fecha_inicio, record.fecha_final, "fecha_inicio", "fecha_final")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_inicio/fecha_final", msg, "Res. 2275/2023", "Fecha inicio debe ser <= fecha final"))

        # 9. Código entidad administradora (6 caracteres)
        valid, msg = LengthValidator.validate_length(record.cod_entidad_administradora, "cod_entidad_administradora", 6, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_entidad_administradora", msg, "Res. 2275/2023", "Verificar código EPS/entidad"))

        # 10. Nombre entidad administradora (60 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.nombre_entidad_administradora, "nombre_entidad_administradora", 60, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "nombre_entidad_administradora", msg, "Res. 2275/2023", "Reducir longitud del nombre"))

        # 17. Valor neto (decimal)
        valid, msg = NumericValidator.validate_decimal(record.valor_neto, "valor_neto", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_neto", msg, "Res. 2275/2023", "Valor debe ser numérico y >= 0"))

        return errors


class USValidator:
    """Validador para archivo de Usuarios (US)"""

    @staticmethod
    def validate(record: USRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro US"""
        errors = []

        # 1. Tipo de documento
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento, "tipo_documento")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento", msg, "Res. 2275/2023", "Usar: CC, TI, RC, CE, PA, etc."))

        # 2. Número de documento (20 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.num_documento, "num_documento", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_documento", msg, "Res. 2275/2023", "Verificar número de identificación"))

        # 3. Código entidad administradora
        valid, msg = LengthValidator.validate_length(record.cod_entidad_administradora, "cod_entidad_administradora", 6, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_entidad_administradora", msg, "Res. 2275/2023", "Verificar código EPS"))

        # 4. Tipo de usuario
        valid, msg = CodeValidator.validate_user_type(record.tipo_usuario, "tipo_usuario")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_usuario", msg, "Res. 2275/2023", "1=Contributivo, 2=Subsidiado, 3=Vinculado, 4=Particular"))

        # 5. Primer apellido (60 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.primer_apellido, "primer_apellido", 60, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "primer_apellido", msg, "Res. 2275/2023", "Verificar primer apellido"))

        # 7. Primer nombre (60 caracteres máx)
        valid, msg = LengthValidator.validate_length(record.primer_nombre, "primer_nombre", 60, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "primer_nombre", msg, "Res. 2275/2023", "Verificar primer nombre"))

        # 9. Edad
        valid, msg = NumericValidator.validate_integer(record.edad, "edad", required=True, min_value=0, max_value=150)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "edad", msg, "Res. 2275/2023", "Edad debe ser entre 0 y 150"))

        # 10. Unidad de medida de edad
        valid, msg = CodeValidator.validate_age_unit(record.unidad_medida_edad, "unidad_medida_edad")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "unidad_medida_edad", msg, "Res. 2275/2023", "1=años, 2=meses, 3=días"))

        # 11. Sexo
        valid, msg = CodeValidator.validate_sex(record.sexo, "sexo")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "sexo", msg, "Res. 2275/2023", "Debe ser M o F"))

        # 12. Código departamento (2 dígitos)
        valid, msg = LengthValidator.validate_length(record.cod_departamento, "cod_departamento", 2, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_departamento", msg, "Res. 2275/2023", "Código DANE de 2 dígitos"))

        # 13. Código municipio (3 dígitos)
        valid, msg = LengthValidator.validate_length(record.cod_municipio, "cod_municipio", 3, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_municipio", msg, "Res. 2275/2023", "Código DANE de 3 dígitos"))

        # 14. Zona residencial
        valid, msg = CodeValidator.validate_zone(record.zona_residencial, "zona_residencial")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "zona_residencial", msg, "Res. 2275/2023", "U=Urbana, R=Rural"))

        return errors


class ACValidator:
    """Validador para archivo de Consultas (AC)"""

    @staticmethod
    def validate(record: ACRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro AC"""
        errors = []

        # 1. Número de factura
        valid, msg = LengthValidator.validate_length(record.num_factura, "num_factura", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_factura", msg, "Res. 2275/2023", "Debe corresponder al AF"))

        # 2. Código del prestador
        valid, msg = LengthValidator.validate_length(record.cod_prestador, "cod_prestador", 12, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_prestador", msg, "Res. 2275/2023", "Código habilitación del prestador"))

        # 3. Tipo de documento
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento, "tipo_documento")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 4. Número de documento
        valid, msg = LengthValidator.validate_length(record.num_documento, "num_documento", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 5. Fecha de consulta
        valid, msg, _ = DateValidator.validate_format(record.fecha_consulta, "fecha_consulta", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_consulta", msg, "Res. 2275/2023", "Formato DD/MM/YYYY"))

        # 7. Código de consulta (CUPS)
        valid, msg = CodeValidator.validate_cups_format(record.cod_consulta, "cod_consulta", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_consulta", msg, "Res. 2275/2023", "Código CUPS de 6 dígitos"))

        # 10. Finalidad de la consulta
        valid, msg = NumericValidator.validate_integer(record.finalidad_consulta, "finalidad_consulta", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "finalidad_consulta", msg, "Res. 2275/2023", "Código de finalidad según tabla"))

        # 11. Causa externa
        valid, msg = NumericValidator.validate_integer(record.causa_externa, "causa_externa", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "causa_externa", msg, "Res. 2275/2023", "Código de causa externa según tabla"))

        # 12. Diagnóstico principal (CIE10)
        valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_principal, "diagnostico_principal", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "diagnostico_principal", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido (ej: A001, Z000)"))

        # 13-15. Diagnósticos relacionados (CIE10, opcionales)
        if not BaseValidator.is_empty(record.diagnostico_relacionado1):
            valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_relacionado1, "diagnostico_relacionado1", required=False)
            if not valid:
                errors.append(ValidationError(file_name, line_number, "diagnostico_relacionado1", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido o vacío"))

        if not BaseValidator.is_empty(record.diagnostico_relacionado2):
            valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_relacionado2, "diagnostico_relacionado2", required=False)
            if not valid:
                errors.append(ValidationError(file_name, line_number, "diagnostico_relacionado2", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido o vacío"))

        if not BaseValidator.is_empty(record.diagnostico_relacionado3):
            valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_relacionado3, "diagnostico_relacionado3", required=False)
            if not valid:
                errors.append(ValidationError(file_name, line_number, "diagnostico_relacionado3", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido o vacío"))

        # 16. Tipo de diagnóstico principal
        valid, msg = NumericValidator.validate_integer(record.tipo_diagnostico_principal, "tipo_diagnostico_principal", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_diagnostico_principal", msg, "Res. 2275/2023", "1=Impresión diagnóstica, 2=Confirmado nuevo, 3=Confirmado repetido"))

        # 17. Valor consulta
        valid, msg = NumericValidator.validate_decimal(record.valor_consulta, "valor_consulta", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_consulta", msg, "Res. 2275/2023", "Valor >= 0"))

        # 19. Valor neto
        valid, msg = NumericValidator.validate_decimal(record.valor_neto, "valor_neto", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_neto", msg, "Res. 2275/2023", "Valor >= 0"))

        # 20. Edad
        valid, msg = NumericValidator.validate_integer(record.edad, "edad", required=True, min_value=0, max_value=150)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "edad", msg, "Res. 2275/2023", "Edad 0-150"))

        # 21. Unidad de medida de edad
        valid, msg = CodeValidator.validate_age_unit(record.unidad_medida_edad, "unidad_medida_edad")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "unidad_medida_edad", msg, "Res. 2275/2023", "1=años, 2=meses, 3=días"))

        # 22. Sexo
        valid, msg = CodeValidator.validate_sex(record.sexo, "sexo")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "sexo", msg, "Res. 2275/2023", "M o F"))

        return errors


class APValidator:
    """Validador para archivo de Procedimientos (AP)"""

    @staticmethod
    def validate(record: APRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro AP"""
        errors = []

        # Validaciones similares a AC
        # 1. Número de factura
        valid, msg = LengthValidator.validate_length(record.num_factura, "num_factura", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_factura", msg, "Res. 2275/2023", "Debe corresponder al AF"))

        # 2. Código del prestador
        valid, msg = LengthValidator.validate_length(record.cod_prestador, "cod_prestador", 12, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_prestador", msg, "Res. 2275/2023", "Código habilitación"))

        # 3. Tipo de documento
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento, "tipo_documento")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 4. Número de documento
        valid, msg = LengthValidator.validate_length(record.num_documento, "num_documento", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 5. Fecha del procedimiento
        valid, msg, _ = DateValidator.validate_format(record.fecha_procedimiento, "fecha_procedimiento", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_procedimiento", msg, "Res. 2275/2023", "Formato DD/MM/YYYY"))

        # 7. Código del procedimiento (CUPS)
        valid, msg = CodeValidator.validate_cups_format(record.cod_procedimiento, "cod_procedimiento", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_procedimiento", msg, "Res. 2275/2023", "Código CUPS de 6 dígitos"))

        # 13. Diagnóstico principal (CIE10)
        valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_principal, "diagnostico_principal", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "diagnostico_principal", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido"))

        # 14. Diagnóstico relacionado (opcional)
        if not BaseValidator.is_empty(record.diagnostico_relacionado):
            valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_relacionado, "diagnostico_relacionado", required=False)
            if not valid:
                errors.append(ValidationError(file_name, line_number, "diagnostico_relacionado", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido o vacío"))

        # 15. Complicación (opcional)
        if not BaseValidator.is_empty(record.complicacion):
            valid, msg = CodeValidator.validate_cie10_format(record.complicacion, "complicacion", required=False)
            if not valid:
                errors.append(ValidationError(file_name, line_number, "complicacion", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido o vacío"))

        # 17. Valor procedimiento
        valid, msg = NumericValidator.validate_decimal(record.valor_procedimiento, "valor_procedimiento", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_procedimiento", msg, "Res. 2275/2023", "Valor >= 0"))

        # 19. Valor neto
        valid, msg = NumericValidator.validate_decimal(record.valor_neto, "valor_neto", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_neto", msg, "Res. 2275/2023", "Valor >= 0"))

        # 20-22. Edad, unidad edad, sexo
        valid, msg = NumericValidator.validate_integer(record.edad, "edad", required=True, min_value=0, max_value=150)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "edad", msg, "Res. 2275/2023", "Edad 0-150"))

        valid, msg = CodeValidator.validate_age_unit(record.unidad_medida_edad, "unidad_medida_edad")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "unidad_medida_edad", msg, "Res. 2275/2023", "1=años, 2=meses, 3=días"))

        valid, msg = CodeValidator.validate_sex(record.sexo, "sexo")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "sexo", msg, "Res. 2275/2023", "M o F"))

        return errors


class ATValidator:
    """Validador para archivo de Otros Servicios (AT)"""

    @staticmethod
    def validate(record: ATRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro AT"""
        errors = []

        # 1. Número de factura
        valid, msg = LengthValidator.validate_length(record.num_factura, "num_factura", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_factura", msg, "Res. 2275/2023", "Debe corresponder al AF"))

        # 2. Código del prestador
        valid, msg = LengthValidator.validate_length(record.cod_prestador, "cod_prestador", 12, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_prestador", msg, "Res. 2275/2023", "Código habilitación"))

        # 3. Tipo de documento
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento, "tipo_documento")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 4. Número de documento
        valid, msg = LengthValidator.validate_length(record.num_documento, "num_documento", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 7. Código del servicio (CUPS)
        valid, msg = CodeValidator.validate_cups_format(record.cod_servicio, "cod_servicio", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cod_servicio", msg, "Res. 2275/2023", "Código CUPS de 6 dígitos"))

        # 10. Cantidad
        valid, msg = NumericValidator.validate_decimal(record.cantidad, "cantidad", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "cantidad", msg, "Res. 2275/2023", "Cantidad > 0"))

        # 11. Valor unitario
        valid, msg = NumericValidator.validate_decimal(record.valor_unitario, "valor_unitario", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_unitario", msg, "Res. 2275/2023", "Valor >= 0"))

        # 12. Valor total
        valid, msg = NumericValidator.validate_decimal(record.valor_total, "valor_total", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_total", msg, "Res. 2275/2023", "Valor >= 0"))

        # 14. Valor neto
        valid, msg = NumericValidator.validate_decimal(record.valor_neto, "valor_neto", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_neto", msg, "Res. 2275/2023", "Valor >= 0"))

        return errors


class AHValidator:
    """Validador para archivo de Hospitalización (AH)"""

    @staticmethod
    def validate(record: AHRecord, line_number: int, file_name: str) -> List[ValidationError]:
        """Valida un registro AH"""
        errors = []

        # 1. Número de factura
        valid, msg = LengthValidator.validate_length(record.num_factura, "num_factura", 20, required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "num_factura", msg, "Res. 2275/2023", "Debe corresponder al AF"))

        # 3. Tipo de documento
        valid, msg = CodeValidator.validate_document_type(record.tipo_documento, "tipo_documento")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "tipo_documento", msg, "Res. 2275/2023", "Debe existir en US"))

        # 6. Fecha de ingreso
        valid, msg, _ = DateValidator.validate_format(record.fecha_ingreso, "fecha_ingreso", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_ingreso", msg, "Res. 2275/2023", "Formato DD/MM/YYYY"))

        # 10. Diagnóstico de ingreso (CIE10)
        valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_ingreso, "diagnostico_ingreso", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "diagnostico_ingreso", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido"))

        # 11. Diagnóstico de egreso (CIE10)
        valid, msg = CodeValidator.validate_cie10_format(record.diagnostico_egreso, "diagnostico_egreso", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "diagnostico_egreso", msg, "Res. 2275/2023 y 3280/2018", "Código CIE10 válido"))

        # 18. Fecha de egreso
        valid, msg, _ = DateValidator.validate_format(record.fecha_egreso, "fecha_egreso", required=True)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_egreso", msg, "Res. 2275/2023", "Formato DD/MM/YYYY"))

        # Validar rango de fechas
        valid, msg = DateValidator.validate_date_range(record.fecha_ingreso, record.fecha_egreso, "fecha_ingreso", "fecha_egreso")
        if not valid:
            errors.append(ValidationError(file_name, line_number, "fecha_ingreso/fecha_egreso", msg, "Res. 2275/2023", "Fecha ingreso <= fecha egreso"))

        # 20. Valor hospitalización
        valid, msg = NumericValidator.validate_decimal(record.valor_hospitalizacion, "valor_hospitalizacion", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_hospitalizacion", msg, "Res. 2275/2023", "Valor >= 0"))

        # 22. Valor neto
        valid, msg = NumericValidator.validate_decimal(record.valor_neto, "valor_neto", required=True, min_value=0)
        if not valid:
            errors.append(ValidationError(file_name, line_number, "valor_neto", msg, "Res. 2275/2023", "Valor >= 0"))

        return errors
