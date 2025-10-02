# Estructura del Proyecto ESE

## Organización Actual

El proyecto ha sido reorganizado siguiendo las mejores prácticas de desarrollo de software:

### 📁 Directorios Principales

#### `/src/` - Código Fuente
Contiene todos los módulos Python del proyecto:
- `validador_completo.py` - Validador principal con todas las reglas ESE
- `errores.py` - Diccionario de códigos de error y explicaciones
- `validaciones.py` - Validaciones originales (compatibilidad)
- `validaciones_nuevas.py` - Validaciones adicionales
- `codigo_principal.py` - Script principal de ejecución
- `generador_csv.py` - Generador de datos de prueba
- `__init__.py` - Configuración del paquete Python

#### `/tests/` - Pruebas
Contiene las pruebas y scripts de demostración:
- `demo_validador.py` - Script de demostración
- `test_validador.py` - Tests unitarios
- `__init__.py` - Configuración del módulo de tests

#### `/docs/` - Documentación
Documentación completa del proyecto:
- `DOCUMENTACION_VALIDACIONES.md` - Documentación técnica completa
- `ESTRUCTURA_PROYECTO.md` - Este archivo
- `PROMPT.txt` - Prompts originales del proyecto

#### `/data/` - Datos
Organización de archivos de datos:
- `input/` - Archivos de entrada para validar
- `output/` - Resultados de validaciones
- `reference/` - Archivos de referencia y configuración

#### `/config/` - Configuración
Archivos de configuración del proyecto:
- `config.py` - Configuración principal
- `__init__.py` - Configuración del módulo

### 📄 Archivos de Configuración

- `README.md` - Documentación principal del proyecto
- `requirements.txt` - Dependencias de Python
- `setup.py` - Configuración de instalación
- `.gitignore` - Archivos a ignorar en control de versiones
- `run_validation.py` - Script principal para ejecutar validaciones

## Cómo Usar la Nueva Estructura

### Ejecutar Validaciones

```bash
# Método 1: Usar el script principal
python run_validation.py archivo.csv --fecha-corte 2023-12-31

# Método 2: Usar directamente el módulo
python -m src.codigo_principal
```

### Importar en Código Python

```python
# Importar desde el paquete src
from src.validador_completo import ValidadorESE, validar_archivo_ese
from src.errores import ERRORES

# O usar el paquete completo
import src
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python -m unittest discover tests

# Ejecutar test específico
python tests/test_validador.py

# Ejecutar demo
python tests/demo_validador.py
```

### Instalar como Paquete

```bash
# Instalar en modo desarrollo
pip install -e .

# Instalar dependencias
pip install -r requirements.txt
```

## Beneficios de la Nueva Estructura

### ✅ Organización Clara
- Separación clara entre código, tests, documentación y datos
- Estructura estándar de proyecto Python
- Fácil navegación y mantenimiento

### ✅ Escalabilidad
- Fácil agregar nuevos módulos y funcionalidades
- Estructura preparada para crecimiento del proyecto
- Separación de responsabilidades

### ✅ Mantenibilidad
- Código organizado en módulos específicos
- Tests separados del código principal
- Documentación centralizada

### ✅ Profesionalismo
- Sigue estándares de la industria
- Preparado para control de versiones (Git)
- Fácil distribución e instalación

## Migración de Código Existente

Si tienes código que importaba los módulos antiguos, actualiza las importaciones:

```python
# Antes
from validador_completo import ValidadorESE

# Ahora
from src.validador_completo import ValidadorESE
```

## Archivos Temporales

Los siguientes directorios contienen archivos que no pudieron moverse automáticamente:

- `documentosbase/` - Contiene archivos Excel que están siendo utilizados
  - Mover manualmente a `data/reference/` cuando sea posible

## Próximos Pasos

1. **Cerrar archivos Excel abiertos** y mover a `data/reference/`
2. **Actualizar imports** en código existente
3. **Ejecutar tests** para verificar funcionamiento
4. **Eliminar directorios temporales** una vez migrados todos los archivos
5. **Configurar Git** para control de versiones

## Comandos de Limpieza

Una vez que hayas cerrado todos los archivos Excel:

```bash
# Mover archivos restantes
move documentosbase\*.* data\reference\

# Eliminar directorios vacíos
rmdir documentosbase
```