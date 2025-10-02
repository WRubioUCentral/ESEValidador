# Proyecto ESE - Validador de Eventos de Salud Específicos

## Descripción

Sistema de validación completo para archivos ESE (Eventos de Salud Específicos) que implementa todas las reglas de validación según las especificaciones técnicas oficiales.

## Estructura del Proyecto

```
ProyectoESE/
├── src/                    # Código fuente
│   ├── validador_completo.py    # Validador principal
│   ├── errores.py              # Códigos de error
│   ├── validaciones.py         # Validaciones originales
│   ├── validaciones_nuevas.py  # Validaciones adicionales
│   ├── codigo_principal.py     # Script principal
│   └── generador_csv.py        # Generador de datos de prueba
├── tests/                  # Pruebas y demos
│   └── demo_validador.py       # Script de demostración
├── docs/                   # Documentación
│   ├── DOCUMENTACION_VALIDACIONES.md  # Documentación completa
│   └── PROMPT.txt              # Prompts del proyecto
├── data/                   # Datos
│   ├── input/              # Archivos de entrada
│   ├── output/             # Archivos de salida
│   └── reference/          # Archivos de referencia
├── config/                 # Configuraciones
├── documentos/             # Documentos originales (temporal)
├── documentosbase/         # Documentos base (temporal)
└── errores/                # Carpeta de errores (temporal)
```

## Instalación

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install pandas openpyxl
   ```

## Uso Básico

```python
from src.validador_completo import validar_archivo_ese
import pandas as pd

# Cargar datos
df = pd.read_xlsx('data/input/202 AGOSTO GENERAL.xlsx')
fecha_corte = '2025-08-31'

# Validar
resultados = validar_archivo_ese(df, fecha_corte)

# Revisar resultados
print(f"Errores: {resultados['total_errores']}")
print(f"Warnings: {resultados['total_warnings']}")
```

## Características

- ✅ Validación completa de todas las columnas ESE
- ✅ Más de 50 tipos de validaciones implementadas
- ✅ Manejo de errores y warnings
- ✅ Validaciones cruzadas entre columnas
- ✅ Cálculo automático de edades
- ✅ Validación de formatos de fecha
- ✅ Validación de rangos por edad
- ✅ Reportes detallados de errores

## Documentación

Para documentación completa, consulta [docs/DOCUMENTACION_VALIDACIONES.md](docs/DOCUMENTACION_VALIDACIONES.md)

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.