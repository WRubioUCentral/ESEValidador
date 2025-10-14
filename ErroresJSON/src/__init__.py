"""
Validador de archivos RIPS según Resolución 2275 de 2023
"""
__version__ = '2.0.0'
__author__ = 'ESE Validador'

from .models import (
    AFRecord, USRecord, ACRecord, APRecord, ATRecord, AHRecord,
    AMRecord, ANRecord, CTRecord
)
from .validators import (
    BaseValidator, DateValidator, NumericValidator,
    LengthValidator, CodeValidator, TextValidator
)
from .rules import ValidationError
from .file_reader import RIPSFileReader
from .cross_validator import CrossFileValidator
from .report_generator import ExcelReportGenerator
from .logger import RIPSLogger, get_logger
from .cie10_catalog import CIE10Catalog, get_cie10_catalog
from .advanced_validators import (
    DuplicateAttentionDetector, CIE10Validator, CoherenceValidator
)
from .auto_corrector import AutoCorrector, CorrectionRecord, apply_safe_corrections

__all__ = [
    'AFRecord', 'USRecord', 'ACRecord', 'APRecord', 'ATRecord', 'AHRecord',
    'AMRecord', 'ANRecord', 'CTRecord',
    'BaseValidator', 'DateValidator', 'NumericValidator',
    'LengthValidator', 'CodeValidator', 'TextValidator',
    'ValidationError', 'RIPSFileReader', 'CrossFileValidator',
    'ExcelReportGenerator', 'RIPSLogger', 'get_logger',
    'CIE10Catalog', 'get_cie10_catalog',
    'DuplicateAttentionDetector', 'CIE10Validator', 'CoherenceValidator',
    'AutoCorrector', 'CorrectionRecord', 'apply_safe_corrections'
]
