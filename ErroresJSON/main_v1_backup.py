"""
Validador de Archivos RIPS
Resoluciones 2275 de 2023 y 3280 de 2018

Script principal para validar archivos RIPS automáticamente
"""
import os
import sys
import argparse
from typing import List, Dict, Any
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.file_reader import RIPSFileReader
from src.cross_validator import CrossFileValidator
from src.report_generator import ExcelReportGenerator
from src.logger import get_logger
from src.rules import ValidationError


class RIPSValidatorApp:
    """Aplicación principal del validador RIPS"""

    def __init__(self, input_dir: str = 'input', output_dir: str = 'output', log_dir: str = 'logs'):
        """
        Inicializa la aplicación

        Args:
            input_dir: Directorio con archivos RIPS a validar
            output_dir: Directorio donde se guardará el informe
            log_dir: Directorio para logs
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.log_dir = log_dir
        self.logger = get_logger(log_dir)
        self.file_reader = RIPSFileReader()
        self.cross_validator = CrossFileValidator()
        self.all_errors: List[ValidationError] = []
        self.stats = {
            'total_files': 0,
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'files_by_type': {}
        }

    def validate_input_directory(self) -> bool:
        """
        Valida que el directorio de entrada exista y contenga archivos

        Returns:
            True si el directorio es válido, False en caso contrario
        """
        if not os.path.exists(self.input_dir):
            self.logger.error(f"El directorio de entrada no existe: {self.input_dir}")
            return False

        txt_files = list(Path(self.input_dir).glob('*.txt'))
        if not txt_files:
            self.logger.warning(f"No se encontraron archivos .txt en: {self.input_dir}")
            return False

        return True

    def collect_rips_files(self) -> Dict[str, List[str]]:
        """
        Recopila y clasifica archivos RIPS por tipo

        Returns:
            Diccionario con archivos organizados por tipo
        """
        files_by_type = {
            'AF': [], 'US': [], 'AC': [], 'AP': [],
            'AT': [], 'AH': [], 'AM': [], 'AN': [], 'CT': []
        }

        for file_path in Path(self.input_dir).glob('*.txt'):
            file_type = self.file_reader.detect_file_type(file_path.name)
            if file_type:
                files_by_type[file_type].append(str(file_path))
                self.logger.info(f"Archivo detectado: {file_path.name} -> Tipo: {file_type}")
            else:
                self.logger.warning(f"No se pudo detectar el tipo del archivo: {file_path.name}")

        return files_by_type

    def process_file(self, file_path: str) -> None:
        """
        Procesa un archivo RIPS individual

        Args:
            file_path: Ruta al archivo
        """
        filename = os.path.basename(file_path)
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Procesando: {filename}")
        self.logger.info(f"{'='*60}")

        try:
            # Leer y validar archivo
            file_type, errors, file_stats = self.file_reader.read_and_validate_file(file_path)

            # Actualizar estadísticas
            self.stats['total_files'] += 1
            self.stats['total_records'] += file_stats.get('total_lines', 0)
            self.stats['valid_records'] += file_stats.get('valid_lines', 0)
            self.stats['invalid_records'] += file_stats.get('invalid_lines', 0)

            if file_type:
                self.stats['files_by_type'][file_type] = self.stats['files_by_type'].get(file_type, 0) + 1

            # Registrar estadísticas del archivo
            self.logger.log_file_stats(filename, file_stats)

            # Agregar errores a la lista general
            self.all_errors.extend(errors)

            # Log de errores encontrados
            if errors:
                self.logger.warning(f"Se encontraron {len(errors)} errores en {filename}")
            else:
                self.logger.info(f"✓ Archivo {filename} validado correctamente (sin errores)")

        except Exception as e:
            self.logger.error(f"Error al procesar {filename}: {str(e)}", exc_info=True)
            self.all_errors.append(ValidationError(
                filename, 0, "archivo",
                f"Error crítico al procesar el archivo: {str(e)}",
                "Sistema",
                "Verificar formato y estructura del archivo"
            ))

    def load_af_us_for_cross_validation(self, files_by_type: Dict[str, List[str]]):
        """
        Carga datos de AF y US para validaciones cruzadas

        Args:
            files_by_type: Diccionario con archivos por tipo
        """
        self.logger.info("\nCargando datos para validación cruzada...")

        # Cargar AF (facturas)
        for af_file in files_by_type.get('AF', []):
            try:
                with open(af_file, 'r', encoding='utf-8', errors='replace') as f:
                    records = []
                    for line in f:
                        if line.strip():
                            fields = line.strip().split(',')
                            if len(fields) >= 5:
                                records.append({
                                    'num_factura': fields[4],
                                    'cod_prestador': fields[0]
                                })
                    self.cross_validator.register_af_data(records, os.path.basename(af_file))
                    self.logger.info(f"  - Cargadas {len(records)} facturas de {os.path.basename(af_file)}")
            except Exception as e:
                self.logger.error(f"Error al cargar AF para validación cruzada: {e}")

        # Cargar US (usuarios)
        for us_file in files_by_type.get('US', []):
            try:
                with open(us_file, 'r', encoding='utf-8', errors='replace') as f:
                    records = []
                    for line in f:
                        if line.strip():
                            fields = line.strip().split(',')
                            if len(fields) >= 2:
                                records.append({
                                    'tipo_documento': fields[0],
                                    'num_documento': fields[1]
                                })
                    self.cross_validator.register_us_data(records, os.path.basename(us_file))
                    self.logger.info(f"  - Cargados {len(records)} usuarios de {os.path.basename(us_file)}")
            except Exception as e:
                self.logger.error(f"Error al cargar US para validación cruzada: {e}")

    def perform_cross_validation(self, files_by_type: Dict[str, List[str]]):
        """
        Realiza validaciones cruzadas entre archivos

        Args:
            files_by_type: Diccionario con archivos por tipo
        """
        self.logger.info("\n" + "="*60)
        self.logger.info("Realizando validaciones cruzadas...")
        self.logger.info("="*60)

        # Validar referencias en AC, AP, AT, AH, AM
        cross_validation_types = {
            'AC': self.cross_validator.validate_ac_references,
            'AP': self.cross_validator.validate_ap_references,
            'AT': self.cross_validator.validate_at_references,
            'AH': self.cross_validator.validate_ah_references,
            'AM': self.cross_validator.validate_am_references,
        }

        for file_type, validator_func in cross_validation_types.items():
            for file_path in files_by_type.get(file_type, []):
                try:
                    filename = os.path.basename(file_path)
                    self.logger.info(f"Validando referencias cruzadas en {filename}...")

                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        records = []
                        for line in f:
                            if line.strip():
                                fields = line.strip().split(',')
                                if len(fields) >= 4:
                                    record = {
                                        'num_factura': fields[0],
                                        'tipo_documento': fields[2],
                                        'num_documento': fields[3]
                                    }
                                    records.append(record)

                    cross_errors = validator_func(records, filename)
                    if cross_errors:
                        self.logger.warning(f"  - {len(cross_errors)} errores de referencia cruzada")
                        self.all_errors.extend(cross_errors)
                    else:
                        self.logger.info(f"  - ✓ Referencias cruzadas correctas")

                except Exception as e:
                    self.logger.error(f"Error en validación cruzada de {filename}: {e}")

        # Verificar duplicados
        self.logger.info("\nVerificando duplicados...")
        duplicate_errors = self.cross_validator.check_duplicates()
        if duplicate_errors:
            self.logger.warning(f"Se encontraron {len(duplicate_errors)} registros duplicados")
            self.all_errors.extend(duplicate_errors)
        else:
            self.logger.info("✓ No se encontraron duplicados")

    def generate_report(self) -> str:
        """
        Genera el informe Excel con los errores

        Returns:
            Ruta al informe generado
        """
        self.logger.info("\n" + "="*60)
        self.logger.info("Generando informe de errores...")
        self.logger.info("="*60)

        output_file = os.path.join(self.output_dir, 'informe_errores.xlsx')
        report_generator = ExcelReportGenerator(output_file)

        # Agregar estadísticas de validación cruzada
        cross_stats = self.cross_validator.get_statistics()
        report_generator.add_cross_validation_summary(cross_stats)

        # Generar informe
        report_path = report_generator.generate_report(self.all_errors, self.stats)

        self.logger.log_report_generation(report_path)
        return report_path

    def run(self):
        """Ejecuta el proceso completo de validación"""
        self.logger.info("="*60)
        self.logger.info("VALIDADOR DE ARCHIVOS RIPS")
        self.logger.info("Resoluciones 2275 de 2023 y 3280 de 2018")
        self.logger.info("="*60)

        # Validar directorio de entrada
        if not self.validate_input_directory():
            self.logger.error("No se puede continuar. Directorio de entrada inválido.")
            return False

        # Recopilar archivos
        files_by_type = self.collect_rips_files()
        total_files = sum(len(files) for files in files_by_type.values())

        if total_files == 0:
            self.logger.warning("No se encontraron archivos RIPS válidos para procesar.")
            return False

        self.logger.info(f"\nTotal de archivos RIPS encontrados: {total_files}")

        # Procesar cada archivo
        self.logger.info("\n" + "="*60)
        self.logger.info("FASE 1: Validación individual de archivos")
        self.logger.info("="*60)

        for file_type in ['AF', 'US', 'AC', 'AP', 'AT', 'AH', 'AM', 'AN', 'CT']:
            for file_path in files_by_type.get(file_type, []):
                self.process_file(file_path)

        # Cargar datos para validación cruzada
        self.load_af_us_for_cross_validation(files_by_type)

        # Realizar validaciones cruzadas
        self.logger.info("\n" + "="*60)
        self.logger.info("FASE 2: Validación cruzada entre archivos")
        self.logger.info("="*60)
        self.perform_cross_validation(files_by_type)

        # Generar informe
        report_path = self.generate_report()

        # Resumen final
        self.logger.log_validation_summary(
            self.stats['total_files'],
            len(self.all_errors),
            self.stats['total_records']
        )

        if self.all_errors:
            self.logger.warning(f"\n⚠️  Se encontraron {len(self.all_errors)} errores en total")
            self.logger.info(f"📊 Informe detallado disponible en: {report_path}")
        else:
            self.logger.info("\n✓ Todos los archivos fueron validados correctamente (sin errores)")

        return True


def main():
    """Función principal con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Validador de archivos RIPS según Resoluciones 2275/2023 y 3280/2018',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py
  python main.py --input ./datos --output ./resultados
  python main.py -i ./input -o ./output -l ./logs

El script procesará todos los archivos .txt en la carpeta de entrada
y generará un informe Excel con los errores encontrados.
        """
    )

    parser.add_argument(
        '-i', '--input',
        default='input',
        help='Directorio con archivos RIPS a validar (default: input)'
    )

    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Directorio para guardar el informe (default: output)'
    )

    parser.add_argument(
        '-l', '--logs',
        default='logs',
        help='Directorio para archivos de log (default: logs)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Validador RIPS v1.0.0'
    )

    args = parser.parse_args()

    # Crear y ejecutar validador
    try:
        validator = RIPSValidatorApp(
            input_dir=args.input,
            output_dir=args.output,
            log_dir=args.logs
        )
        success = validator.run()

        if success:
            print("\n[OK] Proceso completado exitosamente")
            sys.exit(0)
        else:
            print("\n[ERROR] El proceso finalizo con errores")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n[ADVERTENCIA] Proceso interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Error critico: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
