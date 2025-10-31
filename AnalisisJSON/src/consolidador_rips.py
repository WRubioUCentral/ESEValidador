"""
Módulo para consolidar múltiples archivos RIPS y generar reportes consolidados
"""
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from src.cargador_rips import CargadorRIPS


class ConsolidadorRIPS:
    """Clase para consolidar datos de múltiples archivos RIPS"""

    def __init__(self, cargador: CargadorRIPS):
        """
        Inicializa el consolidador

        Args:
            cargador: Instancia de CargadorRIPS
        """
        self.cargador = cargador
        self.datos_consolidados = []
        self.archivos_procesados = []

    def cargar_multiples_rips(self, directorio_input: str) -> List[Dict[str, Any]]:
        """
        Carga todos los archivos JSON del directorio input

        Args:
            directorio_input: Ruta al directorio con archivos RIPS

        Returns:
            Lista con todos los datos RIPS consolidados
        """
        input_path = Path(directorio_input)
        archivos_json = list(input_path.glob("*.json"))

        if not archivos_json:
            print(f"No se encontraron archivos JSON en {directorio_input}")
            return []

        print(f"\nEncontrados {len(archivos_json)} archivos RIPS para procesar:")
        for archivo in archivos_json:
            print(f"  - {archivo.name}")

        for archivo in archivos_json:
            try:
                print(f"\nCargando {archivo.name}...")
                datos = self.cargador.cargar_json(str(archivo))
                self.datos_consolidados.append({
                    "nombre_archivo": archivo.name,
                    "datos": datos
                })
                self.archivos_procesados.append(archivo.name)
            except Exception as e:
                print(f"Error al cargar {archivo.name}: {e}")

        print(f"\nTotal de archivos cargados exitosamente: {len(self.datos_consolidados)}")
        return self.datos_consolidados

    def obtener_datos_consolidados(self) -> Dict[str, Any]:
        """
        Obtiene estructura consolidada con todos los datos

        Returns:
            Diccionario con datos consolidados
        """
        return {
            "archivos_procesados": self.archivos_procesados,
            "total_archivos": len(self.datos_consolidados),
            "fecha_consolidacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "datos": self.datos_consolidados
        }
