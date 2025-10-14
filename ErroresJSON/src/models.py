"""
Modelos de datos para archivos RIPS según Resolución 2275 de 2023
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AFRecord:
    """Archivo de Transacciones (AF) - Datos de la factura"""
    cod_prestador: str  # 1. Código del prestador
    nombre_prestador: str  # 2. Nombre del prestador
    tipo_documento_prestador: str  # 3. Tipo de documento del prestador
    num_documento_prestador: str  # 4. Número de documento del prestador
    num_factura: str  # 5. Número de factura
    fecha_expedicion: str  # 6. Fecha de expedición
    fecha_inicio: str  # 7. Fecha inicio de atención
    fecha_final: str  # 8. Fecha final de atención
    cod_entidad_administradora: str  # 9. Código entidad administradora
    nombre_entidad_administradora: str  # 10. Nombre entidad administradora
    num_contrato: str  # 11. Número de contrato
    plan_beneficios: str  # 12. Plan de beneficios
    num_poliza: str  # 13. Número de póliza
    valor_comision: str  # 14. Valor comisión
    num_cuotas_moderadoras: str  # 15. Número cuotas moderadoras
    valor_comision_cm: str  # 16. Valor comisión CM
    valor_neto: str  # 17. Valor neto


@dataclass
class USRecord:
    """Usuarios (US) - Datos del usuario/paciente"""
    tipo_documento: str  # 1. Tipo de documento
    num_documento: str  # 2. Número de documento
    cod_entidad_administradora: str  # 3. Código entidad administradora
    tipo_usuario: str  # 4. Tipo de usuario
    primer_apellido: str  # 5. Primer apellido
    segundo_apellido: str  # 6. Segundo apellido
    primer_nombre: str  # 7. Primer nombre
    segundo_nombre: str  # 8. Segundo nombre
    edad: str  # 9. Edad
    unidad_medida_edad: str  # 10. Unidad de medida de edad
    sexo: str  # 11. Sexo
    cod_departamento: str  # 12. Código del departamento
    cod_municipio: str  # 13. Código del municipio
    zona_residencial: str  # 14. Zona residencial
    num_autorizacion: str  # 15. Número de autorización


@dataclass
class ACRecord:
    """Consultas (AC) - Registro de consultas médicas"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento: str  # 3. Tipo de documento
    num_documento: str  # 4. Número de documento
    fecha_consulta: str  # 5. Fecha de consulta
    num_autorizacion: str  # 6. Número de autorización
    cod_consulta: str  # 7. Código de consulta (CUPS)
    cod_consulta_sistema: str  # 8. Código de consulta del sistema
    descripcion_consulta: str  # 9. Descripción de la consulta
    finalidad_consulta: str  # 10. Finalidad de la consulta
    causa_externa: str  # 11. Causa externa
    diagnostico_principal: str  # 12. Diagnóstico principal (CIE10)
    diagnostico_relacionado1: str  # 13. Diagnóstico relacionado 1
    diagnostico_relacionado2: str  # 14. Diagnóstico relacionado 2
    diagnostico_relacionado3: str  # 15. Diagnóstico relacionado 3
    tipo_diagnostico_principal: str  # 16. Tipo de diagnóstico principal
    valor_consulta: str  # 17. Valor de la consulta
    valor_cuota_moderadora: str  # 18. Valor cuota moderadora
    valor_neto: str  # 19. Valor neto
    edad: str  # 20. Edad
    unidad_medida_edad: str  # 21. Unidad de medida de edad
    sexo: str  # 22. Sexo


@dataclass
class APRecord:
    """Procedimientos (AP) - Registro de procedimientos"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento: str  # 3. Tipo de documento
    num_documento: str  # 4. Número de documento
    fecha_procedimiento: str  # 5. Fecha del procedimiento
    num_autorizacion: str  # 6. Número de autorización
    cod_procedimiento: str  # 7. Código del procedimiento (CUPS)
    cod_procedimiento_sistema: str  # 8. Código del procedimiento del sistema
    descripcion_procedimiento: str  # 9. Descripción del procedimiento
    ambito_procedimiento: str  # 10. Ámbito del procedimiento
    finalidad_procedimiento: str  # 11. Finalidad del procedimiento
    personal_atiende: str  # 12. Personal que atiende
    diagnostico_principal: str  # 13. Diagnóstico principal (CIE10)
    diagnostico_relacionado: str  # 14. Diagnóstico relacionado
    complicacion: str  # 15. Complicación
    forma_realizacion: str  # 16. Forma de realización
    valor_procedimiento: str  # 17. Valor del procedimiento
    valor_cuota_moderadora: str  # 18. Valor cuota moderadora
    valor_neto: str  # 19. Valor neto
    edad: str  # 20. Edad
    unidad_medida_edad: str  # 21. Unidad de medida de edad
    sexo: str  # 22. Sexo


@dataclass
class ATRecord:
    """Otros Servicios (AT) - Servicios de apoyo diagnóstico y terapéutico"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento: str  # 3. Tipo de documento
    num_documento: str  # 4. Número de documento
    num_autorizacion: str  # 5. Número de autorización
    tipo_servicio: str  # 6. Tipo de servicio
    cod_servicio: str  # 7. Código del servicio (CUPS)
    cod_servicio_sistema: str  # 8. Código del servicio del sistema
    descripcion_servicio: str  # 9. Descripción del servicio
    cantidad: str  # 10. Cantidad
    valor_unitario: str  # 11. Valor unitario
    valor_total: str  # 12. Valor total
    valor_cuota_moderadora: str  # 13. Valor cuota moderadora
    valor_neto: str  # 14. Valor neto


@dataclass
class AHRecord:
    """Hospitalización (AH) - Registro de hospitalizaciones"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento: str  # 3. Tipo de documento
    num_documento: str  # 4. Número de documento
    via_ingreso: str  # 5. Vía de ingreso
    fecha_ingreso: str  # 6. Fecha de ingreso
    hora_ingreso: str  # 7. Hora de ingreso
    num_autorizacion: str  # 8. Número de autorización
    causa_externa: str  # 9. Causa externa
    diagnostico_ingreso: str  # 10. Diagnóstico de ingreso (CIE10)
    diagnostico_egreso: str  # 11. Diagnóstico de egreso (CIE10)
    diagnostico_relacionado1: str  # 12. Diagnóstico relacionado 1
    diagnostico_relacionado2: str  # 13. Diagnóstico relacionado 2
    diagnostico_relacionado3: str  # 14. Diagnóstico relacionado 3
    diagnostico_complicacion: str  # 15. Diagnóstico de complicación
    estado_salida: str  # 16. Estado a la salida
    diagnostico_muerte: str  # 17. Diagnóstico de muerte
    fecha_egreso: str  # 18. Fecha de egreso
    hora_egreso: str  # 19. Hora de egreso
    valor_hospitalizacion: str  # 20. Valor hospitalización
    valor_cuota_moderadora: str  # 21. Valor cuota moderadora
    valor_neto: str  # 22. Valor neto


@dataclass
class AMRecord:
    """Medicamentos (AM) - Registro de medicamentos dispensados"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento: str  # 3. Tipo de documento
    num_documento: str  # 4. Número de documento
    num_autorizacion: str  # 5. Número de autorización
    cod_medicamento: str  # 6. Código del medicamento (CUM)
    tipo_medicamento: str  # 7. Tipo de medicamento
    nombre_medicamento: str  # 8. Nombre del medicamento
    forma_farmaceutica: str  # 9. Forma farmacéutica
    concentracion: str  # 10. Concentración
    unidad_medida: str  # 11. Unidad de medida
    numero_unidades: str  # 12. Número de unidades
    valor_unitario: str  # 13. Valor unitario
    valor_total: str  # 14. Valor total
    valor_cuota_moderadora: str  # 15. Valor cuota moderadora
    valor_neto: str  # 16. Valor neto


@dataclass
class ANRecord:
    """Recién Nacidos (AN) - Registro de recién nacidos"""
    num_factura: str  # 1. Número de factura
    cod_prestador: str  # 2. Código del prestador
    tipo_documento_madre: str  # 3. Tipo de documento de la madre
    num_documento_madre: str  # 4. Número de documento de la madre
    fecha_nacimiento: str  # 5. Fecha de nacimiento
    hora_nacimiento: str  # 6. Hora de nacimiento
    edad_gestacional: str  # 7. Edad gestacional
    control_prenatal: str  # 8. Control prenatal
    sexo: str  # 9. Sexo
    peso: str  # 10. Peso al nacer
    diagnostico_recien_nacido: str  # 11. Diagnóstico del recién nacido (CIE10)
    diagnostico_relacionado: str  # 12. Diagnóstico relacionado
    complicacion: str  # 13. Complicación
    tipo_parto: str  # 14. Tipo de parto


@dataclass
class CTRecord:
    """Control (CT) - Archivo de control"""
    cod_prestador: str  # 1. Código del prestador
    fecha_remision: str  # 2. Fecha de remisión
    num_registros_af: str  # 3. Número de registros AF
    num_registros_us: str  # 4. Número de registros US
    num_registros_ac: str  # 5. Número de registros AC
    num_registros_ap: str  # 6. Número de registros AP
    num_registros_at: str  # 7. Número de registros AT
    num_registros_ah: str  # 8. Número de registros AH
    num_registros_am: str  # 9. Número de registros AM
    num_registros_an: str  # 10. Número de registros AN
