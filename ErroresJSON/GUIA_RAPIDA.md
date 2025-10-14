# Guía Rápida - Validador RIPS

## Inicio Rápido en 3 Pasos

### 1️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Colocar Archivos RIPS
Copie sus archivos `.txt` en la carpeta `input/`:
- AF######.txt (Facturas)
- US######.txt (Usuarios)
- AC######.txt (Consultas)
- AP######.txt (Procedimientos)
- AT######.txt (Otros Servicios)
- AH######.txt (Hospitalización)
- AM######.txt (Medicamentos)
- AN######.txt (Recién Nacidos)
- CT######.txt (Control)

### 3️⃣ Ejecutar Validación
```bash
python main.py
```

El informe se generará en: `output/informe_errores.xlsx`

---

## Estructura de Archivos

```
ErroresJSON/
├── input/          ← COLOQUE AQUÍ SUS ARCHIVOS .txt
├── output/         ← AQUÍ SE GENERA EL INFORME Excel
├── logs/           ← LOGS AUTOMÁTICOS
├── main.py         ← EJECUTE ESTE ARCHIVO
└── README.md       ← DOCUMENTACIÓN COMPLETA
```

---

## Comandos Útiles

### Ejecutar con directorios personalizados
```bash
python main.py --input ./mis_datos --output ./mis_reportes
```

### Ver ayuda
```bash
python main.py --help
```

### Ver versión
```bash
python main.py --version
```

---

## Interpretando el Informe Excel

### Hoja "Errores Detectados"
Cada fila representa un error con:
- **Nombre del Documento**: Archivo con el error
- **Número de Línea**: Ubicación exacta
- **Campo**: Dato específico con problema
- **Descripción**: Qué está mal
- **Regla Normativa**: Resolución que incumple
- **Corrección Recomendada**: Cómo solucionarlo

### Hoja "Resumen"
Estadísticas generales:
- Total de errores
- Errores por archivo
- Campos más problemáticos
- Validaciones cruzadas

---

## Tipos de Errores Comunes

### ❌ Fechas Incorrectas
**Síntoma**: "El campo 'fecha_consulta' debe tener formato DD/MM/YYYY"
**Solución**: Cambiar formato a DD/MM/YYYY (ej: 01/08/2025)

### ❌ Códigos CIE10 Inválidos
**Síntoma**: "no cumple con el formato CIE10 válido"
**Solución**: Usar formato correcto (ej: A001, Z000, I10X)

### ❌ Campos Vacíos
**Síntoma**: "El campo '...' es obligatorio"
**Solución**: Completar el campo requerido

### ❌ Referencias No Encontradas
**Síntoma**: "La factura '...' no existe en el archivo AF"
**Solución**: Verificar que la factura/usuario exista en AF/US

### ❌ Valores Fuera de Rango
**Síntoma**: "Edad debe ser entre 0 y 150"
**Solución**: Corregir el valor numérico

---

## Validaciones Realizadas

✅ Formato de fechas (DD/MM/YYYY)
✅ Códigos CUPS (6 dígitos)
✅ Códigos CIE10 (formato correcto)
✅ Tipos de documento válidos
✅ Valores numéricos en rangos correctos
✅ Longitud de campos
✅ Campos obligatorios
✅ Consistencia entre archivos (facturas, usuarios)
✅ Detección de duplicados
✅ Coherencia de fechas

---

## Resoluciones Aplicadas

- **Resolución 2275 de 2023**: Lineamientos técnicos RIPS
- **Resolución 3280 de 2018**: Estándares de calidad

---

## Soporte

Para problemas o dudas:
1. Consulte el [README.md](README.md) completo
2. Revise los logs en la carpeta `logs/`
3. Verifique que sus archivos cumplan la nomenclatura: `TT######.txt`

---

## Ejemplo de Uso Completo

```bash
# 1. Instalar (solo la primera vez)
pip install -r requirements.txt

# 2. Copiar archivos a input/
# (Manualmente o con comandos del sistema)

# 3. Ejecutar validación
python main.py

# 4. Revisar resultados
# - Abrir: output/informe_errores.xlsx
# - Consultar: logs/validacion_rips_*.log

# 5. Corregir errores y volver a ejecutar
```

---

## Notas Importantes

⚠️ **Codificación**: Los archivos deben estar en UTF-8 o el sistema los convertirá automáticamente

⚠️ **Nomenclatura**: Los archivos DEBEN seguir el patrón: AF######.txt, US######.txt, etc.

⚠️ **Delimitador**: Los campos deben estar separados por comas (,)

⚠️ **Excel Abierto**: Si el informe Excel está abierto, ciérrelo antes de ejecutar nuevamente

---

**¿Listo para validar?** → `python main.py`
