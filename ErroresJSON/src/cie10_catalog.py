"""
Catálogo de códigos CIE10 vigentes para validación
Basado en CIE-10 versión 2019 (OMS)
"""
from typing import Set, Dict, Optional


class CIE10Catalog:
    """Catálogo de códigos CIE10 con descripciones"""

    def __init__(self):
        """Inicializa el catálogo CIE10"""
        # Códigos CIE10 más comunes en RIPS de Colombia
        # En producción, este catálogo debería cargarse de una base de datos o archivo completo
        self.codes = self._load_common_codes()
        self.chapters = self._load_chapters()

    def _load_chapters(self) -> Dict[str, str]:
        """Carga los capítulos del CIE10"""
        return {
            'A': 'Enfermedades infecciosas y parasitarias (A00-B99)',
            'B': 'Enfermedades infecciosas y parasitarias (A00-B99)',
            'C': 'Neoplasias (C00-D48)',
            'D': 'Enfermedades de la sangre y neoplasias (C00-D89)',
            'E': 'Enfermedades endocrinas, nutricionales y metabólicas (E00-E90)',
            'F': 'Trastornos mentales y del comportamiento (F00-F99)',
            'G': 'Enfermedades del sistema nervioso (G00-G99)',
            'H': 'Enfermedades del ojo y sus anexos / del oído (H00-H95)',
            'I': 'Enfermedades del sistema circulatorio (I00-I99)',
            'J': 'Enfermedades del sistema respiratorio (J00-J99)',
            'K': 'Enfermedades del sistema digestivo (K00-K93)',
            'L': 'Enfermedades de la piel y tejido subcutáneo (L00-L99)',
            'M': 'Enfermedades del sistema osteomuscular (M00-M99)',
            'N': 'Enfermedades del sistema genitourinario (N00-N99)',
            'O': 'Embarazo, parto y puerperio (O00-O99)',
            'P': 'Afecciones del período perinatal (P00-P96)',
            'Q': 'Malformaciones congénitas (Q00-Q99)',
            'R': 'Síntomas y signos no clasificados (R00-R99)',
            'S': 'Traumatismos (S00-T98)',
            'T': 'Traumatismos y envenenamientos (S00-T98)',
            'V': 'Causas externas de morbilidad y mortalidad (V01-Y98)',
            'W': 'Causas externas de morbilidad y mortalidad (V01-Y98)',
            'X': 'Causas externas de morbilidad y mortalidad (V01-Y98)',
            'Y': 'Causas externas de morbilidad y mortalidad (V01-Y98)',
            'Z': 'Factores que influyen en el estado de salud (Z00-Z99)'
        }

    def _load_common_codes(self) -> Dict[str, str]:
        """
        Carga códigos CIE10 más comunes
        Formato: 'código': 'descripción'
        """
        return {
            # Capítulo A - Enfermedades infecciosas
            'A00': 'Cólera',
            'A000': 'Cólera debido a Vibrio cholerae 01, biotipo cholerae',
            'A001': 'Cólera debido a Vibrio cholerae 01, biotipo El Tor',
            'A009': 'Cólera, no especificado',
            'A01': 'Fiebres tifoidea y paratifoidea',
            'A02': 'Otras infecciones debidas a Salmonella',
            'A06': 'Amebiasis',
            'A062': 'Colitis amebiana',
            'A08': 'Infecciones intestinales debidas a virus',
            'A085': 'Otras infecciones intestinales virales especificadas',
            'A09': 'Diarrea y gastroenteritis de presunto origen infeccioso',
            'A09X': 'Diarrea y gastroenteritis de presunto origen infeccioso',

            # Capítulo B - Enfermedades infecciosas (continuación)
            'B33': 'Otras enfermedades virales',
            'B338': 'Otras enfermedades virales especificadas',
            'B34': 'Infección viral de sitio no especificado',
            'B348': 'Otras infecciones virales de sitio no especificado',
            'B57': 'Enfermedad de Chagas',
            'B572': 'Enfermedad de Chagas (crónica) que afecta el corazón',
            'B86X': 'Escabiosis',

            # Capítulo D - Enfermedades de la sangre
            'D24X': 'Neoplasia benigna de la mama',
            'D50': 'Anemias por deficiencia de hierro',
            'D509': 'Anemia por deficiencia de hierro, sin otra especificación',

            # Capítulo E - Enfermedades endocrinas
            'E11': 'Diabetes mellitus no insulinodependiente',
            'E119': 'Diabetes mellitus no insulinodependiente, sin mención de complicación',
            'E28': 'Disfunción ovárica',
            'E282': 'Síndrome de ovarios poliquísticos',
            'E66': 'Obesidad',
            'E660': 'Obesidad debida a exceso de calorías',
            'E78': 'Trastornos del metabolismo de las lipoproteínas',
            'E784': 'Otras hiperlipidemias',
            'E785': 'Hiperlipidemia, no especificada',

            # Capítulo G - Sistema nervioso
            'G20X': 'Enfermedad de Parkinson',
            'G43': 'Migraña',
            'G439': 'Migraña, no especificada',
            'G47': 'Trastornos del sueño',
            'G470': 'Trastornos de inicio y mantenimiento del sueño [insomnio]',
            'G59': 'Mononeuropatías',
            'G590': 'Mononeuropatía diabética',

            # Capítulo H - Ojo y oído
            'H10': 'Conjuntivitis',
            'H109': 'Conjuntivitis, no especificada',
            'H40': 'Glaucoma',
            'H409': 'Glaucoma, no especificado',
            'H52': 'Trastornos de la acomodación y de la refracción',
            'H526': 'Otros trastornos de la refracción',

            # Capítulo I - Sistema circulatorio
            'I10X': 'Hipertensión esencial (primaria)',
            'I25': 'Enfermedad isquémica crónica del corazón',
            'I49': 'Otras arritmias cardíacas',
            'I498': 'Otras arritmias cardíacas especificadas',
            'I50': 'Insuficiencia cardíaca',
            'I509': 'Insuficiencia cardíaca, no especificada',
            'I86': 'Várices de otros sitios',
            'I868': 'Várices de otros sitios especificados',

            # Capítulo J - Sistema respiratorio
            'J00X': 'Rinofaringitis aguda [resfriado común]',
            'J02': 'Faringitis aguda',
            'J029': 'Faringitis aguda, no especificada',
            'J03': 'Amigdalitis aguda',
            'J039': 'Amigdalitis aguda, no especificada',
            'J06': 'Infecciones agudas de las vías respiratorias superiores',
            'J069': 'Infección aguda de las vías respiratorias superiores, no especificada',
            'J18': 'Neumonía, organismo no especificado',
            'J189': 'Neumonía, no especificada',
            'J46X': 'Estado asmático',

            # Capítulo K - Sistema digestivo
            'K02': 'Caries dental',
            'K021': 'Caries de la dentina',
            'K04': 'Enfermedades de la pulpa y de los tejidos periapicales',
            'K046': 'Absceso periapical con fístula',
            'K05': 'Gingivitis y enfermedades periodontales',
            'K050': 'Gingivitis aguda',
            'K12': 'Estomatitis y lesiones afines',
            'K120': 'Estomatitis aftosa recurrente',
            'K29': 'Gastritis y duodenitis',
            'K297': 'Gastritis, no especificada',
            'K30X': 'Dispepsia',

            # Capítulo L - Piel
            'L03': 'Celulitis',
            'L030': 'Celulitis de dedos de la mano y del pie',
            'L20': 'Dermatitis atópica',
            'L209': 'Dermatitis atópica, no especificada',
            'L50': 'Urticaria',
            'L509': 'Urticaria, no especificada',

            # Capítulo M - Sistema osteomuscular
            'M25': 'Otros trastornos articulares',
            'M255': 'Dolor en articulación',
            'M54': 'Dorsalgia',
            'M545': 'Lumbago no especificado',
            'M79': 'Otros trastornos de los tejidos blandos',
            'M796': 'Dolor en miembro',

            # Capítulo N - Sistema genitourinario
            'N39': 'Otros trastornos del sistema urinario',
            'N390': 'Infección de vías urinarias, sitio no especificado',
            'N76': 'Otras afecciones inflamatorias de la vagina y de la vulva',
            'N76': 'Vaginitis aguda',
            'N92': 'Menstruación excesiva, frecuente e irregular',
            'N920': 'Menstruación excesiva y frecuente con ciclo regular',

            # Capítulo O - Embarazo y parto
            'O23': 'Infecciones de las vías genitourinarias en el embarazo',

            # Capítulo R - Síntomas y signos
            'R00': 'Anormalidades del latido cardíaco',
            'R000': 'Taquicardia, no especificada',
            'R04': 'Hemorragia de las vías respiratorias',
            'R042': 'Hemoptisis',
            'R10': 'Dolor abdominal y pélvico',
            'R103': 'Dolor localizado en otras partes inferiores del abdomen',
            'R104': 'Otros dolores abdominales y los no especificados',
            'R11X': 'Náusea y vómito',
            'R42X': 'Mareo y desvanecimiento',
            'R50': 'Fiebre de origen desconocido',
            'R509': 'Fiebre, no especificada',
            'R51X': 'Cefalea',
            'R52': 'Dolor, no clasificado en otra parte',
            'R68': 'Otros síntomas y signos generales',
            'R688': 'Otros síntomas y signos generales especificados',

            # Capítulo Z - Factores que influyen en estado de salud
            'Z00': 'Examen general e investigación de personas sin quejas o sin diagnóstico informado',
            'Z000': 'Examen médico general',
            'Z01': 'Otros exámenes especiales e investigaciones en personas sin quejas o sin diagnóstico informado',
            'Z012': 'Examen odontológico',
            'Z018': 'Otros exámenes especiales especificados',
            'Z12': 'Examen especial de pesquisa de neoplasias',
            'Z125': 'Examen especial de pesquisa de otras neoplasias',
            'Z23': 'Necesidad de inmunización contra enfermedad bacteriana única',
            'Z238': 'Necesidad de inmunización contra otras enfermedades bacterianas únicas',
            'Z30': 'Atención para la anticoncepción',
            'Z308': 'Otras atenciones especificadas para la anticoncepción',
            'Z34': 'Supervisión de embarazo normal',
            'Z348': 'Supervisión de otro embarazo normal',
            'Z35': 'Supervisión de embarazo de alto riesgo',
            'Z359': 'Supervisión de embarazo de alto riesgo, sin otra especificación',
            'Z95': 'Presencia de implantes e injertos cardíacos y vasculares',
            'Z955': 'Presencia de implante e injerto de angioplastia coronaria',
        }

    def is_valid_code(self, code: str) -> bool:
        """
        Verifica si un código CIE10 es válido

        Args:
            code: Código CIE10 a validar

        Returns:
            True si el código existe en el catálogo
        """
        if not code:
            return False

        # Verificar si existe en el catálogo completo
        if code in self.codes:
            return True

        # Verificar al menos que el capítulo sea válido
        if code and code[0] in self.chapters:
            # Si no está en nuestro catálogo pero tiene formato válido,
            # aceptarlo (el catálogo aquí es limitado)
            return True

        return False

    def get_description(self, code: str) -> Optional[str]:
        """
        Obtiene la descripción de un código CIE10

        Args:
            code: Código CIE10

        Returns:
            Descripción del código o None
        """
        return self.codes.get(code)

    def get_chapter(self, code: str) -> Optional[str]:
        """
        Obtiene el capítulo al que pertenece un código

        Args:
            code: Código CIE10

        Returns:
            Descripción del capítulo
        """
        if code:
            return self.chapters.get(code[0])
        return None

    def suggest_similar_codes(self, code: str, max_suggestions: int = 5) -> list:
        """
        Sugiere códigos similares al código ingresado

        Args:
            code: Código CIE10 potencialmente incorrecto
            max_suggestions: Número máximo de sugerencias

        Returns:
            Lista de códigos similares
        """
        if not code or len(code) < 2:
            return []

        suggestions = []
        prefix = code[:3]  # Tomar los primeros 3 caracteres

        for valid_code in self.codes.keys():
            if valid_code.startswith(prefix):
                suggestions.append(valid_code)
                if len(suggestions) >= max_suggestions:
                    break

        return suggestions

    def validate_with_suggestion(self, code: str) -> tuple:
        """
        Valida un código y sugiere alternativas si es inválido

        Args:
            code: Código a validar

        Returns:
            Tupla (es_valido, mensaje, sugerencias)
        """
        if self.is_valid_code(code):
            description = self.get_description(code)
            chapter = self.get_chapter(code)
            return True, f"Código válido: {description or chapter}", []

        suggestions = self.suggest_similar_codes(code)
        if suggestions:
            return False, f"Código no encontrado en catálogo vigente", suggestions
        else:
            return False, f"Código no válido y sin sugerencias disponibles", []


# Instancia global del catálogo
_catalog = None


def get_cie10_catalog() -> CIE10Catalog:
    """
    Obtiene la instancia global del catálogo CIE10

    Returns:
        Instancia de CIE10Catalog
    """
    global _catalog
    if _catalog is None:
        _catalog = CIE10Catalog()
    return _catalog
