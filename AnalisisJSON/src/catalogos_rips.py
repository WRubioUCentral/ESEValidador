"""
Catálogos y constantes para análisis RIPS según Resolución 2275 de 2023
"""

# ============================================================================
# CÓDIGOS CIE-10 PARA GESTACIÓN Y SALUD MATERNA
# ============================================================================
CODIGOS_GESTACION = {
    # Capítulo O: Embarazo, parto y puerperio
    "O00": "Embarazo ectópico",
    "O01": "Mola hidatiforme",
    "O02": "Otros productos anormales de la concepción",
    "O03": "Aborto espontáneo",
    "O04": "Aborto médico",
    "O05": "Otro aborto",
    "O06": "Aborto no especificado",
    "O07": "Intento fallido de aborto",
    "O08": "Complicaciones consecutivas al aborto y al embarazo ectópico y molar",
    "O10": "Hipertensión preexistente que complica el embarazo, el parto y el puerperio",
    "O11": "Trastornos hipertensivos preexistentes, con proteinuria agregada",
    "O12": "Edema y proteinuria gestacionales [inducidos por el embarazo], sin hipertensión",
    "O13": "Hipertensión gestacional [inducida por el embarazo] sin proteinuria significativa",
    "O14": "Hipertensión gestacional [inducida por el embarazo] con proteinuria significativa",
    "O15": "Eclampsia",
    "O16": "Hipertensión materna no especificada",
    "O20": "Hemorragia precoz del embarazo",
    "O21": "Vómitos excesivos en el embarazo",
    "O22": "Complicaciones venosas en el embarazo",
    "O23": "Infección de las vías genitourinarias en el embarazo",
    "O24": "Diabetes mellitus en el embarazo",
    "O25": "Desnutrición en el embarazo",
    "O26": "Atención a la madre por otras complicaciones principalmente relacionadas con el embarazo",
    "O28": "Hallazgos anormales en el examen prenatal de la madre",
    "O29": "Complicaciones de la anestesia administrada durante el embarazo",
    "O30": "Embarazo múltiple",
    "O31": "Complicaciones específicas del embarazo múltiple",
    "O32": "Atención materna por presentación anormal del feto, conocida o presunta",
    "O33": "Atención materna por desproporción conocida o presunta",
    "O34": "Atención materna por anormalidades conocidas o presuntas de los órganos pelvianos de la madre",
    "O35": "Atención materna por anormalidad o lesión fetal, conocida o presunta",
    "O36": "Atención materna por otros problemas fetales conocidos o presuntos",
    "O40": "Polihidramnios",
    "O41": "Otros trastornos del líquido amniótico y de las membranas",
    "O42": "Ruptura prematura de las membranas",
    "O43": "Trastornos placentarios",
    "O44": "Placenta previa",
    "O45": "Desprendimiento prematuro de la placenta",
    "O46": "Hemorragia anteparto no clasificada en otra parte",
    "O47": "Falso trabajo de parto",
    "O48": "Embarazo prolongado",
    "O60": "Parto prematuro",
    "O61": "Fracaso de la inducción del trabajo de parto",
    "O62": "Anormalidades de la contractilidad uterina",
    "O63": "Trabajo de parto prolongado",
    "O64": "Trabajo de parto obstruido debido a mala posición y presentación anormal del feto",
    "O65": "Trabajo de parto obstruido debido a anormalidad de la pelvis materna",
    "O66": "Otras obstrucciones del trabajo de parto",
    "O67": "Trabajo de parto y parto complicados por hemorragia intraparto, no clasificados en otra parte",
    "O68": "Trabajo de parto y parto complicados por sufrimiento fetal",
    "O69": "Trabajo de parto y parto complicados por problemas del cordón umbilical",
    "O70": "Desgarro perineal durante el parto",
    "O71": "Otro trauma obstétrico",
    "O72": "Hemorragia postparto",
    "O73": "Retención de la placenta y de las membranas, sin hemorragia",
    "O74": "Complicaciones de la anestesia administrada durante el trabajo de parto y el parto",
    "O75": "Otras complicaciones del trabajo de parto y del parto, no clasificadas en otra parte",
    "O80": "Parto único espontáneo",
    "O81": "Parto único con fórceps y ventosa extractora",
    "O82": "Parto único por cesárea",
    "O83": "Otros partos únicos asistidos",
    "O84": "Parto múltiple",
    "O85": "Sepsis puerperal",
    "O86": "Otras infecciones puerperales",
    "O87": "Complicaciones venosas en el puerperio",
    "O88": "Embolia obstétrica",
    "O89": "Complicaciones de la anestesia administrada durante el puerperio",
    "O90": "Complicaciones del puerperio, no clasificadas en otra parte",
    "O91": "Infecciones de la mama asociadas con el parto",
    "O92": "Otros trastornos de la mama y de la lactancia asociados con el parto",
    "O94": "Secuelas de complicaciones del embarazo, parto y puerperio",
    "O95": "Muerte obstétrica de causa no especificada",
    "O96": "Muerte materna debida a cualquier causa obstétrica que ocurre después de 42 días pero antes de un año del parto",
    "O97": "Muerte por secuelas de causas obstétricas directas",
    "O98": "Enfermedades maternas infecciosas y parasitarias clasificables en otra parte, pero que complican el embarazo, el parto y el puerperio",
    "O99": "Otras enfermedades maternas clasificables en otra parte, pero que complican el embarazo, el parto y el puerperio",

    # Capítulo Z: Códigos relacionados con embarazo
    "Z30": "Atención para la anticoncepción",
    "Z31": "Atención para la procreación",
    "Z32": "Examen y prueba del embarazo",
    "Z33": "Estado de embarazo, incidental",
    "Z34": "Supervisión de embarazo normal",
    "Z35": "Supervisión de embarazo de alto riesgo",
    "Z36": "Tamizaje prenatal",
    "Z37": "Resultado del parto",
    "Z38": "Nacidos vivos según lugar de nacimiento",
    "Z39": "Atención y examen postparto",
}

# Prefijos para identificación rápida
PREFIJOS_GESTACION = ["O", "Z3"]

# Finalidades relacionadas con salud materna (Resolución 2275/2023)
FINALIDADES_SALUD_MATERNA = {
    "10": "Atención del parto (incluye puerperio)",
    "11": "Atención del recién nacido",
    "12": "Atención en planificación familiar",
    "15": "Detección de alteraciones del embarazo",
}

# ============================================================================
# ENFERMEDADES CRÓNICAS NO TRANSMISIBLES (ECNT)
# ============================================================================
CODIGOS_ENFERMEDADES_CRONICAS = {
    # Diabetes
    "E10": "Diabetes mellitus insulinodependiente",
    "E11": "Diabetes mellitus no insulinodependiente",
    "E12": "Diabetes mellitus asociada con desnutrición",
    "E13": "Otras diabetes mellitus especificadas",
    "E14": "Diabetes mellitus, no especificada",

    # Hipertensión
    "I10": "Hipertensión esencial (primaria)",
    "I11": "Enfermedad cardíaca hipertensiva",
    "I12": "Enfermedad renal hipertensiva",
    "I13": "Enfermedad cardíaca y renal hipertensiva",
    "I15": "Hipertensión secundaria",

    # Enfermedades cardiovasculares
    "I20": "Angina de pecho",
    "I21": "Infarto agudo del miocardio",
    "I22": "Infarto del miocardio recurrente",
    "I25": "Enfermedad isquémica crónica del corazón",
    "I50": "Insuficiencia cardíaca",
    "I51": "Complicaciones y descripciones mal definidas de enfermedad cardíaca",

    # Enfermedades cerebrovasculares
    "I60": "Hemorragia subaracnoidea",
    "I61": "Hemorragia intraencefálica",
    "I63": "Infarto cerebral",
    "I64": "Accidente vascular encefálico agudo, no especificado como hemorrágico o isquémico",

    # EPOC
    "J40": "Bronquitis, no especificada como aguda o crónica",
    "J41": "Bronquitis crónica simple y mucopurulenta",
    "J42": "Bronquitis crónica no especificada",
    "J43": "Enfisema",
    "J44": "Otras enfermedades pulmonares obstructivas crónicas",

    # Enfermedad renal crónica
    "N18": "Enfermedad renal crónica",
    "N19": "Insuficiencia renal no especificada",

    # Cáncer (ejemplos principales)
    "C50": "Tumor maligno de la mama",
    "C53": "Tumor maligno del cuello del útero",
    "C61": "Tumor maligno de la próstata",
    "C18": "Tumor maligno del colon",
    "C34": "Tumor maligno de los bronquios y del pulmón",
}

PREFIJOS_ENFERMEDADES_CRONICAS = ["E10", "E11", "E12", "E13", "E14", "I10", "I11", "I12", "I13", "I15",
                                   "I20", "I21", "I25", "I50", "I60", "I61", "I63", "I64",
                                   "J40", "J41", "J42", "J43", "J44", "N18", "N19"]

# ============================================================================
# EVENTOS DE INTERÉS EN SALUD PÚBLICA
# ============================================================================
CODIGOS_EVENTOS_SALUD_PUBLICA = {
    # Enfermedades transmisibles de notificación obligatoria
    "A00": "Cólera",
    "A01": "Fiebres tifoidea y paratifoidea",
    "A15": "Tuberculosis respiratoria",
    "A16": "Tuberculosis respiratoria, sin confirmación bacteriológica o histológica",
    "A17": "Tuberculosis del sistema nervioso",
    "A18": "Tuberculosis de otros órganos",
    "A19": "Tuberculosis miliar",
    "A33": "Tétanos neonatal",
    "A35": "Otros tétanos",
    "A36": "Difteria",
    "A37": "Tos ferina",
    "A80": "Poliomielitis aguda",
    "A82": "Rabia",
    "A90": "Fiebre del dengue [dengue clásico]",
    "A91": "Fiebre del dengue hemorrágico",
    "A92": "Otras fiebres virales transmitidas por mosquitos",
    "B01": "Varicela",
    "B05": "Sarampión",
    "B06": "Rubéola [sarampión alemán]",
    "B15": "Hepatitis aguda tipo A",
    "B16": "Hepatitis aguda tipo B",
    "B17": "Otras hepatitis virales agudas",
    "B18": "Hepatitis viral crónica",
    "B20": "Enfermedad por virus de la inmunodeficiencia humana [VIH]",
    "B24": "Enfermedad por virus de la inmunodeficiencia humana [VIH], sin otra especificación",
    "B50": "Paludismo [malaria] debido a Plasmodium falciparum",
    "B51": "Paludismo [malaria] debido a Plasmodium vivax",
    "B54": "Paludismo [malaria] no especificado",
}

# ============================================================================
# CAUSAS EXTERNAS Y VIOLENCIAS
# ============================================================================
CODIGOS_CAUSAS_EXTERNAS = {
    "V01-V99": "Accidentes de transporte",
    "W00-W19": "Caídas",
    "W20-W49": "Exposición a fuerzas mecánicas inanimadas",
    "W50-W64": "Exposición a fuerzas mecánicas animadas",
    "W65-W74": "Ahogamiento y sumersión accidentales",
    "W75-W84": "Otros riesgos accidentales de la respiración",
    "W85-W99": "Exposición a la corriente eléctrica, radiación, y temperaturas extremas",
    "X00-X09": "Exposición al humo, fuego y llamas",
    "X10-X19": "Contacto con fuente de calor o sustancias calientes",
    "X40-X49": "Envenenamiento accidental",
    "X60-X84": "Lesiones autoinfligidas intencionalmente",
    "X85-Y09": "Agresiones",
    "Y10-Y34": "Eventos de intención no determinada",
}

# ============================================================================
# CATÁLOGO COMPLETO DE FINALIDADES (Resolución 2275/2023)
# ============================================================================
FINALIDADES_TECNOLOGIA_SALUD = {
    "01": "Diagnóstico",
    "02": "Tratamiento",
    "03": "Protección específica",
    "04": "Detección temprana de enfermedad general",
    "05": "Detección temprana de enfermedad profesional",
    "06": "Protección específica y detección temprana de enfermedad general",
    "07": "Protección específica y detección temprana de enfermedad profesional",
    "08": "Protección específica, detección temprana de enfermedad general y profesional",
    "09": "Atención de planificación familiar y anticoncepción",
    "10": "Atención del parto (incluye puerperio)",
    "11": "Atención del recién nacido",
    "12": "Atención en planificación familiar",
    "13": "Detección de alteraciones de crecimiento y desarrollo del menor de 10 años",
    "14": "Detección de alteraciones del desarrollo joven (10 a 29 años)",
    "15": "Detección de alteraciones del embarazo",
    "16": "Detección de alteraciones del adulto (mayor a 45 años)",
    "17": "Detección de alteraciones de agudeza visual",
    "18": "Detección de cáncer de cuello uterino",
    "19": "Detección de cáncer seno",
    "20": "Detección de alteraciones del adulto mayor (mayor a 60 años)",
}

# ============================================================================
# CATÁLOGO COMPLETO DE CAUSAS DE ATENCIÓN (Resolución 2275/2023)
# ============================================================================
CAUSAS_ATENCION = {
    "01": "Accidente de trabajo",
    "02": "Accidente de tránsito",
    "03": "Accidente rábico",
    "04": "Accidente ofídico",
    "05": "Otro tipo de accidente",
    "06": "Evento catastrófico de origen natural",
    "07": "Lesión por agresión",
    "08": "Lesión autoinfligida",
    "09": "Sospecha de maltrato físico",
    "10": "Sospecha de abuso sexual",
    "11": "Sospecha de violencia sexual",
    "12": "Sospecha de maltrato emocional",
    "13": "Enfermedad general",
    "14": "Enfermedad profesional",
    "15": "Otra",
    "16": "Promoción y prevención",
    "17": "Patología asociada a consumo de sustancias psicoactivas",
    "18": "Lesión por accidente deportivo",
    "19": "Lesión por accidente escolar",
    "20": "Lesión por accidente doméstico",
    "21": "Lesión por accidente recreativo",
    "22": "Lesión en el lugar de residencia",
    "23": "Lesión en el lugar de trabajo",
    "24": "Lesión en la vía pública",
    "25": "Lesión en otro lugar",
    "26": "Planificación familiar",
    "27": "Control prenatal",
    "28": "Control de crecimiento y desarrollo",
    "29": "Vacunación",
    "30": "Odontología",
    "31": "Otro",
    "32": "Lesión por pólvora",
    "33": "Intoxicación por medicamentos",
    "34": "Intoxicación por sustancias psicoactivas",
    "35": "Intoxicación por plaguicidas",
    "36": "Intoxicación por otras sustancias químicas",
    "37": "Intoxicación por alimentos",
    "38": "Promoción y prevención",
    "39": "Infección respiratoria aguda",
    "40": "Enfermedad diarreica aguda",
}

# ============================================================================
# RUTAS DE VIDA (Resolución 3280 de 2018)
# ============================================================================
RUTAS_VIDA = {
    "primera_infancia": {"nombre": "Primera infancia", "rango": (0, 5), "descripcion": "0 a 5 años"},
    "infancia": {"nombre": "Infancia", "rango": (6, 11), "descripcion": "6 a 11 años"},
    "adolescencia": {"nombre": "Adolescencia", "rango": (12, 17), "descripcion": "12 a 17 años"},
    "juventud": {"nombre": "Juventud", "rango": (18, 28), "descripcion": "18 a 28 años"},
    "adultez": {"nombre": "Adultez", "rango": (29, 59), "descripcion": "29 a 59 años"},
    "vejez": {"nombre": "Vejez", "rango": (60, 150), "descripcion": "60 años o más"},
}

# ============================================================================
# MODALIDADES DE ATENCIÓN (Resolución 2275/2023)
# ============================================================================
MODALIDADES_ATENCION = {
    "01": "Intramural",
    "02": "Extramural unidad móvil",
    "03": "Extramural domiciliaria",
    "04": "Extramural jornada de salud",
    "05": "Telemedicina interactiva",
    "06": "Telemedicina no interactiva",
    "07": "Telexperticia",
    "08": "Telemonitoreo",
}

# ============================================================================
# TIPOS DE DIAGNÓSTICO (Resolución 2275/2023)
# ============================================================================
TIPOS_DIAGNOSTICO = {
    "01": "Impresión diagnóstica",
    "02": "Confirmado nuevo",
    "03": "Confirmado repetido",
}

# ============================================================================
# UMBRALES PARA ALERTAS
# ============================================================================
UMBRALES_ALERTAS = {
    "servicios_sin_autorizacion": 10,  # % de servicios sin autorización
    "gestantes_adolescentes": 15,  # % de gestantes adolescentes
    "comorbilidades_altas": 30,  # % de pacientes con 3+ comorbilidades
    "reingreso_30dias": 10,  # % de reingresos en 30 días
    "enfermedades_cronicas": 40,  # % de pacientes con ECNT
}

# ============================================================================
# CÓDIGOS DE PROCEDIMIENTOS CUPS PRIORITARIOS
# ============================================================================
PROCEDIMIENTOS_PRIORITARIOS = {
    # Controles prenatales
    "890201": "Consulta de primera vez por medicina general",
    "890202": "Consulta de primera vez por especialista en ginecología y obstetricia",
    "890203": "Consulta de primera vez por especialista diferente a ginecología y obstetricia",
    "890301": "Consulta de control prenatal por medicina general",
    "890302": "Consulta de control prenatal por especialista",

    # Atención del parto
    "879101": "Parto vaginal espontáneo",
    "879102": "Parto vaginal asistido",
    "740101": "Cesárea",

    # Crecimiento y desarrollo
    "890701": "Consulta de primera vez para valoración integral y detección temprana de alteraciones del niño menor de 10 años",
    "890801": "Consulta de control de desarrollo y crecimiento del niño menor de 10 años",

    # Planificación familiar
    "890601": "Consulta de primera vez en planificación familiar",
    "890602": "Consulta de control en planificación familiar",
}

# ============================================================================
# GRUPOS DE RIESGO ESPECÍFICOS
# ============================================================================
GRUPOS_RIESGO = {
    "gestante_adolescente": "Gestante menor de 18 años",
    "gestante_mayor_35": "Gestante mayor de 35 años",
    "gestante_mayor_40": "Gestante de edad materna avanzada (>40 años)",
    "gestante_sin_control": "Gestante sin control prenatal",
    "menor_desnutrido": "Menor con diagnóstico de desnutrición",
    "adulto_mayor_fragil": "Adulto mayor de 75 años",
    "paciente_multimorbido": "Paciente con 3 o más comorbilidades",
    "paciente_oncologico": "Paciente con diagnóstico oncológico",
}
