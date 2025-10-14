# Ejemplos de Errores y Correcciones

Esta guía muestra ejemplos reales de errores detectados por el validador y cómo corregirlos.

---

## 1. Errores de Formato de Fecha

### ❌ Error: Formato Incorrecto
```
Archivo: AC029785.txt, Línea 45
Campo: fecha_consulta
Error: El campo 'fecha_consulta' debe tener formato DD/MM/YYYY.
       Valor recibido: '2025-08-01'
```

**Corrección:**
```
ANTES: 2025-08-01
DESPUÉS: 01/08/2025
```

### ❌ Error: Fecha Futura
```
Campo: fecha_expedicion
Error: El campo 'fecha_expedicion' no puede ser una fecha futura.
       Fecha: 15/01/2026
```

**Corrección:**
```
ANTES: 15/01/2026
DESPUÉS: 15/01/2025  (o la fecha correcta del pasado)
```

### ❌ Error: Incoherencia de Fechas
```
Campo: fecha_inicio/fecha_final
Error: La fecha 'fecha_inicio' (15/08/2025) no puede ser posterior
       a 'fecha_final' (01/08/2025)
```

**Corrección:**
```
ANTES: fecha_inicio=15/08/2025, fecha_final=01/08/2025
DESPUÉS: fecha_inicio=01/08/2025, fecha_final=15/08/2025
```

---

## 2. Errores de Códigos CIE10

### ❌ Error: Formato Incompleto
```
Campo: diagnostico_principal
Error: El campo 'diagnostico_principal' no cumple con el formato CIE10 válido.
       Valor: 'A00'. Formato esperado: Letra + 2 dígitos + opcional(dígito/X)
```

**Corrección:**
```
ANTES: A00
DESPUÉS: A001  (código CIE10 completo de 4 caracteres)
```

### ❌ Error: Código Inválido
```
Campo: diagnostico_relacionado1
Error: Formato CIE10 no válido. Valor: 'ABC123'
```

**Corrección:**
```
ANTES: ABC123
DESPUÉS: A001  (o el código CIE10 correcto)

Formato válido:
- A001 (letra + 3 dígitos)
- I10X (letra + 2 dígitos + X)
- Z000 (letra + 3 dígitos)
```

---

## 3. Errores de Códigos CUPS

### ❌ Error: Longitud Incorrecta
```
Campo: cod_consulta
Error: El campo 'cod_consulta' debe ser un código CUPS de 6 dígitos.
       Valor: '8902'
```

**Corrección:**
```
ANTES: 8902
DESPUÉS: 890201  (código CUPS completo de 6 dígitos)
```

### ❌ Error: No Numérico
```
Campo: cod_procedimiento
Error: Código CUPS debe ser de 6 dígitos. Valor: 'ABC123'
```

**Corrección:**
```
ANTES: ABC123
DESPUÉS: 890301  (código CUPS numérico válido)
```

---

## 4. Errores de Tipo de Documento

### ❌ Error: Tipo No Permitido
```
Campo: tipo_documento
Error: El campo 'tipo_documento' contiene un tipo inválido: 'DN'.
       Valores permitidos: CC, TI, RC, CE, PA, MS, AS, CD, SC, PE, PT, NI
```

**Corrección:**
```
ANTES: DN
DESPUÉS: CC  (o el tipo correcto: TI, RC, CE, etc.)

Tipos válidos:
- CC: Cédula de Ciudadanía
- TI: Tarjeta de Identidad
- RC: Registro Civil
- CE: Cédula de Extranjería
- PA: Pasaporte
- MS: Menor Sin Identificación
- AS: Adulto Sin Identificación
```

---

## 5. Errores de Campos Obligatorios

### ❌ Error: Campo Vacío
```
Campo: primer_apellido
Error: El campo 'primer_apellido' es obligatorio y no puede estar vacío
```

**Corrección:**
```
ANTES: CC,1005655572,EPSS34,2,,CORREDOR,JENNIFER,YERALDY,...
                                  ↑ vacío
DESPUÉS: CC,1005655572,EPSS34,2,SOLANO,CORREDOR,JENNIFER,YERALDY,...
```

---

## 6. Errores de Valores Numéricos

### ❌ Error: Edad Fuera de Rango
```
Campo: edad
Error: El campo 'edad' debe ser entre 0 y 150. Valor: 200
```

**Corrección:**
```
ANTES: 200
DESPUÉS: 20  (o la edad correcta)
```

### ❌ Error: Valor Negativo
```
Campo: valor_consulta
Error: El campo 'valor_consulta' debe ser >= 0. Valor: -50000
```

**Corrección:**
```
ANTES: -50000.00
DESPUÉS: 50000.00
```

### ❌ Error: No Numérico
```
Campo: valor_neto
Error: El campo 'valor_neto' debe ser un número decimal.
       Valor recibido: 'N/A'
```

**Corrección:**
```
ANTES: N/A
DESPUÉS: 0.00  (o el valor numérico correcto)
```

---

## 7. Errores de Catálogos

### ❌ Error: Sexo Inválido
```
Campo: sexo
Error: El campo 'sexo' debe ser 'M' o 'F'. Valor recibido: 'X'
```

**Corrección:**
```
ANTES: X
DESPUÉS: F  (o M según corresponda)
```

### ❌ Error: Unidad de Edad Incorrecta
```
Campo: unidad_medida_edad
Error: El campo debe ser '1' (años), '2' (meses) o '3' (días).
       Valor: '0'
```

**Corrección:**
```
ANTES: 0
DESPUÉS: 1  (1=años, 2=meses, 3=días)
```

### ❌ Error: Zona Residencial Inválida
```
Campo: zona_residencial
Error: El campo debe ser 'U' (Urbana) o 'R' (Rural). Valor: 'S'
```

**Corrección:**
```
ANTES: S
DESPUÉS: U  (U=Urbana, R=Rural)
```

---

## 8. Errores de Validación Cruzada

### ❌ Error: Factura No Encontrada
```
Archivo: AC029785.txt, Línea 150
Campo: num_factura
Error: La factura '110129786' no existe en el archivo AF
```

**Corrección:**
1. Verificar que la factura existe en AF029785.txt
2. Si no existe, agregar la factura al archivo AF
3. Si el número está mal, corregirlo en AC

```
Verificar en AF029785.txt:
501100063411,ESE...,NI,822006595,110129785,31/08/2025,...
                                   ↑ este es el número correcto

Corregir en AC029785.txt:
ANTES: 110129786,501100063411,CC,1118166965,...
DESPUÉS: 110129785,501100063411,CC,1118166965,...
```

### ❌ Error: Usuario No Encontrado
```
Archivo: AC029785.txt, Línea 75
Campo: tipo_documento/num_documento
Error: El usuario CC 1234567890 no existe en el archivo US
```

**Corrección:**
1. Verificar que el usuario existe en US029785.txt
2. Si no existe, agregarlo al archivo US
3. Si el documento está mal, corregirlo en AC

```
Agregar a US029785.txt:
CC,1234567890,EPSS34,2,LOPEZ,GARCIA,JUAN,CARLOS,35,1,M,50,110,U,1234567890
```

---

## 9. Errores de Longitud de Campos

### ❌ Error: Campo Muy Largo
```
Campo: nombre_prestador
Error: El campo excede la longitud máxima de 60 caracteres.
       Longitud actual: 75
```

**Corrección:**
```
ANTES: ESE DEPARTAMENTAL SOLUCION SALUD Y BIENESTAR INTEGRAL PARA LA COMUNIDAD
       (75 caracteres)
DESPUÉS: ESE DEPARTAMENTAL SOLUCION SALUD Y BIENESTAR INTEGRAL
         (55 caracteres - abreviado)
```

---

## 10. Errores de Estructura

### ❌ Error: Número de Campos Incorrecto
```
Línea 25: Se esperaban 15 campos, se encontraron 14
```

**Corrección:**
Verificar que todos los campos estén presentes:

```
ANTES (14 campos):
CC,1005655572,EPSS34,2,SOLANO,CORREDOR,JENNIFER,YERALDY,26,1,F,50,110,U

DESPUÉS (15 campos):
CC,1005655572,EPSS34,2,SOLANO,CORREDOR,JENNIFER,YERALDY,26,1,F,50,110,U,1005655572
                                                                           ↑ campo faltante
```

---

## 11. Errores de Duplicados

### ❌ Error: Factura Duplicada
```
Archivo: AF (archivo)
Campo: num_factura
Error: La factura '110129785' aparece 2 veces en el archivo AF (duplicado)
```

**Corrección:**
Eliminar el registro duplicado en AF029785.txt

---

## Consejos para Evitar Errores

### ✅ Formato de Fechas
- Siempre usar: DD/MM/YYYY
- Ejemplo: 01/08/2025
- Verificar día (01-31), mes (01-12), año (4 dígitos)

### ✅ Códigos
- CIE10: Letra + 2-4 caracteres (A001, Z000, I10X)
- CUPS: 6 dígitos exactos (890201, 890301)

### ✅ Campos Numéricos
- No usar texto en campos numéricos
- No usar valores negativos donde no corresponde
- Usar punto decimal (.) para decimales: 50000.00

### ✅ Campos Obligatorios
- Nunca dejar vacíos campos obligatorios
- Si no tiene dato, consultar normativa sobre valores por defecto

### ✅ Consistencia
- Verificar que facturas en AC/AP/AT existan en AF
- Verificar que usuarios en AC/AP/AT existan en US
- No duplicar registros clave

---

## Herramientas de Ayuda

### Para revisar duplicados en Excel:
1. Abrir archivo en Excel
2. Seleccionar columna de facturas/usuarios
3. Usar: Datos → Quitar duplicados

### Para corrección masiva de fechas:
1. Usar Buscar y Reemplazar en editor de texto
2. Patrón: YYYY-MM-DD → DD/MM/YYYY

### Para validar códigos:
- CIE10: Consultar [https://ais.paho.org/classifications/chapters/](https://ais.paho.org/classifications/chapters/)
- CUPS: Consultar manual CUPS vigente

---

**Recuerde**: Después de corregir, vuelva a ejecutar `python main.py` para validar los cambios.
