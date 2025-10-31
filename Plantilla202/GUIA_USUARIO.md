# Guía Rápida de Usuario
## Sistema de Validación Automática - Resolución 202 de 2021

---

## 🚀 Inicio Rápido

### 1. Abrir el Archivo

1. Abra el archivo **"Plantilla_Resolucion_202.xlsm"**
2. Cuando aparezca la advertencia de seguridad, haga clic en **"Habilitar contenido"**
3. Aparecerá un mensaje de bienvenida
4. Haga clic en **"Sí"** para abrir el Panel de Control

### 2. Panel de Control

El Panel de Control es su centro de operaciones:

![Panel de Control]

**Botones principales:**
- **Validar Todo:** Revisa todos los datos
- **Ver Log:** Muestra errores encontrados
- **Siguiente Error:** Salta al siguiente error
- **Limpiar:** Elimina marcas de error

---

## ✏️ Ingreso de Datos

### Campos Obligatorios (Marcados con *)

1. **Tipo de Documento*** → Seleccione de la lista: RC, TI, CC, CE, PA, MS, AS, CD, PE, CN
2. **Número de Documento*** → Ingrese el número sin puntos ni guiones
3. **Primer Apellido*** → Solo letras, sin números
4. **Primer Nombre*** → Solo letras, sin números
5. **Fecha de Nacimiento*** → Formato: DD/MM/AAAA
6. **Sexo*** → Seleccione: M (Masculino), F (Femenino) o I (Indeterminado)
7. **Fecha de Consulta*** → Formato: DD/MM/AAAA

### Campos Opcionales

- **Segundo Apellido** → Puede dejarse vacío
- **Segundo Nombre** → Puede dejarse vacío
- **Otros campos** → Complete según aplique

---

## 🎨 Códigos de Color

Mientras ingresa datos, las celdas cambiarán de color:

| Color | Significado | ¿Qué hacer? |
|-------|-------------|-------------|
| ⚪ **Blanco** | Dato correcto | Continuar |
| 🟡 **Amarillo** | Advertencia | Revisar el dato (puede ser correcto) |
| 🔴 **Rojo** | Error | Corregir inmediatamente |

### Ver el Error

Coloque el cursor sobre una celda roja para ver el mensaje de error:

```
💬 "Tipo de documento inválido. Use: RC, TI, CC, CE, PA..."
```

---

## 🤖 Funciones Automáticas

El sistema completa algunos campos automáticamente:

### 1. Si marca Sexo = "M" (Masculino)

✅ **El sistema automáticamente completa:**
- Gestación → 0 (No aplica)
- Edad Gestacional → 0 (No aplica)
- Control Prenatal → 0 (No aplica)
- Citología → 0 (No aplica)
- Mamografía → 0 (No aplica)

**¡No necesita llenar estos campos manualmente!**

### 2. Si marca Gestación = "No" o "0"

✅ **El sistema automáticamente completa:**
- Edad Gestacional → 0
- Control Prenatal → 0

### 3. Al ingresar Fecha de Nacimiento

✅ **El sistema sugiere el tipo de documento correcto:**

| Edad | Documento Sugerido |
|------|-------------------|
| 0-6 años | RC (Registro Civil) |
| 7-17 años | TI (Tarjeta de Identidad) |
| 18+ años | CC (Cédula de Ciudadanía) |

---

## 📋 Ejemplos Prácticos

### Ejemplo 1: Paciente Masculino Adulto

```
Tipo de Documento: CC
Número: 12345678
Primer Apellido: GARCIA
Segundo Apellido: LOPEZ
Primer Nombre: JUAN
Segundo Nombre: CARLOS
Fecha de Nacimiento: 15/03/1985
Sexo: M  ← Al seleccionar M...
Gestación: 0  ← Se completa automáticamente
Edad Gestacional: 0  ← Se completa automáticamente
```

### Ejemplo 2: Paciente Femenino Gestante

```
Tipo de Documento: CC
Número: 87654321
Primer Apellido: MARTINEZ
Primer Nombre: MARIA
Fecha de Nacimiento: 20/07/1995
Sexo: F
Gestación: 1  ← Sí está gestante
Edad Gestacional: 28  ← Debe llenar (0-42 semanas)
Control Prenatal: 1  ← Debe llenar
```

### Ejemplo 3: Menor con TI

```
Tipo de Documento: TI
Número: 1234567890
Primer Apellido: RAMIREZ
Primer Nombre: SOFIA
Fecha de Nacimiento: 10/05/2012  ← 13 años
Sexo: F
```

**Si ingresa CC en lugar de TI:**
🟡 Advertencia: "CC solo aplica para mayores de 18 años. Edad: 13"
✅ Sugerencia: "Tipo de documento sugerido: TI"

---

## 🔍 Validar los Datos

### Validación Manual (Una por una)

El sistema valida automáticamente cada celda cuando la modifica.
**No necesita hacer nada especial.**

### Validación Completa (Todo el documento)

**Paso 1:** Haga clic en el menú **"VALIDACIÓN 202"**

**Paso 2:** Seleccione **"Validar Todo el Documento"**

**Paso 3:** Espere mientras el sistema revisa (aparece una barra de progreso)

**Paso 4:** Revise el resumen:

```
═══════════════════════════════════════
  VALIDACIÓN COMPLETA FINALIZADA
  Resolución 202 de 2021
═══════════════════════════════════════

Total de registros validados: 150
Errores encontrados: 8

Estado: ✗ SE ENCONTRARON ERRORES

Las celdas con error están marcadas en rojo.
Revise la hoja 'LOG_ERRORES' para ver el detalle.
```

---

## 📊 Ver y Corregir Errores

### Opción 1: Navegar con "Siguiente Error"

1. Menú **"VALIDACIÓN 202"** → **"Ir a Siguiente Error"**
2. El sistema salta a la primera celda con error
3. Vea el mensaje de error en el comentario
4. Corrija el dato
5. Repita para el siguiente error

### Opción 2: Ver el Log de Errores

1. Menú **"VALIDACIÓN 202"** → **"Ver Log de Errores"**
2. Se abrirá una hoja con todos los errores:

| FECHA/HORA | FILA | COLUMNA | CAMPO | ERROR | VALOR INGRESADO | VALOR ESPERADO |
|------------|------|---------|-------|-------|-----------------|----------------|
| 15/10/2025 10:30 | 5 | 1 | Tipo de Documento | Tipo inválido | XX | RC, TI, CC... |
| 15/10/2025 10:31 | 8 | 8 | Sexo | Sexo inválido | K | M, F o I |

3. Vaya a la fila indicada y corrija el error
4. Valide nuevamente

---

## ⚠️ Errores Comunes

### ❌ "Tipo de documento inválido"

**Causa:** Ingresó un código que no existe

**Solución:** Use solo estos códigos:
- RC, TI, CC, CE, PA, MS, AS, CD, PE, CN

**Ejemplo:** Cambiar "CI" por "CC"

---

### ❌ "Longitud de documento incorrecta para tipo XX"

**Causa:** El número de documento tiene muy pocos o muchos dígitos

**Solución:** Revise la tabla:

| Tipo | Longitud Permitida |
|------|-------------------|
| RC | 10-11 dígitos |
| TI | 10-11 dígitos |
| CC | 6-10 dígitos |
| CE | 6-10 caracteres |
| PA | 6-20 caracteres |

**Ejemplo:** CC debe tener entre 6 y 10 dígitos, no 5 ni 11

---

### ❌ "El documento debe contener solo números"

**Causa:** Ingresó letras en un documento que debe ser numérico

**Solución:** Tipos que deben ser SOLO números:
- RC, TI, CC, CN

**Ejemplo:** Cambiar "123ABC" por "123456"

---

### ❌ "Sexo inválido"

**Causa:** Ingresó un valor diferente a M, F o I

**Solución:** Use solo:
- **M** = Masculino
- **F** = Femenino
- **I** = Indeterminado

**Ejemplo:** Cambiar "H" o "MASCULINO" por "M"

---

### ❌ "Nombre contiene caracteres no permitidos"

**Causa:** Ingresó números o símbolos en el nombre

**Solución:** Use solo letras (se permiten tildes y ñ)

**Permitido:** MARÍA, JOSÉ, NUÑEZ
**No permitido:** JUAN123, MARIA@, LOPEZ-2

---

### ❌ "Fecha de nacimiento inválida"

**Causa:** Fecha futura o muy antigua

**Solución:**
- No use fechas futuras
- No use fechas de más de 150 años atrás
- Use formato DD/MM/AAAA

**Ejemplo:** 15/03/2026 → cambiar por 15/03/1986

---

### ❌ "Incoherencia: sexo masculino no puede tener gestación"

**Causa:** Marcó Sexo = M pero Gestación = Sí

**Solución:**
- Si es hombre: El sistema autocompleta Gestación = 0
- Si está gestante: Cambie Sexo a F

---

### ❌ "Edad gestacional debe estar entre 0 y 42 semanas"

**Causa:** Ingresó un número fuera del rango

**Solución:** Ingrese un valor entre 0 y 42

**Ejemplo:** Cambiar "50" por "38"

---

### ❌ "RC solo aplica para menores de 7 años. Edad: XX"

**Causa:** Usó Registro Civil para una persona mayor de 7 años

**Solución:** Use el documento correcto según la edad:

| Edad | Documento Correcto |
|------|--------------------|
| 0-6 años | RC |
| 7-17 años | TI |
| 18+ años | CC |

**Ejemplo:** Para 15 años, cambiar RC por TI

---

## 🧹 Limpiar y Reiniciar

### Limpiar Solo las Marcas de Error

1. Menú **"VALIDACIÓN 202"** → **"Limpiar Todas las Validaciones"**
2. Confirme la acción
3. Los datos permanecen, solo se eliminan los colores y comentarios

### Limpiar el Log de Errores

1. Panel de Control → **"Limpiar Log"**
2. Confirme la acción
3. Se eliminan todos los registros de errores

**Nota:** Los datos en la hoja principal NO se eliminan

---

## 📁 Guardar y Exportar

### Guardar el Archivo

**Siempre use:**
```
Archivo → Guardar Como → Tipo: "Libro de Excel habilitado para macros (*.xlsm)"
```

**❌ No guarde como .xlsx** → Perderá las macros

### Exportar el Log de Errores

1. Menú **"VALIDACIÓN 202"** → **"Exportar Log a CSV"**
2. Se creará un archivo CSV en la misma carpeta
3. Nombre: `LOG_ERRORES_20251015_103045.csv`
4. Puede abrirlo con Excel o importarlo a otros sistemas

### Generar Reporte

1. Menú **"VALIDACIÓN 202"** → **"Generar Reporte"**
2. Se creará una nueva hoja con:
   - Estadísticas generales
   - Detalle de todos los errores
   - Fecha y hora del reporte

---

## ⚡ Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| `Alt + F11` | Abrir editor VBA (administradores) |
| `Ctrl + S` | Guardar archivo |
| `F5` | Ir a celda específica |
| `Ctrl + Inicio` | Ir al inicio de la hoja |
| `Ctrl + Fin` | Ir al final de los datos |

---

## 🆘 Preguntas Frecuentes

### ¿Puedo desactivar la validación automática?

**Sí:**
1. Abra el Panel de Control
2. Desmarque "Activar validación en tiempo real"
3. Ahora puede ingresar datos sin validación automática
4. Use "Validar Todo" cuando termine

### ¿Qué hago si el sistema está muy lento?

**Solución:**
1. Desactive la validación en tiempo real
2. Ingrese todos los datos
3. Al final, use "Validar Todo el Documento"

### ¿Puedo copiar y pegar datos?

**Sí, pero:**
1. La validación se ejecutará para cada celda pegada
2. Si pega muchos datos, puede ser lento
3. Recomendación: Desactive validación en tiempo real antes de pegar

### ¿Los datos se guardan automáticamente?

**No.** Debe guardar manualmente:
- Use `Ctrl + S` regularmente
- O Archivo → Guardar

### ¿Puedo usar este archivo en Google Sheets?

**No.** Este sistema usa macros VBA que solo funcionan en Microsoft Excel.

### ¿Qué hago si aparece un error de VBA?

1. Haga clic en "Finalizar"
2. Guarde su trabajo
3. Cierre y vuelva a abrir el archivo
4. Si persiste, contacte al administrador

---

## 📞 Ayuda Adicional

### Dentro del Sistema

Menú **"VALIDACIÓN 202"** → **"Ayuda"**

### Panel de Control

Botón **"Ayuda"** en el formulario

### Menú de Estadísticas

Menú **"VALIDACIÓN 202"** → **"Mostrar Estadísticas"**

Muestra:
- Total de registros
- Total de errores
- Porcentaje de error
- Estado general

---

## ✅ Checklist Antes de Enviar

Antes de enviar o cerrar el archivo, verifique:

- [ ] Ejecutó "Validar Todo el Documento"
- [ ] Revisó y corrigió todos los errores en rojo
- [ ] Verificó las advertencias en amarillo
- [ ] Guardó el archivo como .xlsm
- [ ] Revisó el Log de Errores
- [ ] Total de errores = 0

---

## 🎓 Mejores Prácticas

1. **Guarde frecuentemente** → Cada 10-15 minutos
2. **Valide mientras ingresa** → Corrija errores inmediatamente
3. **Use las listas desplegables** → Evita errores de digitación
4. **Revise el log periódicamente** → No espere al final
5. **Haga copias de seguridad** → Antes de hacer cambios masivos
6. **No modifique los encabezados** → Están protegidos por una razón
7. **Mantenga las macros habilitadas** → Son esenciales para el sistema

---

**Versión:** 1.0
**Para:** Usuarios finales del sistema
**Sistema:** Validación Resolución 202 de 2021 - MinSalud Colombia

---

¡Gracias por usar el Sistema de Validación Automática! 🎉
