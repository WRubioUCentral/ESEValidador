"""
Sistema de corrección automática de errores en archivos RIPS
Con registro detallado de cambios realizados
"""
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .validators import DateValidator, NumericValidator
from .cie10_catalog import get_cie10_catalog


class CorrectionRecord:
    """Registro de una corrección realizada"""

    def __init__(self, file_name: str, line_number: int, field_name: str,
                 original_value: str, corrected_value: str, correction_type: str,
                 confidence: str, reason: str):
        """
        Inicializa un registro de corrección

        Args:
            file_name: Nombre del archivo
            line_number: Número de línea
            field_name: Campo corregido
            original_value: Valor original
            corrected_value: Valor corregido
            correction_type: Tipo de corrección
            confidence: Nivel de confianza (alta, media, baja)
            reason: Razón de la corrección
        """
        self.file_name = file_name
        self.line_number = line_number
        self.field_name = field_name
        self.original_value = original_value
        self.corrected_value = corrected_value
        self.correction_type = correction_type
        self.confidence = confidence
        self.reason = reason
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict:
        """Convierte el registro a diccionario"""
        return {
            'nombre_archivo': self.file_name,
            'numero_linea': self.line_number,
            'campo': self.field_name,
            'valor_original': self.original_value,
            'valor_corregido': self.corrected_value,
            'tipo_correccion': self.correction_type,
            'confianza': self.confidence,
            'razon': self.reason,
            'fecha_hora': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


class AutoCorrector:
    """Sistema de corrección automática de errores"""

    def __init__(self, auto_mode: bool = False):
        """
        Inicializa el corrector

        Args:
            auto_mode: Si True, aplica correcciones automáticamente.
                      Si False, solo sugiere correcciones.
        """
        self.auto_mode = auto_mode
        self.corrections: List[CorrectionRecord] = []
        self.cie10_catalog = get_cie10_catalog()

    def correct_date_format(self, date_str: str, field_name: str, file_name: str,
                           line_number: int) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Corrige formatos de fecha incorrectos

        Formatos detectados y corregidos:
        - YYYY-MM-DD → DD/MM/YYYY
        - DD-MM-YYYY → DD/MM/YYYY
        - YYYY/MM/DD → DD/MM/YYYY

        Args:
            date_str: Cadena de fecha
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Tupla (fecha_corregida, registro_correccion)
        """
        if not date_str or date_str.strip() == '':
            return date_str, None

        original = date_str
        corrected = date_str

        # Patrón YYYY-MM-DD o YYYY/MM/DD
        pattern1 = r'^(\d{4})[-/](\d{2})[-/](\d{2})$'
        match = re.match(pattern1, date_str)
        if match:
            year, month, day = match.groups()
            corrected = f"{day}/{month}/{year}"

        # Patrón DD-MM-YYYY
        pattern2 = r'^(\d{2})-(\d{2})-(\d{4})$'
        match = re.match(pattern2, date_str)
        if match:
            day, month, year = match.groups()
            corrected = f"{day}/{month}/{year}"

        # Verificar si hubo corrección
        if corrected != original:
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, corrected,
                'formato_fecha',
                'alta',
                f"Formato de fecha corregido de '{original}' a '{corrected}' (DD/MM/YYYY)"
            )
            self.corrections.append(record)
            return corrected, record

        return date_str, None

    def correct_text_normalization(self, text: str, field_name: str, file_name: str,
                                   line_number: int) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Normaliza texto: elimina espacios extras, convierte a mayúsculas

        Args:
            text: Texto a normalizar
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Tupla (texto_corregido, registro_correccion)
        """
        if not text:
            return text, None

        original = text
        corrected = text

        # Eliminar espacios al inicio y final
        corrected = corrected.strip()

        # Eliminar espacios múltiples
        corrected = re.sub(r'\s+', ' ', corrected)

        # Convertir a mayúsculas (solo para campos de nombres)
        if 'nombre' in field_name.lower() or 'apellido' in field_name.lower():
            corrected = corrected.upper()

        if corrected != original:
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, corrected,
                'normalizacion_texto',
                'alta',
                f"Texto normalizado: espacios eliminados y/o convertido a mayúsculas"
            )
            self.corrections.append(record)
            return corrected, record

        return text, None

    def correct_numeric_format(self, value: str, field_name: str, file_name: str,
                              line_number: int, is_decimal: bool = False) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Corrige formatos numéricos

        Args:
            value: Valor a corregir
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea
            is_decimal: Si es un número decimal

        Returns:
            Tupla (valor_corregido, registro_correccion)
        """
        if not value or value.strip() == '':
            return value, None

        original = value
        corrected = value

        # Eliminar espacios
        corrected = corrected.strip().replace(' ', '')

        # Reemplazar coma por punto en decimales
        if is_decimal and ',' in corrected:
            corrected = corrected.replace(',', '.')

        # Eliminar caracteres no numéricos excepto punto y signo negativo
        if is_decimal:
            corrected = re.sub(r'[^\d.-]', '', corrected)
        else:
            corrected = re.sub(r'[^\d-]', '', corrected)

        # Validar que sea un número válido
        try:
            if is_decimal:
                float(corrected)
            else:
                int(corrected)
        except ValueError:
            # No se pudo corregir
            return original, None

        if corrected != original:
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, corrected,
                'formato_numerico',
                'alta',
                f"Formato numérico corregido"
            )
            self.corrections.append(record)
            return corrected, record

        return value, None

    def suggest_cie10_correction(self, code: str, field_name: str, file_name: str,
                                 line_number: int) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Sugiere corrección para códigos CIE10 inválidos

        Args:
            code: Código CIE10
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Tupla (codigo_sugerido, registro_correccion)
        """
        if not code or code.strip() == '':
            return code, None

        original = code.strip().upper()

        # Verificar si es válido
        is_valid, message, suggestions = self.cie10_catalog.validate_with_suggestion(original)

        if is_valid:
            return code, None

        # Si hay sugerencias, tomar la primera
        if suggestions:
            suggested = suggestions[0]
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, suggested,
                'sugerencia_cie10',
                'media',  # Confianza media porque es una sugerencia
                f"Código CIE10 '{original}' no válido. Sugerencia basada en similitud: '{suggested}'. "
                f"REQUIERE VALIDACIÓN MÉDICA antes de aplicar."
            )
            self.corrections.append(record)
            return suggested, record

        return code, None

    def correct_cups_format(self, code: str, field_name: str, file_name: str,
                           line_number: int) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Corrige formato de códigos CUPS (debe ser 6 dígitos)

        Args:
            code: Código CUPS
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Tupla (codigo_corregido, registro_correccion)
        """
        if not code or code.strip() == '':
            return code, None

        original = code.strip()
        corrected = original

        # Eliminar caracteres no numéricos
        corrected = re.sub(r'[^\d]', '', corrected)

        # Si tiene menos de 6 dígitos, completar con ceros a la derecha
        if len(corrected) < 6 and len(corrected) > 0:
            corrected = corrected.ljust(6, '0')

        # Si tiene más de 6, tomar solo los primeros 6
        if len(corrected) > 6:
            corrected = corrected[:6]

        if corrected != original and len(corrected) == 6:
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, corrected,
                'formato_cups',
                'media',
                f"Código CUPS ajustado a 6 dígitos. REQUIERE VALIDACIÓN."
            )
            self.corrections.append(record)
            return corrected, record

        return code, None

    def correct_document_type(self, doc_type: str, field_name: str, file_name: str,
                             line_number: int) -> Tuple[str, Optional[CorrectionRecord]]:
        """
        Corrige tipos de documento comunes

        Args:
            doc_type: Tipo de documento
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Tupla (tipo_corregido, registro_correccion)
        """
        if not doc_type:
            return doc_type, None

        original = doc_type.strip().upper()
        corrected = original

        # Correcciones comunes
        corrections_map = {
            'CI': 'CC',  # Cédula
            'C.C': 'CC',
            'C.C.': 'CC',
            'T.I': 'TI',
            'T.I.': 'TI',
            'R.C': 'RC',
            'R.C.': 'RC',
            'C.E': 'CE',
            'C.E.': 'CE',
            'DN': 'CC',  # Documento Nacional -> Cédula
        }

        if original in corrections_map:
            corrected = corrections_map[original]

        if corrected != original:
            record = CorrectionRecord(
                file_name, line_number, field_name,
                original, corrected,
                'tipo_documento',
                'alta',
                f"Tipo de documento estandarizado de '{original}' a '{corrected}'"
            )
            self.corrections.append(record)
            return corrected, record

        return doc_type, None

    def get_corrections_by_confidence(self, confidence: str) -> List[CorrectionRecord]:
        """
        Obtiene correcciones por nivel de confianza

        Args:
            confidence: 'alta', 'media', 'baja'

        Returns:
            Lista de correcciones
        """
        return [c for c in self.corrections if c.confidence == confidence]

    def get_corrections_summary(self) -> Dict:
        """
        Obtiene resumen de correcciones

        Returns:
            Diccionario con estadísticas
        """
        total = len(self.corrections)
        by_type = {}
        by_confidence = {'alta': 0, 'media': 0, 'baja': 0}

        for correction in self.corrections:
            # Por tipo
            by_type[correction.correction_type] = by_type.get(correction.correction_type, 0) + 1
            # Por confianza
            by_confidence[correction.confidence] = by_confidence.get(correction.confidence, 0) + 1

        return {
            'total_correcciones': total,
            'por_tipo': by_type,
            'por_confianza': by_confidence,
            'alta_confianza': by_confidence['alta'],
            'requieren_revision': by_confidence['media'] + by_confidence['baja']
        }

    def export_corrections(self) -> List[Dict]:
        """
        Exporta todas las correcciones como lista de diccionarios

        Returns:
            Lista de correcciones
        """
        return [c.to_dict() for c in self.corrections]


def apply_safe_corrections(line: str, line_number: int, file_name: str,
                          file_type: str, auto_corrector: AutoCorrector) -> Tuple[str, List[CorrectionRecord]]:
    """
    Aplica correcciones seguras (alta confianza) a una línea

    Args:
        line: Línea del archivo
        line_number: Número de línea
        file_name: Nombre del archivo
        file_type: Tipo de archivo RIPS
        auto_corrector: Instancia del corrector

    Returns:
        Tupla (linea_corregida, lista_de_correcciones)
    """
    fields = line.strip().split(',')
    corrections = []
    corrected_fields = []

    # Mapeo de índices de campos por tipo de archivo
    # Solo se aplican correcciones de alta confianza

    if file_type == 'US':
        # US: 15 campos
        for idx, field in enumerate(fields):
            corrected_field = field
            correction = None

            if idx == 0:  # tipo_documento
                corrected_field, correction = auto_corrector.correct_document_type(
                    field, 'tipo_documento', file_name, line_number
                )
            elif idx in [4, 5, 6, 7]:  # apellidos y nombres
                corrected_field, correction = auto_corrector.correct_text_normalization(
                    field, f'nombre_{idx}', file_name, line_number
                )
            elif idx == 8:  # edad
                corrected_field, correction = auto_corrector.correct_numeric_format(
                    field, 'edad', file_name, line_number, is_decimal=False
                )

            corrected_fields.append(corrected_field)
            if correction:
                corrections.append(correction)

    elif file_type == 'AC':
        # AC: 22 campos
        for idx, field in enumerate(fields):
            corrected_field = field
            correction = None

            if idx == 2:  # tipo_documento
                corrected_field, correction = auto_corrector.correct_document_type(
                    field, 'tipo_documento', file_name, line_number
                )
            elif idx == 4:  # fecha_consulta
                corrected_field, correction = auto_corrector.correct_date_format(
                    field, 'fecha_consulta', file_name, line_number
                )
            elif idx == 6:  # cod_consulta (CUPS)
                corrected_field, correction = auto_corrector.correct_cups_format(
                    field, 'cod_consulta', file_name, line_number
                )
            elif idx in [16, 17, 18]:  # valores monetarios
                corrected_field, correction = auto_corrector.correct_numeric_format(
                    field, f'valor_{idx}', file_name, line_number, is_decimal=True
                )

            corrected_fields.append(corrected_field)
            if correction:
                corrections.append(correction)

    else:
        # Para otros tipos, solo correcciones básicas
        corrected_fields = fields

    # Reconstruir línea
    corrected_line = ','.join(corrected_fields)

    return corrected_line, corrections
