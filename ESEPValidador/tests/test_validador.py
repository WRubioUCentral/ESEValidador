"""
Tests unitarios para el validador ESE
"""

import unittest
import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validador_completo import ValidadorESE
import pandas as pd


class TestValidadorESE(unittest.TestCase):
    """Tests para la clase ValidadorESE"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.validador = ValidadorESE()
        self.fecha_corte = "2023-12-31"
    
    def test_calcular_edad(self):
        """Test para el cálculo de edad"""
        edad = self.validador.calcular_edad("1990-01-01", "2023-01-01")
        self.assertEqual(edad, 33)
        
        edad = self.validador.calcular_edad("2000-06-15", "2023-06-14")
        self.assertEqual(edad, 22)
    
    def test_validar_fecha_formato(self):
        """Test para validación de formato de fecha"""
        self.assertTrue(self.validador.validar_fecha_formato("2023-01-01"))
        self.assertFalse(self.validador.validar_fecha_formato("01-01-2023"))
        self.assertFalse(self.validador.validar_fecha_formato("2023/01/01"))
        self.assertFalse(self.validador.validar_fecha_formato("fecha_invalida"))
    
    def test_validar_caracteres_permitidos(self):
        """Test para validación de caracteres permitidos"""
        self.assertTrue(self.validador.validar_caracteres_permitidos("123456789"))
        self.assertTrue(self.validador.validar_caracteres_permitidos("ABC123"))
        self.assertFalse(self.validador.validar_caracteres_permitidos("123Ñ456"))
        self.assertFalse(self.validador.validar_caracteres_permitidos("123@456"))
    
    def test_validar_columna_0(self):
        """Test para validación de tipo de registro"""
        # Caso válido
        errores, warnings = self.validador.validar_columna_0("123", 2)
        self.assertEqual(len(errores), 0)
        
        # Caso inválido
        errores, warnings = self.validador.validar_columna_0("123", 1)
        self.assertEqual(len(errores), 1)
        self.assertEqual(errores[0]['codigo'], 'Error001')
    
    def test_validar_columna_3(self):
        """Test para validación de tipo de identificación"""
        # Caso válido
        errores, warnings = self.validador.validar_columna_3("123", "CC")
        self.assertEqual(len(errores), 0)
        
        # Caso inválido
        errores, warnings = self.validador.validar_columna_3("123", "XX")
        self.assertEqual(len(errores), 1)
        self.assertEqual(errores[0]['codigo'], 'Error003')
    
    def test_validar_columna_10(self):
        """Test para validación de sexo"""
        # Casos válidos
        errores, warnings = self.validador.validar_columna_10("123", "F")
        self.assertEqual(len(errores), 0)
        
        errores, warnings = self.validador.validar_columna_10("123", "M")
        self.assertEqual(len(errores), 0)
        
        # Caso inválido
        errores, warnings = self.validador.validar_columna_10("123", "X")
        self.assertEqual(len(errores), 1)
        self.assertEqual(errores[0]['codigo'], 'Error004')


if __name__ == '__main__':
    unittest.main()