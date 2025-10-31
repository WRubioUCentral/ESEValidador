VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} frmPanelControl
   Caption         =   "Panel de Control - Validador Resolución 202"
   ClientHeight    =   6525
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   7350
   OleObjectBlob   =   "frmPanelControl.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "frmPanelControl"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

'═══════════════════════════════════════════════════════════════════════════════
' USERFORM: PANEL DE CONTROL
' Interfaz gráfica para gestionar el sistema de validación
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: UserForm_Initialize
' Descripción: Inicializa el formulario
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub UserForm_Initialize()
    ' Actualizar estadísticas al abrir
    Call ActualizarEstadisticas
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Validar Todo el Documento
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnValidarTodo_Click()
    Me.Hide
    Call ValidarTodoElDocumento
    Call ActualizarEstadisticas
    Me.Show
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Limpiar Validaciones
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnLimpiarValidaciones_Click()
    Me.Hide
    Call LimpiarTodasLasValidaciones
    Call ActualizarEstadisticas
    Me.Show
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Ver Log de Errores
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnVerLog_Click()
    On Error Resume Next
    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If Not wsLog Is Nothing Then
        wsLog.Visible = xlSheetVisible
        wsLog.Activate
        Me.Hide
    Else
        MsgBox "No se encontró la hoja de log.", vbExclamation
    End If
    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Limpiar Log
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnLimpiarLog_Click()
    Call LimpiarLog
    Call ActualizarEstadisticas
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Exportar Log
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnExportarLog_Click()
    Me.Hide
    Call ExportarLog
    Me.Show
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Ir a Siguiente Error
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnSiguienteError_Click()
    Me.Hide
    Call IrASiguienteError
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Generar Reporte
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnGenerarReporte_Click()
    Me.Hide
    Call GenerarReporteValidacion
    Me.Show
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Mostrar Estadísticas
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnEstadisticas_Click()
    Call MostrarEstadisticasValidacion
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' CHECKBOX: Activar/Desactivar Validación en Tiempo Real
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub chkValidacionTiempoReal_Click()
    ValidacionActiva = chkValidacionTiempoReal.Value

    If ValidacionActiva Then
        lblEstado.Caption = "Estado: ACTIVO"
        lblEstado.ForeColor = RGB(0, 128, 0) ' Verde
    Else
        lblEstado.Caption = "Estado: DESACTIVADO"
        lblEstado.ForeColor = RGB(255, 0, 0) ' Rojo
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Cerrar
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnCerrar_Click()
    Unload Me
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: ActualizarEstadisticas
' Descripción: Actualiza los labels con las estadísticas actuales
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub ActualizarEstadisticas()
    On Error Resume Next

    ' Total de errores
    lblTotalErrores.Caption = "Total de errores: " & ContarErrores()

    ' Estado del sistema
    chkValidacionTiempoReal.Value = ValidacionActiva

    If ValidacionActiva Then
        lblEstado.Caption = "Estado: ACTIVO"
        lblEstado.ForeColor = RGB(0, 128, 0)
    Else
        lblEstado.Caption = "Estado: DESACTIVADO"
        lblEstado.ForeColor = RGB(255, 0, 0)
    End If

    ' Total de registros
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)
    If Not ws Is Nothing Then
        Dim totalRegistros As Long
        totalRegistros = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row - FILA_INICIO_DATOS + 1
        lblTotalRegistros.Caption = "Total de registros: " & totalRegistros
    End If

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' BOTÓN: Ayuda
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub btnAyuda_Click()
    Dim mensaje As String

    mensaje = "═══════════════════════════════════════════════" & vbCrLf
    mensaje = mensaje & "  SISTEMA DE VALIDACIÓN" & vbCrLf
    mensaje = mensaje & "  Resolución 202 de 2021" & vbCrLf
    mensaje = mensaje & "  Ministerio de Salud y Protección Social" & vbCrLf
    mensaje = mensaje & "═══════════════════════════════════════════════" & vbCrLf & vbCrLf

    mensaje = mensaje & "FUNCIONES PRINCIPALES:" & vbCrLf & vbCrLf

    mensaje = mensaje & "• Validar Todo: Valida todos los registros" & vbCrLf
    mensaje = mensaje & "• Ver Log: Muestra la hoja de errores" & vbCrLf
    mensaje = mensaje & "• Siguiente Error: Navega al siguiente error" & vbCrLf
    mensaje = mensaje & "• Generar Reporte: Crea informe detallado" & vbCrLf
    mensaje = mensaje & "• Limpiar: Elimina marcas y registros" & vbCrLf & vbCrLf

    mensaje = mensaje & "VALIDACIÓN EN TIEMPO REAL:" & vbCrLf
    mensaje = mensaje & "Cuando está activa, valida automáticamente" & vbCrLf
    mensaje = mensaje & "cada celda al modificarla." & vbCrLf & vbCrLf

    mensaje = mensaje & "CÓDIGOS DE COLOR:" & vbCrLf
    mensaje = mensaje & "• Rojo: Error crítico" & vbCrLf
    mensaje = mensaje & "• Amarillo: Advertencia" & vbCrLf
    mensaje = mensaje & "• Blanco: Correcto"

    MsgBox mensaje, vbInformation, "Ayuda del Sistema"
End Sub
