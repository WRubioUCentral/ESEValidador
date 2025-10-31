# Manual de Implementación
## Sistema de Validación Automática - Resolución 202 de 2021

---

## 📋 Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Instalación Paso a Paso](#instalación-paso-a-paso)
4. [Configuración Inicial](#configuración-inicial)
5. [Validaciones Implementadas](#validaciones-implementadas)
6. [Uso del Sistema](#uso-del-sistema)
7. [Solución de Problemas](#solución-de-problemas)

---

## 📌 Requisitos

### Software Necesario
- Microsoft Excel 2010 o superior
- Windows 7 o superior
- Macros habilitadas en Excel

### Conocimientos Recomendados
- Uso básico de Excel
- Conocimiento de la Resolución 202 de 2021 del Ministerio de Salud

---

## 🗂️ Estructura del Proyecto

El sistema está compuesto por los siguientes módulos VBA:

```
Plantilla202/
├── VBA_Modulo1_Configuracion.bas        # Configuración y constantes
├── VBA_Modulo2_Validaciones.bas         # Funciones de validación de datos
├── VBA_Modulo3_ReglasNegocio.bas        # Reglas de negocio específicas
├── VBA_Modulo4_LogAlertas.bas           # Sistema de log y alertas
├── VBA_Modulo5_ValidacionCompleta.bas   # Validación masiva de datos
├── VBA_Hoja_DATOS_202.cls               # Eventos de la hoja de datos
├── VBA_ThisWorkbook.cls                 # Eventos del libro
├── VBA_UserForm_PanelControl.frm        # Formulario de panel de control
└── MANUAL_IMPLEMENTACION.md             # Este manual
```

---

## 🔧 Instalación Paso a Paso

### Paso 1: Crear el Archivo Excel Base

1. Abra Microsoft Excel
2. Cree un nuevo libro de trabajo
3. Guarde el archivo como **"Plantilla_Resolucion_202.xlsm"** (formato con macros)

### Paso 2: Habilitar el Editor de VBA

1. Presione `Alt + F11` para abrir el Editor de Visual Basic
2. Si no puede acceder, habilite la pestaña "Desarrollador":
   - Archivo → Opciones → Personalizar cinta de opciones
   - Active la casilla "Desarrollador"

### Paso 3: Importar los Módulos VBA

**Opción A: Importar archivos .bas directamente**

1. En el Editor de VBA, haga clic derecho en el proyecto
2. Seleccione "Importar archivo..."
3. Importe los siguientes archivos en orden:
   - `VBA_Modulo1_Configuracion.bas`
   - `VBA_Modulo2_Validaciones.bas`
   - `VBA_Modulo3_ReglasNegocio.bas`
   - `VBA_Modulo4_LogAlertas.bas`
   - `VBA_Modulo5_ValidacionCompleta.bas`

**Opción B: Copiar el código manualmente**

1. Para cada módulo:
   - En VBA, seleccione Insertar → Módulo
   - Copie el contenido del archivo .bas correspondiente
   - Pegue en el módulo creado
   - Cambie el nombre del módulo (F4) según corresponda

### Paso 4: Configurar el Código de la Hoja

1. En el Editor de VBA, haga doble clic en la hoja que contendrá los datos
2. Renombre la hoja a **"DATOS_202"** (desde Excel, no desde VBA)
3. En el código de la hoja (VBA), copie el contenido de `VBA_Hoja_DATOS_202.cls`

### Paso 5: Configurar el Código del Workbook

1. En el Editor de VBA, haga doble clic en "ThisWorkbook"
2. Copie el contenido de `VBA_ThisWorkbook.cls`

### Paso 6: Crear el UserForm

1. En VBA, seleccione Insertar → UserForm
2. Nombre el formulario como **"frmPanelControl"**
3. Diseñe el formulario con los siguientes controles:

#### Controles del Formulario

| Tipo | Nombre | Caption/Texto |
|------|--------|---------------|
| Label | lblTitulo | "Panel de Control - Validación Resolución 202" |
| Label | lblEstado | "Estado: ACTIVO" |
| Label | lblTotalRegistros | "Total de registros: 0" |
| Label | lblTotalErrores | "Total de errores: 0" |
| CheckBox | chkValidacionTiempoReal | "Activar validación en tiempo real" |
| Button | btnValidarTodo | "Validar Todo el Documento" |
| Button | btnLimpiarValidaciones | "Limpiar Validaciones" |
| Button | btnVerLog | "Ver Log de Errores" |
| Button | btnLimpiarLog | "Limpiar Log" |
| Button | btnExportarLog | "Exportar Log a CSV" |
| Button | btnSiguienteError | "Ir a Siguiente Error" |
| Button | btnGenerarReporte | "Generar Reporte" |
| Button | btnEstadisticas | "Mostrar Estadísticas" |
| Button | btnAyuda | "Ayuda" |
| Button | btnCerrar | "Cerrar" |

4. Copie el código de `VBA_UserForm_PanelControl.frm` en el código del formulario

### Paso 7: Crear la Estructura de Hojas

1. Renombre la primera hoja a **"DATOS_202"**
2. En la fila 1, agregue los encabezados de las 119 columnas según la Resolución 202:

**Columnas 1-10 (Identificación):**
- A1: Tipo de Documento
- B1: Número de Documento
- C1: Primer Apellido
- D1: Segundo Apellido
- E1: Primer Nombre
- F1: Segundo Nombre
- G1: Fecha de Nacimiento
- H1: Sexo
- I1: Departamento
- J1: Municipio

**Continúe con las 109 columnas restantes según la Resolución 202...**

3. El sistema creará automáticamente las hojas **"CONFIG"** y **"LOG_ERRORES"** al inicializarse

### Paso 8: Configurar las Listas de Validación

En la hoja DATOS_202, configure validaciones de datos para las columnas críticas:

**Columna A - Tipo de Documento:**
```
Datos → Validación de datos → Lista
Origen: RC,TI,CC,CE,PA,MS,AS,CD,PE,CN
```

**Columna H - Sexo:**
```
Datos → Validación de datos → Lista
Origen: M,F,I
```

**Columna 11 - Régimen:**
```
Datos → Validación de datos → Lista
Origen: C,S,E,N
```

### Paso 9: Proteger la Estructura

1. Seleccione la fila 1 (encabezados)
2. Haga clic derecho → Formato de celdas → Protección → Bloqueado
3. Revisar → Proteger hoja
4. Configure solo permitir:
   - ☑ Seleccionar celdas bloqueadas
   - ☑ Seleccionar celdas desbloqueadas
   - ☑ Dar formato a celdas

---

## ⚙️ Configuración Inicial

### Primera Ejecución

1. Guarde el archivo
2. Cierre y vuelva a abrir el archivo
3. Habilite las macros cuando Excel lo solicite
4. Verá un mensaje de bienvenida
5. Elija "Sí" para abrir el Panel de Control

### Verificar la Instalación

1. Verifique que aparece el menú **"VALIDACIÓN 202"** en la barra de menú
2. Verifique que existe la hoja **"LOG_ERRORES"**
3. Pruebe ingresar un dato en la columna "Sexo" con valor "M"
4. Verifique que las columnas de gestación se completan automáticamente con "0"

---

## ✅ Validaciones Implementadas

### 1. Validaciones de Tipo de Documento

| Tipo | Código | Longitud | Tipo de Dato |
|------|--------|----------|--------------|
| Registro Civil | RC | 10-11 | Numérico |
| Tarjeta de Identidad | TI | 10-11 | Numérico |
| Cédula de Ciudadanía | CC | 6-10 | Numérico |
| Cédula de Extranjería | CE | 6-10 | Alfanumérico |
| Pasaporte | PA | 6-20 | Alfanumérico |
| Menor sin ID | MS | Máx 15 | Alfanumérico |
| Adulto sin ID | AS | Máx 15 | Alfanumérico |
| Carné Diplomático | CD | 6-15 | Alfanumérico |
| Permiso Especial | PE | 6-15 | Alfanumérico |
| Certificado Nacido Vivo | CN | 10-12 | Numérico |

### 2. Coherencia Edad vs Documento

- **RC (Registro Civil):** Solo para menores de 7 años
- **TI (Tarjeta de Identidad):** Solo de 7 a 17 años
- **CC (Cédula de Ciudadanía):** Solo para mayores de 18 años
- **MS (Menor sin ID):** Solo para menores de 18 años

**Acción del sistema:** Si la edad no coincide, marca advertencia en amarillo y sugiere el tipo correcto.

### 3. Reglas de Sexo y Gestación

**Si Sexo = "M" (Masculino):**
- Gestación → Autocompletar con "0"
- Edad Gestacional → Autocompletar con "0"
- Control Prenatal → Autocompletar con "0"
- Citología → Autocompletar con "0"
- Mamografía → Autocompletar con "0"

**Si Gestación = "1" (Sí):**
- Edad Gestacional debe estar entre 1-42 semanas
- Control Prenatal debe tener valor

**Si Gestación = "0" (No):**
- Edad Gestacional debe ser "0"
- Control Prenatal debe ser "0"

### 4. Validaciones de Fechas

- **Fecha de Nacimiento:**
  - No puede ser futura
  - No puede ser anterior a 150 años
  - Debe ser fecha válida

- **Fecha de Consulta:**
  - Debe ser fecha válida
  - No puede ser anterior a la fecha de nacimiento
  - No puede ser muy futura (más de 1 año)

### 5. Validaciones de Nombres y Apellidos

- Solo letras (A-Z, a-z)
- Espacios permitidos
- Caracteres especiales permitidos: Ñ, ñ, tildes (á, é, í, ó, ú)
- Primer Apellido y Primer Nombre son **obligatorios**
- Segundo Apellido y Segundo Nombre son opcionales

### 6. Código Diagnóstico CIE-10

- Formato: Letra seguida de 2-3 dígitos
- Ejemplos válidos: A00, J44, I25.0, Z00.0
- Validación básica de formato (no verifica existencia en catálogo)

---

## 📊 Uso del Sistema

### Panel de Control

Acceso: Menú "VALIDACIÓN 202" → "Panel de Control"

**Funciones disponibles:**

1. **Validar Todo el Documento**
   - Valida todos los registros
   - Marca errores en rojo
   - Genera log detallado

2. **Limpiar Validaciones**
   - Elimina marcas visuales
   - Limpia comentarios
   - Limpia log de errores

3. **Ver Log de Errores**
   - Muestra hoja con todos los errores
   - Incluye fecha/hora, fila, columna, error

4. **Exportar Log**
   - Genera archivo CSV con errores
   - Útil para reportes externos

5. **Ir a Siguiente Error**
   - Navega automáticamente al siguiente error
   - Útil para corrección sistemática

6. **Generar Reporte**
   - Crea hoja con estadísticas completas
   - Incluye resumen y detalle de errores

### Validación en Tiempo Real

**Activación/Desactivación:**
- Desde el Panel de Control
- Checkbox "Activar validación en tiempo real"

**Comportamiento:**
- Se ejecuta al modificar cualquier celda
- Marca errores inmediatamente en rojo
- Agrega comentario con descripción del error
- Autocompleta campos cuando corresponde

### Códigos de Color

| Color | Significado | Acción Requerida |
|-------|-------------|------------------|
| 🔴 Rojo | Error crítico | Corrección obligatoria |
| 🟡 Amarillo | Advertencia | Revisar y confirmar |
| ⚪ Blanco | Correcto | Ninguna |

### Interpretación de Errores

**Mensajes comunes:**

- **"Tipo de documento inválido"**
  → Use solo: RC, TI, CC, CE, PA, MS, AS, CD, PE, CN

- **"Longitud de documento incorrecta"**
  → Verifique la cantidad de dígitos según el tipo

- **"El documento debe contener solo números"**
  → Para RC, TI, CC, CN solo use números

- **"Sexo inválido"**
  → Use solo: M, F o I

- **"Incoherencia: sexo masculino no puede tener gestación"**
  → Revise el campo de sexo o gestación

- **"Edad gestacional debe estar entre 0 y 42 semanas"**
  → Ingrese un valor válido de semanas

---

## 🛠️ Solución de Problemas

### Problema 1: Las macros no se ejecutan

**Solución:**
1. Archivo → Opciones → Centro de confianza → Configuración del Centro de confianza
2. Configuración de macros → Habilitar todas las macros
3. Reinicie Excel

### Problema 2: El menú "VALIDACIÓN 202" no aparece

**Solución:**
1. Presione Alt + F11
2. Verifique que existe el código en "ThisWorkbook"
3. Ejecute manualmente: `CrearMenuValidacion`
4. Si persiste, cierre y vuelva a abrir el archivo

### Problema 3: Las validaciones no se ejecutan automáticamente

**Solución:**
1. Abra el Panel de Control
2. Verifique que "Activar validación en tiempo real" esté marcado
3. Si no funciona, en VBA ejecute: `ValidacionActiva = True`

### Problema 4: Errores al importar los módulos

**Solución:**
1. Copie el código manualmente en lugar de importar
2. Verifique que cada módulo tenga el nombre correcto
3. Compile el código: Debug → Compilar proyecto VBA

### Problema 5: La hoja LOG_ERRORES no se crea

**Solución:**
1. En VBA, ejecute manualmente: `CrearHojaLog`
2. O use el menú: Insertar → Hoja, y nómbrela "LOG_ERRORES"
3. Ejecute: `InicializarSistema`

### Problema 6: Errores de "Variable no definida"

**Solución:**
1. Verifique que todos los módulos están importados
2. Verifique que las constantes están definidas en Modulo1_Configuracion
3. Compile el proyecto VBA para encontrar errores

---

## 📝 Personalización

### Modificar las Columnas de Validación

Edite las constantes en `Modulo1_Configuracion`:

```vba
Public Const COL_TIPO_DOC As Integer = 1
Public Const COL_NUM_DOC As String = "B"
Public Const COL_SEXO As Integer = 8
' ... etc
```

### Agregar Nuevas Validaciones

1. Cree la función de validación en `Modulo2_Validaciones`
2. Agregue la regla de negocio en `Modulo3_ReglasNegocio`
3. Integre en el evento `Worksheet_Change` de la hoja

### Cambiar Códigos "No Aplica"

Modifique las constantes en `Modulo1_Configuracion`:

```vba
Public Const CODIGO_NO_APLICA As String = "0"
Public Const CODIGO_NO_GESTANTE As String = "0"
' Cambie "0" por el código que use su institución
```

---

## 📞 Soporte

Este sistema fue desarrollado según la Resolución 202 de 2021 del Ministerio de Salud y Protección Social de Colombia.

**Documentación oficial:**
- Resolución 202 de 2021 - MinSalud

**Notas importantes:**
- Este sistema es una ayuda para la validación, no reemplaza la revisión manual
- Siempre verifique que los datos cumplan con la normativa vigente
- Realice respaldos periódicos del archivo

---

## 📄 Licencia y Uso

Este código VBA es de uso libre para instituciones de salud colombianas que deban cumplir con la Resolución 202 de 2021.

**Restricciones:**
- No modificar las validaciones que incumplan la normativa
- Mantener la integridad de los datos
- Respetar la privacidad de la información de salud

---

**Versión:** 1.0
**Fecha:** 2025
**Desarrollado para:** Sistema de Validación Resolución 202 de 2021
