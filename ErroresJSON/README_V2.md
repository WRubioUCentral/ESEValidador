# Validador de Archivos RIPS v2.0 🚀

Sistema avanzado de validación y corrección automática de archivos RIPS (Registros Individuales de Prestación de Servicios de Salud) según la **Resolución 2275 de 2023** del Ministerio de Salud de Colombia, incorporando criterios de la **Resolución 3280 de 2018**.

## 🆕 Novedades Versión 2.0

### Validaciones Avanzadas
- ✅ **Códigos CIE10 contra catálogo vigente** - Valida diagnósticos con sugerencias
- ✅ **Detección de atenciones duplicadas** - Mismo usuario, mismo día
- ✅ **Coherencia entre campos** - Finalidad, diagnóstico y procedimiento
- ✅ **Coherencia sexo-diagnóstico** - Detecta inconsistencias de género
- ✅ **Coherencia edad-diagnóstico** - Diagnósticos apropiados para la edad

### Corrección Automática
- ✅ **Formatos estandarizados** - Fechas, texto, números automáticamente
- ✅ **Registro completo de cambios** - Trazabilidad total
- ✅ **Niveles de confianza** - Alta, media, baja para cada corrección
- ✅ **Archivos corregidos** - Generados en carpeta separada

### Informes Mejorados
- ✅ **Hoja "Correcciones Realizadas"** - Detalle de cada cambio
- ✅ **Hoja "Log de Ejecución"** - Registro completo del proceso
- ✅ **Estadísticas CIE10** - Códigos más frecuentes
- ✅ **Análisis de duplicados** - Métricas detalladas

---

## 📋 Características Principales

### Validaciones Estándar (v1.0)
- Longitud de campos
- Tipos de datos (numérico, alfabético, alfanumérico, fecha)
- Obligatoriedad de campos
- Valores permitidos según catálogos oficiales
- Formato de códigos CUPS y CIE10
- Coherencia de fechas
- Validaciones cruzadas entre archivos
- Detección de duplicados en facturas/usuarios

### Validaciones Avanzadas (v2.0)
- **Catálogo CIE10:** >100 códigos vigentes más comunes
- **Atenciones duplicadas:** Por usuario y fecha
- **Coherencia clínica:** Validaciones médicas inteligentes
- **Sugerencias automáticas:** Para códigos incorrectos

### Sistema de Corrección
- **Alta confianza:** Formatos, texto, números
- **Media confianza:** Códigos incompletos (requieren revisión)
- **Baja confianza:** Datos clínicos (solo sugerencias)

---

## 🚀 Instalación Rápida

### 1. Requisitos
- Python 3.8 o superior

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Listo para usar
```bash
python main.py
```

---

## 💻 Uso

### Modo 1: Solo Validación (Por Defecto)
```bash
python main.py
```
- Valida todos los archivos
- Genera informe de errores
- **NO modifica archivos**

### Modo 2: Con Sugerencias de Corrección
```bash
python main.py --suggest-corrections
```
- Todo lo anterior +
- Analiza qué se puede corregir
- Sugiere correcciones en el informe

### Modo 3: Corrección Automática
```bash
python main.py --auto-correct
```
- Todo lo anterior +
- **Aplica correcciones automáticas**
- Genera archivos corregidos
- Registra todos los cambios

### Opciones Avanzadas
```bash
# Directorios personalizados
python main.py -i ./datos -o ./reportes -l ./logs

# Ver ayuda completa
python main.py --help

# Ver versión
python main.py --version
```

---

## 📁 Estructura del Proyecto

```
ErroresJSON/
│
├── input/                          # Archivos RIPS a validar
│   ├── AF029785.txt               # Facturas
│   ├── US029785.txt               # Usuarios
│   ├── AC029785.txt               # Consultas
│   ├── AP029785.txt               # Procedimientos
│   ├── AT029785.txt               # Otros Servicios
│   ├── AH029785.txt               # Hospitalización
│   ├── AM029785.txt               # Medicamentos
│   ├── AN029785.txt               # Recién Nacidos
│   └── CT029785.txt               # Control
│
├── output/                         # Resultados
│   ├── informe_errores.xlsx       # Informe completo
│   └── archivosCorregidos/        # Archivos corregidos (v2.0)
│       ├── US029785_corregido.txt
│       └── ...
│
├── logs/                           # Logs de ejecución
│   └── validacion_rips_*.log
│
├── src/                            # Código fuente
│   ├── models.py                  # Modelos de datos
│   ├── validators.py              # Validadores básicos
│   ├── rules.py                   # Reglas por tipo de archivo
│   ├── file_reader.py             # Lector de RIPS
│   ├── cross_validator.py         # Validaciones cruzadas
│   ├── cie10_catalog.py           # Catálogo CIE10 (v2.0)
│   ├── advanced_validators.py     # Validadores avanzados (v2.0)
│   ├── auto_corrector.py          # Corrección automática (v2.0)
│   ├── report_generator.py        # Generador Excel
│   └── logger.py                  # Sistema de logging
│
├── main.py                         # Script principal v2.0
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
├── GUIA_USO_V2.md                 # Guía de uso v2.0
├── NUEVAS_FUNCIONALIDADES.md      # Detalle de mejoras
└── EJEMPLOS_ERRORES.md            # Ejemplos de corrección
```

---

## 📊 Informe Excel Generado

El archivo `output/informe_errores.xlsx` contiene:

### Hoja 1: "Errores Detectados"
| Columna | Descripción |
|---------|-------------|
| Nombre del Documento | Archivo donde se encontró el error |
| Número de Línea | Ubicación exacta |
| Nombre del Campo | Campo específico con error |
| Descripción del Error | Qué está mal |
| Regla Normativa | Resolución que incumple |
| Corrección Recomendada | Cómo solucionarlo |

### Hoja 2: "Resumen"
- Total de archivos procesados
- Total de errores por tipo
- Archivos más problemáticos
- Campos con más errores
- **Nuevo:** Estadísticas CIE10
- **Nuevo:** Métricas de duplicados
- **Nuevo:** Análisis de coherencia

### Hoja 3: "Correcciones Realizadas" 🆕
- Cada corrección aplicada
- Valor original y corregido
- Tipo y confianza
- Razón del cambio
- Timestamp
- **Color según confianza:**
  - 🟢 Verde: Alta (aplicada)
  - 🟡 Amarillo: Media (revisar)
  - 🔴 Naranja: Baja (validar)

### Hoja 4: "Log de Ejecución" 🆕
- Registro completo del proceso
- Todo lo mostrado en consola
- Útil para auditoría

### Hoja 5: "Validación Cruzada"
- Referencias entre archivos
- Facturas/usuarios no encontrados
- Duplicados detectados

---

## 🎯 Ejemplos de Validaciones

### Código CIE10 Inválido
```
Campo: diagnostico_principal
Error: El código CIE10 'A00' no se encuentra en el catálogo vigente.
       Códigos similares válidos: A000, A001, A009
Resolución: Res. 2275/2023 y 3280/2018
Corrección: Usar código CIE10 completo de 4 caracteres
```

### Atención Duplicada
```
Campo: duplicado_atencion
Error: Usuario CC 1234567890 tiene consulta duplicada el 01/08/2025
       (código: 890201). También en AC029785.txt línea 45
Resolución: Res. 2275/2023 - Calidad de datos
Corrección: Verificar si es error o atención real. Eliminar duplicado.
```

### Incoherencia de Género
```
Campo: sexo/diagnostico
Error: Paciente masculino (M) con diagnóstico 'O23' exclusivo de
       mujeres (embarazo)
Resolución: Res. 2275/2023 - Coherencia
Corrección: Verificar sexo del paciente o código de diagnóstico
```

### Corrección Automática Aplicada
```
Campo: fecha_consulta
Original: 2025-08-01
Corregido: 01/08/2025
Confianza: Alta
Razón: Formato de fecha estandarizado a DD/MM/YYYY
```

---

## 📈 Tipos de Validaciones

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Formato** | Estructura de datos | Fecha DD/MM/YYYY |
| **Longitud** | Tamaño de campos | CUPS 6 dígitos |
| **Catálogo** | Valores permitidos | Tipo documento: CC, TI, RC... |
| **CIE10** | Diagnósticos válidos | A001, Z000, I10X |
| **Cruzada** | Entre archivos | Factura existe en AF |
| **Duplicados** | Registros repetidos | Usuario 2 veces mismo día |
| **Coherencia** | Lógica clínica | Embarazo solo en mujeres |

---

## 🛠️ Correcciones Automáticas

### Alta Confianza (Aplicadas Automáticamente)
- ✅ Formato de fechas: `2025-08-01` → `01/08/2025`
- ✅ Normalización texto: `"  JUAN  "` → `"JUAN"`
- ✅ Tipo documento: `C.C.` → `CC`
- ✅ Números: `50.000,00` → `50000.00`

### Media Confianza (Requieren Revisión)
- ⚠️ CUPS incompletos: `8902` → `890200`
- ⚠️ Sugerencias CIE10: `A00` → `A001`

### Baja Confianza (Solo Sugerencias)
- ❌ Diagnósticos médicos
- ❌ Datos de identidad
- ❌ Valores críticos

---

## 🔒 Seguridad y Trazabilidad

- ✅ **Archivos originales NUNCA se modifican**
- ✅ **Archivos corregidos en carpeta separada**
- ✅ **Registro completo de cada cambio**
- ✅ **Timestamp de cada operación**
- ✅ **Nivel de confianza documentado**
- ✅ **Reversión posible en cualquier momento**

---

## 📚 Documentación

1. **[README.md](README.md)** - Este archivo (documentación principal)
2. **[GUIA_USO_V2.md](GUIA_USO_V2.md)** - Guía paso a paso de uso
3. **[NUEVAS_FUNCIONALIDADES.md](NUEVAS_FUNCIONALIDADES.md)** - Detalle técnico de v2.0
4. **[EJEMPLOS_ERRORES.md](EJEMPLOS_ERRORES.md)** - Ejemplos de errores y correcciones
5. **[GUIA_RAPIDA.md](GUIA_RAPIDA.md)** - Inicio rápido

---

## 🎓 Casos de Uso

### 1. Auditoría Previa al Envío
```bash
python main.py
# Revisar informe
# Corregir errores críticos manualmente
# Validar nuevamente
```

### 2. Limpieza Masiva de Datos
```bash
python main.py --auto-correct
# Revisar correcciones realizadas
# Validar archivos corregidos
# Usar archivos de output/archivosCorregidos/
```

### 3. Análisis de Calidad
```bash
python main.py
# Revisar métricas en "Resumen"
# Identificar problemas recurrentes
# Implementar mejoras en procesos
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Opcional)
```bash
export RIPS_INPUT_DIR="./mis_datos"
export RIPS_OUTPUT_DIR="./mis_reportes"
export RIPS_LOG_DIR="./mis_logs"
```

### Integración con Scripts
```python
from main import RIPSValidatorAppV2

validator = RIPSValidatorAppV2(
    input_dir='input',
    output_dir='output',
    auto_correct=True
)
validator.run()
```

---

## 📞 Soporte

### Problemas Comunes

**No encuentra archivos:**
- Verificar nomenclatura: `TT######.txt`
- Verificar ubicación: carpeta `input/`

**Errores de codificación:**
- Guardar archivos en UTF-8
- El sistema maneja automáticamente otros formatos

**Excel no abre:**
- Cerrar archivo si está abierto
- Verificar: `pip install openpyxl`

### Reportar Problemas
1. Revisar logs en carpeta `logs/`
2. Consultar [GUIA_USO_V2.md](GUIA_USO_V2.md)
3. Verificar [EJEMPLOS_ERRORES.md](EJEMPLOS_ERRORES.md)

---

## 🚀 Próximas Mejoras

- [ ] Catálogos actualizables desde archivos externos
- [ ] Interfaz gráfica (GUI)
- [ ] Exportación a PDF
- [ ] API REST
- [ ] Integración con sistemas HIS
- [ ] Validaciones de tarifas SOAT
- [ ] Reportes personalizables

---

## 📜 Resoluciones Aplicadas

### Resolución 2275 de 2023
- Lineamientos técnicos RIPS
- Estructura de archivos
- Campos obligatorios
- Tipos de datos
- Catálogos de códigos

### Resolución 3280 de 2018
- Codificación CIE10
- Procedimientos CUPS
- Estándares de calidad

---

## 🏆 Beneficios

- ⏱️ **Ahorro de tiempo:** Validación automática vs manual
- 🎯 **Precisión:** Detecta errores imperceptibles
- 📋 **Cumplimiento:** Resoluciones 2275/2023 y 3280/2018
- 📊 **Trazabilidad:** Logs completos de cada validación
- 🔄 **Eficiencia:** Corrección automática de errores comunes
- 📈 **Calidad:** Mejora continua de datos
- 🔍 **Transparencia:** Registro de cada cambio
- ✅ **Confianza:** Validaciones médicas inteligentes

---

## 📊 Estadísticas de Uso

En archivos de ejemplo:
- **9 archivos** procesados
- **2,616 registros** analizados
- **2,226 códigos CIE10** validados
- **90 duplicados** detectados
- **1 corrección** aplicada automáticamente

---

## 📝 Licencia

Este proyecto está desarrollado para uso interno de instituciones de salud en Colombia para cumplimiento de normativa vigente.

---

## 👥 Créditos

**Desarrollado con:** Python 3.8+, openpyxl, python-dateutil

**Versión:** 2.0.0
**Fecha:** Octubre 2025
**Autor:** ESE Validador

---

## 🌟 Changelog

### v2.0.0 (Octubre 2025)
- ✨ Validación de códigos CIE10 contra catálogo
- ✨ Detección de atenciones duplicadas
- ✨ Validaciones de coherencia clínica
- ✨ Sistema de corrección automática
- ✨ Registro de cambios en Excel
- ✨ Hoja de log de consola
- ✨ Archivos corregidos generados
- ✨ Argumentos CLI mejorados

### v1.0.0 (Octubre 2025)
- 🎉 Lanzamiento inicial
- ✅ Validaciones estándar
- ✅ Validaciones cruzadas
- ✅ Generación de informes Excel
- ✅ Sistema de logging

---

**¿Listo para validar?** → `python main.py --auto-correct`

Para más información, consulta [GUIA_USO_V2.md](GUIA_USO_V2.md)
