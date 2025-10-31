Attribute VB_Name = "Modulo2_Validaciones"
'═══════════════════════════════════════════════════════════════════════════════
' MÓDULO 2: FUNCIONES DE VALIDACIÓN
' Validaciones de formato, tipo y longitud de datos
' Resolución 202 de 2021
'═══════════════════════════════════════════════════════════════════════════════

Option Explicit

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarTipoDocumento
' Descripción: Valida que el tipo de documento sea válido
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarTipoDocumento(tipoDoc As String) As Boolean
    Dim tiposValidos As Variant
    tiposValidos = Array("RC", "TI", "CC", "CE", "PA", "MS", "AS", "CD", "PE", "CN")

    ValidarTipoDocumento = False

    Dim i As Integer
    For i = LBound(tiposValidos) To UBound(tiposValidos)
        If UCase(Trim(tipoDoc)) = tiposValidos(i) Then
            ValidarTipoDocumento = True
            Exit Function
        End If
    Next i
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarLongitudDocumento
' Descripción: Valida la longitud del número de documento según su tipo
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarLongitudDocumento(tipoDoc As String, numDoc As String) As Boolean
    Dim longitud As Integer
    longitud = Len(Trim(numDoc))

    ValidarLongitudDocumento = True

    Select Case UCase(Trim(tipoDoc))
        Case "RC" ' Registro Civil: 10-11 dígitos
            If longitud < 10 Or longitud > 11 Then
                ValidarLongitudDocumento = False
            End If

        Case "TI" ' Tarjeta de Identidad: 10-11 dígitos
            If longitud < 10 Or longitud > 11 Then
                ValidarLongitudDocumento = False
            End If

        Case "CC" ' Cédula de Ciudadanía: 6-10 dígitos
            If longitud < 6 Or longitud > 10 Then
                ValidarLongitudDocumento = False
            End If

        Case "CE" ' Cédula de Extranjería: 6-10 caracteres
            If longitud < 6 Or longitud > 10 Then
                ValidarLongitudDocumento = False
            End If

        Case "PA" ' Pasaporte: 6-20 caracteres
            If longitud < 6 Or longitud > 20 Then
                ValidarLongitudDocumento = False
            End If

        Case "MS", "AS" ' Sin identificación: máximo 15 caracteres
            If longitud > 15 Then
                ValidarLongitudDocumento = False
            End If

        Case "CD" ' Carné Diplomático: 6-15 caracteres
            If longitud < 6 Or longitud > 15 Then
                ValidarLongitudDocumento = False
            End If

        Case "PE" ' Permiso Especial: 6-15 caracteres
            If longitud < 6 Or longitud > 15 Then
                ValidarLongitudDocumento = False
            End If

        Case "CN" ' Certificado de Nacido Vivo: 10-12 dígitos
            If longitud < 10 Or longitud > 12 Then
                ValidarLongitudDocumento = False
            End If
    End Select
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarDocumentoNumerico
' Descripción: Valida que el documento contenga solo números (para tipos que lo requieren)
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarDocumentoNumerico(tipoDoc As String, numDoc As String) As Boolean
    Dim tiposNumericos As Variant
    tiposNumericos = Array("RC", "TI", "CC", "CN")

    ValidarDocumentoNumerico = True

    Dim i As Integer
    For i = LBound(tiposNumericos) To UBound(tiposNumericos)
        If UCase(Trim(tipoDoc)) = tiposNumericos(i) Then
            ' Verificar que solo contenga números
            If Not IsNumeric(numDoc) Then
                ValidarDocumentoNumerico = False
            End If
            Exit Function
        End If
    Next i
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarSexo
' Descripción: Valida que el sexo sea M, F o I
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarSexo(sexo As String) As Boolean
    ValidarSexo = False

    Select Case UCase(Trim(sexo))
        Case "M", "F", "I"
            ValidarSexo = True
    End Select
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarFecha
' Descripción: Valida que una fecha sea válida y esté en formato correcto
' Retorna: True si es válida, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarFecha(fecha As Variant) As Boolean
    ValidarFecha = False

    On Error Resume Next
    If IsDate(fecha) Then
        ValidarFecha = True
    End If
    On Error GoTo 0
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarFechaNacimiento
' Descripción: Valida que la fecha de nacimiento sea coherente (no futura, no muy antigua)
' Retorna: True si es válida, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarFechaNacimiento(fechaNac As Variant) As Boolean
    ValidarFechaNacimiento = False

    If Not IsDate(fechaNac) Then
        Exit Function
    End If

    Dim fecha As Date
    fecha = CDate(fechaNac)

    ' No debe ser fecha futura
    If fecha > Date Then
        Exit Function
    End If

    ' No debe ser anterior a 150 años
    If fecha < DateAdd("yyyy", -150, Date) Then
        Exit Function
    End If

    ValidarFechaNacimiento = True
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: CalcularEdad
' Descripción: Calcula la edad en años a partir de la fecha de nacimiento
' Retorna: Edad en años
' ═══════════════════════════════════════════════════════════════════════════════

Public Function CalcularEdad(fechaNac As Variant) As Integer
    If Not IsDate(fechaNac) Then
        CalcularEdad = 0
        Exit Function
    End If

    Dim fecha As Date
    fecha = CDate(fechaNac)

    CalcularEdad = DateDiff("yyyy", fecha, Date)

    ' Ajustar si aún no ha cumplido años este año
    If Month(fecha) > Month(Date) Or _
       (Month(fecha) = Month(Date) And Day(fecha) > Day(Date)) Then
        CalcularEdad = CalcularEdad - 1
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarEdadGestacional
' Descripción: Valida que la edad gestacional esté en el rango válido (0-42 semanas)
' Retorna: True si es válida, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarEdadGestacional(edadGest As Variant) As Boolean
    ValidarEdadGestacional = False

    If Not IsNumeric(edadGest) Then
        Exit Function
    End If

    Dim edad As Integer
    edad = CInt(edadGest)

    If edad >= 0 And edad <= 42 Then
        ValidarEdadGestacional = True
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarCodigoDiagnostico
' Descripción: Valida formato básico de código CIE-10
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarCodigoDiagnostico(codigo As String) As Boolean
    ValidarCodigoDiagnostico = False

    codigo = UCase(Trim(codigo))

    ' Formato básico CIE-10: Letra seguida de 2-3 dígitos, opcionalmente seguido de punto y más dígitos
    ' Ejemplos: A00, A009, J44.0
    If Len(codigo) >= 3 Then
        ' Primera letra debe ser alfabética
        If Asc(Left(codigo, 1)) >= 65 And Asc(Left(codigo, 1)) <= 90 Then
            ValidarCodigoDiagnostico = True
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarCampoObligatorio
' Descripción: Valida que un campo obligatorio no esté vacío
' Retorna: True si tiene valor, False si está vacío
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarCampoObligatorio(valor As Variant) As Boolean
    ValidarCampoObligatorio = False

    If Not IsEmpty(valor) Then
        If Trim(CStr(valor)) <> "" Then
            ValidarCampoObligatorio = True
        End If
    End If
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarRegimen
' Descripción: Valida que el régimen sea válido (Contributivo, Subsidiado, Especial, No afiliado)
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarRegimen(regimen As String) As Boolean
    Dim regimenesValidos As Variant
    regimenesValidos = Array("C", "S", "E", "N", "CONTRIBUTIVO", "SUBSIDIADO", "ESPECIAL", "NO AFILIADO")

    ValidarRegimen = False

    Dim i As Integer
    For i = LBound(regimenesValidos) To UBound(regimenesValidos)
        If UCase(Trim(regimen)) = regimenesValidos(i) Then
            ValidarRegimen = True
            Exit Function
        End If
    Next i
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: NormalizarTexto
' Descripción: Normaliza texto quitando espacios extras y convirtiendo a mayúsculas
' Retorna: Texto normalizado
' ═══════════════════════════════════════════════════════════════════════════════

Public Function NormalizarTexto(texto As String) As String
    NormalizarTexto = UCase(Trim(texto))
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ValidarNombre
' Descripción: Valida que un nombre solo contenga letras, espacios y caracteres válidos
' Retorna: True si es válido, False si no
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ValidarNombre(nombre As String) As Boolean
    ValidarNombre = True

    If Trim(nombre) = "" Then
        ValidarNombre = False
        Exit Function
    End If

    ' Validar que solo contenga letras, espacios, tildes y ñ
    Dim i As Integer
    Dim caracter As String
    For i = 1 To Len(nombre)
        caracter = Mid(nombre, i, 1)
        ' Permitir letras (mayúsculas y minúsculas), espacios, tildes y ñ
        If Not ((caracter >= "A" And caracter <= "Z") Or _
                (caracter >= "a" And caracter <= "z") Or _
                caracter = " " Or caracter = "Ñ" Or caracter = "ñ" Or _
                caracter = "Á" Or caracter = "É" Or caracter = "Í" Or caracter = "Ó" Or caracter = "Ú" Or _
                caracter = "á" Or caracter = "é" Or caracter = "í" Or caracter = "ó" Or caracter = "ú") Then
            ValidarNombre = False
            Exit Function
        End If
    Next i
End Function

' ═══════════════════════════════════════════════════════════════════════════════
' FUNCIÓN: ObtenerMensajeError
' Descripción: Retorna un mensaje de error descriptivo según el tipo de validación
' ═══════════════════════════════════════════════════════════════════════════════

Public Function ObtenerMensajeError(tipoError As String, Optional param1 As String = "", Optional param2 As String = "") As String
    Select Case tipoError
        Case "TIPO_DOC_INVALIDO"
            ObtenerMensajeError = "Tipo de documento inválido. Use: RC, TI, CC, CE, PA, MS, AS, CD, PE o CN"

        Case "LONGITUD_DOC"
            ObtenerMensajeError = "Longitud de documento incorrecta para tipo " & param1

        Case "DOC_NO_NUMERICO"
            ObtenerMensajeError = "El documento debe contener solo números para tipo " & param1

        Case "SEXO_INVALIDO"
            ObtenerMensajeError = "Sexo inválido. Use: M (Masculino), F (Femenino) o I (Indeterminado)"

        Case "FECHA_INVALIDA"
            ObtenerMensajeError = "Fecha inválida o formato incorrecto"

        Case "FECHA_NAC_INVALIDA"
            ObtenerMensajeError = "Fecha de nacimiento inválida (no puede ser futura ni muy antigua)"

        Case "EDAD_GESTACIONAL"
            ObtenerMensajeError = "Edad gestacional debe estar entre 0 y 42 semanas"

        Case "CAMPO_OBLIGATORIO"
            ObtenerMensajeError = "Este campo es obligatorio"

        Case "REGIMEN_INVALIDO"
            ObtenerMensajeError = "Régimen inválido. Use: C, S, E o N"

        Case "NOMBRE_INVALIDO"
            ObtenerMensajeError = "Nombre contiene caracteres no permitidos"

        Case "CODIGO_DX_INVALIDO"
            ObtenerMensajeError = "Código diagnóstico CIE-10 inválido"

        Case "INCOHERENCIA_SEXO_EDAD"
            ObtenerMensajeError = "Incoherencia entre sexo, edad y valores de gestación/exámenes ginecológicos"

        Case Else
            ObtenerMensajeError = "Error de validación: " & tipoError
    End Select
End Function
