"""
Lector de archivos RIPS con detección automática de tipo
"""
import os
import re
from typing import List, Tuple, Optional, Dict, Any
from .models import AFRecord, USRecord, ACRecord, APRecord, ATRecord, AHRecord, AMRecord, ANRecord, CTRecord
from .rules import ValidationError, AFValidator, USValidator, ACValidator, APValidator, ATValidator, AHValidator


class RIPSFileReader:
    """Lector de archivos RIPS"""

    # Número de campos esperados por tipo de archivo
    EXPECTED_FIELDS = {
        'AF': 17,
        'US': 15,
        'AC': 22,
        'AP': 22,
        'AT': 14,
        'AH': 22,
        'AM': 16,
        'AN': 14,
        'CT': 10
    }

    @staticmethod
    def detect_file_type(filename: str) -> Optional[str]:
        """
        Detecta el tipo de archivo RIPS por su nombre

        Args:
            filename: Nombre del archivo

        Returns:
            Tipo de archivo (AF, US, AC, etc.) o None si no se reconoce
        """
        # Buscar patrón: AF, US, AC, AP, AT, AH, AM, AN, CT seguido de dígitos
        match = re.search(r'(AF|US|AC|AP|AT|AH|AM|AN|CT)\d+\.txt$', filename, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None

    @staticmethod
    def parse_af_line(line: str, line_number: int) -> Tuple[Optional[AFRecord], List[str]]:
        """Parsea una línea del archivo AF"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['AF']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['AF']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = AFRecord(
                cod_prestador=fields[0],
                nombre_prestador=fields[1],
                tipo_documento_prestador=fields[2],
                num_documento_prestador=fields[3],
                num_factura=fields[4],
                fecha_expedicion=fields[5],
                fecha_inicio=fields[6],
                fecha_final=fields[7],
                cod_entidad_administradora=fields[8],
                nombre_entidad_administradora=fields[9],
                num_contrato=fields[10],
                plan_beneficios=fields[11],
                num_poliza=fields[12],
                valor_comision=fields[13],
                num_cuotas_moderadoras=fields[14],
                valor_comision_cm=fields[15],
                valor_neto=fields[16]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def parse_us_line(line: str, line_number: int) -> Tuple[Optional[USRecord], List[str]]:
        """Parsea una línea del archivo US"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['US']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['US']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = USRecord(
                tipo_documento=fields[0],
                num_documento=fields[1],
                cod_entidad_administradora=fields[2],
                tipo_usuario=fields[3],
                primer_apellido=fields[4],
                segundo_apellido=fields[5],
                primer_nombre=fields[6],
                segundo_nombre=fields[7],
                edad=fields[8],
                unidad_medida_edad=fields[9],
                sexo=fields[10],
                cod_departamento=fields[11],
                cod_municipio=fields[12],
                zona_residencial=fields[13],
                num_autorizacion=fields[14]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def parse_ac_line(line: str, line_number: int) -> Tuple[Optional[ACRecord], List[str]]:
        """Parsea una línea del archivo AC"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['AC']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['AC']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = ACRecord(
                num_factura=fields[0],
                cod_prestador=fields[1],
                tipo_documento=fields[2],
                num_documento=fields[3],
                fecha_consulta=fields[4],
                num_autorizacion=fields[5],
                cod_consulta=fields[6],
                cod_consulta_sistema=fields[7],
                descripcion_consulta=fields[8],
                finalidad_consulta=fields[9],
                causa_externa=fields[10],
                diagnostico_principal=fields[11],
                diagnostico_relacionado1=fields[12],
                diagnostico_relacionado2=fields[13],
                diagnostico_relacionado3=fields[14],
                tipo_diagnostico_principal=fields[15],
                valor_consulta=fields[16],
                valor_cuota_moderadora=fields[17],
                valor_neto=fields[18],
                edad=fields[19],
                unidad_medida_edad=fields[20],
                sexo=fields[21]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def parse_ap_line(line: str, line_number: int) -> Tuple[Optional[APRecord], List[str]]:
        """Parsea una línea del archivo AP"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['AP']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['AP']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = APRecord(
                num_factura=fields[0],
                cod_prestador=fields[1],
                tipo_documento=fields[2],
                num_documento=fields[3],
                fecha_procedimiento=fields[4],
                num_autorizacion=fields[5],
                cod_procedimiento=fields[6],
                cod_procedimiento_sistema=fields[7],
                descripcion_procedimiento=fields[8],
                ambito_procedimiento=fields[9],
                finalidad_procedimiento=fields[10],
                personal_atiende=fields[11],
                diagnostico_principal=fields[12],
                diagnostico_relacionado=fields[13],
                complicacion=fields[14],
                forma_realizacion=fields[15],
                valor_procedimiento=fields[16],
                valor_cuota_moderadora=fields[17],
                valor_neto=fields[18],
                edad=fields[19],
                unidad_medida_edad=fields[20],
                sexo=fields[21]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def parse_at_line(line: str, line_number: int) -> Tuple[Optional[ATRecord], List[str]]:
        """Parsea una línea del archivo AT"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['AT']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['AT']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = ATRecord(
                num_factura=fields[0],
                cod_prestador=fields[1],
                tipo_documento=fields[2],
                num_documento=fields[3],
                num_autorizacion=fields[4],
                tipo_servicio=fields[5],
                cod_servicio=fields[6],
                cod_servicio_sistema=fields[7],
                descripcion_servicio=fields[8],
                cantidad=fields[9],
                valor_unitario=fields[10],
                valor_total=fields[11],
                valor_cuota_moderadora=fields[12],
                valor_neto=fields[13]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def parse_ah_line(line: str, line_number: int) -> Tuple[Optional[AHRecord], List[str]]:
        """Parsea una línea del archivo AH"""
        fields = line.strip().split(',')
        errors = []

        if len(fields) != RIPSFileReader.EXPECTED_FIELDS['AH']:
            errors.append(f"Línea {line_number}: Se esperaban {RIPSFileReader.EXPECTED_FIELDS['AH']} campos, se encontraron {len(fields)}")
            return None, errors

        try:
            record = AHRecord(
                num_factura=fields[0],
                cod_prestador=fields[1],
                tipo_documento=fields[2],
                num_documento=fields[3],
                via_ingreso=fields[4],
                fecha_ingreso=fields[5],
                hora_ingreso=fields[6],
                num_autorizacion=fields[7],
                causa_externa=fields[8],
                diagnostico_ingreso=fields[9],
                diagnostico_egreso=fields[10],
                diagnostico_relacionado1=fields[11],
                diagnostico_relacionado2=fields[12],
                diagnostico_relacionado3=fields[13],
                diagnostico_complicacion=fields[14],
                estado_salida=fields[15],
                diagnostico_muerte=fields[16],
                fecha_egreso=fields[17],
                hora_egreso=fields[18],
                valor_hospitalizacion=fields[19],
                valor_cuota_moderadora=fields[20],
                valor_neto=fields[21]
            )
            return record, []
        except Exception as e:
            errors.append(f"Error al parsear línea {line_number}: {str(e)}")
            return None, errors

    @staticmethod
    def read_and_validate_file(file_path: str) -> Tuple[str, List[ValidationError], Dict[str, Any]]:
        """
        Lee y valida un archivo RIPS completo

        Args:
            file_path: Ruta completa al archivo

        Returns:
            Tupla con (tipo_archivo, lista_errores, estadísticas)
        """
        filename = os.path.basename(file_path)
        file_type = RIPSFileReader.detect_file_type(filename)

        if not file_type:
            return None, [ValidationError(filename, 0, "nombre_archivo",
                                         f"No se pudo detectar el tipo de archivo RIPS. Nombre: {filename}",
                                         "Res. 2275/2023",
                                         "El nombre debe seguir el formato: AF######.txt, US######.txt, etc.")], {}

        errors = []
        stats = {
            'total_lines': 0,
            'valid_lines': 0,
            'invalid_lines': 0,
            'parse_errors': 0
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                for line_number, line in enumerate(f, start=1):
                    # Saltar líneas vacías
                    if not line.strip():
                        continue

                    stats['total_lines'] += 1

                    # Parsear línea según tipo de archivo
                    record = None
                    parse_errors = []

                    if file_type == 'AF':
                        record, parse_errors = RIPSFileReader.parse_af_line(line, line_number)
                    elif file_type == 'US':
                        record, parse_errors = RIPSFileReader.parse_us_line(line, line_number)
                    elif file_type == 'AC':
                        record, parse_errors = RIPSFileReader.parse_ac_line(line, line_number)
                    elif file_type == 'AP':
                        record, parse_errors = RIPSFileReader.parse_ap_line(line, line_number)
                    elif file_type == 'AT':
                        record, parse_errors = RIPSFileReader.parse_at_line(line, line_number)
                    elif file_type == 'AH':
                        record, parse_errors = RIPSFileReader.parse_ah_line(line, line_number)

                    # Si hubo errores de parseo
                    if parse_errors:
                        stats['parse_errors'] += 1
                        for error_msg in parse_errors:
                            errors.append(ValidationError(filename, line_number, "estructura_archivo",
                                                         error_msg,
                                                         "Res. 2275/2023",
                                                         "Verificar estructura del archivo y delimitadores"))
                        continue

                    # Si se parseó correctamente, validar
                    if record:
                        validation_errors = []

                        if file_type == 'AF':
                            validation_errors = AFValidator.validate(record, line_number, filename)
                        elif file_type == 'US':
                            validation_errors = USValidator.validate(record, line_number, filename)
                        elif file_type == 'AC':
                            validation_errors = ACValidator.validate(record, line_number, filename)
                        elif file_type == 'AP':
                            validation_errors = APValidator.validate(record, line_number, filename)
                        elif file_type == 'AT':
                            validation_errors = ATValidator.validate(record, line_number, filename)
                        elif file_type == 'AH':
                            validation_errors = AHValidator.validate(record, line_number, filename)

                        if validation_errors:
                            stats['invalid_lines'] += 1
                            errors.extend(validation_errors)
                        else:
                            stats['valid_lines'] += 1

        except FileNotFoundError:
            errors.append(ValidationError(filename, 0, "archivo",
                                         f"Archivo no encontrado: {file_path}",
                                         "Sistema",
                                         "Verificar que el archivo existe en la carpeta input"))
        except Exception as e:
            errors.append(ValidationError(filename, 0, "archivo",
                                         f"Error al leer el archivo: {str(e)}",
                                         "Sistema",
                                         "Verificar permisos y codificación del archivo"))

        return file_type, errors, stats
