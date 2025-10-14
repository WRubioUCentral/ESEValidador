# Guía de Uso - Validador RIPS v2.0

## 🎯 Qué hay de Nuevo en v2.0

### Nuevas Validaciones
- ✅ **Validación de códigos CIE10** contra catálogo vigente
- ✅ **Detección de atenciones duplicadas** (mismo usuario, mismo día)
- ✅ **Coherencia entre campos** (finalidad-diagnóstico-procedimiento)
- ✅ **Coherencia sexo-diagnóstico** (ej: embarazo solo en mujeres)
- ✅ **Coherencia edad-diagnóstico** (ej: Parkinson no en niños)

### Corrección Automática
- ✅ **Formato de fechas** automáticamente corregido
- ✅ **Normalización de texto** (espacios, mayúsculas)
- ✅ **Códigos estandarizados** (tipos de documento)
- ✅ **Registro completo** de todos los cambios

### Informes Mejorados
- ✅ Nueva hoja: **"Correcciones Realizadas"**
- ✅ Nueva hoja: **"Log de Ejecución"**
- ✅ Estadísticas CIE10 detalladas
- ✅ Análisis de duplicados
- ✅ Métricas de coherencia

---

## 🚀 Comandos Principales

### 1. Solo Validación (Modo por Defecto)
```bash
python main.py
```
**Qué hace:**
- Valida TODOS los archivos RIPS
- Detecta errores de formato, CIE10, duplicados, coherencia
- **NO modifica** los archivos originales
- Genera informe completo en Excel

**Usa este modo cuando:**
- Quieres revisar la calidad de tus datos
- Necesitas un informe para auditoría
- Vas a corregir manualmente

---

### 2. Validación con Sugerencias
```bash
python main.py --suggest-corrections
```
**Qué hace:**
- Todo lo del modo 1
- **Analiza** qué se puede corregir automáticamente
- **Sugiere** correcciones en el informe
- **NO aplica** las correcciones

**Usa este modo cuando:**
- Quieres saber qué errores son corregibles
- Necesitas planificar correcciones masivas
- Quieres ver el potencial de auto-corrección

---

### 3. Corrección Automática 🔥
```bash
python main.py --auto-correct
```
**Qué hace:**
- Todo lo de los modos anteriores
- **Aplica correcciones** de alta confianza automáticamente
- **Genera archivos corregidos** en `output/archivosCorregidos/`
- **Registra TODOS los cambios** en el informe Excel

**Usa este modo cuando:**
- Tienes muchos errores de formato
- Confías en las correcciones automáticas
- Quieres ahorrar tiempo en correcciones manuales

**⚠️ IMPORTANTE:**
- Los archivos originales **NUNCA se modifican**
- Archivos corregidos se guardan en carpeta separada
- Todos los cambios quedan registrados

---

## 📊 Entendiendo el Informe Excel

El informe generado (`output/informe_errores.xlsx`) ahora tiene **5 hojas**:

### Hoja 1: "Errores Detectados"
**Qué contiene:**
- Todos los errores encontrados
- Ubicación exacta (archivo y línea)
- Descripción del error
- Regla normativa violada
- Sugerencia de corrección

**Errores nuevos detectados:**
- Códigos CIE10 inválidos
- Atenciones duplicadas
- Incoherencias entre campos

### Hoja 2: "Resumen"
**Qué contiene:**
- Total de errores por tipo
- Archivos más problemáticos
- Campos con más errores
- **Nuevos:** Códigos CIE10 más frecuentes
- **Nuevos:** Estadísticas de duplicados
- **Nuevos:** Problemas de coherencia

### Hoja 3: "Correcciones Realizadas" 🆕
**Qué contiene:**
- Cada corrección aplicada
- Valor original vs valor corregido
- Tipo de corrección
- **Nivel de confianza** (color):
  - 🟢 Verde: Alta confianza (aplicada)
  - 🟡 Amarillo: Media (revisar)
  - 🔴 Naranja: Baja (validar)

**Ejemplo:**
| Archivo | Línea | Campo | Original | Corregido | Confianza |
|---------|-------|-------|----------|-----------|-----------|
| US029785.txt | 45 | tipo_documento | C.C. | CC | Alta |
| AC029785.txt | 123 | fecha_consulta | 2025-08-01 | 01/08/2025 | Alta |

### Hoja 4: "Log de Ejecución" 🆕
**Qué contiene:**
- TODO lo que se mostró en consola
- Proceso completo paso a paso
- Útil para auditoría y troubleshooting

### Hoja 5: "Validación Cruzada"
**Qué contiene:**
- Referencias entre archivos
- Facturas no encontradas
- Usuarios no encontrados
- Duplicados detectados

---

## 📁 Archivos Corregidos

Cuando usas `--auto-correct`, se crea:

```
output/
├── informe_errores.xlsx          ← Informe completo
└── archivosCorregidos/            ← Nueva carpeta
    ├── US029785_corregido.txt     ← Archivos con correcciones
    ├── AC029785_corregido.txt
    └── ...
```

**¿Qué archivos se generan?**
- Solo los que tuvieron correcciones
- Con el sufijo `_corregido.txt`
- Listos para usar/enviar

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Primera Validación
```bash
# Paso 1: Validar sin modificar
python main.py

# Paso 2: Revisar informe_errores.xlsx
# - Ver Hoja "Errores Detectados"
# - Revisar Hoja "Resumen"

# Paso 3: Corregir errores críticos manualmente
# (aquellos que requieren conocimiento médico)

# Paso 4: Volver a validar
python main.py
```

### Ejemplo 2: Con Corrección Automática
```bash
# Paso 1: Aplicar correcciones automáticas
python main.py --auto-correct

# Paso 2: Revisar hoja "Correcciones Realizadas"
# - Verificar que todo esté OK
# - Prestar atención a las amarillas/naranjas

# Paso 3: Usar archivos corregidos
# Los archivos están en output/archivosCorregidos/

# Paso 4: Validar archivos corregidos (opcional)
python main.py -i output/archivosCorregidos
```

### Ejemplo 3: Solo Análisis
```bash
# Ver qué se puede corregir sin aplicar cambios
python main.py --suggest-corrections

# Revisar el informe para decidir
# ¿Vale la pena aplicar correcciones automáticas?
```

---

## 📈 Interpretando las Validaciones Nuevas

### Códigos CIE10 Inválidos
**Qué significa:**
```
El código CIE10 'A00' no se encuentra en el catálogo vigente.
Códigos similares válidos: A000, A001, A009
```

**Cómo corregir:**
1. Consultar catálogo CIE10 oficial
2. Usar el código sugerido si es apropiado
3. **IMPORTANTE:** Validar con personal médico

### Atenciones Duplicadas
**Qué significa:**
```
Usuario CC 1234567890 tiene consulta duplicada el 01/08/2025
(código: 890201). También registrada en AC línea 45
```

**Cómo corregir:**
1. Verificar si es error de digitación
2. Revisar historia clínica del paciente
3. Eliminar el registro duplicado
4. **O** confirmar que sí hubo dos consultas

### Problemas de Coherencia
**Qué significa:**
```
Incoherencia de género: Paciente masculino (M) con diagnóstico 'O23'
que es exclusivo de mujeres (embarazo)
```

**Cómo corregir:**
1. Verificar sexo del paciente
2. Verificar diagnóstico asignado
3. Corregir el campo incorrecto
4. Consultar con área médica si hay duda

---

## ⚙️ Opciones Avanzadas

### Cambiar Directorios
```bash
# Archivos de entrada en otra carpeta
python main.py -i ./mis_archivos

# Salida en carpeta específica
python main.py -o ./resultados

# Todo personalizado
python main.py -i ./datos -o ./informes -l ./registros
```

### Ver Versión
```bash
python main.py --version
# Salida: Validador RIPS v2.0.0
```

### Ayuda Completa
```bash
python main.py --help
```

---

## 🔍 Validaciones Realizadas

### Estándar (v1.0)
- ✅ Formato de campos
- ✅ Longitud de campos
- ✅ Tipos de datos
- ✅ Campos obligatorios
- ✅ Catálogos básicos
- ✅ Referencias cruzadas

### Avanzadas (v2.0)
- ✅ **CIE10:** Códigos contra catálogo oficial
- ✅ **Duplicados:** Mismo usuario, mismo día, mismo servicio
- ✅ **Coherencia finalidad-procedimiento:** Códigos CUPS apropiados
- ✅ **Coherencia finalidad-diagnóstico:** CIE10 coherente con finalidad
- ✅ **Coherencia sexo-diagnóstico:** Diagnósticos apropiados para el sexo
- ✅ **Coherencia edad-diagnóstico:** Diagnósticos normales para la edad

---

## 💡 Consejos y Mejores Prácticas

### Antes de Enviar a la EPS
1. Ejecutar: `python main.py`
2. Revisar errores críticos
3. Corregir manualmente lo necesario
4. Ejecutar: `python main.py --auto-correct`
5. Usar archivos de `output/archivosCorregidos/`

### Para Limpieza Masiva de Datos
1. Hacer backup de archivos originales
2. Ejecutar: `python main.py --auto-correct`
3. Revisar hoja "Correcciones Realizadas"
4. Validar correcciones de confianza media
5. Corregir manualmente lo que quede

### Para Auditoría
1. Ejecutar: `python main.py`
2. Usar hoja "Log de Ejecución" como evidencia
3. Documentar errores encontrados
4. Presentar plan de corrección

---

## ❓ Preguntas Frecuentes

### ¿Se modifican mis archivos originales?
**NO.** Los archivos originales NUNCA se modifican. Los archivos corregidos se guardan en `output/archivosCorregidos/`.

### ¿Qué pasa si no confío en una corrección?
Revisa la hoja "Correcciones Realizadas". Las marcadas en 🟡 amarillo o 🔴 naranja requieren tu revisión antes de usarlas.

### ¿Puedo revertir las correcciones?
Sí. Los archivos originales no cambian. Simplemente no uses los archivos de la carpeta `archivosCorregidos`.

### ¿Cuántos códigos CIE10 tiene el catálogo?
Actualmente >100 códigos más comunes. El sistema acepta también códigos no catalogados si tienen formato válido.

### ¿Detecta todos los tipos de duplicados?
Detecta duplicados de:
- Consultas (AC)
- Procedimientos (AP)
- Servicios (AT)
- Hospitalizaciones (AH)

---

## 🆘 Solución de Problemas

### "No se encontraron archivos RIPS"
- Verifica que los archivos estén en carpeta `input/`
- Verifica nomenclatura: `AF######.txt`, `US######.txt`, etc.

### "Error al procesar archivo"
- Verifica codificación (UTF-8 recomendado)
- Verifica delimitador (debe ser coma `,`)
- Revisa que el archivo no esté corrupto

### El informe Excel no abre
- Cierra el archivo si está abierto
- Verifica que tengas openpyxl instalado
- Ejecuta: `pip install -r requirements.txt`

---

**Versión:** 2.0.0
**Actualizado:** Octubre 2025
**Soporte:** Ver [NUEVAS_FUNCIONALIDADES.md](NUEVAS_FUNCIONALIDADES.md)
