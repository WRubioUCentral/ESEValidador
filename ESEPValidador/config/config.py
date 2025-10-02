"""
Configuración del proyecto ESE
"""

import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
REFERENCE_DIR = DATA_DIR / "reference"
DOCS_DIR = PROJECT_ROOT / "docs"
TESTS_DIR = PROJECT_ROOT / "tests"

# Configuración de validación
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
COMODIN_DATE = "1800-01-01"

# Configuración de archivos
SUPPORTED_INPUT_FORMATS = ['.csv', '.xlsx', '.xls', 'xlsb']
DEFAULT_OUTPUT_FORMAT = '.csv'

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de validación ESE
ESE_COLUMNS = {
    0: "tipo_registro",
    1: "numero_consecutivo", 
    2: "codigo_ips",
    3: "tipo_identificacion",
    4: "numero_identificacion",
    9: "fecha_nacimiento",
    10: "sexo",
    14: "gestante",
    15: "sifilis_gestacional",
    16: "resultado_mini_mental",
    17: "hipotiroidismo_congenito",
    18: "sintomatico_respiratorio",
    19: "consumo_tabaco",
    20: "lepra",
    21: "obesidad_desnutricion",
    22: "resultado_tacto_rectal",
    23: "acido_folico_preconcepcional",
    29: "peso",
    30: "fecha_peso",
    31: "talla",
    32: "fecha_talla"
}

# Valores permitidos
TIPOS_IDENTIFICACION = ['RC', 'TI', 'CE', 'CC', 'PA', 'MS', 'AS', 'NV', 'PE', 'SC', 'DE', 'CN', 'PT', 'PPT']
SEXOS = ['F', 'M']

# Rangos de edad para validaciones
RANGOS_EDAD = {
    'menor_2': (0, 2),
    'entre_2_4': (2, 5),
    'entre_5_12': (5, 13),
    'entre_13_17': (13, 18),
    'mayor_18': (18, 150)
}