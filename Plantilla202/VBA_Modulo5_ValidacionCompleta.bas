Attribute VB_Name = "Modulo5_ValidacionCompleta"
'═══════════════════════════════════════════════════════════════════════════════
' MÓDULO 5: VALIDACIÓN COMPLETA
' Funciones para validar toda la base de datos y generar reportes
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: ValidarTodoElDocumento
' Descripción: Valida todos los registros del documento
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub ValidarTodoElDocumento()
    On Error GoTo ErrorHandler

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    If ws Is Nothing Then
        MsgBox "No se encontró la hoja de datos: " & HOJA_DATOS, vbCritical
        Exit Sub
    End If

    ' Confirmar acción
    Dim respuesta As VbMsgBoxResult
    respuesta = MsgBox("Se validará todo el documento." & vbCrLf & vbCrLf & _
                       "Esto puede tomar varios minutos dependiendo de la cantidad de registros." & vbCrLf & vbCrLf & _
                       "¿Desea continuar?", vbYesNo + vbQuestion, "Validación Completa")

    If respuesta = vbNo Then Exit Sub

    ' Configurar aplicación
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False

    ' Limpiar log anterior
    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)
    If Not wsLog Is Nothing Then
        If wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row > 1 Then
            wsLog.Rows("2:" & wsLog.Rows.Count).Delete
        End If
    End If

    ' Encontrar última fila con datos
    Dim ultimaFila As Long
    ultimaFila = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Dim totalRegistros As Long
    totalRegistros = ultimaFila - FILA_INICIO_DATOS + 1

    If totalRegistros <= 0 Then
        MsgBox "No hay registros para validar.", vbInformation
        GoTo Finalizar
    End If

    ' Barra de progreso (usando barra de estado)
    Dim fila As Long
    Dim erroresEncontrados As Long
    erroresEncontrados = 0

    ' Recorrer cada fila
    For fila = FILA_INICIO_DATOS To ultimaFila
        ' Actualizar barra de progreso
        Application.StatusBar = "Validando registro " & (fila - FILA_INICIO_DATOS + 1) & " de " & totalRegistros & "..."

        ' Validar la fila completa
        Call ValidarFilaCompleta(fila, erroresEncontrados)
    Next fila

Finalizar:
    ' Restaurar configuración
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    Application.StatusBar = False

    ' Mostrar resumen
    Call MostrarResumenValidacion(totalRegistros, erroresEncontrados)

    Exit Sub

ErrorHandler:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    Application.StatusBar = False

    MsgBox "Error durante la validación: " & Err.Description, vbCritical, "Error"
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: ValidarFilaCompleta
' Descripción: Valida todos los campos de una fila específica
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub ValidarFilaCompleta(fila As Long, ByRef erroresEncontrados As Long)
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    Dim tipoDoc As String, numDoc As String, sexo As String
    Dim fechaNac As Variant, fechaConsulta As Variant
    Dim mensajeError As String

    ' ───────────────────────────────────────────────────────────────────────────
    ' 1. VALIDAR TIPO DE DOCUMENTO
    ' ───────────────────────────────────────────────────────────────────────────
    tipoDoc = UCase(Trim(ws.Cells(fila, COL_TIPO_DOC).Value))
    If Not ValidarCampoObligatorio(tipoDoc) Then
        Call RegistrarErrorValidacion(ws, fila, COL_TIPO_DOC, "Campo obligatorio vacío", tipoDoc, "RC, TI, CC, etc.")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarTipoDocumento(tipoDoc) Then
        Call RegistrarErrorValidacion(ws, fila, COL_TIPO_DOC, ObtenerMensajeError("TIPO_DOC_INVALIDO"), tipoDoc, "RC, TI, CC, CE, PA, MS, AS, CD, PE, CN")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 2. VALIDAR NÚMERO DE DOCUMENTO
    ' ───────────────────────────────────────────────────────────────────────────
    numDoc = Trim(ws.Cells(fila, 2).Value) ' COL_NUM_DOC
    If Not ValidarCampoObligatorio(numDoc) Then
        Call RegistrarErrorValidacion(ws, fila, 2, "Campo obligatorio vacío", numDoc, "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf tipoDoc <> "" Then
        If Not ValidarLongitudDocumento(tipoDoc, numDoc) Then
            Call RegistrarErrorValidacion(ws, fila, 2, ObtenerMensajeError("LONGITUD_DOC", tipoDoc), numDoc, "")
            erroresEncontrados = erroresEncontrados + 1
        End If
        If Not ValidarDocumentoNumerico(tipoDoc, numDoc) Then
            Call RegistrarErrorValidacion(ws, fila, 2, ObtenerMensajeError("DOC_NO_NUMERICO", tipoDoc), numDoc, "Solo números")
            erroresEncontrados = erroresEncontrados + 1
        End If
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 3. VALIDAR NOMBRES Y APELLIDOS
    ' ───────────────────────────────────────────────────────────────────────────
    Dim primerApellido As String, primerNombre As String
    primerApellido = Trim(ws.Cells(fila, COL_PRIMER_APELLIDO).Value)
    primerNombre = Trim(ws.Cells(fila, COL_PRIMER_NOMBRE).Value)

    If Not ValidarCampoObligatorio(primerApellido) Then
        Call RegistrarErrorValidacion(ws, fila, COL_PRIMER_APELLIDO, "Primer apellido es obligatorio", primerApellido, "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarNombre(primerApellido) Then
        Call RegistrarErrorValidacion(ws, fila, COL_PRIMER_APELLIDO, ObtenerMensajeError("NOMBRE_INVALIDO"), primerApellido, "")
        erroresEncontrados = erroresEncontrados + 1
    End If

    If Not ValidarCampoObligatorio(primerNombre) Then
        Call RegistrarErrorValidacion(ws, fila, COL_PRIMER_NOMBRE, "Primer nombre es obligatorio", primerNombre, "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarNombre(primerNombre) Then
        Call RegistrarErrorValidacion(ws, fila, COL_PRIMER_NOMBRE, ObtenerMensajeError("NOMBRE_INVALIDO"), primerNombre, "")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 4. VALIDAR FECHA DE NACIMIENTO
    ' ───────────────────────────────────────────────────────────────────────────
    fechaNac = ws.Cells(fila, COL_FECHA_NACIMIENTO).Value
    If Not ValidarCampoObligatorio(fechaNac) Then
        Call RegistrarErrorValidacion(ws, fila, COL_FECHA_NACIMIENTO, "Fecha de nacimiento es obligatoria", CStr(fechaNac), "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarFechaNacimiento(fechaNac) Then
        Call RegistrarErrorValidacion(ws, fila, COL_FECHA_NACIMIENTO, ObtenerMensajeError("FECHA_NAC_INVALIDA"), CStr(fechaNac), "")
        erroresEncontrados = erroresEncontrados + 1
    Else
        ' Validar coherencia edad vs tipo documento
        mensajeError = ValidarEdadVsTipoDocumento(fila)
        If mensajeError <> "" Then
            Call RegistrarErrorValidacion(ws, fila, COL_TIPO_DOC, mensajeError, tipoDoc, SugerirTipoDocumento(fechaNac))
            erroresEncontrados = erroresEncontrados + 1
        End If
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 5. VALIDAR SEXO
    ' ───────────────────────────────────────────────────────────────────────────
    sexo = UCase(Trim(ws.Cells(fila, COL_SEXO).Value))
    If Not ValidarCampoObligatorio(sexo) Then
        Call RegistrarErrorValidacion(ws, fila, COL_SEXO, "Sexo es obligatorio", sexo, "M, F o I")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarSexo(sexo) Then
        Call RegistrarErrorValidacion(ws, fila, COL_SEXO, ObtenerMensajeError("SEXO_INVALIDO"), sexo, "M, F o I")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 6. VALIDAR FECHA DE CONSULTA
    ' ───────────────────────────────────────────────────────────────────────────
    fechaConsulta = ws.Cells(fila, COL_FECHA_CONSULTA).Value
    If Not ValidarCampoObligatorio(fechaConsulta) Then
        Call RegistrarErrorValidacion(ws, fila, COL_FECHA_CONSULTA, "Fecha de consulta es obligatoria", CStr(fechaConsulta), "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarFecha(fechaConsulta) Then
        Call RegistrarErrorValidacion(ws, fila, COL_FECHA_CONSULTA, ObtenerMensajeError("FECHA_INVALIDA"), CStr(fechaConsulta), "")
        erroresEncontrados = erroresEncontrados + 1
    ElseIf Not ValidarFechaConsultaVsNacimiento(fila) Then
        Call RegistrarErrorValidacion(ws, fila, COL_FECHA_CONSULTA, "Fecha de consulta anterior a nacimiento", CStr(fechaConsulta), "")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 7. VALIDAR COHERENCIA SEXO - GESTACIÓN
    ' ───────────────────────────────────────────────────────────────────────────
    If Not ValidarCoherenciaSexoGestacion(fila) Then
        Call RegistrarErrorValidacion(ws, fila, COL_GESTACION, "Incoherencia: sexo masculino no puede tener gestación", _
                                      ws.Cells(fila, COL_GESTACION).Value, "0")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 8. VALIDAR COHERENCIA GESTACIÓN - EDAD GESTACIONAL
    ' ───────────────────────────────────────────────────────────────────────────
    If Not ValidarCoherenciaGestacionEdadGestacional(fila) Then
        Call RegistrarErrorValidacion(ws, fila, COL_EDAD_GESTACIONAL, "Incoherencia entre gestación y edad gestacional", _
                                      ws.Cells(fila, COL_EDAD_GESTACIONAL).Value, "")
        erroresEncontrados = erroresEncontrados + 1
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 9. VALIDAR EDAD GESTACIONAL (SI APLICA)
    ' ───────────────────────────────────────────────────────────────────────────
    Dim edadGest As String
    edadGest = Trim(ws.Cells(fila, COL_EDAD_GESTACIONAL).Value)
    If edadGest <> "" And edadGest <> "0" Then
        If Not ValidarEdadGestacional(edadGest) Then
            Call RegistrarErrorValidacion(ws, fila, COL_EDAD_GESTACIONAL, ObtenerMensajeError("EDAD_GESTACIONAL"), edadGest, "0-42")
            erroresEncontrados = erroresEncontrados + 1
        End If
    End If

    ' ───────────────────────────────────────────────────────────────────────────
    ' 10. VALIDAR RÉGIMEN
    ' ───────────────────────────────────────────────────────────────────────────
    Dim regimen As String
    regimen = Trim(ws.Cells(fila, COL_REGIMEN).Value)
    If regimen <> "" Then
        If Not ValidarRegimen(regimen) Then
            Call RegistrarErrorValidacion(ws, fila, COL_REGIMEN, ObtenerMensajeError("REGIMEN_INVALIDO"), regimen, "C, S, E o N")
            erroresEncontrados = erroresEncontrados + 1
        End If
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: RegistrarErrorValidacion
' Descripción: Registra un error encontrado y marca visualmente la celda
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub RegistrarErrorValidacion(ws As Worksheet, fila As Long, columna As Integer, _
                                     mensajeError As String, valorIngresado As String, valorEsperado As String)
    ' Marcar celda con error
    ws.Cells(fila, columna).Interior.Color = COLOR_ERROR

    ' Agregar o actualizar comentario
    On Error Resume Next
    ws.Cells(fila, columna).Comment.Delete
    On Error GoTo 0
    ws.Cells(fila, columna).AddComment mensajeError

    ' Registrar en log
    Call RegistrarError(fila, columna, ObtenerNombreColumna(columna), mensajeError, valorIngresado, valorEsperado)
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: MostrarResumenValidacion
' Descripción: Muestra un resumen de la validación completa
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub MostrarResumenValidacion(totalRegistros As Long, erroresEncontrados As Long)
    Dim mensaje As String

    mensaje = "═══════════════════════════════════════" & vbCrLf
    mensaje = mensaje & "  VALIDACIÓN COMPLETA FINALIZADA" & vbCrLf
    mensaje = mensaje & "  Resolución 202 de 2021" & vbCrLf
    mensaje = mensaje & "═══════════════════════════════════════" & vbCrLf & vbCrLf

    mensaje = mensaje & "Total de registros validados: " & totalRegistros & vbCrLf
    mensaje = mensaje & "Errores encontrados: " & erroresEncontrados & vbCrLf & vbCrLf

    If erroresEncontrados = 0 Then
        mensaje = mensaje & "Estado: ✓ VALIDACIÓN EXITOSA" & vbCrLf
        mensaje = mensaje & vbCrLf & "Todos los datos cumplen con la normativa."
        MsgBox mensaje, vbInformation, "Validación Exitosa"
    Else
        mensaje = mensaje & "Estado: ✗ SE ENCONTRARON ERRORES" & vbCrLf & vbCrLf
        mensaje = mensaje & "Las celdas con error están marcadas en rojo." & vbCrLf
        mensaje = mensaje & "Revise la hoja '" & HOJA_LOG & "' para ver el detalle."

        MsgBox mensaje, vbExclamation, "Errores Encontrados"

        ' Mostrar la hoja de log
        Dim wsLog As Worksheet
        Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)
        wsLog.Visible = xlSheetVisible
        wsLog.Activate
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: LimpiarTodasLasValidaciones
' Descripción: Limpia todas las validaciones y reinicia el sistema
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub LimpiarTodasLasValidaciones()
    Dim respuesta As VbMsgBoxResult
    respuesta = MsgBox("¿Está seguro de que desea limpiar todas las validaciones?" & vbCrLf & vbCrLf & _
                       "Esto eliminará:" & vbCrLf & _
                       "- Marcas visuales de error" & vbCrLf & _
                       "- Comentarios en celdas" & vbCrLf & _
                       "- Registro de errores en log", _
                       vbYesNo + vbExclamation, "Confirmar Limpieza")

    If respuesta = vbYes Then
        Call LimpiarMarcasErrores
        Call LimpiarLog

        MsgBox "Sistema de validación reiniciado correctamente.", vbInformation
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: GenerarReporteValidacion
' Descripción: Genera un reporte detallado de la validación
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub GenerarReporteValidacion()
    On Error GoTo ErrorHandler

    Dim wsReporte As Worksheet
    Set wsReporte = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    wsReporte.Name = "REPORTE_VALIDACION_" & Format(Now, "yyyymmdd")

    With wsReporte
        ' Encabezado del reporte
        .Cells(1, 1).Value = "REPORTE DE VALIDACIÓN"
        .Cells(1, 1).Font.Size = 16
        .Cells(1, 1).Font.Bold = True

        .Cells(2, 1).Value = "Resolución 202 de 2021 - Ministerio de Salud y Protección Social"
        .Cells(3, 1).Value = "Fecha de generación: " & Format(Now, "dd/mm/yyyy hh:mm:ss")

        ' Estadísticas generales
        .Cells(5, 1).Value = "ESTADÍSTICAS GENERALES"
        .Cells(5, 1).Font.Bold = True

        Dim ws As Worksheet
        Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)
        Dim totalRegistros As Long
        totalRegistros = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row - FILA_INICIO_DATOS + 1

        .Cells(6, 1).Value = "Total de registros:"
        .Cells(6, 2).Value = totalRegistros

        .Cells(7, 1).Value = "Total de errores:"
        .Cells(7, 2).Value = ContarErrores()

        ' Copiar tabla de errores desde LOG
        .Cells(10, 1).Value = "DETALLE DE ERRORES"
        .Cells(10, 1).Font.Bold = True

        Dim wsLog As Worksheet
        Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

        If Not wsLog Is Nothing Then
            Dim ultimaFilaLog As Long
            ultimaFilaLog = wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row

            If ultimaFilaLog > 1 Then
                wsLog.Range("A1:G" & ultimaFilaLog).Copy .Cells(11, 1)
            End If
        End If

        ' Formato
        .Columns("A:G").AutoFit
    End With

    MsgBox "Reporte generado exitosamente en la hoja: " & wsReporte.Name, vbInformation

    Exit Sub

ErrorHandler:
    MsgBox "Error al generar el reporte: " & Err.Description, vbCritical
End Sub
