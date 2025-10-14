# Analizador RIPS - Resolución 2275 de 2023 🏥

Sistema completo de análisis y **validación de calidad de datos RIPS** (Registros Individuales de Prestación de Servicios de Salud) según la Resolución 2275 de 2023 del Ministerio de Salud de Colombia.

## 🎯 Características Principales

El sistema analiza archivos RIPS JSON, **valida su calidad** y genera reportes ejecutivos detallados incluyendo:

### 1. **Análisis Demográfico**
- Distribución por sexo, edad, tipo de documento
- Análisis por zona territorial (urbana/rural)
- Distribución geográfica por municipio
- Cruces de sexo × edad

### 2. **Análisis de Diagnósticos (CIE-10)**
- Top 10 diagnósticos más frecuentes **con nombre y descripción CIE-10**
- Identificación de comorbilidades
- Diagnósticos por grupo etario
- Diagnósticos por sexo
- Análisis de diagnósticos relacionados

### 3. **Análisis de Servicios**
- Total de consultas y distribución temporal
- Usuarios con múltiples consultas
- Modalidad y finalidad de atención
- Causas de atención
- Servicios sin autorización
- Análisis financiero (valores y copagos)

### 4. **Análisis de Acudientes**
- Relación paciente-acudiente
- Menores atendidos con acudiente
- Identificación de acompañantes

### 5. **✨ NUEVO: Validación de Calidad de Datos**
Sistema exhaustivo de validación que detecta:

#### 🔍 **Validaciones Implementadas**
- ✅ **Campos Obligatorios**: Verifica presencia de todos los campos requeridos
- ✅ **Formatos**: Documentos, fechas, diagnósticos CIE-10, valores numéricos
- ✅ **Coherencia Lógica**:
  - Edad vs Tipo de Documento (RC/TI/CC)
  - Diagnóstico vs Sexo (embarazo en hombres)
  - Fechas futuras o muy antiguas
- ✅ **Códigos Válidos**: Finalidad, causa externa, zona territorial
- ✅ **Relaciones**: Menores sin acudiente, mayores con acudiente

#### 📊 **Niveles de Calidad**
- 🟢 **EXCELENTE**: 0 anomalías
- 🟢 **BUENA**: 1-5 anomalías
- 🟡 **REGULAR**: 6-15 anomalías
- 🟠 **DEFICIENTE**: 16-30 anomalías
- 🔴 **CRÍTICA**: >30 anomalías

#### 🎨 **Severidades de Anomalías**
- 🔴 **ALTA**: Errores críticos (campos obligatorios, formatos inválidos)
- 🟡 **MEDIA**: Inconsistencias (tipo doc vs edad, fechas antiguas)
- 🟢 **BAJA**: Advertencias (mayor con acudiente)

### 6. **📁 Organización por Carpetas**
Cada archivo JSON procesado genera su propia carpeta con timestamp:
```
output/
├── 7687_156_2275_20251007_191305/
│   ├── informe_completo.xlsx
│   └── informe_gerencial.docx
└── otro_archivo_20251007_192000/
    ├── informe_completo.xlsx
    └── informe_gerencial.docx
```

## 🗂️ Estructura del Proyecto

```
InformadorJSON/
├── config/
│   └── cie10_codigos.json          # 12,634 códigos CIE-10 con nombres y descripciones
├── input/
│   └── 7687_156_2275.json          # Archivo RIPS de ejemplo
├── output/                          # Reportes generados (carpetas por archivo)
│   └── 7687_156_2275_20251007_191305/
│       ├── informe_completo.xlsx
│       └── informe_gerencial.docx
├── src/
│   ├── cargador_rips.py            # Carga de datos y códigos CIE-10
│   ├── analizador_rips.py          # Análisis de datos
│   ├── validador_calidad.py        # 🆕 Validación de calidad de datos
│   └── generador_reportes.py       # Generación de reportes Excel y DOCX
├── main.py                          # Script principal
└── README.md
```

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalar dependencias

```bash
pip install openpyxl python-docx matplotlib
```

## 📖 Uso

### 1. Preparar los datos

Coloca **uno o varios archivos JSON RIPS** en la carpeta `input/`:
```
input/
├── 7687_156_2275.json
├── 7687_156_2222.json
└── otro_archivo.json
```

### 2. Ejecutar el análisis

El sistema procesará **automáticamente TODOS los archivos JSON** en la carpeta `input/`:

```bash
python main.py
```

**Salida en consola:**
```
================================================================================
ANALIZADOR MASIVO DE RIPS - RESOLUCIÓN 2275 DE 2023
================================================================================

Se encontraron 2 archivo(s) JSON para procesar:
  1. 7687_156_2222.json
  2. 7687_156_2275.json

Cargando códigos CIE-10...
[OK] Cargados 12634 códigos CIE-10

================================================================================
PROCESANDO ARCHIVO 1 DE 2
================================================================================
Archivo: input\7687_156_2222.json
...
[OK] Archivo procesado exitosamente

================================================================================
PROCESANDO ARCHIVO 2 DE 2
================================================================================
Archivo: input\7687_156_2275.json
...
[OK] Archivo procesado exitosamente

================================================================================
RESUMEN FINAL DEL PROCESO
================================================================================

Total de archivos procesados: 2
  [OK] Exitosos: 2

Los reportes se generaron en carpetas individuales dentro de 'output/'
```

### 3. Revisar los reportes

Los reportes se generan en **carpetas organizadas** dentro de `output/`:

Cada archivo JSON procesado crea una carpeta con formato `{nombre_archivo}_{timestamp}/`:

#### 📊 **Informe Excel Completo** (`informe_completo.xlsx`)
Libro con **11 hojas especializadas**:
1. **Información General**: Datos básicos del reporte
2. **Datos Personales**: Info completa de cada paciente
3. **Servicios por Paciente**: Detalle de servicios prestados
4. **Análisis Demográfico**: Distribuciones por sexo, edad, documento
5. **Diagnósticos**: Top diagnósticos más frecuentes
6. **Diagnósticos por Género**: Análisis segregado por sexo
7. **Distribución por Edad**: Análisis etario con porcentajes
8. **Distribución Territorial**: Por zona y municipio
9. **Análisis de Servicios**: Finalidades y causas de atención
10. **Acudientes**: Relación menores-acudientes
11. **🆕 Validación de Calidad**:
    - Nivel de calidad con código de color
    - Distribución por severidad (ALTA, MEDIA, BAJA)
    - Top 10 tipos de anomalías
    - Detalle completo de todas las anomalías

#### 📄 **Informe Gerencial DOCX** (`informe_gerencial.docx`)
Documento Word profesional con:
1. **Resumen Ejecutivo**: Análisis narrativo
2. **Análisis Demográfico**: Con gráficos de torta y barras
3. **Distribución Territorial**: Gráficos urbana/rural
4. **Análisis de Diagnósticos**: Gráficos y tablas top 10
5. **Análisis por Género**: Comparación F vs M
6. **Motivos de Consulta**: Gráficos de causas
7. **Análisis de Servicios**: Distribución por finalidad
8. **🆕 Validación de Calidad**:
   - Nivel de calidad con código de color
   - Distribución por severidad
   - Top 10 anomalías más frecuentes
   - Detalle de anomalías críticas
9. **Conclusiones y Recomendaciones**: Hallazgos y sugerencias

## 📊 Ejemplo de Salida

### Resumen en Consola

```
================================================================================
ANALIZADOR DE RIPS - RESOLUCIÓN 2275 DE 2023
================================================================================

Procesando archivo: input/7687_156_2275.json

Cargando códigos CIE-10...
[OK] Cargados 12634 códigos CIE-10

Cargando datos RIPS...
[OK] Datos RIPS cargados exitosamente

Ejecutando análisis...
[OK] Análisis completado

Validando calidad de datos...
[OK] Validación completada - Nivel de calidad: EXCELENTE
    Total de anomalías detectadas: 0

Generando reportes...
[OK] Reporte Excel: output\7687_156_2275_20251007_191305\informe_completo.xlsx
[OK] Informe Gerencial DOCX: output\7687_156_2275_20251007_191305\informe_gerencial.docx

================================================================================
RESUMEN EJECUTIVO
================================================================================

Total de usuarios: 22
Total de consultas: 42
Diagnósticos únicos: 10

--- TOP 5 DIAGNÓSTICOS MÁS FRECUENTES ---
1. [Z719] CONSULTA, NO ESPECIFICADA
   PERSONA EN CONTACTO CON LOS SERVICIOS DE SALUD POR OTRAS CONSULTAS...
   Cantidad: 14

2. [Z717] CONSULTA PARA ASESORIA SOBRE EL VIRUS DE LA INMUNODEFICIENCIA...
   PERSONA EN CONTACTO CON LOS SERVICIOS DE SALUD POR OTRAS CONSULTAS...
   Cantidad: 8

3. [Z012] EXAMEN ODONTOLOGICO
   OTROS EXAMENES ESPECIALES E INVESTIGACION DE PERSONAS SIN QUEJAS...
   Cantidad: 7

4. [Z359] SUPERVISION DE EMBARAZO DE ALTO RIESGO, SIN OTRA ESPECIFICACION
   SUPERVISION DE EMBARAZO DE ALTO RIESGO
   Cantidad: 4

5. [Z391] ATENCION Y EXAMEN DE MADRE EN PERIODO DE LACTANCIA
   EXAMEN Y ATENCION DEL POSTPARTO
   Cantidad: 3

================================================================================
Proceso completado exitosamente
================================================================================
```

### Reporte de Texto (fragmento)

```
================================================================================
REPORTE DE ANÁLISIS RIPS - RESOLUCIÓN 2275 DE 2023
================================================================================

ANÁLISIS DE DIAGNÓSTICOS
================================================================================
Total de Diagnósticos Registrados: 56
Diagnósticos Únicos: 11
Casos con Comorbilidades: 3

TOP 10 DIAGNÓSTICOS MÁS FRECUENTES:
--------------------------------------------------------------------------------
1. [Z719] CONSULTA NO ESPECIFICADA
   Descripción: PERSONAS EN CONTACTO CON LOS SERVICIOS DE SALUD POR OTRAS RAZONES
   Cantidad: 20

2. [Z717] ORIENTACION Y CONSEJO SOBRE ANTICONCEPCION
   Descripción: PERSONAS EN CONTACTO CON LOS SERVICIOS DE SALUD POR OTRAS RAZONES
   Cantidad: 10

COMORBILIDADES IDENTIFICADAS:
--------------------------------------------------------------------------------
1. Diagnóstico Principal: [Z000] EXAMEN GENERAL Y EVALUACION DE SALUD DE NIÑOS NO ENFERMOS
   Diagnósticos Relacionados:
   - [N771] VAGINITIS VULVITIS Y VULVOVAGINITIS EN ENFERMEDADES CLASIFICADAS EN OTRA PARTE
   - [Z308] OTRAS INVESTIGACIONES ESPECIALES DE PESQUISA
```

## 🔍 Información Clave que se Extrae

### Cruces de Información Importantes

1. **Edad × Sexo × Diagnóstico**: Morbilidad por grupo poblacional
2. **Municipio × Diagnóstico**: Caracterización epidemiológica territorial
3. **Finalidad × Causa**: Diferenciación preventiva vs curativa
4. **Usuario × Múltiples consultas**: Fragmentación de atención
5. **Diagnóstico principal × Relacionados**: Comorbilidades
6. **Paciente × Acudiente**: Atención a menores

### Códigos Especiales Identificados

- **Códigos Z**: Atención preventiva y administrativa
  - Z719: Consulta no especificada
  - Z717: Anticoncepción
  - Z012: Examen de rutina infantil
  - Z359: Asesoría anticonceptiva

## 📁 Configuración CIE-10

El archivo `config/cie10_codigos.json` contiene **12,634 códigos CIE-10** con:
- **Código**: Identificador CIE-10 (ej: "Z719")
- **Nombre**: Descripción detallada del diagnóstico
- **Descripción**: Categoría general del diagnóstico

Este archivo se genera automáticamente desde el Excel `TablaReferencia_CIE10__1.xlsx`.

### Regenerar el archivo CIE-10

Si necesitas actualizar los códigos:

```bash
python -c "import openpyxl, json; wb = openpyxl.load_workbook(r'TablaReferencia_CIE10__1.xlsx'); ws = wb.active; cie10 = {str(ws.cell(i, 1).value): {'nombre': str(ws.cell(i, 2).value) if ws.cell(i, 2).value else '', 'descripcion': str(ws.cell(i, 3).value) if ws.cell(i, 3).value else ''} for i in range(2, ws.max_row + 1) if ws.cell(i, 1).value}; open('config/cie10_codigos.json', 'w', encoding='utf-8').write(json.dumps(cie10, indent=2, ensure_ascii=False))"
```

## 🛠️ Personalización

### Analizar otro archivo RIPS

Edita [main.py](main.py:19) línea 19:

```python
archivo_rips = "input/tu_archivo.json"
```

### Modificar análisis

Los módulos están separados por funcionalidad:
- **[cargador_rips.py](src/cargador_rips.py)**: Añadir métodos de carga
- **[analizador_rips.py](src/analizador_rips.py)**: Añadir nuevos análisis
- **[generador_reportes.py](src/generador_reportes.py)**: Modificar formatos de salida

## 📌 Notas Importantes

1. Los códigos CIE-10 se almacenan **separadamente** en `config/cie10_codigos.json`
2. El sistema es **defensivo**: valida datos faltantes y maneja errores
3. Los reportes incluyen **timestamps** para evitar sobrescritura
4. Compatible con la estructura JSON de la **Resolución 2275 de 2023**

## 🔍 Tipos de Anomalías Detectadas

### 🔴 Severidad ALTA (Críticas)
- Campos obligatorios faltantes
- Formato de documento inválido
- Formato de fecha inválido
- Fechas futuras
- Edad negativa o excesiva (>120 años)
- Formato de edad inválido
- Valor de sexo inválido (debe ser F o M)
- Formato de diagnóstico inválido (debe seguir CIE-10)
- Incoherencia diagnóstico-sexo (ej: embarazo en hombres)
- Códigos de finalidad/causa inválidos

### 🟡 Severidad MEDIA
- Longitud de documento inválida según tipo
- Fechas muy antiguas (>10 años)
- Incoherencia tipo documento-edad (RC/TI/CC)
- Tipo de diagnóstico inválido
- Menor sin acudiente registrado
- Valores negativos (consulta, copago)
- Formato de valores numéricos inválido
- Código de zona territorial inválido

### 🟢 Severidad BAJA
- Mayor de edad con acudiente (verificar si aplica)

## 📚 Referencias

- **Resolución 2275 de 2023**: Estándares de reportes RIPS en Colombia
- **CIE-10**: Clasificación Internacional de Enfermedades, 10ª revisión

## 📄 Licencia

Proyecto de análisis para entidades de salud bajo normativa colombiana.

## 👨‍💻 Autor

Desarrollado para análisis y validación de calidad de RIPS en el sector salud colombiano.

---

**Versión**: 2.0 con Validación de Calidad
**Última actualización**: Octubre 2025
**Desarrollado con**: Python 3.10, OpenPyXL, python-docx, Matplotlib
