Attribute VB_Name = "Modulo3_ReglasNegocio"
'═══════════════════════════════════════════════════════════════════════════════
' MÓDULO 3: REGLAS DE NEGOCIO
' Validaciones específicas según Resolución 202 de 2021
' Incluye reglas de sexo, edad, gestación y coherencia de datos
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: AplicarReglaSexoMasculino
' Descripción: Completa automáticamente campos de gestación y ginecología cuando sexo = M
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub AplicarReglaSexoMasculino(fila As Long)
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ' Desactivar temporalmente las validaciones para evitar recursión
    ValidacionActiva = False

    With ws
        ' Gestación = No aplica
        If .Cells(fila, COL_GESTACION).Value <> CODIGO_NO_GESTANTE Then
            .Cells(fila, COL_GESTACION).Value = CODIGO_NO_GESTANTE
            .Cells(fila, COL_GESTACION).Interior.Color = COLOR_NORMAL
        End If

        ' Edad gestacional = No aplica
        If .Cells(fila, COL_EDAD_GESTACIONAL).Value <> CODIGO_NO_EDAD_GESTACIONAL Then
            .Cells(fila, COL_EDAD_GESTACIONAL).Value = CODIGO_NO_EDAD_GESTACIONAL
            .Cells(fila, COL_EDAD_GESTACIONAL).Interior.Color = COLOR_NORMAL
        End If

        ' Control prenatal = No aplica
        If .Cells(fila, COL_CONTROL_PRENATAL).Value <> CODIGO_NO_CONTROL_PRENATAL Then
            .Cells(fila, COL_CONTROL_PRENATAL).Value = CODIGO_NO_CONTROL_PRENATAL
            .Cells(fila, COL_CONTROL_PRENATAL).Interior.Color = COLOR_NORMAL
        End If

        ' Citología = No aplica
        If .Cells(fila, COL_CITOLOGIA).Value <> CODIGO_NO_CITOLOGIA Then
            .Cells(fila, COL_CITOLOGIA).Value = CODIGO_NO_CITOLOGIA
            .Cells(fila, COL_CITOLOGIA).Interior.Color = COLOR_NORMAL
        End If

        ' Mamografía = No aplica
        If .Cells(fila, COL_MAMOGRAFIA).Value <> CODIGO_NO_MAMOGRAFIA Then
            .Cells(fila, COL_MAMOGRAFIA).Value = CODIGO_NO_MAMOGRAFIA
            .Cells(fila, COL_MAMOGRAFIA).Interior.Color = COLOR_NORMAL
        End If
    End With

    ' Reactivar validaciones
    ValidacionActiva = True
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarCoherenciaSexoGestacion
' Descripción: Valida coherencia entre sexo y datos de gestación
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarCoherenciaSexoGestacion(fila As Long) As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarCoherenciaSexoGestacion = True

    Dim sexo As String
    Dim gestacion As String

    sexo = UCase(Trim(ws.Cells(fila, COL_SEXO).Value))
    gestacion = Trim(ws.Cells(fila, COL_GESTACION).Value)

    ' Si es masculino, gestación debe ser "0" (No aplica)
    If sexo = SEXO_MASCULINO Then
        If gestacion <> CODIGO_NO_GESTANTE And gestacion <> "" Then
            ValidarCoherenciaSexoGestacion = False
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarCoherenciaGestacionEdadGestacional
' Descripción: Si gestación = Sí, debe haber edad gestacional
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarCoherenciaGestacionEdadGestacional(fila As Long) As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarCoherenciaGestacionEdadGestacional = True

    Dim gestacion As String
    Dim edadGest As String

    gestacion = Trim(ws.Cells(fila, COL_GESTACION).Value)
    edadGest = Trim(ws.Cells(fila, COL_EDAD_GESTACIONAL).Value)

    ' Si está gestante (código "1" o "SI"), debe tener edad gestacional
    If (gestacion = "1" Or UCase(gestacion) = "SI") Then
        If edadGest = "" Or edadGest = "0" Then
            ValidarCoherenciaGestacionEdadGestacional = False
        End If
    End If

    ' Si no está gestante, edad gestacional debe ser 0 o vacío
    If gestacion = "0" Or UCase(gestacion) = "NO" Then
        If edadGest <> "" And edadGest <> "0" Then
            ValidarCoherenciaGestacionEdadGestacional = False
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarEdadVsTipoDocumento
' Descripción: Valida coherencia entre edad y tipo de documento
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarEdadVsTipoDocumento(fila As Long) As String
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarEdadVsTipoDocumento = ""

    Dim tipoDoc As String
    Dim fechaNac As Variant
    Dim edad As Integer

    tipoDoc = UCase(Trim(ws.Cells(fila, COL_TIPO_DOC).Value))
    fechaNac = ws.Cells(fila, COL_FECHA_NACIMIENTO).Value

    If Not IsDate(fechaNac) Then
        Exit Function
    End If

    edad = CalcularEdad(fechaNac)

    ' Validaciones según tipo de documento
    Select Case tipoDoc
        Case "RC" ' Registro Civil: menores de 7 años
            If edad >= 7 Then
                ValidarEdadVsTipoDocumento = "RC solo aplica para menores de 7 años. Edad: " & edad
            End If

        Case "TI" ' Tarjeta de Identidad: 7 a 17 años
            If edad < 7 Or edad >= 18 Then
                ValidarEdadVsTipoDocumento = "TI solo aplica para personas entre 7 y 17 años. Edad: " & edad
            End If

        Case "CC" ' Cédula de Ciudadanía: mayores de 18 años
            If edad < 18 Then
                ValidarEdadVsTipoDocumento = "CC solo aplica para mayores de 18 años. Edad: " & edad
            End If

        Case "MS" ' Menor sin identificación: menores de 18 años
            If edad >= 18 Then
                ValidarEdadVsTipoDocumento = "MS solo aplica para menores de 18 años. Edad: " & edad
            End If
    End Select
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: SugerirTipoDocumento
' Descripción: Sugiere el tipo de documento correcto según la edad
' ═══════════════════════════════════════════════════════════════════════════════

Public Function SugerirTipoDocumento(fechaNac As Variant) As String
    SugerirTipoDocumento = ""

    If Not IsDate(fechaNac) Then
        Exit Function
    End If

    Dim edad As Integer
    edad = CalcularEdad(fechaNac)

    If edad < 7 Then
        SugerirTipoDocumento = "RC"
    ElseIf edad >= 7 And edad < 18 Then
        SugerirTipoDocumento = "TI"
    Else
        SugerirTipoDocumento = "CC"
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarEdadMujerGestante
' Descripción: Valida que si hay gestación, la edad sea coherente (generalmente 10-55 años)
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarEdadMujerGestante(fila As Long) As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarEdadMujerGestante = True

    Dim gestacion As String
    Dim fechaNac As Variant
    Dim edad As Integer

    gestacion = Trim(ws.Cells(fila, COL_GESTACION).Value)
    fechaNac = ws.Cells(fila, COL_FECHA_NACIMIENTO).Value

    ' Si está gestante
    If gestacion = "1" Or UCase(gestacion) = "SI" Then
        If IsDate(fechaNac) Then
            edad = CalcularEdad(fechaNac)

            ' Advertencia si edad < 10 o > 55 (valores atípicos pero posibles)
            If edad < 10 Or edad > 55 Then
                ValidarEdadMujerGestante = False
            End If
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: AutocompletarNoGestante
' Descripción: Cuando gestación = No, autocompleta campos relacionados
' ═══════════════════════════════════════════════════════════════════════════════

Public Sub AutocompletarNoGestante(fila As Long)
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidacionActiva = False

    With ws
        ' Edad gestacional = 0
        .Cells(fila, COL_EDAD_GESTACIONAL).Value = CODIGO_NO_EDAD_GESTACIONAL
        .Cells(fila, COL_EDAD_GESTACIONAL).Interior.Color = COLOR_NORMAL

        ' Control prenatal = 0
        .Cells(fila, COL_CONTROL_PRENATAL).Value = CODIGO_NO_CONTROL_PRENATAL
        .Cells(fila, COL_CONTROL_PRENATAL).Interior.Color = COLOR_NORMAL
    End With

    ValidacionActiva = True
End Sub

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarFechaConsultaVsNacimiento
' Descripción: Valida que la fecha de consulta sea posterior al nacimiento
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarFechaConsultaVsNacimiento(fila As Long) As Boolean
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarFechaConsultaVsNacimiento = True

    Dim fechaNac As Variant
    Dim fechaConsulta As Variant

    fechaNac = ws.Cells(fila, COL_FECHA_NACIMIENTO).Value
    fechaConsulta = ws.Cells(fila, COL_FECHA_CONSULTA).Value

    If IsDate(fechaNac) And IsDate(fechaConsulta) Then
        If CDate(fechaConsulta) < CDate(fechaNac) Then
            ValidarFechaConsultaVsNacimiento = False
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarCamposObligatoriosFila
' Descripción: Valida todos los campos obligatorios de una fila
' Retorna: Array con índices de columnas que tienen errores
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarCamposObligatoriosFila(fila As Long) As Collection
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    Dim errores As New Collection
    Dim camposObligatorios As Variant

    ' Lista de columnas obligatorias (ajustar según Resolución 202)
    camposObligatorios = Array(COL_TIPO_DOC, COL_PRIMER_APELLIDO, COL_PRIMER_NOMBRE, _
                               COL_FECHA_NACIMIENTO, COL_SEXO, COL_FECHA_CONSULTA)

    Dim i As Integer
    For i = LBound(camposObligatorios) To UBound(camposObligatorios)
        If Not ValidarCampoObligatorio(ws.Cells(fila, camposObligatorios(i)).Value) Then
            errores.Add camposObligatorios(i)
        End If
    Next i

    Set ValidarCamposObligatoriosFila = errores
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: NormalizarRegimen
' Descripción: Normaliza el código de régimen a la letra correspondiente
' ═══════════════════════════════════════════════════════════════════════════════

Public Function NormalizarRegimen(regimen As String) As String
    Select Case UCase(Trim(regimen))
        Case "C", "CONTRIBUTIVO"
            NormalizarRegimen = "C"
        Case "S", "SUBSIDIADO"
            NormalizarRegimen = "S"
        Case "E", "ESPECIAL"
            NormalizarRegimen = "E"
        Case "N", "NO AFILIADO"
            NormalizarRegimen = "N"
        Case Else
            NormalizarRegimen = regimen
    End Select
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: NormalizarSexo
' Descripción: Normaliza el código de sexo
' ═══════════════════════════════════════════════════════════════════════════════

Public Function NormalizarSexo(sexo As String) As String
    Select Case UCase(Trim(sexo))
        Case "M", "MASCULINO", "HOMBRE"
            NormalizarSexo = "M"
        Case "F", "FEMENINO", "MUJER"
            NormalizarSexo = "F"
        Case "I", "INDETERMINADO"
            NormalizarSexo = "I"
        Case Else
            NormalizarSexo = sexo
    End Select
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarYNormalizarCelda
' Descripción: Valida y normaliza el contenido de una celda específica
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarYNormalizarCelda(fila As Long, columna As Integer) As String
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(HOJA_DATOS)

    ValidarYNormalizarCelda = ""
    Dim valor As String
    valor = Trim(ws.Cells(fila, columna).Value)

    Select Case columna
        Case COL_SEXO
            If valor <> "" Then
                Dim sexoNorm As String
                sexoNorm = NormalizarSexo(valor)
                If ValidarSexo(sexoNorm) Then
                    ws.Cells(fila, columna).Value = sexoNorm
                Else
                    ValidarYNormalizarCelda = ObtenerMensajeError("SEXO_INVALIDO")
                End If
            End If

        Case COL_REGIMEN
            If valor <> "" Then
                Dim regimenNorm As String
                regimenNorm = NormalizarRegimen(valor)
                If ValidarRegimen(regimenNorm) Then
                    ws.Cells(fila, columna).Value = regimenNorm
                Else
                    ValidarYNormalizarCelda = ObtenerMensajeError("REGIMEN_INVALIDO")
                End If
            End If

        Case COL_TIPO_DOC
            If valor <> "" Then
                Dim tipoDocNorm As String
                tipoDocNorm = UCase(valor)
                If ValidarTipoDocumento(tipoDocNorm) Then
                    ws.Cells(fila, columna).Value = tipoDocNorm
                Else
                    ValidarYNormalizarCelda = ObtenerMensajeError("TIPO_DOC_INVALIDO")
                End If
            End If
    End Select
End Function
