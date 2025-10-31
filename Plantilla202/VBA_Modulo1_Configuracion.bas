Attribute VB_Name = "Modulo1_Configuracion"
'═══════════════════════════════════════════════════════════════════════════════
' MÓDULO 1: CONFIGURACIÓN Y CONSTANTES
' Sistema de Validación - Resolución 202 de 2021
' Ministerio de Salud y Protección Social - Colombia
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' CONSTANTES DE COLUMNAS (Índices de las 119 columnas obligatorias)
' ═══════════════════════════════════════════════════════════════════════════════

' Datos de Identificación (Columnas 1-10)
Public Const COL_TIPO_DOC As Integer = 1           ' Tipo de Documento
Public Const COL_NUM_DOC As String = "B"           ' Número de Documento
Public Const COL_PRIMER_APELLIDO As Integer = 3    ' Primer Apellido
Public Const COL_SEGUNDO_APELLIDO As Integer = 4   ' Segundo Apellido
Public Const COL_PRIMER_NOMBRE As Integer = 5      ' Primer Nombre
Public Const COL_SEGUNDO_NOMBRE As Integer = 6     ' Segundo Nombre
Public Const COL_FECHA_NACIMIENTO As Integer = 7   ' Fecha de Nacimiento
Public Const COL_SEXO As Integer = 8               ' Sexo
Public Const COL_DEPARTAMENTO As Integer = 9       ' Departamento de Residencia
Public Const COL_MUNICIPIO As Integer = 10         ' Municipio de Residencia

' Datos de Afiliación (Columnas 11-20)
Public Const COL_REGIMEN As Integer = 11           ' Régimen de Afiliación
Public Const COL_EAPB As Integer = 12              ' Código EAPB
Public Const COL_TIPO_USUARIO As Integer = 13      ' Tipo de Usuario

' Datos de Atención (Columnas 14-30)
Public Const COL_FECHA_CONSULTA As Integer = 14    ' Fecha de Consulta
Public Const COL_CAUSA_EXTERNA As Integer = 15     ' Causa Externa
Public Const COL_CODIGO_DIAGNOSTICO As Integer = 16 ' Código Diagnóstico Principal
Public Const COL_TIPO_DIAGNOSTICO As Integer = 17  ' Tipo de Diagnóstico

' Datos Específicos de Mujer (Columnas 31-40)
Public Const COL_GESTACION As Integer = 31         ' Gestación
Public Const COL_EDAD_GESTACIONAL As Integer = 32  ' Edad Gestacional
Public Const COL_CONTROL_PRENATAL As Integer = 33  ' Control Prenatal
Public Const COL_CITOLOGIA As Integer = 34         ' Citología Cervicouterina
Public Const COL_MAMOGRAFIA As Integer = 35        ' Mamografía

' ═══════════════════════════════════════════════════════════════════════════════
' CÓDIGOS DE "NO APLICA" SEGÚN RESOLUCIÓN 202
' ═══════════════════════════════════════════════════════════════════════════════

Public Const CODIGO_NO_APLICA As String = "0"      ' Código general para "No Aplica"
Public Const CODIGO_NO_GESTANTE As String = "0"    ' No gestante
Public Const CODIGO_NO_EDAD_GESTACIONAL As String = "0" ' No edad gestacional
Public Const CODIGO_NO_CONTROL_PRENATAL As String = "0" ' No control prenatal
Public Const CODIGO_NO_CITOLOGIA As String = "0"   ' No citología
Public Const CODIGO_NO_MAMOGRAFIA As String = "0"  ' No mamografía

' ═══════════════════════════════════════════════════════════════════════════════
' CÓDIGOS DE SEXO
' ═══════════════════════════════════════════════════════════════════════════════

Public Const SEXO_MASCULINO As String = "M"
Public Const SEXO_FEMENINO As String = "F"
Public Const SEXO_INDETERMINADO As String = "I"

' ═══════════════════════════════════════════════════════════════════════════════
' TIPOS DE DOCUMENTO Y SUS RESTRICCIONES
' ═══════════════════════════════════════════════════════════════════════════════

Public Enum TipoDocumento
    RC = 1  ' Registro Civil
    TI = 2  ' Tarjeta de Identidad
    CC = 3  ' Cédula de Ciudadanía
    CE = 4  ' Cédula de Extranjería
    PA = 5  ' Pasaporte
    MS = 6  ' Menor sin Identificación
    ASI = 7  ' Adulto sin Identificación (AS es palabra reservada en VBA)
    CD = 8  ' Carné Diplomático
    PE = 9  ' Permiso Especial de Permanencia
End Enum

' ═══════════════════════════════════════════════════════════════════════════════
' CONFIGURACIÓN DE VALIDACIÓN
' ═══════════════════════════════════════════════════════════════════════════════

Public Const HOJA_DATOS As String = "DATOS_202"     ' Nombre de la hoja principal
Public Const HOJA_CONFIG As String = "CONFIG"       ' Nombre de la hoja de configuración
Public Const HOJA_LOG As String = "LOG_ERRORES"     ' Nombre de la hoja de log
Public Const FILA_ENCABEZADO As Integer = 1         ' Fila de encabezados
Public Const FILA_INICIO_DATOS As Integer = 2       ' Primera fila de datos

' Colores para marcado de errores
Public Const COLOR_ERROR As Long = 255              ' Rojo (RGB: 255, 0, 0)
Public Const COLOR_ADVERTENCIA As Long = 65535      ' Amarillo (RGB: 255, 255, 0)
Public Const COLOR_CORRECTO As Long = 15773696      ' Verde claro (RGB: 0, 255, 0)
Public Const COLOR_NORMAL As Long = 16777215        ' Blanco

' ═══════════════════════════════════════════════════════════════════════════════
' VARIABLES GLOBALES
' ═══════════════════════════════════════════════════════════════════════════════

Public ValidacionActiva As Boolean  ' Flag para activar/desactivar validaciones temporalmente

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: InicializarSistema
' Descripción: Inicializa el sistema de validación
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub InicializarSistema()
    ValidacionActiva = True

    ' Verificar que existan las hojas necesarias
    Call VerificarHojas

    ' Configurar hojas
    Call ConfigurarHojas

    MsgBox "Sistema de validación iniciado correctamente." & vbCrLf & _
           "Resolución 202 de 2021 - MinSalud Colombia", vbInformation, "Sistema Iniciado"
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: VerificarHojas
' Descripción: Verifica que existan las hojas necesarias, si no las crea
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub VerificarHojas()
    Dim ws As Worksheet
    Dim encontrado As Boolean

    ' Verificar hoja de LOG
    encontrado = False
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name = HOJA_LOG Then
            encontrado = True
            Exit For
        End If
    Next ws

    If Not encontrado Then
        Call CrearHojaLog
    End If

    ' Verificar hoja de CONFIG
    encontrado = False
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name = HOJA_CONFIG Then
            encontrado = True
            Exit For
        End If
    Next ws

    If Not encontrado Then
        Call CrearHojaConfig
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: CrearHojaLog
' Descripción: Crea la hoja de registro de errores
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub CrearHojaLog()
    Dim wsLog As Worksheet
    Set wsLog = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    wsLog.Name = HOJA_LOG

    ' Encabezados
    With wsLog
        .Cells(1, 1).Value = "FECHA/HORA"
        .Cells(1, 2).Value = "FILA"
        .Cells(1, 3).Value = "COLUMNA"
        .Cells(1, 4).Value = "CAMPO"
        .Cells(1, 5).Value = "ERROR"
        .Cells(1, 6).Value = "VALOR_INGRESADO"
        .Cells(1, 7).Value = "VALOR_ESPERADO"

        ' Formato de encabezados
        .Range("A1:G1").Font.Bold = True
        .Range("A1:G1").Interior.Color = RGB(68, 114, 196)
        .Range("A1:G1").Font.Color = RGB(255, 255, 255)
        .Range("A1:G1").HorizontalAlignment = xlCenter

        ' Ajustar anchos
        .Columns("A:A").ColumnWidth = 20
        .Columns("B:C").ColumnWidth = 8
        .Columns("D:D").ColumnWidth = 25
        .Columns("E:E").ColumnWidth = 50
        .Columns("F:G").ColumnWidth = 20
    End With
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ConfigurarHojas
' Descripción: Configura las protecciones y formatos de las hojas
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub ConfigurarHojas()
    On Error Resume Next

    ' Ocultar hoja de configuración
    ThisWorkbook.Worksheets(HOJA_CONFIG).Visible = xlSheetVeryHidden

    On Error GoTo 0
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ObtenerNombreColumna
' Descripción: Obtiene el nombre del campo según el número de columna
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ObtenerNombreColumna(numCol As Integer) As String
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)
    If Not ws Is Nothing Then
        ObtenerNombreColumna = ws.Cells(FILA_ENCABEZADO, numCol).Value
    Else
        ObtenerNombreColumna = "Columna " & numCol
    End If
    On Error GoTo 0
End Function
