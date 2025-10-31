VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
'═══════════════════════════════════════════════════════════════════════════════
' CÓDIGO DE EVENTOS DEL WORKBOOK
' Maneja eventos de apertura, cierre y configuración del libro
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: Workbook_Open
' Descripción: Se ejecuta al abrir el archivo
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub Workbook_Open()
    ' Inicializar el sistema
    Call InicializarSistema

    ' Crear menú personalizado
    Call CrearMenuValidacion

    ' Mostrar mensaje de bienvenida
    Dim mensaje As String
    mensaje = "Sistema de Validación - Resolución 202 de 2021" & vbCrLf & vbCrLf
    mensaje = mensaje & "El sistema de validación automática está activo." & vbCrLf & vbCrLf
    mensaje = mensaje & "Para acceder a las funciones, use el menú:" & vbCrLf
    mensaje = mensaje & "'VALIDACIÓN 202' en la barra de menú." & vbCrLf & vbCrLf
    mensaje = mensaje & "¿Desea abrir el Panel de Control?"

    Dim respuesta As VbMsgBoxResult
    respuesta = MsgBox(mensaje, vbYesNo + vbQuestion, "Bienvenido")

    If respuesta = vbYes Then
        Call MostrarPanelControl
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: Workbook_BeforeClose
' Descripción: Se ejecuta antes de cerrar el archivo
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub Workbook_BeforeClose(Cancel As Boolean)
    ' Eliminar menú personalizado
    Call EliminarMenuValidacion

    ' Verificar si hay errores sin revisar
    Dim totalErrores As Long
    totalErrores = ContarErrores()

    If totalErrores > 0 Then
        Dim mensaje As String
        mensaje = "ADVERTENCIA: Existen " & totalErrores & " error(es) pendientes." & vbCrLf & vbCrLf
        mensaje = mensaje & "¿Está seguro de que desea cerrar el archivo?"

        Dim respuesta As VbMsgBoxResult
        respuesta = MsgBox(mensaje, vbYesNo + vbExclamation, "Errores Pendientes")

        If respuesta = vbNo Then
            Cancel = True
        End If
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: Workbook_BeforeSave
' Descripción: Se ejecuta antes de guardar el archivo
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub Workbook_BeforeSave(ByVal SaveAsUI As Boolean, Cancel As Boolean)
    ' Ocultar la hoja de configuración antes de guardar
    On Error Resume Next
    ThisWorkbook.Worksheets(HOJA_CONFIG).Visible = xlSheetVeryHidden
    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: CrearMenuValidacion
' Descripción: Crea un menú personalizado en la cinta de opciones
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub CrearMenuValidacion()
    On Error Resume Next

    Dim menuBar As CommandBar
    Dim menuPrincipal As CommandBarControl
    Dim submenu As CommandBarPopup

    ' Eliminar menú si ya existe
    Application.CommandBars("Worksheet Menu Bar").Controls("VALIDACIÓN 202").Delete

    ' Crear menú principal
    Set menuBar = Application.CommandBars("Worksheet Menu Bar")
    Set menuPrincipal = menuBar.Controls.Add(Type:=msoControlPopup, temporary:=True)

    menuPrincipal.Caption = "VALIDACIÓN 202"

    ' Agregar opciones al menú
    With menuPrincipal.CommandBar.Controls

        ' Panel de Control
        With .Add(Type:=msoControlButton)
            .Caption = "Panel de Control"
            .OnAction = "MostrarPanelControl"
            .FaceId = 2
        End With

        ' Separador
        .Add Type:=msoControlButton
        .Item(.Count).BeginGroup = True

        ' Validar Todo
        With .Add(Type:=msoControlButton)
            .Caption = "Validar Todo el Documento"
            .OnAction = "ValidarTodoElDocumento"
            .FaceId = 570
        End With

        ' Limpiar Validaciones
        With .Add(Type:=msoControlButton)
            .Caption = "Limpiar Todas las Validaciones"
            .OnAction = "LimpiarTodasLasValidaciones"
            .FaceId = 484
        End With

        ' Separador
        .Add Type:=msoControlButton
        .Item(.Count).BeginGroup = True

        ' Ver Log
        With .Add(Type:=msoControlButton)
            .Caption = "Ver Log de Errores"
            .OnAction = "AbrirHojaLog"
            .FaceId = 433
        End With

        ' Limpiar Log
        With .Add(Type:=msoControlButton)
            .Caption = "Limpiar Log"
            .OnAction = "LimpiarLog"
            .FaceId = 478
        End With

        ' Exportar Log
        With .Add(Type:=msoControlButton)
            .Caption = "Exportar Log a CSV"
            .OnAction = "ExportarLog"
            .FaceId = 620
        End With

        ' Separador
        .Add Type:=msoControlButton
        .Item(.Count).BeginGroup = True

        ' Siguiente Error
        With .Add(Type:=msoControlButton)
            .Caption = "Ir a Siguiente Error"
            .OnAction = "IrASiguienteError"
            .FaceId = 537
        End With

        ' Estadísticas
        With .Add(Type:=msoControlButton)
            .Caption = "Mostrar Estadísticas"
            .OnAction = "MostrarEstadisticasValidacion"
            .FaceId = 463
        End With

        ' Generar Reporte
        With .Add(Type:=msoControlButton)
            .Caption = "Generar Reporte"
            .OnAction = "GenerarReporteValidacion"
            .FaceId = 590
        End With

        ' Separador
        .Add Type:=msoControlButton
        .Item(.Count).BeginGroup = True

        ' Ayuda
        With .Add(Type:=msoControlButton)
            .Caption = "Ayuda"
            .OnAction = "MostrarAyuda"
            .FaceId = 49
        End With

    End With

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: EliminarMenuValidacion
' Descripción: Elimina el menú personalizado
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub EliminarMenuValidacion()
    On Error Resume Next
    Application.CommandBars("Worksheet Menu Bar").Controls("VALIDACIÓN 202").Delete
    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: MostrarPanelControl
' Descripción: Muestra el formulario de panel de control
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub MostrarPanelControl()
    frmPanelControl.Show
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: AbrirHojaLog
' Descripción: Abre y activa la hoja de log
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub AbrirHojaLog()
    On Error Resume Next
    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets(HOJA_LOG)

    If Not wsLog Is Nothing Then
        wsLog.Visible = xlSheetVisible
        wsLog.Activate
    Else
        MsgBox "No se encontró la hoja de log.", vbExclamation
    End If
    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTO: MostrarAyuda
' Descripción: Muestra la ventana de ayuda
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub MostrarAyuda()
    Dim mensaje As String

    mensaje = "═══════════════════════════════════════════════════════════" & vbCrLf
    mensaje = mensaje & "  SISTEMA DE VALIDACIÓN AUTOMÁTICA" & vbCrLf
    mensaje = mensaje & "  Resolución 202 de 2021" & vbCrLf
    mensaje = mensaje & "  Ministerio de Salud y Protección Social - Colombia" & vbCrLf
    mensaje = mensaje & "═══════════════════════════════════════════════════════════" & vbCrLf & vbCrLf

    mensaje = mensaje & "CARACTERÍSTICAS PRINCIPALES:" & vbCrLf & vbCrLf

    mensaje = mensaje & "1. VALIDACIÓN EN TIEMPO REAL" & vbCrLf
    mensaje = mensaje & "   • Se ejecuta automáticamente al modificar cada celda" & vbCrLf
    mensaje = mensaje & "   • Marca errores en color rojo" & vbCrLf
    mensaje = mensaje & "   • Muestra mensajes de error en comentarios" & vbCrLf & vbCrLf

    mensaje = mensaje & "2. AUTOCOMPLETADO INTELIGENTE" & vbCrLf
    mensaje = mensaje & "   • Completa automáticamente campos dependientes" & vbCrLf
    mensaje = mensaje & "   • Sugiere valores correctos según contexto" & vbCrLf
    mensaje = mensaje & "   • Normaliza códigos y formatos" & vbCrLf & vbCrLf

    mensaje = mensaje & "3. VALIDACIONES IMPLEMENTADAS" & vbCrLf
    mensaje = mensaje & "   • Tipo y número de documento" & vbCrLf
    mensaje = mensaje & "   • Coherencia entre edad y tipo de documento" & vbCrLf
    mensaje = mensaje & "   • Sexo y campos de gestación/ginecología" & vbCrLf
    mensaje = mensaje & "   • Fechas y rangos de valores" & vbCrLf
    mensaje = mensaje & "   • Campos obligatorios" & vbCrLf & vbCrLf

    mensaje = mensaje & "4. REGLAS ESPECÍFICAS" & vbCrLf
    mensaje = mensaje & "   • Sexo masculino: Auto-completa 'No aplica' en gestación" & vbCrLf
    mensaje = mensaje & "   • Edad vs documento: Valida coherencia (RC<7, TI 7-17, CC≥18)" & vbCrLf
    mensaje = mensaje & "   • Gestación: Valida edad gestacional y coherencia" & vbCrLf & vbCrLf

    mensaje = mensaje & "CÓDIGOS DE COLOR:" & vbCrLf
    mensaje = mensaje & "   • Rojo: Error que debe corregirse" & vbCrLf
    mensaje = mensaje & "   • Amarillo: Advertencia o valor atípico" & vbCrLf
    mensaje = mensaje & "   • Blanco: Valor correcto" & vbCrLf & vbCrLf

    mensaje = mensaje & "MENÚ 'VALIDACIÓN 202':" & vbCrLf
    mensaje = mensaje & "   • Panel de Control: Interfaz principal" & vbCrLf
    mensaje = mensaje & "   • Validar Todo: Valida todos los registros" & vbCrLf
    mensaje = mensaje & "   • Ver Log: Muestra errores registrados" & vbCrLf
    mensaje = mensaje & "   • Generar Reporte: Crea informe detallado" & vbCrLf & vbCrLf

    mensaje = mensaje & "Para más información, use el Panel de Control."

    MsgBox mensaje, vbInformation, "Ayuda del Sistema"
End Sub
