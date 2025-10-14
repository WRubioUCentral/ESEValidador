"""
Validadores de tipos de datos y formatos según Resoluciones 2275/2023 y 3280/2018
"""
import re
from datetime import datetime
from typing import Optional, Tuple


class BaseValidator:
    """Clase base para validadores"""

    @staticmethod
    def is_empty(value: str) -> bool:
        """Verifica si un valor está vacío"""
        return value is None or value.strip() == ""

    @staticmethod
    def validate_required(value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo obligatorio no esté vacío

        Returns:
            Tuple[bool, Optional[str]]: (es_valido, mensaje_error)
        """
        if BaseValidator.is_empty(value):
            return False, f"El campo '{field_name}' es obligatorio y no puede estar vacío (Res. 2275/2023)"
        return True, None


class DateValidator:
    """Validador de fechas"""

    @staticmethod
    def validate_format(date_str: str, field_name: str, required: bool = True) -> Tuple[bool, Optional[str], Optional[datetime]]:
        """
        Valida formato de fecha DD/MM/YYYY

        Returns:
            Tuple[bool, Optional[str], Optional[datetime]]: (es_valido, mensaje_error, fecha_parseada)
        """
        if BaseValidator.is_empty(date_str):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)", None
            return True, None, None

        # Validar formato DD/MM/YYYY
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, date_str):
            return False, f"El campo '{field_name}' debe tener formato DD/MM/YYYY. Valor recibido: '{date_str}' (Res. 2275/2023)", None

        try:
            fecha = datetime.strptime(date_str, '%d/%m/%Y')

            # Validar que la fecha no sea futura
            if fecha > datetime.now():
                return False, f"El campo '{field_name}' no puede ser una fecha futura. Fecha: {date_str} (Res. 2275/2023)", None

            # Validar rango razonable (no anterior a 1900)
            if fecha.year < 1900:
                return False, f"El campo '{field_name}' tiene una fecha no válida (anterior a 1900). Fecha: {date_str}", None

            return True, None, fecha

        except ValueError:
            return False, f"El campo '{field_name}' contiene una fecha inválida: '{date_str}' (Res. 2275/2023)", None

    @staticmethod
    def validate_date_range(date_start: str, date_end: str, field_start: str, field_end: str) -> Tuple[bool, Optional[str]]:
        """
        Valida que fecha_inicio <= fecha_final
        """
        valid_start, error_start, fecha_inicio = DateValidator.validate_format(date_start, field_start)
        valid_end, error_end, fecha_final = DateValidator.validate_format(date_end, field_end)

        if not valid_start:
            return False, error_start
        if not valid_end:
            return False, error_end

        if fecha_inicio and fecha_final and fecha_inicio > fecha_final:
            return False, f"La fecha '{field_start}' ({date_start}) no puede ser posterior a '{field_end}' ({date_end}) (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_age_consistency(birth_date: str, attention_date: str, age: str, age_unit: str) -> Tuple[bool, Optional[str]]:
        """
        Valida coherencia entre fecha de nacimiento, fecha de atención y edad reportada
        """
        valid_birth, error_birth, fecha_nacimiento = DateValidator.validate_format(birth_date, "fecha_nacimiento")
        valid_attention, error_attention, fecha_atencion = DateValidator.validate_format(attention_date, "fecha_atencion")

        if not valid_birth or not valid_attention:
            return True, None  # No validar si las fechas no son válidas

        if fecha_nacimiento and fecha_atencion:
            if fecha_nacimiento > fecha_atencion:
                return False, f"La fecha de nacimiento ({birth_date}) no puede ser posterior a la fecha de atención ({attention_date}) (Res. 2275/2023)"

        return True, None


class NumericValidator:
    """Validador de campos numéricos"""

    @staticmethod
    def validate_integer(value: str, field_name: str, required: bool = True, min_value: int = None, max_value: int = None) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo sea un número entero
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo numérico '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        try:
            num = int(value)

            if min_value is not None and num < min_value:
                return False, f"El campo '{field_name}' debe ser mayor o igual a {min_value}. Valor: {value} (Res. 2275/2023)"

            if max_value is not None and num > max_value:
                return False, f"El campo '{field_name}' debe ser menor o igual a {max_value}. Valor: {value} (Res. 2275/2023)"

            return True, None

        except ValueError:
            return False, f"El campo '{field_name}' debe ser un número entero. Valor recibido: '{value}' (Res. 2275/2023)"

    @staticmethod
    def validate_decimal(value: str, field_name: str, required: bool = True, min_value: float = None, max_value: float = None) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo sea un número decimal
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo numérico '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        try:
            num = float(value)

            if min_value is not None and num < min_value:
                return False, f"El campo '{field_name}' debe ser mayor o igual a {min_value}. Valor: {value} (Res. 2275/2023)"

            if max_value is not None and num > max_value:
                return False, f"El campo '{field_name}' debe ser menor o igual a {max_value}. Valor: {value} (Res. 2275/2023)"

            return True, None

        except ValueError:
            return False, f"El campo '{field_name}' debe ser un número decimal. Valor recibido: '{value}' (Res. 2275/2023)"


class LengthValidator:
    """Validador de longitud de campos"""

    @staticmethod
    def validate_length(value: str, field_name: str, max_length: int, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida la longitud máxima de un campo
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        if len(value) > max_length:
            return False, f"El campo '{field_name}' excede la longitud máxima de {max_length} caracteres. Longitud actual: {len(value)} (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_exact_length(value: str, field_name: str, exact_length: int, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo tenga una longitud exacta
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        if len(value) != exact_length:
            return False, f"El campo '{field_name}' debe tener exactamente {exact_length} caracteres. Longitud actual: {len(value)} (Res. 2275/2023)"

        return True, None


class CodeValidator:
    """Validador de códigos específicos (CUPS, CIE10, etc.)"""

    @staticmethod
    def validate_document_type(doc_type: str, field_name: str = "tipo_documento") -> Tuple[bool, Optional[str]]:
        """
        Valida tipo de documento según catálogo oficial
        Valores permitidos: CC, TI, RC, CE, PA, MS, AS, CD, SC, PE, PT
        """
        valid_types = ['CC', 'TI', 'RC', 'CE', 'PA', 'MS', 'AS', 'CD', 'SC', 'PE', 'PT', 'NI']

        if BaseValidator.is_empty(doc_type):
            return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"

        if doc_type not in valid_types:
            return False, f"El campo '{field_name}' contiene un tipo de documento inválido: '{doc_type}'. Valores permitidos: {', '.join(valid_types)} (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_sex(sex: str, field_name: str = "sexo") -> Tuple[bool, Optional[str]]:
        """
        Valida sexo
        Valores permitidos: M, F
        """
        valid_values = ['M', 'F']

        if BaseValidator.is_empty(sex):
            return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"

        if sex not in valid_values:
            return False, f"El campo '{field_name}' debe ser 'M' o 'F'. Valor recibido: '{sex}' (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_age_unit(age_unit: str, field_name: str = "unidad_medida_edad") -> Tuple[bool, Optional[str]]:
        """
        Valida unidad de medida de edad
        Valores permitidos: 1 (años), 2 (meses), 3 (días)
        """
        valid_values = ['1', '2', '3']

        if BaseValidator.is_empty(age_unit):
            return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"

        if age_unit not in valid_values:
            return False, f"El campo '{field_name}' debe ser '1' (años), '2' (meses) o '3' (días). Valor: '{age_unit}' (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_zone(zone: str, field_name: str = "zona_residencial") -> Tuple[bool, Optional[str]]:
        """
        Valida zona residencial
        Valores permitidos: U (Urbana), R (Rural)
        """
        valid_values = ['U', 'R']

        if BaseValidator.is_empty(zone):
            return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"

        if zone not in valid_values:
            return False, f"El campo '{field_name}' debe ser 'U' (Urbana) o 'R' (Rural). Valor: '{zone}' (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_cie10_format(code: str, field_name: str, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida formato básico de código CIE10
        Formato: Letra seguida de 2 dígitos, opcionalmente seguidos de otro dígito o X
        Ejemplos: A00, A001, A00X, Z000
        """
        if BaseValidator.is_empty(code):
            if required:
                return False, f"El campo '{field_name}' es obligatorio cuando aplica (Res. 2275/2023)"
            return True, None

        # Formato CIE10: Letra + 2 dígitos + opcional (dígito o X)
        pattern = r'^[A-Z]\d{2}[0-9X]?$'
        if not re.match(pattern, code):
            return False, f"El campo '{field_name}' no cumple con el formato CIE10 válido. Valor: '{code}'. Formato esperado: Letra + 2 dígitos + opcional(dígito/X) (Res. 2275/2023, 3280/2018)"

        return True, None

    @staticmethod
    def validate_cups_format(code: str, field_name: str, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida formato básico de código CUPS
        Formato: 6 dígitos
        """
        if BaseValidator.is_empty(code):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        # Formato CUPS: 6 dígitos
        pattern = r'^\d{6}$'
        if not re.match(pattern, code):
            return False, f"El campo '{field_name}' debe ser un código CUPS de 6 dígitos. Valor: '{code}' (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_user_type(user_type: str, field_name: str = "tipo_usuario") -> Tuple[bool, Optional[str]]:
        """
        Valida tipo de usuario
        Valores permitidos según Res. 2275/2023: 1, 2, 3, 4
        """
        valid_values = ['1', '2', '3', '4']

        if BaseValidator.is_empty(user_type):
            return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"

        if user_type not in valid_values:
            return False, f"El campo '{field_name}' debe ser: 1 (Contributivo), 2 (Subsidiado), 3 (Vinculado), 4 (Particular). Valor: '{user_type}' (Res. 2275/2023)"

        return True, None


class TextValidator:
    """Validador de campos de texto"""

    @staticmethod
    def validate_alpha(value: str, field_name: str, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo contenga solo letras
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        # Permitir letras, espacios, tildes y caracteres especiales del español
        pattern = r'^[A-ZÁÉÍÓÚÑa-záéíóúñ\s]+$'
        if not re.match(pattern, value):
            return False, f"El campo '{field_name}' debe contener solo letras. Valor: '{value}' (Res. 2275/2023)"

        return True, None

    @staticmethod
    def validate_alphanumeric(value: str, field_name: str, required: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Valida que un campo sea alfanumérico
        """
        if BaseValidator.is_empty(value):
            if required:
                return False, f"El campo '{field_name}' es obligatorio (Res. 2275/2023)"
            return True, None

        # Permitir letras, números y algunos caracteres especiales comunes
        pattern = r'^[A-ZÁÉÍÓÚÑa-záéíóúñ0-9\s\-.,]+$'
        if not re.match(pattern, value):
            return False, f"El campo '{field_name}' contiene caracteres no permitidos. Valor: '{value}' (Res. 2275/2023)"

        return True, None
