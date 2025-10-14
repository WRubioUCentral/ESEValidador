"""
Validadores avanzados para RIPS
- Validación de códigos CIE10 contra catálogo vigente
- Detección de duplicados de atenciones
- Validación de coherencia entre campos
"""
from typing import List, Dict, Tuple, Set
from collections import defaultdict
from datetime import datetime
from .rules import ValidationError
from .cie10_catalog import get_cie10_catalog


class DuplicateAttentionDetector:
    """Detector de atenciones duplicadas por usuario en el mismo día"""

    def __init__(self):
        """Inicializa el detector"""
        # Estructura: {(tipo_doc, num_doc, fecha): [lista de tipos de atención]}
        self.user_attentions: Dict[Tuple[str, str, str], List[Dict]] = defaultdict(list)
        self.duplicates_found = []

    def register_attention(self, tipo_doc: str, num_doc: str, fecha: str,
                          tipo_atencion: str, codigo: str, file_name: str, line_number: int):
        """
        Registra una atención

        Args:
            tipo_doc: Tipo de documento
            num_doc: Número de documento
            fecha: Fecha de atención
            tipo_atencion: Tipo (consulta, procedimiento, etc.)
            codigo: Código CUPS del servicio
            file_name: Nombre del archivo
            line_number: Número de línea
        """
        key = (tipo_doc, num_doc, fecha)
        attention = {
            'tipo': tipo_atencion,
            'codigo': codigo,
            'file': file_name,
            'line': line_number
        }
        self.user_attentions[key].append(attention)

    def detect_duplicates(self) -> List[ValidationError]:
        """
        Detecta atenciones duplicadas

        Returns:
            Lista de errores de validación por duplicados
        """
        errors = []

        for (tipo_doc, num_doc, fecha), attentions in self.user_attentions.items():
            if len(attentions) > 1:
                # Verificar si son realmente duplicados (mismo tipo y código)
                seen = {}
                for attention in attentions:
                    key = (attention['tipo'], attention['codigo'])
                    if key in seen:
                        # Duplicado encontrado
                        prev = seen[key]
                        errors.append(ValidationError(
                            attention['file'],
                            attention['line'],
                            'duplicado_atencion',
                            f"Atención duplicada detectada: Usuario {tipo_doc} {num_doc} "
                            f"tiene {attention['tipo']} duplicada el {fecha} "
                            f"(código: {attention['codigo']}). "
                            f"También registrada en {prev['file']} línea {prev['line']}",
                            "Res. 2275/2023 - Validación de calidad de datos",
                            f"Verificar si se trata de un error de digitación o una atención real. "
                            f"Eliminar el registro duplicado si no corresponde."
                        ))
                    else:
                        seen[key] = attention

        self.duplicates_found = errors
        return errors

    def get_statistics(self) -> Dict:
        """Retorna estadísticas de detección de duplicados"""
        return {
            'total_users_with_attentions': len(self.user_attentions),
            'total_duplicate_attentions': len(self.duplicates_found)
        }


class CIE10Validator:
    """Validador de códigos CIE10 contra catálogo vigente"""

    def __init__(self):
        """Inicializa el validador"""
        self.catalog = get_cie10_catalog()
        self.invalid_codes: Dict[str, int] = defaultdict(int)

    def validate_code(self, code: str, field_name: str, file_name: str,
                     line_number: int, required: bool = True) -> List[ValidationError]:
        """
        Valida un código CIE10 contra el catálogo

        Args:
            code: Código CIE10
            field_name: Nombre del campo
            file_name: Nombre del archivo
            line_number: Número de línea
            required: Si el campo es obligatorio

        Returns:
            Lista de errores encontrados
        """
        errors = []

        # Si está vacío y no es requerido, OK
        if not code or code.strip() == '':
            if required:
                errors.append(ValidationError(
                    file_name, line_number, field_name,
                    f"El campo '{field_name}' es obligatorio",
                    "Res. 2275/2023",
                    "Completar con el código CIE10 correspondiente"
                ))
            return errors

        # Validar contra catálogo
        is_valid, message, suggestions = self.catalog.validate_with_suggestion(code)

        if not is_valid:
            self.invalid_codes[code] += 1

            suggestion_text = ""
            if suggestions:
                suggestion_text = f" Códigos similares válidos: {', '.join(suggestions[:3])}"

            errors.append(ValidationError(
                file_name, line_number, field_name,
                f"El código CIE10 '{code}' no se encuentra en el catálogo vigente. "
                f"{message}.{suggestion_text}",
                "Res. 2275/2023 y 3280/2018 - Validación de calidad de datos",
                f"Verificar el código en el catálogo CIE10 vigente. "
                f"{suggestion_text if suggestions else 'Consultar con el área médica.'}"
            ))

        return errors

    def get_most_common_invalid_codes(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Obtiene los códigos inválidos más frecuentes

        Args:
            limit: Número máximo de códigos a retornar

        Returns:
            Lista de tuplas (código, frecuencia)
        """
        return sorted(self.invalid_codes.items(), key=lambda x: x[1], reverse=True)[:limit]


class CoherenceValidator:
    """Validador de coherencia entre campos relacionados"""

    # Tabla de coherencia: finalidad -> procedimientos esperados (prefijos CUPS)
    COHERENCE_RULES = {
        # Finalidad de consultas
        '10': {  # Detección temprana de enfermedad general
            'valid_cups_prefix': ['89'],
            'expected_diagnosis_chapter': ['Z'],
            'description': 'Detección temprana'
        },
        '11': {  # Detección temprana de enfermedad profesional
            'valid_cups_prefix': ['89'],
            'expected_diagnosis_chapter': ['Z'],
            'description': 'Detección temprana profesional'
        },
        '20': {  # Protección específica
            'valid_cups_prefix': ['89', '99'],
            'expected_diagnosis_chapter': ['Z'],
            'description': 'Protección específica (vacunación, etc.)'
        },
        '30': {  # Diagnóstico
            'valid_cups_prefix': ['87', '88', '89', '90'],
            'expected_diagnosis_chapter': None,  # Cualquier diagnóstico
            'description': 'Diagnóstico'
        },
        '40': {  # Tratamiento
            'valid_cups_prefix': None,  # Cualquier procedimiento
            'expected_diagnosis_chapter': None,
            'description': 'Tratamiento'
        },
        '50': {  # Rehabilitación
            'valid_cups_prefix': ['93'],
            'expected_diagnosis_chapter': ['G', 'M', 'S', 'T'],
            'description': 'Rehabilitación'
        },
        '60': {  # Paliación
            'valid_cups_prefix': None,
            'expected_diagnosis_chapter': ['C', 'D'],
            'description': 'Paliación'
        },
    }

    def __init__(self):
        """Inicializa el validador de coherencia"""
        pass

    def validate_coherence(self, finalidad: str, codigo_cups: str, diagnostico_cie10: str,
                          file_name: str, line_number: int, field_context: str = "") -> List[ValidationError]:
        """
        Valida coherencia entre finalidad, procedimiento y diagnóstico

        Args:
            finalidad: Código de finalidad
            codigo_cups: Código CUPS del procedimiento
            diagnostico_cie10: Código CIE10 del diagnóstico
            file_name: Nombre del archivo
            line_number: Número de línea
            field_context: Contexto adicional

        Returns:
            Lista de errores de coherencia
        """
        errors = []

        # Obtener regla de coherencia
        rule = self.COHERENCE_RULES.get(finalidad)

        if not rule:
            # No hay regla definida, no validar
            return errors

        # Validar coherencia de procedimiento con finalidad
        if rule['valid_cups_prefix'] and codigo_cups:
            cups_prefix = codigo_cups[:2] if len(codigo_cups) >= 2 else ''
            if cups_prefix not in rule['valid_cups_prefix']:
                errors.append(ValidationError(
                    file_name, line_number, f'finalidad/codigo_procedimiento{field_context}',
                    f"Posible incoherencia: La finalidad '{finalidad}' ({rule['description']}) "
                    f"generalmente no corresponde con el procedimiento CUPS '{codigo_cups}'. "
                    f"Se esperan procedimientos que inicien con: {', '.join(rule['valid_cups_prefix'])}",
                    "Res. 2275/2023 - Validación de coherencia",
                    f"Verificar que la finalidad y el procedimiento sean coherentes. "
                    f"Consultar con el área de facturación."
                ))

        # Validar coherencia de diagnóstico con finalidad
        if rule['expected_diagnosis_chapter'] and diagnostico_cie10:
            diag_chapter = diagnostico_cie10[0] if diagnostico_cie10 else ''
            if diag_chapter and diag_chapter not in rule['expected_diagnosis_chapter']:
                errors.append(ValidationError(
                    file_name, line_number, f'finalidad/diagnostico{field_context}',
                    f"Posible incoherencia: La finalidad '{finalidad}' ({rule['description']}) "
                    f"generalmente no corresponde con diagnósticos del capítulo '{diag_chapter}' (CIE10: {diagnostico_cie10}). "
                    f"Se esperan diagnósticos de capítulos: {', '.join(rule['expected_diagnosis_chapter'])}",
                    "Res. 2275/2023 - Validación de coherencia",
                    f"Verificar que la finalidad y el diagnóstico sean coherentes. "
                    f"Consultar con el área médica."
                ))

        return errors

    def validate_gender_diagnosis_coherence(self, sexo: str, diagnostico: str,
                                           file_name: str, line_number: int) -> List[ValidationError]:
        """
        Valida coherencia entre sexo y diagnósticos específicos de género

        Args:
            sexo: M o F
            diagnostico: Código CIE10
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Lista de errores
        """
        errors = []

        if not diagnostico or not sexo:
            return errors

        # Diagnósticos exclusivos de mujeres (Capítulo O, N76, N80-N98)
        female_exclusive = diagnostico.startswith('O') or \
                          (diagnostico.startswith('N') and diagnostico[1:3] in ['76', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98'])

        # Diagnósticos exclusivos de hombres (N40-N51)
        male_exclusive = diagnostico.startswith('N') and diagnostico[1:3] in ['40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51']

        if sexo == 'M' and female_exclusive:
            errors.append(ValidationError(
                file_name, line_number, 'sexo/diagnostico',
                f"Incoherencia de género: Paciente masculino (M) con diagnóstico '{diagnostico}' "
                f"que es exclusivo de mujeres (embarazo, ginecología)",
                "Res. 2275/2023 - Validación de coherencia",
                "Verificar el sexo del paciente o el código de diagnóstico"
            ))

        if sexo == 'F' and male_exclusive:
            errors.append(ValidationError(
                file_name, line_number, 'sexo/diagnostico',
                f"Incoherencia de género: Paciente femenino (F) con diagnóstico '{diagnostico}' "
                f"que es exclusivo de hombres (próstata, etc.)",
                "Res. 2275/2023 - Validación de coherencia",
                "Verificar el sexo del paciente o el código de diagnóstico"
            ))

        return errors

    def validate_age_diagnosis_coherence(self, edad: int, unidad_edad: str, diagnostico: str,
                                        file_name: str, line_number: int) -> List[ValidationError]:
        """
        Valida coherencia entre edad y diagnósticos

        Args:
            edad: Edad del paciente
            unidad_edad: Unidad (1=años, 2=meses, 3=días)
            diagnostico: Código CIE10
            file_name: Nombre del archivo
            line_number: Número de línea

        Returns:
            Lista de errores
        """
        errors = []

        if not diagnostico:
            return errors

        try:
            edad_num = int(edad)
            unidad = str(unidad_edad)

            # Convertir edad a años aproximados
            edad_anios = edad_num
            if unidad == '2':  # Meses
                edad_anios = edad_num / 12
            elif unidad == '3':  # Días
                edad_anios = edad_num / 365

            # Diagnósticos perinatales (P00-P96) solo para recién nacidos
            if diagnostico.startswith('P') and edad_anios > 0.1:  # Más de un mes
                errors.append(ValidationError(
                    file_name, line_number, 'edad/diagnostico',
                    f"Incoherencia de edad: Paciente con edad {edad} {['años', 'meses', 'días'][int(unidad)-1]} "
                    f"con diagnóstico perinatal '{diagnostico}' que es típico de recién nacidos",
                    "Res. 2275/2023 - Validación de coherencia",
                    "Verificar la edad del paciente o el código de diagnóstico"
                ))

            # Enfermedades seniles en niños
            if diagnostico in ['G20X', 'G30X'] and edad_anios < 40:  # Parkinson, Alzheimer
                errors.append(ValidationError(
                    file_name, line_number, 'edad/diagnostico',
                    f"Incoherencia de edad: Paciente con edad {edad} {['años', 'meses', 'días'][int(unidad)-1]} "
                    f"con diagnóstico '{diagnostico}' que es poco común en esta edad",
                    "Res. 2275/2023 - Validación de coherencia",
                    "Verificar la edad del paciente o el código de diagnóstico"
                ))

        except (ValueError, TypeError):
            pass

        return errors
