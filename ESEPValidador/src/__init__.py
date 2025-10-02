"""
Paquete de validación ESE (Eventos de Salud Específicos)

Este paquete contiene todas las herramientas necesarias para validar
archivos ESE según las especificaciones técnicas oficiales.
"""

from .validador_completo import ValidadorESE, validar_archivo_ese
from .errores import ERRORES

__version__ = "1.0.0"
__author__ = "Proyecto ESE"

__all__ = [
    "ValidadorESE",
    "validar_archivo_ese", 
    "ERRORES"
]