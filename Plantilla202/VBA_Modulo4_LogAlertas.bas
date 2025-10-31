Attribute VB_Name = "Modulo4_LogAlertas"
'═══════════════════════════════════════════════════════════════════════════════
' MÓDULO 4: SISTEMA DE LOG Y ALERTAS
' Registro de errores y sistema de alertas visuales
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: RegistrarError
' Descripción: Registra un error en la hoja LOG_ERRORES
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub RegistrarError(fila As Long, columna As Integer, nombreCampo As String, _
                          mensajeError As String, valorIngresado As String, valorEsperado As String)

    On Error Resume Next

    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If wsLog Is Nothing Then Exit Sub

    ' Encontrar la primera fila vacía
    Dim ultimaFila As Long
    ultimaFila = wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row + 1

    ' Registrar el error
    With wsLog
        .Cells(ultimaFila, 1).Value = Now                           ' Fecha/Hora
        .Cells(ultimaFila, 2).Value = fila                          ' Fila
        .Cells(ultimaFila, 3).Value = columna                       ' Columna
        .Cells(ultimaFila, 4).Value = nombreCampo                   ' Campo
        .Cells(ultimaFila, 5).Value = mensajeError                  ' Error
        .Cells(ultimaFila, 6).Value = valorIngresado                ' Valor ingresado
        .Cells(ultimaFila, 7).Value = valorEsperado                 ' Valor esperado

        ' Formato de fila
        .Rows(ultimaFila).Interior.Color = RGB(255, 230, 230)       ' Fondo rosado claro
    End With

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: LimpiarLog
' Descripción: Limpia todos los registros del log
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub LimpiarLog()
    On Error Resume Next

    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If wsLog Is Nothing Then Exit Sub

    Dim respuesta As VbMsgBoxResult
    respuesta = MsgBox("¿Está seguro de que desea limpiar el registro de errores?", _
                       vbYesNo + vbQuestion, "Limpiar Log")

    If respuesta = vbYes Then
        ' Eliminar todas las filas excepto el encabezado
        If wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row > 1 Then
            wsLog.Rows("2:" & wsLog.Rows.Count).Delete
        End If

        MsgBox "Log de errores limpiado correctamente.", vbInformation
    End If

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ExportarLog
' Descripción: Exporta el log de errores a un archivo CSV
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub ExportarLog()
    On Error GoTo ErrorHandler

    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If wsLog Is Nothing Then
        MsgBox "No se encontró la hoja de log.", vbExclamation
        Exit Sub
    End If

    ' Verificar que haya datos
    If wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row <= 1 Then
        MsgBox "No hay errores registrados para exportar.", vbInformation
        Exit Sub
    End If

    ' Crear archivo CSV
    Dim nombreArchivo As String
    nombreArchivo = ThisWorkbook.Path & "\LOG_ERRORES_" & Format(Now, "yyyymmdd_hhmmss") & ".csv"

    ' Copiar hoja a nuevo libro
    wsLog.Copy

    ' Guardar como CSV
    ActiveWorkbook.SaveAs nombreArchivo, xlCSV
    ActiveWorkbook.Close False

    MsgBox "Log exportado exitosamente a:" & vbCrLf & nombreArchivo, vbInformation, "Exportación completada"

    Exit Sub

ErrorHandler:
    MsgBox "Error al exportar el log: " & Err.Description, vbCritical
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ContarErrores
' Descripción: Cuenta el número de errores registrados
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ContarErrores() As Long
    On Error Resume Next

    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If wsLog Is Nothing Then
        ContarErrores = 0
    Else
        ContarErrores = wsLog.Cells(wsLog.Rows.Count, 1).End(xlUp).Row - 1
    End If

    On Error GoTo 0
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: MostrarResumenErrores
' Descripción: Muestra un resumen de los errores encontrados
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub MostrarResumenErrores()
    Dim totalErrores As Long
    totalErrores = ContarErrores()

    If totalErrores = 0 Then
        MsgBox "¡Excelente! No se encontraron errores en los datos.", vbInformation, "Validación Exitosa"
    Else
        Dim mensaje As String
        mensaje = "Se encontraron " & totalErrores & " error(es) en los datos." & vbCrLf & vbCrLf
        mensaje = mensaje & "Revise la hoja '" & HOJA_LOG & "' para ver el detalle de los errores." & vbCrLf & vbCrLf
        mensaje = mensaje & "Las celdas con error están marcadas en color rojo."

        MsgBox mensaje, vbExclamation, "Errores Encontrados"

        ' Activar la hoja de log
        ThisWorkbook.Worksheets(HOJA_LOG).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(HOJA_LOG).Activate
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: LimpiarMarcasErrores
' Descripción: Limpia las marcas visuales de error en las celdas
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub LimpiarMarcasErrores()
    On Error Resume Next

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    If ws Is Nothing Then Exit Sub

    Dim respuesta As VbMsgBoxResult
    respuesta = MsgBox("¿Desea limpiar todas las marcas visuales de error en las celdas?", _
                       vbYesNo + vbQuestion, "Limpiar Marcas")

    If respuesta = vbYes Then
        Application.ScreenUpdating = False

        ' Encontrar última fila con datos
        Dim ultimaFila As Long
        ultimaFila = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

        ' Limpiar formatos de todas las celdas de datos
        Dim rango As Range
        Set rango = ws.Range(ws.Cells(FILA_INICIO_DATOS, 1), ws.Cells(ultimaFila, 119))

        rango.Interior.Color = COLOR_NORMAL
        rango.ClearComments

        Application.ScreenUpdating = True

        MsgBox "Marcas de error limpiadas correctamente.", vbInformation
    End If

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ResaltarCeldasConError
' Descripción: Resalta todas las celdas que tienen errores
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub ResaltarCeldasConError()
    On Error Resume Next

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    If ws Is Nothing Then Exit Sub

    Application.ScreenUpdating = False

    Dim ultimaFila As Long
    ultimaFila = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Dim celdasError As Long
    celdasError = 0

    ' Recorrer todas las celdas y resaltar las que tienen comentarios (errores)
    Dim fila As Long, col As Integer
    For fila = FILA_INICIO_DATOS To ultimaFila
        For col = 1 To 119
            If Not ws.Cells(fila, col).Comment Is Nothing Then
                ws.Cells(fila, col).Interior.Color = COLOR_ERROR
                celdasError = celdasError + 1
            End If
        Next col
    Next fila

    Application.ScreenUpdating = True

    MsgBox "Se resaltaron " & celdasError & " celda(s) con error.", vbInformation

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: IrASiguienteError
' Descripción: Navega a la siguiente celda con error
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub IrASiguienteError()
    On Error Resume Next

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    If ws Is Nothing Then Exit Sub

    Dim celdaActual As Range
    Set celdaActual = ActiveCell

    Dim ultimaFila As Long
    ultimaFila = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    ' Buscar siguiente celda con comentario (error)
    Dim fila As Long, col As Integer
    Dim encontrado As Boolean
    encontrado = False

    ' Buscar desde la celda actual hacia adelante
    For fila = celdaActual.Row To ultimaFila
        For col = IIf(fila = celdaActual.Row, celdaActual.Column + 1, 1) To 119
            If Not ws.Cells(fila, col).Comment Is Nothing Then
                ws.Cells(fila, col).Select
                encontrado = True
                Exit Sub
            End If
        Next col
    Next fila

    ' Si no encontró, buscar desde el inicio
    If Not encontrado Then
        For fila = FILA_INICIO_DATOS To celdaActual.Row
            For col = 1 To IIf(fila = celdaActual.Row, celdaActual.Column, 119)
                If Not ws.Cells(fila, col).Comment Is Nothing Then
                    ws.Cells(fila, col).Select
                    encontrado = True
                    Exit Sub
                End If
            Next col
        Next fila
    End If

    If Not encontrado Then
        MsgBox "No se encontraron más errores.", vbInformation
    End If

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: MostrarEstadisticasValidacion
' Descripción: Muestra estadísticas de la validación
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub MostrarEstadisticasValidacion()
    On Error Resume Next

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    If ws Is Nothing Then Exit Sub

    Dim ultimaFila As Long
    ultimaFila = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    Dim totalRegistros As Long
    totalRegistros = ultimaFila - FILA_INICIO_DATOS + 1

    Dim totalErrores As Long
    totalErrores = ContarErrores()

    Dim celdasConError As Long
    celdasConError = 0

    ' Contar celdas con error (comentarios)
    Dim fila As Long, col As Integer
    For fila = FILA_INICIO_DATOS To ultimaFila
        For col = 1 To 119
            If Not ws.Cells(fila, col).Comment Is Nothing Then
                celdasConError = celdasConError + 1
            End If
        Next col
    Next fila

    ' Mostrar estadísticas
    Dim mensaje As String
    mensaje = "═══════════════════════════════════════" & vbCrLf
    mensaje = mensaje & "  ESTADÍSTICAS DE VALIDACIÓN" & vbCrLf
    mensaje = mensaje & "  Resolución 202 de 2021" & vbCrLf
    mensaje = mensaje & "═══════════════════════════════════════" & vbCrLf & vbCrLf
    mensaje = mensaje & "Total de registros: " & totalRegistros & vbCrLf
    mensaje = mensaje & "Errores registrados en log: " & totalErrores & vbCrLf
    mensaje = mensaje & "Celdas marcadas con error: " & celdasConError & vbCrLf & vbCrLf

    If celdasConError = 0 Then
        mensaje = mensaje & "Estado: ✓ TODOS LOS DATOS VÁLIDOS"
    Else
        Dim porcentajeError As Double
        porcentajeError = (celdasConError / (totalRegistros * 119)) * 100
        mensaje = mensaje & "Porcentaje de error: " & Format(porcentajeError, "0.00") & "%" & vbCrLf
        mensaje = mensaje & "Estado: ✗ REQUIERE CORRECCIONES"
    End If

    MsgBox mensaje, vbInformation, "Estadísticas de Validación"

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: CrearHojaConfig
' Descripción: Crea la hoja de configuración con catálogos y reglas
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub CrearHojaConfig()
    On Error Resume Next

    Dim wsConfig As Worksheet
    Set wsConfig = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    wsConfig.Name = HOJA_CONFIG

    With wsConfig
        ' ─────────────────────────────────────────────────────────────────
        ' CATÁLOGO: TIPOS DE DOCUMENTO
        ' ─────────────────────────────────────────────────────────────────
        .Cells(1, 1).Value = "TIPOS_DOCUMENTO"
        .Cells(1, 1).Font.Bold = True
        .Cells(2, 1).Value = "RC"
        .Cells(3, 1).Value = "TI"
        .Cells(4, 1).Value = "CC"
        .Cells(5, 1).Value = "CE"
        .Cells(6, 1).Value = "PA"
        .Cells(7, 1).Value = "MS"
        .Cells(8, 1).Value = "AS"
        .Cells(9, 1).Value = "CD"
        .Cells(10, 1).Value = "PE"
        .Cells(11, 1).Value = "CN"

        ' ─────────────────────────────────────────────────────────────────
        ' CATÁLOGO: SEXO
        ' ─────────────────────────────────────────────────────────────────
        .Cells(1, 3).Value = "SEXO"
        .Cells(1, 3).Font.Bold = True
        .Cells(2, 3).Value = "M"
        .Cells(3, 3).Value = "F"
        .Cells(4, 3).Value = "I"

        ' ─────────────────────────────────────────────────────────────────
        ' CATÁLOGO: RÉGIMEN
        ' ─────────────────────────────────────────────────────────────────
        .Cells(1, 5).Value = "REGIMEN"
        .Cells(1, 5).Font.Bold = True
        .Cells(2, 5).Value = "C"
        .Cells(3, 5).Value = "S"
        .Cells(4, 5).Value = "E"
        .Cells(5, 5).Value = "N"

        ' ─────────────────────────────────────────────────────────────────
        ' CONFIGURACIÓN DE VALIDACIONES
        ' ─────────────────────────────────────────────────────────────────
        .Cells(15, 1).Value = "CONFIGURACIÓN DE VALIDACIONES"
        .Cells(15, 1).Font.Bold = True
        .Cells(15, 1).Font.Size = 12

        .Cells(16, 1).Value = "Parámetro"
        .Cells(16, 2).Value = "Valor"
        .Cells(16, 1).Font.Bold = True
        .Cells(16, 2).Font.Bold = True

        .Cells(17, 1).Value = "Validar en tiempo real"
        .Cells(17, 2).Value = "SI"

        .Cells(18, 1).Value = "Mostrar alertas"
        .Cells(18, 2).Value = "SI"

        .Cells(19, 1).Value = "Autocompletar campos"
        .Cells(19, 2).Value = "SI"

        .Cells(20, 1).Value = "Registrar en log"
        .Cells(20, 2).Value = "SI"

        ' Ajustar anchos de columna
        .Columns("A:A").ColumnWidth = 25
        .Columns("B:B").ColumnWidth = 15
        .Columns("C:C").ColumnWidth = 15
        .Columns("D:D").ColumnWidth = 15
        .Columns("E:E").ColumnWidth = 15
    End With

    On Error GoTo 0
End Sub
