"""
Sistema de logging para el validador RIPS
"""
import logging
import os
from datetime import datetime
from typing import Optional


class RIPSLogger:
    """Configurador y gestor de logs para el sistema de validación RIPS"""

    def __init__(self, log_dir: str = 'logs', log_level: int = logging.INFO):
        """
        Inicializa el sistema de logging

        Args:
            log_dir: Directorio donde se guardarán los logs
            log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        self._setup_logger()

    def _setup_logger(self):
        """Configura el logger con formato y handlers"""
        # Crear directorio de logs si no existe
        os.makedirs(self.log_dir, exist_ok=True)

        # Nombre del archivo de log con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = os.path.join(self.log_dir, f'validacion_rips_{timestamp}.log')

        # Configurar logger
        self.logger = logging.getLogger('RIPSValidator')
        self.logger.setLevel(self.log_level)

        # Evitar duplicación de handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para archivo
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Sistema de logging inicializado. Archivo: {log_filename}")

    def info(self, message: str):
        """Log nivel INFO"""
        self.logger.info(message)

    def debug(self, message: str):
        """Log nivel DEBUG"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log nivel WARNING"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """Log nivel ERROR"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info: bool = False):
        """Log nivel CRITICAL"""
        self.logger.critical(message, exc_info=exc_info)

    def log_file_processing(self, filename: str, file_type: str):
        """
        Log inicio de procesamiento de archivo

        Args:
            filename: Nombre del archivo
            file_type: Tipo de archivo RIPS (AF, US, AC, etc.)
        """
        self.info(f"Procesando archivo: {filename} (Tipo: {file_type})")

    def log_file_stats(self, filename: str, stats: dict):
        """
        Log estadísticas de procesamiento de archivo

        Args:
            filename: Nombre del archivo
            stats: Diccionario con estadísticas
        """
        self.info(f"Estadísticas de {filename}:")
        for key, value in stats.items():
            self.info(f"  - {key}: {value}")

    def log_validation_summary(self, total_files: int, total_errors: int, total_records: int):
        """
        Log resumen general de validación

        Args:
            total_files: Total de archivos procesados
            total_errors: Total de errores encontrados
            total_records: Total de registros procesados
        """
        self.info("=" * 60)
        self.info("RESUMEN DE VALIDACIÓN")
        self.info("=" * 60)
        self.info(f"Archivos procesados: {total_files}")
        self.info(f"Registros procesados: {total_records}")
        self.info(f"Errores encontrados: {total_errors}")
        self.info("=" * 60)

    def log_report_generation(self, report_path: str):
        """
        Log generación de informe

        Args:
            report_path: Ruta del informe generado
        """
        self.info(f"Informe de errores generado: {report_path}")


# Instancia global del logger
_global_logger: Optional[RIPSLogger] = None


def get_logger(log_dir: str = 'logs', log_level: int = logging.INFO) -> RIPSLogger:
    """
    Obtiene la instancia global del logger (Singleton)

    Args:
        log_dir: Directorio de logs
        log_level: Nivel de logging

    Returns:
        Instancia de RIPSLogger
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = RIPSLogger(log_dir, log_level)
    return _global_logger
