# Documentación de Validaciones ESE

## Descripción General

Este sistema implementa las validaciones completas para archivos ESE (Eventos de Salud Específicos) según las especificaciones técnicas proporcionadas. El validador verifica la integridad y consistencia de los datos en cada columna del archivo.

## Estructura del Sistema

### Archivos Principales

1. **`validador_completo.py`** - Validador principal con todas las reglas implementadas
2. **`errores.py`** - Diccionario con todos los códigos de error y sus explicaciones
3. **`demo_validador.py`** - Script de demostración con datos de ejemplo
4. **`validaciones.py`** - Validaciones originales (mantenido por compatibilidad)

### Clase Principal: ValidadorESE

La clase `ValidadorESE` encapsula toda la lógica de validación y proporciona métodos para:
- Validar filas individuales
- Validar DataFrames completos
- Generar reportes de errores y warnings
- Calcular edades y validar formatos

## Validaciones Implementadas por Columna

### Columna 0 - Tipo de Registro
- **Valores permitidos**: 2
- **Error**: Error001 si el valor no es 2

### Columna 1 - Número Consecutivo
- **Valores permitidos**: Número consecutivo iniciando en 1
- **Error**: Error002 si no coincide con el número de registro esperado

### Columna 2 - Código IPS
- **Valores permitidos**: Código válido del REPS o 999 (desconocido)
- **Error**: Error021 si la IPS no existe (cuando no es 999)

### Columna 3 - Tipo de Identificación
- **Valores permitidos**: RC, TI, CE, CC, PA, MS, AS, NV, PE, SC, DE
- **Error**: Error003 si no es uno de los valores permitidos

### Columna 4 - Número de Identificación
- **Validaciones**:
  - Error220: Solo números 0-9 y letras A-Z (sin Ñ)
  - Error676: Longitud según tipo de identificación:
    - CC: máximo 10 dígitos
    - TI: máximo 11 dígitos
    - CE: 3-7 caracteres
    - CD: máximo 11 dígitos
    - PA: 3-16 caracteres
    - SC: máximo 9 dígitos
    - PE: 3-15 caracteres

### Columna 9 - Fecha de Nacimiento
- **Validaciones**:
  - Error020: Campo requerido
  - Error421: Formato AAAA-MM-DD válido
  - Error677: No se permiten comodines
  - Error120: No puede ser mayor a la fecha de corte

### Columna 10 - Sexo
- **Valores permitidos**: F, M
- **Error**: Error004 si no es F o M

### Columna 14 - Gestante
- **Validaciones**:
  - Error030: Si es gestante (1, 2, 21), el sexo debe ser F
  - Error222: Si edad < 10 años o >= 60 años, debe ser 0 (no aplica)
  - Error223: Si es mujer de 10-59 años, debe ser diferente de 0
  - Error244: Si no es gestante, variables relacionadas deben ser "no aplica"
  - Error379: Si es gestante, variables relacionadas deben tener datos válidos

### Columna 15 - Sífilis Gestacional
- **Valores permitidos**: 0
- **Error**: Error500 si no es 0

### Columna 16 - Resultado Prueba Mini-Mental
- **Validaciones**:
  - Error503: Si registra resultado (4, 5), debe tener fecha de valoración válida
  - Error504: Valores permitidos: 0, 4, 5, 21
  - Error227: Validación según edad (0 para < 60 años, otros para >= 60 años)

### Columna 17 - Hipotiroidismo Congénito
- **Valores permitidos**: 0
- **Error**: Error505 si no es 0

### Columna 18 - Sintomático Respiratorio
- **Validaciones**:
  - Error232: Si es sintomático (1), debe tener baciloscopia válida
  - Error506: Si no es sintomático (2), baciloscopia debe ser "no aplica"
  - Error507: Si es "riesgo no evaluado" (21), baciloscopia debe ser 21

### Columna 19 - Consumo de Tabaco
- **Validaciones**:
  - Error508: Si edad < 12 años, debe ser 98 (no aplica)

### Columna 20 - Lepra
- **Valores permitidos**: 21
- **Error**: Error509 si no es 21

### Columna 21 - Obesidad/Desnutrición
- **Valores permitidos**: 21
- **Error**: Error510 si no es 21

### Columna 22 - Resultado Tacto Rectal
- **Validaciones**:
  - Error037: Si registra resultado (4, 5, 21), sexo debe ser M
  - Error038: Si es hombre < 40 años, debe ser 0 (no aplica)
  - Error513: Si es mujer, debe ser 0 (no aplica)
  - Error514: Valores permitidos: 0, 4, 5, 21
  - Error237: Si registra fecha válida, debe cumplir condiciones
  - Error512: Si resultado es 21, fecha debe ser comodín

### Columna 23 - Ácido Fólico Preconcepcional
- **Valores permitidos**: 0, 1, 2, 21
- **Error**: Error515 si no es uno de los valores permitidos

### Columnas 29-32 - Peso y Talla
- **Validaciones de Peso**:
  - Error121: Fecha peso no mayor a fecha de corte
  - Error171: Fecha peso no menor a fecha de nacimiento
  - Error041: Si peso es 999, fecha debe ser 1800-01-01
  - Error680-684: Rangos de peso por edad:
    - < 2 años: 1-15 kg
    - 2-4 años: 3-25 kg
    - 5-12 años: 9-80 kg
    - 13-17 años: 30-80 kg
    - >= 18 años: 35-250 kg

- **Validaciones de Talla**:
  - Error122: Fecha talla no mayor a fecha de corte
  - Error172: Fecha talla no menor a fecha de nacimiento
  - Error043: Si talla es 999, fecha debe ser 1800-01-01
  - Error685-689: Rangos de talla por edad:
    - < 2 años: 40-100 cm
    - 2-4 años: 70-110 cm
    - 5-12 años: 80-225 cm
    - 13-17 años: 130-225 cm
    - >= 18 años: 130-225 cm

## Uso del Sistema

### Validación Básica
```python
from validador_completo import validar_archivo_ese
import pandas as pd

# Cargar datos
df = pd.read_csv('archivo_ese.csv')
fecha_corte = '2023-12-31'

# Validar
resultados = validar_archivo_ese(df, fecha_corte)

# Revisar resultados
print(f"Errores: {resultados['total_errores']}")
print(f"Warnings: {resultados['total_warnings']}")
```

### Validación Avanzada
```python
from validador_completo import ValidadorESE

# Crear instancia del validador
validador = ValidadorESE()

# Validar DataFrame
resultados = validador.validar_dataframe(df, fecha_corte)

# Acceder a errores específicos
for error in resultados['errores']:
    print(f"Usuario: {error['usuario']}")
    print(f"Error: {error['codigo']} - {error['explicacion']}")
    print(f"Dato: {error['dato_erroneo']}")
```

## Tipos de Salida

### Estructura de Errores
```python
{
    'usuario': 'ID del usuario con error',
    'dato_erroneo': 'Valor que causó el error',
    'codigo': 'Código del error (ej: Error020)',
    'explicacion': 'Descripción del error'
}
```

### Estructura de Resultados
```python
{
    'errores': [lista de errores],
    'warnings': [lista de warnings],
    'total_errores': número_total_errores,
    'total_warnings': número_total_warnings
}
```

## Funciones Auxiliares

### `calcular_edad(fecha_nacimiento, fecha_referencia)`
Calcula la edad en años entre dos fechas.

### `validar_fecha_formato(fecha_str)`
Valida que una fecha tenga formato AAAA-MM-DD.

### `validar_caracteres_permitidos(texto)`
Valida que el texto solo contenga números 0-9 y letras A-Z (sin Ñ).

## Códigos de Error Implementados

- **Error001-004**: Validaciones básicas de estructura
- **Error020**: Fecha de nacimiento requerida
- **Error021**: IPS no existe
- **Error030**: Validación sexo-gestante
- **Error037-038**: Validaciones tacto rectal
- **Error041, 043**: Validaciones peso/talla sin fecha
- **Error120-122**: Fechas mayores a fecha de corte
- **Error171-172**: Fechas menores a fecha de nacimiento
- **Error220**: Caracteres no permitidos
- **Error222-223**: Validaciones gestante por edad
- **Error227**: Mini-mental según edad
- **Error232**: Sintomático respiratorio
- **Error237**: Tacto rectal con fecha válida
- **Error244**: Variables gestación cuando no es gestante
- **Error379**: Variables gestación cuando es gestante
- **Error421**: Formato fecha nacimiento
- **Error500-515**: Validaciones valores específicos
- **Error676**: Longitud número identificación
- **Error677**: Comodines no permitidos
- **Error680-689**: Rangos peso/talla por edad
- **Warning674-675**: Advertencias comodines fecha

## Extensibilidad

El sistema está diseñado para ser fácilmente extensible:

1. **Agregar nuevas validaciones**: Crear métodos `validar_columna_X()` en la clase ValidadorESE
2. **Nuevos códigos de error**: Agregar al diccionario ERRORES
3. **Validaciones cruzadas**: Implementar en métodos específicos que accedan a múltiples columnas
4. **Nuevos tipos de salida**: Extender los métodos de reporte

## Consideraciones de Rendimiento

- El validador procesa fila por fila para mantener bajo uso de memoria
- Las validaciones están optimizadas para datasets grandes
- Se recomienda procesar archivos en lotes para archivos muy grandes (>100k registros)

## Mantenimiento

Para mantener el sistema actualizado:

1. Revisar periódicamente las especificaciones ESE
2. Actualizar códigos de error según nuevas versiones
3. Agregar pruebas unitarias para nuevas validaciones
4. Documentar cambios en este archivo