VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Hoja_DATOS_202"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
'═══════════════════════════════════════════════════════════════════════════════
' CÓDIGO DE EVENTOS DE HOJA: DATOS_202
' Validaciones en tiempo real al cambiar valores
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: Worksheet_Change
' Descripción: Se ejecuta cada vez que el usuario cambia el valor de una celda
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub Worksheet_Change(ByVal Target As Range)
    ' Salir si las validaciones están desactivadas
    If Not ValidacionActiva Then Exit Sub

    ' Solo procesar si es una celda única
    If Target.Cells.Count > 1 Then Exit Sub

    ' Solo procesar filas de datos (no encabezados)
    If Target.Row < FILA_INICIO_DATOS Then Exit Sub

    Dim fila As Long
    Dim columna As Integer

    fila = Target.Row
    columna = Target.Column

    ' Desactivar temporalmente Application Events para evitar recursión
    Application.EnableEvents = False

    On Error GoTo ErrorHandler

    ' ═══════════════════════════════════════════════════════════════════════════════
    ' VALIDACIONES SEGÚN COLUMNA MODIFICADA
    ' ═══════════════════════════════════════════════════════════════════════════════

    Select Case columna

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: TIPO DE DOCUMENTO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_TIPO_DOC
            Call ValidarTipoDoc(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: NÚMERO DE DOCUMENTO
        ' ───────────────────────────────────────────────────────────────────────────
        Case 2 ' COL_NUM_DOC (usar número en lugar de "B")
            Call ValidarNumeroDoc(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: PRIMER APELLIDO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_PRIMER_APELLIDO
            Call ValidarNombreApellido(Target, "Primer Apellido")

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: SEGUNDO APELLIDO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_SEGUNDO_APELLIDO
            Call ValidarNombreApellido(Target, "Segundo Apellido")

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: PRIMER NOMBRE
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_PRIMER_NOMBRE
            Call ValidarNombreApellido(Target, "Primer Nombre")

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: SEGUNDO NOMBRE
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_SEGUNDO_NOMBRE
            Call ValidarNombreApellido(Target, "Segundo Nombre")

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: FECHA DE NACIMIENTO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_FECHA_NACIMIENTO
            Call ValidarFechaNac(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: SEXO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_SEXO
            Call ValidarSexoCelda(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: FECHA DE CONSULTA
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_FECHA_CONSULTA
            Call ValidarFechaConsulta(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: RÉGIMEN
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_REGIMEN
            Call ValidarRegimenCelda(Target)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: CÓDIGO DIAGNÓSTICO
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_CODIGO_DIAGNOSTICO
            Call ValidarCodigoDx(Target)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: GESTACIÓN
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_GESTACION
            Call ValidarGestacionCelda(Target, fila)

        ' ───────────────────────────────────────────────────────────────────────────
        ' COLUMNA: EDAD GESTACIONAL
        ' ───────────────────────────────────────────────────────────────────────────
        Case COL_EDAD_GESTACIONAL
            Call ValidarEdadGestacionalCelda(Target, fila)

    End Select

ErrorHandler:
    Application.EnableEvents = True
    If Err.Number <> 0 Then
        MsgBox "Error en validación: " & Err.Description, vbExclamation
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' PROCEDIMIENTOS DE VALIDACIÓN POR CAMPO
' ═══════════════════════════════════════════════════════════════════════════════

' ───────────────────────────────────────────────────────────────────────────────
' ValidarTipoDoc
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarTipoDoc(Target As Range, fila As Long)
    Dim valor As String
    valor = UCase(Trim(Target.Value))

    If valor = "" Then Exit Sub

    If ValidarTipoDocumento(valor) Then
        Target.Value = valor
        Target.Interior.Color = COLOR_NORMAL
        ' Validar número de documento si ya existe
        Dim numDoc As String
        numDoc = Trim(Me.Cells(fila, 2).Value)
        If numDoc <> "" Then
            Call ValidarNumeroDoc(Me.Cells(fila, 2), fila)
        End If
    Else
        Call MarcarError(Target, ObtenerMensajeError("TIPO_DOC_INVALIDO"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarNumeroDoc
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarNumeroDoc(Target As Range, fila As Long)
    Dim tipoDoc As String
    Dim numDoc As String

    tipoDoc = UCase(Trim(Me.Cells(fila, COL_TIPO_DOC).Value))
    numDoc = Trim(Target.Value)

    If numDoc = "" Then Exit Sub
    If tipoDoc = "" Then Exit Sub

    ' Validar longitud
    If Not ValidarLongitudDocumento(tipoDoc, numDoc) Then
        Call MarcarError(Target, ObtenerMensajeError("LONGITUD_DOC", tipoDoc))
        Exit Sub
    End If

    ' Validar que sea numérico si corresponde
    If Not ValidarDocumentoNumerico(tipoDoc, numDoc) Then
        Call MarcarError(Target, ObtenerMensajeError("DOC_NO_NUMERICO", tipoDoc))
        Exit Sub
    End If

    ' Si todo está bien
    Target.Interior.Color = COLOR_NORMAL
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarNombreApellido
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarNombreApellido(Target As Range, nombreCampo As String)
    Dim valor As String
    valor = Trim(Target.Value)

    If valor = "" Then
        ' El segundo nombre y segundo apellido pueden estar vacíos
        If InStr(nombreCampo, "Segundo") > 0 Then
            Target.Interior.Color = COLOR_NORMAL
            Exit Sub
        End If
    End If

    If ValidarNombre(valor) Then
        Target.Interior.Color = COLOR_NORMAL
    Else
        Call MarcarError(Target, ObtenerMensajeError("NOMBRE_INVALIDO"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarFechaNac
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarFechaNac(Target As Range, fila As Long)
    If IsEmpty(Target.Value) Then Exit Sub

    If ValidarFechaNacimiento(Target.Value) Then
        Target.Interior.Color = COLOR_NORMAL

        ' Sugerir tipo de documento según edad
        Dim tipoDocActual As String
        tipoDocActual = Trim(Me.Cells(fila, COL_TIPO_DOC).Value)

        Dim tipoDocSugerido As String
        tipoDocSugerido = SugerirTipoDocumento(Target.Value)

        If tipoDocActual = "" Then
            ' Preguntar si desea autocompletar
            Dim respuesta As VbMsgBoxResult
            respuesta = MsgBox("Según la fecha de nacimiento (edad: " & CalcularEdad(Target.Value) & " años), " & _
                              "el tipo de documento sugerido es: " & tipoDocSugerido & vbCrLf & vbCrLf & _
                              "¿Desea completarlo automáticamente?", vbYesNo + vbQuestion, "Sugerencia")
            If respuesta = vbYes Then
                Me.Cells(fila, COL_TIPO_DOC).Value = tipoDocSugerido
            End If
        Else
            ' Validar coherencia
            Dim mensajeError As String
            mensajeError = ValidarEdadVsTipoDocumento(fila)
            If mensajeError <> "" Then
                Me.Cells(fila, COL_TIPO_DOC).Interior.Color = COLOR_ADVERTENCIA
                Me.Cells(fila, COL_TIPO_DOC).AddComment mensajeError
            End If
        End If
    Else
        Call MarcarError(Target, ObtenerMensajeError("FECHA_NAC_INVALIDA"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarSexoCelda
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarSexoCelda(Target As Range, fila As Long)
    Dim valor As String
    valor = NormalizarSexo(Target.Value)

    If valor = "" Then Exit Sub

    If ValidarSexo(valor) Then
        Target.Value = valor
        Target.Interior.Color = COLOR_NORMAL

        ' Si es masculino, autocompletar campos de gestación
        If valor = SEXO_MASCULINO Then
            Call AplicarReglaSexoMasculino(fila)
            ' Mostrar mensaje informativo (opcional)
            Target.AddComment "Campos de gestación y ginecología completados automáticamente con 'No aplica'"
        End If
    Else
        Call MarcarError(Target, ObtenerMensajeError("SEXO_INVALIDO"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarFechaConsulta
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarFechaConsulta(Target As Range, fila As Long)
    If IsEmpty(Target.Value) Then Exit Sub

    If ValidarFecha(Target.Value) Then
        ' Validar que sea posterior a fecha de nacimiento
        If Not ValidarFechaConsultaVsNacimiento(fila) Then
            Call MarcarError(Target, "La fecha de consulta no puede ser anterior a la fecha de nacimiento")
        Else
            Target.Interior.Color = COLOR_NORMAL
        End If
    Else
        Call MarcarError(Target, ObtenerMensajeError("FECHA_INVALIDA"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarRegimenCelda
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarRegimenCelda(Target As Range)
    Dim valor As String
    valor = NormalizarRegimen(Target.Value)

    If valor = "" Then Exit Sub

    If ValidarRegimen(valor) Then
        Target.Value = valor
        Target.Interior.Color = COLOR_NORMAL
    Else
        Call MarcarError(Target, ObtenerMensajeError("REGIMEN_INVALIDO"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarCodigoDx
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarCodigoDx(Target As Range)
    Dim valor As String
    valor = UCase(Trim(Target.Value))

    If valor = "" Then Exit Sub

    If ValidarCodigoDiagnostico(valor) Then
        Target.Value = valor
        Target.Interior.Color = COLOR_NORMAL
    Else
        Call MarcarError(Target, ObtenerMensajeError("CODIGO_DX_INVALIDO"))
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarGestacionCelda
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarGestacionCelda(Target As Range, fila As Long)
    Dim valor As String
    valor = Trim(Target.Value)

    If valor = "" Then Exit Sub

    ' Normalizar valores
    If UCase(valor) = "SI" Or valor = "1" Then
        Target.Value = "1"
    ElseIf UCase(valor) = "NO" Or valor = "0" Then
        Target.Value = "0"
        ' Autocompletar campos relacionados
        Call AutocompletarNoGestante(fila)
    End If

    ' Validar coherencia con sexo
    If Not ValidarCoherenciaSexoGestacion(fila) Then
        Call MarcarError(Target, "Incoherencia: Sexo masculino no puede tener gestación")
    Else
        Target.Interior.Color = COLOR_NORMAL
    End If
End Sub

' ───────────────────────────────────────────────────────────────────────────────
' ValidarEdadGestacionalCelda
' ───────────────────────────────────────────────────────────────────────────────
Private Sub ValidarEdadGestacionalCelda(Target As Range, fila As Long)
    Dim valor As String
    valor = Trim(Target.Value)

    If valor = "" Then Exit Sub

    If ValidarEdadGestacional(valor) Then
        Target.Interior.Color = COLOR_NORMAL

        ' Validar coherencia con gestación
        If Not ValidarCoherenciaGestacionEdadGestacional(fila) Then
            Call MarcarError(Target, "Incoherencia entre gestación y edad gestacional")
        End If
    Else
        Call MarcarError(Target, ObtenerMensajeError("EDAD_GESTACIONAL"))
    End If
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: MarcarError
' Descripción: Marca una celda con error y agrega comentario
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub MarcarError(Target As Range, mensaje As String)
    Target.Interior.Color = COLOR_ERROR

    ' Limpiar comentario anterior si existe
    On Error Resume Next
    Target.Comment.Delete
    On Error GoTo 0

    ' Agregar nuevo comentario
    Target.AddComment mensaje

    ' Registrar en log
    Call RegistrarError(Target.Row, Target.Column, ObtenerNombreColumna(Target.Column), mensaje, Target.Value, "")
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' EVENTO: Worksheet_SelectionChange
' Descripción: Muestra información de ayuda al seleccionar una celda
' ═══════════════════════════════════════════════════════════════════════════════

Private Sub Worksheet_SelectionChange(ByVal Target As Range)
    ' Mostrar información en barra de estado
    If Target.Row >= FILA_INICIO_DATOS And Target.Cells.Count = 1 Then
        Application.StatusBar = "Campo: " & Me.Cells(FILA_ENCABEZADO, Target.Column).Value
    Else
        Application.StatusBar = False
    End If
End Sub
