# Validador de Archivos RIPS

Sistema automatizado de validación de archivos RIPS (Registros Individuales de Prestación de Servicios de Salud) según la **Resolución 2275 de 2023** del Ministerio de Salud de Colombia, incorporando criterios de la **Resolución 3280 de 2018**.

## Características Principales

- ✅ **Validación automática** de todos los tipos de archivos RIPS (AF, US, AC, AP, AT, AH, AM, AN, CT)
- ✅ **Detección automática** del tipo de archivo según nomenclatura
- ✅ **Validaciones exhaustivas**:
  - Longitud de campos
  - Tipos de datos (numérico, alfabético, alfanumérico, fecha)
  - Obligatoriedad de campos
  - Valores permitidos según catálogos oficiales
  - Formato de códigos CUPS y CIE10
  - Coherencia de fechas
- ✅ **Validaciones cruzadas** entre archivos (facturas, usuarios, referencias)
- ✅ **Detección de duplicados** en facturas y usuarios
- ✅ **Informes detallados en Excel** con:
  - Nombre del archivo con error
  - Número de línea/registro
  - Campo específico con error
  - Descripción detallada del error
  - Regla normativa que incumple
  - Sugerencia de corrección
- ✅ **Sistema de logging completo** para auditoría
- ✅ **CLI parametrizable** para diferentes entornos

## Estructura del Proyecto

```
ErroresJSON/
│
├── input/                      # Carpeta con archivos RIPS a validar
│   ├── AF029785.txt
│   ├── US029785.txt
│   ├── AC029785.txt
│   ├── AP029785.txt
│   ├── AT029785.txt
│   ├── AH029785.txt
│   ├── AM029785.txt
│   ├── AN029785.txt
│   └── CT029785.txt
│
├── output/                     # Carpeta donde se generan informes
│   └── informe_errores.xlsx
│
├── logs/                       # Carpeta con archivos de log
│   └── validacion_rips_YYYYMMDD_HHMMSS.log
│
├── src/                        # Código fuente
│   ├── __init__.py
│   ├── models.py              # Modelos de datos para cada tipo de archivo
│   ├── validators.py          # Validadores por tipo de dato
│   ├── rules.py               # Reglas de validación por archivo
│   ├── file_reader.py         # Lector de archivos RIPS
│   ├── cross_validator.py    # Validaciones cruzadas
│   ├── report_generator.py   # Generador de informes Excel
│   └── logger.py              # Sistema de logging
│
├── main.py                     # Script principal
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Instalación

### Requisitos Previos

- Python 3.8 o superior

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Uso Básico

Simplemente coloque sus archivos RIPS (formato .txt) en la carpeta `input/` y ejecute:

```bash
python main.py
```

El sistema:
1. Detectará automáticamente todos los archivos RIPS
2. Los validará según las resoluciones
3. Generará un informe Excel en `output/informe_errores.xlsx`
4. Creará logs detallados en `logs/`

### Uso Avanzado con Parámetros

```bash
# Especificar directorios personalizados
python main.py --input ./mis_archivos --output ./resultados --logs ./registros

# Ver ayuda
python main.py --help

# Ver versión
python main.py --version
```

### Parámetros Disponibles

- `-i, --input`: Directorio con archivos RIPS a validar (default: `input`)
- `-o, --output`: Directorio para guardar informes (default: `output`)
- `-l, --logs`: Directorio para archivos de log (default: `logs`)

## Tipos de Validaciones

### 1. Validaciones de Formato

- **Fechas**: Formato DD/MM/YYYY, coherencia temporal
- **Números**: Validación de enteros y decimales, rangos permitidos
- **Texto**: Caracteres permitidos, longitud máxima
- **Códigos**:
  - CUPS: 6 dígitos numéricos
  - CIE10: Letra + 2-4 caracteres (ej: A001, Z000, I10X)
  - Tipos de documento: CC, TI, RC, CE, PA, MS, AS, CD, SC, PE, PT, NI

### 2. Validaciones de Catálogos

- Tipo de usuario (1-4)
- Sexo (M/F)
- Unidad de edad (1=años, 2=meses, 3=días)
- Zona residencial (U=Urbana, R=Rural)
- Códigos DANE de departamentos y municipios

### 3. Validaciones Cruzadas

- Facturas en AC, AP, AT, AH, AM deben existir en AF
- Usuarios en AC, AP, AT, AH, AM deben existir en US
- Detección de facturas duplicadas en AF
- Detección de usuarios duplicados en US

### 4. Validaciones de Coherencia

- Fecha de inicio ≤ Fecha final
- Fecha de nacimiento ≤ Fecha de atención
- Fecha de ingreso ≤ Fecha de egreso
- Valores monetarios ≥ 0
- Edad coherente con unidad de medida

## Formato del Informe

El archivo Excel generado contiene dos hojas:

### Hoja "Errores Detectados"
Tabla con los siguientes campos:
- **Nombre del Documento**: Archivo donde se encontró el error
- **Número de Registro/Línea**: Ubicación exacta del error
- **Nombre del Campo**: Campo específico con problema
- **Descripción del Error**: Explicación detallada
- **Regla Normativa Asociada**: Resolución que incumple
- **Corrección Recomendada**: Sugerencia para solucionar

### Hoja "Resumen"
Estadísticas generales:
- Total de archivos procesados
- Total de registros procesados
- Total de errores encontrados
- Errores por archivo
- Campos con más errores
- Estadísticas de validación cruzada

## Ejemplos de Errores Detectados

### Error de Formato de Fecha
```
Campo: fecha_consulta
Error: El campo 'fecha_consulta' debe tener formato DD/MM/YYYY.
       Valor recibido: '01-08-2025'
Regla: Res. 2275/2023
Corrección: Cambiar formato a 01/08/2025
```

### Error de Código CIE10
```
Campo: diagnostico_principal
Error: El campo 'diagnostico_principal' no cumple con el formato CIE10 válido.
       Valor: 'A00'. Formato esperado: Letra + 2 dígitos + opcional(dígito/X)
Regla: Res. 2275/2023 y 3280/2018
Corrección: Usar código CIE10 completo, ej: A001
```

### Error de Referencia Cruzada
```
Campo: num_factura
Error: La factura '110129786' no existe en el archivo AF
Regla: Res. 2275/2023 - Validación cruzada
Corrección: Verificar que la factura esté registrada en el archivo AF o corregir el número
```

## Logs

Los logs se generan automáticamente en la carpeta `logs/` con nombre:
```
validacion_rips_YYYYMMDD_HHMMSS.log
```

Contienen información detallada sobre:
- Archivos procesados
- Estadísticas por archivo
- Errores encontrados
- Validaciones cruzadas realizadas
- Resumen general

## Resoluciones Aplicadas

### Resolución 2275 de 2023
Establece los lineamientos técnicos para la transmisión de información de RIPS, incluyendo:
- Estructura de archivos
- Campos obligatorios y opcionales
- Longitudes máximas
- Tipos de datos
- Catálogos de códigos

### Resolución 3280 de 2018
Complementa con criterios sobre:
- Codificación de diagnósticos (CIE10)
- Procedimientos (CUPS)
- Estándares de calidad de información

## Mantenimiento y Extensión

### Agregar Nuevas Validaciones

Para agregar validaciones personalizadas, edite:
- `src/validators.py`: Para validadores genéricos
- `src/rules.py`: Para reglas específicas por tipo de archivo

### Actualizar Catálogos

Los catálogos (tipos de documento, códigos DANE, etc.) están en `src/validators.py` en la clase `CodeValidator`.

## Solución de Problemas

### El script no encuentra archivos

**Problema**: No se detectan archivos en la carpeta input
**Solución**:
- Verificar que los archivos tengan extensión `.txt`
- Verificar nomenclatura: AF######.txt, US######.txt, etc.
- Los # pueden ser cualquier dígito

### Errores de codificación

**Problema**: Caracteres extraños en nombres (ej: MU�ETON)
**Solución**:
- El script maneja automáticamente problemas de codificación
- Se recomienda guardar archivos en UTF-8
- Los errores de codificación no afectan la validación

### Archivo Excel no se genera

**Problema**: No se crea el informe
**Solución**:
- Verificar permisos de escritura en carpeta `output/`
- Cerrar el archivo Excel si está abierto
- Verificar que openpyxl esté instalado: `pip install openpyxl`

## Contribuciones

Para contribuir al proyecto:
1. Documente el problema o mejora propuesta
2. Mantenga la estructura modular del código
3. Agregue comentarios y docstrings
4. Actualice la documentación

## Licencia

Este proyecto está desarrollado para uso interno de instituciones de salud en Colombia para cumplimiento de normativa vigente.

## Contacto y Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contacte al administrador del sistema.

## Changelog

### Versión 1.0.0 (2025)
- Implementación inicial
- Soporte para todos los tipos de archivo RIPS (AF, US, AC, AP, AT, AH, AM, AN, CT)
- Validaciones según Resolución 2275/2023
- Validaciones cruzadas entre archivos
- Generación de informes Excel
- Sistema de logging completo
- CLI con parámetros configurables

---

**Nota**: Este validador es una herramienta de apoyo para verificar la calidad de los archivos RIPS. Se recomienda revisar manualmente los errores críticos y consultar la normativa oficial para casos específicos.
