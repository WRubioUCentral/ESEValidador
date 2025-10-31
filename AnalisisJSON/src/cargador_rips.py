"""
Módulo para cargar y procesar archivos JSON RIPS según Resolución 2275 de 2023
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class CargadorRIPS:
    """Clase para cargar y procesar archivos RIPS en formato JSON"""

    def __init__(self, ruta_cie10: str = "config/cie10_codigos.json", ruta_cups: str = "config/cups_codigos.json", ruta_maestros: str = "config/codigos_maestros.json"):
        """
        Inicializa el cargador RIPS

        Args:
            ruta_cie10: Ruta al archivo JSON con códigos CIE-10
            ruta_cups: Ruta al archivo JSON con códigos CUPS
            ruta_maestros: Ruta al archivo JSON con códigos maestros
        """
        self.codigos_cie10 = self._cargar_cie10(ruta_cie10)
        self.codigos_cups = self._cargar_cups(ruta_cups)
        self.codigos_maestros = self._cargar_maestros(ruta_maestros)

    def _cargar_cie10(self, ruta: str) -> Dict[str, Dict[str, str]]:
        """Carga el diccionario de códigos CIE-10"""
        try:
            with open(ruta, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo {ruta}")
            return {}

    def _cargar_cups(self, ruta: str) -> Dict[str, str]:
        """Carga el diccionario de códigos CUPS"""
        try:
            with open(ruta, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo {ruta}")
            return {}

    def _cargar_maestros(self, ruta: str) -> Dict[str, Dict[str, str]]:
        """Carga el diccionario de códigos maestros"""
        try:
            with open(ruta, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo {ruta}")
            return {"prestadores": {}, "municipios": {}, "modalidades": {}, "paises": {}}

    def cargar_json(self, ruta_archivo: str) -> Dict[str, Any]:
        """
        Carga un archivo JSON RIPS

        Args:
            ruta_archivo: Ruta al archivo JSON

        Returns:
            Diccionario con los datos del archivo
        """
        with open(ruta_archivo, 'r', encoding='utf-8-sig') as f:
            return json.load(f)

    def obtener_info_diagnostico(self, codigo: str) -> Dict[str, str]:
        """
        Obtiene nombre y descripción de un código diagnóstico CIE-10

        Args:
            codigo: Código CIE-10

        Returns:
            Diccionario con nombre y descripción
        """
        if not codigo:
            return {"nombre": "Sin diagnóstico", "descripcion": ""}

        codigo_upper = codigo.upper()
        info = self.codigos_cie10.get(codigo_upper, {})

        return {
            "codigo": codigo,
            "nombre": info.get("nombre", "Código no encontrado"),
            "descripcion": info.get("descripcion", "")
        }

    def obtener_nombre_cups(self, codigo: str) -> str:
        """
        Obtiene el nombre de un procedimiento CUPS

        Args:
            codigo: Código CUPS

        Returns:
            Nombre del procedimiento
        """
        if not codigo:
            return ""
        return self.codigos_cups.get(codigo, f"PROCEDIMIENTO {codigo}")

    def obtener_nombre_municipio(self, codigo: str) -> str:
        """Obtiene el nombre de un municipio"""
        if not codigo:
            return ""
        return self.codigos_maestros.get("municipios", {}).get(codigo, f"MUNICIPIO {codigo}")

    def obtener_nombre_prestador(self, codigo: str) -> str:
        """Obtiene el nombre de un prestador"""
        if not codigo:
            return ""
        return self.codigos_maestros.get("prestadores", {}).get(codigo, f"PRESTADOR {codigo}")

    def obtener_nombre_modalidad(self, codigo: str) -> str:
        """Obtiene el nombre de una modalidad"""
        if not codigo:
            return ""
        return self.codigos_maestros.get("modalidades", {}).get(codigo, f"MODALIDAD {codigo}")

    def obtener_nombre_pais(self, codigo: str) -> str:
        """Obtiene el nombre de un país"""
        if not codigo:
            return ""
        return self.codigos_maestros.get("paises", {}).get(codigo, f"PAÍS {codigo}")

    def calcular_edad(self, fecha_nacimiento: str, fecha_referencia: str = None) -> int:
        """
        Calcula la edad a partir de fecha de nacimiento

        Args:
            fecha_nacimiento: Fecha en formato YYYY-MM-DD
            fecha_referencia: Fecha de referencia (default: hoy)

        Returns:
            Edad en años
        """
        try:
            fn = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            if fecha_referencia:
                fr = datetime.strptime(fecha_referencia, "%Y-%m-%d")
            else:
                fr = datetime.now()

            edad = fr.year - fn.year
            if (fr.month, fr.day) < (fn.month, fn.day):
                edad -= 1

            return edad
        except:
            return None

    def extraer_usuarios(self, datos: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae la lista de usuarios del JSON RIPS

        Args:
            datos: Diccionario con datos RIPS

        Returns:
            Lista de usuarios
        """
        return datos.get("usuarios", [])

    def extraer_consultas(self, usuario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae las consultas de un usuario

        Args:
            usuario: Diccionario con datos del usuario

        Returns:
            Lista de consultas
        """
        servicios = usuario.get("servicios", {})
        return servicios.get("consultas", [])

    def extraer_procedimientos(self, usuario: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae los procedimientos de un usuario

        Args:
            usuario: Diccionario con datos del usuario

        Returns:
            Lista de procedimientos
        """
        servicios = usuario.get("servicios", {})
        return servicios.get("procedimientos", [])
