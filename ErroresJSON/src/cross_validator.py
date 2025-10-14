"""
Validaciones cruzadas entre archivos RIPS
Verifica consistencia de datos entre diferentes archivos
"""
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from .rules import ValidationError


class CrossFileValidator:
    """Validador de consistencia cruzada entre archivos RIPS"""

    def __init__(self):
        """Inicializa el validador cruzado"""
        # Diccionarios para almacenar datos de referencia
        self.facturas_af: Set[str] = set()  # Facturas del archivo AF
        self.usuarios_us: Set[Tuple[str, str]] = set()  # (tipo_doc, num_doc) del archivo US
        self.prestadores_af: Set[str] = set()  # Códigos de prestadores del AF

        # Para detectar duplicados
        self.facturas_duplicadas: Dict[str, int] = defaultdict(int)
        self.usuarios_duplicados: Dict[Tuple[str, str], int] = defaultdict(int)

        # Estadísticas
        self.stats = {
            'total_facturas_af': 0,
            'total_usuarios_us': 0,
            'facturas_no_encontradas': 0,
            'usuarios_no_encontrados': 0,
            'duplicados': 0
        }

    def register_af_data(self, records: List[Dict[str, str]], filename: str):
        """
        Registra datos del archivo AF para validaciones cruzadas

        Args:
            records: Lista de registros parseados del AF
            filename: Nombre del archivo
        """
        for record in records:
            num_factura = record.get('num_factura', '')
            cod_prestador = record.get('cod_prestador', '')

            if num_factura:
                self.facturas_af.add(num_factura)
                self.facturas_duplicadas[num_factura] += 1
                self.stats['total_facturas_af'] += 1

            if cod_prestador:
                self.prestadores_af.add(cod_prestador)

    def register_us_data(self, records: List[Dict[str, str]], filename: str):
        """
        Registra datos del archivo US para validaciones cruzadas

        Args:
            records: Lista de registros parseados del US
            filename: Nombre del archivo
        """
        for record in records:
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                self.usuarios_us.add(user_key)
                self.usuarios_duplicados[user_key] += 1
                self.stats['total_usuarios_us'] += 1

    def validate_ac_references(self, records: List[Dict[str, str]], filename: str, line_offset: int = 1) -> List[ValidationError]:
        """
        Valida que los registros AC hagan referencia a facturas y usuarios válidos

        Args:
            records: Lista de registros AC
            filename: Nombre del archivo AC
            line_offset: Línea inicial (por defecto 1)

        Returns:
            Lista de errores encontrados
        """
        errors = []

        for idx, record in enumerate(records, start=line_offset):
            num_factura = record.get('num_factura', '')
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            # Validar que la factura exista en AF
            if num_factura and num_factura not in self.facturas_af:
                errors.append(ValidationError(
                    filename, idx, 'num_factura',
                    f"La factura '{num_factura}' no existe en el archivo AF",
                    "Res. 2275/2023 - Validación cruzada",
                    "Verificar que la factura esté registrada en el archivo AF o corregir el número"
                ))
                self.stats['facturas_no_encontradas'] += 1

            # Validar que el usuario exista en US
            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                if user_key not in self.usuarios_us:
                    errors.append(ValidationError(
                        filename, idx, 'tipo_documento/num_documento',
                        f"El usuario {tipo_doc} {num_doc} no existe en el archivo US",
                        "Res. 2275/2023 - Validación cruzada",
                        "Verificar que el usuario esté registrado en el archivo US"
                    ))
                    self.stats['usuarios_no_encontrados'] += 1

        return errors

    def validate_ap_references(self, records: List[Dict[str, str]], filename: str, line_offset: int = 1) -> List[ValidationError]:
        """
        Valida que los registros AP hagan referencia a facturas y usuarios válidos

        Args:
            records: Lista de registros AP
            filename: Nombre del archivo AP
            line_offset: Línea inicial

        Returns:
            Lista de errores encontrados
        """
        errors = []

        for idx, record in enumerate(records, start=line_offset):
            num_factura = record.get('num_factura', '')
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            # Validar que la factura exista en AF
            if num_factura and num_factura not in self.facturas_af:
                errors.append(ValidationError(
                    filename, idx, 'num_factura',
                    f"La factura '{num_factura}' no existe en el archivo AF",
                    "Res. 2275/2023 - Validación cruzada",
                    "Verificar que la factura esté registrada en el archivo AF"
                ))
                self.stats['facturas_no_encontradas'] += 1

            # Validar que el usuario exista en US
            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                if user_key not in self.usuarios_us:
                    errors.append(ValidationError(
                        filename, idx, 'tipo_documento/num_documento',
                        f"El usuario {tipo_doc} {num_doc} no existe en el archivo US",
                        "Res. 2275/2023 - Validación cruzada",
                        "Verificar que el usuario esté registrado en el archivo US"
                    ))
                    self.stats['usuarios_no_encontrados'] += 1

        return errors

    def validate_at_references(self, records: List[Dict[str, str]], filename: str, line_offset: int = 1) -> List[ValidationError]:
        """
        Valida que los registros AT hagan referencia a facturas y usuarios válidos

        Args:
            records: Lista de registros AT
            filename: Nombre del archivo AT
            line_offset: Línea inicial

        Returns:
            Lista de errores encontrados
        """
        errors = []

        for idx, record in enumerate(records, start=line_offset):
            num_factura = record.get('num_factura', '')
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            # Validar que la factura exista en AF
            if num_factura and num_factura not in self.facturas_af:
                errors.append(ValidationError(
                    filename, idx, 'num_factura',
                    f"La factura '{num_factura}' no existe en el archivo AF",
                    "Res. 2275/2023 - Validación cruzada",
                    "Verificar que la factura esté registrada en el archivo AF"
                ))
                self.stats['facturas_no_encontradas'] += 1

            # Validar que el usuario exista en US
            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                if user_key not in self.usuarios_us:
                    errors.append(ValidationError(
                        filename, idx, 'tipo_documento/num_documento',
                        f"El usuario {tipo_doc} {num_doc} no existe en el archivo US",
                        "Res. 2275/2023 - Validación cruzada",
                        "Verificar que el usuario esté registrado en el archivo US"
                    ))
                    self.stats['usuarios_no_encontrados'] += 1

        return errors

    def validate_ah_references(self, records: List[Dict[str, str]], filename: str, line_offset: int = 1) -> List[ValidationError]:
        """
        Valida que los registros AH hagan referencia a facturas y usuarios válidos

        Args:
            records: Lista de registros AH
            filename: Nombre del archivo AH
            line_offset: Línea inicial

        Returns:
            Lista de errores encontrados
        """
        errors = []

        for idx, record in enumerate(records, start=line_offset):
            num_factura = record.get('num_factura', '')
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            # Validar que la factura exista en AF
            if num_factura and num_factura not in self.facturas_af:
                errors.append(ValidationError(
                    filename, idx, 'num_factura',
                    f"La factura '{num_factura}' no existe en el archivo AF",
                    "Res. 2275/2023 - Validación cruzada",
                    "Verificar que la factura esté registrada en el archivo AF"
                ))
                self.stats['facturas_no_encontradas'] += 1

            # Validar que el usuario exista en US
            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                if user_key not in self.usuarios_us:
                    errors.append(ValidationError(
                        filename, idx, 'tipo_documento/num_documento',
                        f"El usuario {tipo_doc} {num_doc} no existe en el archivo US",
                        "Res. 2275/2023 - Validación cruzada",
                        "Verificar que el usuario esté registrado en el archivo US"
                    ))
                    self.stats['usuarios_no_encontrados'] += 1

        return errors

    def validate_am_references(self, records: List[Dict[str, str]], filename: str, line_offset: int = 1) -> List[ValidationError]:
        """
        Valida que los registros AM hagan referencia a facturas y usuarios válidos

        Args:
            records: Lista de registros AM
            filename: Nombre del archivo AM
            line_offset: Línea inicial

        Returns:
            Lista de errores encontrados
        """
        errors = []

        for idx, record in enumerate(records, start=line_offset):
            num_factura = record.get('num_factura', '')
            tipo_doc = record.get('tipo_documento', '')
            num_doc = record.get('num_documento', '')

            # Validar que la factura exista en AF
            if num_factura and num_factura not in self.facturas_af:
                errors.append(ValidationError(
                    filename, idx, 'num_factura',
                    f"La factura '{num_factura}' no existe en el archivo AF",
                    "Res. 2275/2023 - Validación cruzada",
                    "Verificar que la factura esté registrada en el archivo AF"
                ))
                self.stats['facturas_no_encontradas'] += 1

            # Validar que el usuario exista en US
            if tipo_doc and num_doc:
                user_key = (tipo_doc, num_doc)
                if user_key not in self.usuarios_us:
                    errors.append(ValidationError(
                        filename, idx, 'tipo_documento/num_documento',
                        f"El usuario {tipo_doc} {num_doc} no existe en el archivo US",
                        "Res. 2275/2023 - Validación cruzada",
                        "Verificar que el usuario esté registrado en el archivo US"
                    ))
                    self.stats['usuarios_no_encontrados'] += 1

        return errors

    def check_duplicates(self) -> List[ValidationError]:
        """
        Verifica duplicados en facturas y usuarios

        Returns:
            Lista de errores de duplicados
        """
        errors = []

        # Verificar facturas duplicadas
        for factura, count in self.facturas_duplicadas.items():
            if count > 1:
                errors.append(ValidationError(
                    "AF (archivo)", 0, 'num_factura',
                    f"La factura '{factura}' aparece {count} veces en el archivo AF (duplicado)",
                    "Res. 2275/2023 - Validación de integridad",
                    "Verificar y eliminar facturas duplicadas"
                ))
                self.stats['duplicados'] += 1

        # Verificar usuarios duplicados
        for user_key, count in self.usuarios_duplicados.items():
            if count > 1:
                tipo_doc, num_doc = user_key
                errors.append(ValidationError(
                    "US (archivo)", 0, 'tipo_documento/num_documento',
                    f"El usuario {tipo_doc} {num_doc} aparece {count} veces en el archivo US (duplicado)",
                    "Res. 2275/2023 - Validación de integridad",
                    "Verificar y eliminar usuarios duplicados"
                ))
                self.stats['duplicados'] += 1

        return errors

    def get_statistics(self) -> Dict[str, int]:
        """Retorna estadísticas de validación cruzada"""
        return self.stats
