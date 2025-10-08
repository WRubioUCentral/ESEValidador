# Validador ESE - Resolución 202 de 2021

## Descripción

Sistema de validación completo para archivos ESE (Eventos de Salud Específicos) que implementa todas las validaciones de calidad de datos e incoherencias según los **lineamientos técnicos de la Resolución 202 de 2021** del Ministerio de Salud y Protección Social.

El validador se enfoca en la **calidad de los datos** y la **detección de incoherencias** para garantizar la integridad de la información de salud.

## 🎯 Características Principales

- ✅ **Validación según Resolución 202 de 2021**
- ✅ **Generación directa de reportes en Excel** (sin paso intermedio por CSV)
- ✅ **Detección de errores e incoherencias de datos**
- ✅ **Tabla de distribución de frecuencia de errores**
- ✅ **Validaciones cruzadas entre campos**
- ✅ **Validación de formatos, rangos y coherencia**
- ✅ **+200 tipos de errores documentados**

## 📁 Estructura del Proyecto

```
ESEPValidador/
├── src/                          # Código fuente
│   ├── validador_completo.py     # Validador principal (Resolución 202/2021)
│   ├── errores.py                # Catálogo completo de errores
│   ├── codigo_principal.py       # Script principal de ejecución
│   └── generador_excel.py        # Generador de reportes Excel
├── data/                         # Datos
│   ├── input/                    # ⬅️ COLOCA AQUÍ tus archivos Excel a validar
│   └── output/                   # ⬅️ REPORTES generados automáticamente
├── config/                       # Configuraciones
│   └── config.py                 # Configuración de rutas y parámetros
├── tests/                        # Pruebas
├── docs/                         # Documentación
└── requirements.txt              # Dependencias del proyecto
```

## 🚀 Instalación

1. **Clona o descarga el repositorio**

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

   O manualmente:
   ```bash
   pip install pandas openpyxl numpy
   ```

## 📖 Uso

### 1. Coloca tus archivos a validar

Copia los archivos Excel (`.xlsx` o `.xls`) que deseas validar en la carpeta:
```
data/input/
```

### 2. Ejecuta el validador

```bash
python src/codigo_principal.py
```

### 3. Revisa los reportes generados

Los reportes se generan automáticamente en:
```
data/output/
```

Cada reporte incluye **4 hojas Excel**:
- **Errores**: Listado detallado de todos los errores encontrados
- **Distribución de Errores**: Tabla de frecuencia y porcentaje por tipo de error
- **Advertencias**: Warnings detectados
- **Resumen**: Resumen ejecutivo de la validación

## 📊 Ejemplo de Reporte

```
nombre_archivo_reporte_errores_20250108_153045.xlsx

📋 Hoja "Errores":
Código Error | ID Usuario | Dato Erróneo | Explicación
Error220    | 123456789  | ABC@123      | Número de identificación con caracteres no permitidos
Error676    | 987654321  | 12345678901  | La longitud del número de identificación no corresponde...

📊 Hoja "Distribución de Errores":
Código Error | Descripción                              | Frecuencia | Porcentaje
Error220    | Número de identificación con caracteres... | 145        | 23.5%
Error676    | La longitud del número de identificación... | 89         | 14.4%
```

## 🔍 Validaciones Implementadas

El validador implementa las siguientes categorías de validaciones según la Resolución 202 de 2021:

### ✅ Validaciones de Estructura
- Tipo de registro
- Código IPS
- Tipo y número de identificación
- Caracteres permitidos

### ✅ Validaciones de Fechas
- Formato de fechas (AAAA-MM-DD)
- Coherencia con fecha de corte
- Coherencia con fecha de nacimiento
- Validación de comodines

### ✅ Validaciones por Edad y Sexo
- Gestación (solo mujeres 10-59 años)
- Tacto rectal (solo hombres ≥40 años)
- Mamografía (solo mujeres ≥35 años)
- Mini-mental (≥60 años)

### ✅ Validaciones de Rangos
- Peso y talla por grupos de edad
- Rangos de laboratorios
- Valores permitidos por campo

### ✅ Validaciones Cruzadas
- Coherencia entre gestación y variables relacionadas
- Coherencia entre sintomático respiratorio y baciloscopia
- Coherencia entre resultados y fechas de toma

## 📝 Catálogo de Errores

El sistema implementa **más de 200 tipos de errores** documentados en `src/errores.py`:

- **Error001-Error099**: Errores de estructura y formato
- **Error100-Error199**: Errores de fechas
- **Error200-Error299**: Errores de coherencia
- **Error300-Error399**: Errores de validaciones cruzadas
- **Error400-Error499**: Errores de formato de campos
- **Error500-Error599**: Errores de valores permitidos
- **Error600-Error699**: Errores de coherencia avanzada

## ⚙️ Configuración

Puedes ajustar la configuración en `config/config.py`:

```python
# Rutas
INPUT_DIR = DATA_DIR / "input"    # Carpeta de entrada
OUTPUT_DIR = DATA_DIR / "output"  # Carpeta de salida

# Fecha de corte (modifícala en src/codigo_principal.py)
fecha_corte = pd.Timestamp("2025-08-31")
```

## 🛠️ Desarrollo

### Estructura del Código

- **validador_completo.py**: Clase `ValidadorESE` con todas las validaciones
- **errores.py**: Diccionario con códigos y descripciones de errores
- **codigo_principal.py**: Script de ejecución principal
- **generador_excel.py**: Generador de reportes en Excel

### Agregar Nuevas Validaciones

1. Agrega el código de error en `src/errores.py`
2. Implementa la validación en `src/validador_completo.py`
3. Documenta la validación

## 📋 Notas Importantes

- ⚠️ **No se requiere** la carpeta `errores/` - ha sido eliminada
- ✅ Los reportes se generan **directamente en Excel**
- ✅ La carpeta `input/` es la **única fuente** de archivos a validar
- ✅ La carpeta `output/` contiene **todos los reportes** generados

## 🤝 Soporte

Para reportar problemas o solicitar nuevas validaciones, por favor documenta:
1. El archivo que genera el error
2. El error específico encontrado
3. El código de error (si aplica)

## 📄 Licencia

Este proyecto está desarrollado para cumplir con la normativa de la Resolución 202 de 2021 del Ministerio de Salud y Protección Social de Colombia.