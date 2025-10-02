# validador_completo.py
import pandas as pd
import re
from datetime import datetime, timedelta
from errores import ERRORES
from config import TIPOS_IDENTIFICACION

class ValidadorESE:
    """Validador completo para archivos ESE según especificaciones"""
    
    def __init__(self):
        self.errores = []
        self.warnings = []
    
    def calcular_edad(self, fecha_nacimiento, fecha_referencia):
        """Calcula la edad en años entre dos fechas"""
        if pd.isna(fecha_nacimiento) or pd.isna(fecha_referencia):
            return None
        
        try:
            fecha_nac = pd.to_datetime(fecha_nacimiento)
            fecha_ref = pd.to_datetime(fecha_referencia)
            return (fecha_ref - fecha_nac).days / 365.25
        except:
            return None
    
    def validar_fecha_formato(self, fecha_str):
        """Valida que la fecha tenga formato AAAA-MM-DD"""
        if pd.isna(fecha_str):
            return True
        
        try:
            datetime.strptime(str(fecha_str), '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def validar_caracteres_permitidos(self, texto):
        """Valida que solo contenga números 0-9 y letras A-Z (sin Ñ)"""
        if pd.isna(texto):
            return True
        
        patron = r'^[0-9A-Z]*$'
        return bool(re.match(patron, str(texto).upper()))
    
    def agregar_error(self, id_usuario, dato_erroneo, codigo, explicacion):
        """Agrega un error a la lista"""
        self.errores.append({
            "usuario": id_usuario,
            "dato_erroneo": dato_erroneo,
            "codigo": codigo,
            "explicacion": explicacion
        })
    
    def agregar_warning(self, id_usuario, dato_erroneo, codigo, explicacion):
        """Agrega un warning a la lista"""
        self.warnings.append({
            "usuario": id_usuario,
            "dato_erroneo": dato_erroneo,
            "codigo": codigo,
            "explicacion": explicacion
        })
    
    # ======================
    # VALIDACIONES POR COLUMNA
    # ======================
    
    def validar_columna_0(self, fila):
        """Columna 0: Tipo de registro debe ser 2"""
        valor = fila.iloc[0]
        id_usuario = fila.iloc[4]
        
        if valor != 2:
            self.agregar_error(id_usuario, valor, "Error001", "La columna 0 debe tener valor 2")
    
    def validar_columna_1(self, fila, numero_registro):
        """Columna 1: Número consecutivo"""
        valor = fila.iloc[1]
        id_usuario = fila.iloc[4]
        
        if valor != numero_registro:
            self.agregar_error(id_usuario, valor, "Error002", f"El número consecutivo debe ser {numero_registro}")
    
    def validar_columna_2(self, fila):
        """Columna 2: Código IPS"""
        valor = fila.iloc[2]
        id_usuario = fila.iloc[4]
        
        if valor != 999 and pd.isna(valor):
            self.agregar_error(id_usuario, valor, "Error021", ERRORES["Error021"])
    
    def validar_columna_3(self, fila):
        """Columna 3: Tipo de identificación"""
        valor = fila.iloc[3]
        id_usuario = fila.iloc[4]
        
        valores_permitidos = TIPOS_IDENTIFICACION
        
        if valor not in valores_permitidos:
            self.agregar_error(id_usuario, valor, "Error003", f"Tipo de identificación debe ser uno de: {valores_permitidos}")
    
    def validar_columna_4(self, fila):
        """Columna 4: Número de identificación"""
        tipo_id = fila.iloc[3]
        numero_id = fila.iloc[4]
        
        # Error220: Validar caracteres permitidos
        if not self.validar_caracteres_permitidos(numero_id):
            self.agregar_error(numero_id, numero_id, "Error220", ERRORES["Error220"])
        
        # Error676: Validar longitud según tipo de identificación
        if pd.notna(numero_id) and pd.notna(tipo_id):
            longitud = len(str(numero_id))
            
            if ((tipo_id == 'CC' and longitud > 10) or
                (tipo_id == 'TI' and longitud > 11) or
                (tipo_id == 'CE' and (longitud < 3 or longitud > 7)) or
                (tipo_id == 'CD' and longitud > 11) or
                (tipo_id == 'PA' and (longitud < 3 or longitud > 16)) or
                (tipo_id == 'SC' and longitud > 9) or
                (tipo_id == 'PE' and (longitud < 3 or longitud > 15))):
                
                self.agregar_error(numero_id, numero_id, "Error676", ERRORES["Error676"])
    
    def validar_columna_9(self, fila, fecha_corte):
        """Columna 9: Fecha de nacimiento"""
        fecha_nacimiento = fila.iloc[9]
        id_usuario = fila.iloc[4]
        
        # Error020: La fecha de nacimiento es requerida
        if pd.isna(fecha_nacimiento):
            self.agregar_error(id_usuario, fecha_nacimiento, "Error020", ERRORES["Error020"])
            return
        
        # Error421: Validar contenido de fecha
        if not self.validar_fecha_formato(fecha_nacimiento):
            self.agregar_error(id_usuario, fecha_nacimiento, "Error421", ERRORES["Error421"])
        
        # Error677: No se permiten comodines
        comodines_no_permitidos = ['1800-01-01', '1805-01-01', '1810-01-01', '1825-01-01', '1830-01-01', '1835-01-01', '1845-01-01']
        if str(fecha_nacimiento) in comodines_no_permitidos:
            self.agregar_error(id_usuario, fecha_nacimiento, "Error677", ERRORES["Error677"])
        
        # Error120: Fecha de nacimiento mayor a fecha de corte
        try:
            if pd.to_datetime(fecha_nacimiento) > pd.to_datetime(fecha_corte):
                self.agregar_error(id_usuario, fecha_nacimiento, "Error120", ERRORES["Error120"])
        except:
            pass
    
    def validar_columna_10(self, fila):
        """Columna 10: Sexo"""
        sexo = fila.iloc[10]
        id_usuario = fila.iloc[4]
        
        if sexo not in ['F', 'M']:
            self.agregar_error(id_usuario, sexo, "Error004", "El sexo debe ser F o M")
    
    def validar_columna_14(self, fila, fecha_corte):
        """Columna 14: Gestante"""
        gestante = fila.iloc[14]
        sexo = fila.iloc[10]
        fecha_nacimiento = fila.iloc[9]
        id_usuario = fila.iloc[4]
        
        edad = self.calcular_edad(fecha_nacimiento, fecha_corte)
        
        # Error030: Si registra 1, 2 ó 21 en gestante, el sexo debe ser F
        if gestante in [1, 2, 21] and sexo != 'F':
            self.agregar_error(id_usuario, gestante, "Error030", ERRORES["Error030"])
        
        # Error222: Si la edad < 10 años o >= 60 años, gestación no aplica
        if edad is not None and (edad < 10 or edad >= 60) and gestante != 0:
            self.agregar_error(id_usuario, gestante, "Error222", ERRORES["Error222"])
        
        # Error223: Si sexo F y edad entre 10-59 años, debe registrar valor diferente de 0
        if sexo == 'F' and edad is not None and 10 <= edad < 60 and gestante == 0:
            self.agregar_error(id_usuario, gestante, "Error223", ERRORES["Error223"])
        
        # Validaciones relacionadas con gestación
        if len(fila) > 23:
            var_23 = fila.iloc[23] if len(fila) > 23 else None
            var_35 = fila.iloc[35] if len(fila) > 35 else None
            var_59 = fila.iloc[59] if len(fila) > 59 else None
            var_60 = fila.iloc[60] if len(fila) > 60 else None
            var_61 = fila.iloc[61] if len(fila) > 61 else None
            var_33 = fila.iloc[33] if len(fila) > 33 else None
            var_56 = fila.iloc[56] if len(fila) > 56 else None
            var_58 = fila.iloc[58] if len(fila) > 58 else None
            
            # Error244: Si no es gestante, variables relacionadas deben ser "No aplica"
            if gestante != 1:
                if (var_23 not in [0, None] or var_35 not in [0, None] or var_59 not in [0, None] or 
                    var_60 not in [0, None] or var_61 not in [0, None] or 
                    str(var_33) != '1845-01-01' or str(var_56) != '1845-01-01' or str(var_58) != '1845-01-01'):
                    self.agregar_error(id_usuario, gestante, "Error244", ERRORES["Error244"])
            
            # Error379: Si es gestante, variables relacionadas deben tener datos
            if gestante == 1:
                if (var_23 == 0 or var_35 == 0 or var_59 == 0 or var_60 == 0 or var_61 == 0 or
                    str(var_33) == '1845-01-01' or str(var_56) == '1845-01-01' or str(var_58) == '1845-01-01'):
                    self.agregar_error(id_usuario, gestante, "Error379", ERRORES["Error379"])
    
    def validar_columna_15(self, fila):
        """Columna 15: Sífilis gestacional"""
        valor = fila.iloc[15]
        id_usuario = fila.iloc[4]
        
        if valor != 0:
            self.agregar_error(id_usuario, valor, "Error500", ERRORES["Error500"])
    
    def validar_columna_16(self, fila, fecha_corte):
        """Columna 16: Resultado prueba mini-mental"""
        resultado = fila.iloc[16]
        fecha_nacimiento = fila.iloc[9]
        fecha_valoracion = fila.iloc[52] if len(fila) > 52 else None
        id_usuario = fila.iloc[4]
        
        edad = self.calcular_edad(fecha_nacimiento, fecha_corte)
        
        # Error503: Si registra resultado, debe registrar fecha de valoración integral válida
        if resultado in [4, 5] and (pd.isna(fecha_valoracion) or str(fecha_valoracion) <= '1900-01-01'):
            self.agregar_error(id_usuario, resultado, "Error503", ERRORES["Error503"])
        
        # Error504: Valores permitidos
        if resultado not in [0, 4, 5, 21]:
            self.agregar_error(id_usuario, resultado, "Error504", ERRORES["Error504"])
        
        # Error227: Validar según edad
        if edad is not None:
            if (resultado in [4, 5, 21] and edad < 60) or (resultado == 0 and edad >= 60):
                self.agregar_error(id_usuario, resultado, "Error227", ERRORES["Error227"])
    
    def validar_columna_17(self, fila):
        """Columna 17: Hipotiroidismo congénito"""
        valor = fila.iloc[17]
        id_usuario = fila.iloc[4]
        
        if valor != 0:
            self.agregar_error(id_usuario, valor, "Error505", ERRORES["Error505"])
    
    def validar_columna_18(self, fila):
        """Columna 18: Sintomático respiratorio"""
        sintomatico = fila.iloc[18]
        resultado_bacilo = fila.iloc[113] if len(fila) > 113 else None
        fecha_bacilo = fila.iloc[112] if len(fila) > 112 else None
        id_usuario = fila.iloc[4]
        
        # Error232: Si es sintomático respiratorio
        if sintomatico == 1 and (resultado_bacilo == 4 or str(fecha_bacilo) == '1845-01-01'):
            self.agregar_error(id_usuario, sintomatico, "Error232", ERRORES["Error232"])
        
        # Error506: Si no es sintomático respiratorio
        if sintomatico == 2 and (resultado_bacilo != 4 or str(fecha_bacilo) != '1845-01-01'):
            self.agregar_error(id_usuario, sintomatico, "Error506", ERRORES["Error506"])
        
        # Error507: Riesgo no evaluado
        if sintomatico == 21 and (resultado_bacilo != 21 or str(fecha_bacilo) != '1800-01-01'):
            self.agregar_error(id_usuario, sintomatico, "Error507", ERRORES["Error507"])
    
    def validar_columna_19(self, fila, fecha_corte):
        """Columna 19: Consumo de tabaco"""
        consumo_tabaco = fila.iloc[19]
        fecha_nacimiento = fila.iloc[9]
        id_usuario = fila.iloc[4]
        
        edad = self.calcular_edad(fecha_nacimiento, fecha_corte)
        
        # Error508: Si edad < 12 años, no aplica
        if edad is not None and edad < 12 and consumo_tabaco != 98:
            self.agregar_error(id_usuario, consumo_tabaco, "Error508", ERRORES["Error508"])
    
    def validar_columna_20(self, fila):
        """Columna 20: Lepra"""
        valor = fila.iloc[20]
        id_usuario = fila.iloc[4]
        
        if valor != 21:
            self.agregar_error(id_usuario, valor, "Error509", ERRORES["Error509"])
    
    def validar_columna_21(self, fila):
        """Columna 21: Obesidad o desnutrición"""
        valor = fila.iloc[21]
        id_usuario = fila.iloc[4]
        
        if valor != 21:
            self.agregar_error(id_usuario, valor, "Error510", ERRORES["Error510"])
    
    def validar_columna_22(self, fila, fecha_corte):
        """Columna 22: Resultado tacto rectal"""
        resultado = fila.iloc[22]
        sexo = fila.iloc[10]
        fecha_nacimiento = fila.iloc[9]
        fecha_tacto = fila.iloc[64] if len(fila) > 64 else None
        id_usuario = fila.iloc[4]
        
        edad = self.calcular_edad(fecha_nacimiento, fecha_corte)
        
        # Error037: Si registra resultado, sexo debe ser M
        if resultado in [4, 5, 21] and sexo != 'M':
            self.agregar_error(id_usuario, resultado, "Error037", ERRORES["Error037"])
        
        # Error038: Si es hombre < 40 años, debe registrar no aplica
        if sexo == 'M' and edad is not None and edad < 40 and (resultado != 0 or str(fecha_tacto) != '1845-01-01'):
            self.agregar_error(id_usuario, resultado, "Error038", ERRORES["Error038"])
        
        # Error513: Si sexo F, debe registrar no aplica
        if sexo == 'F' and (resultado != 0 or str(fecha_tacto) != '1845-01-01'):
            self.agregar_error(id_usuario, resultado, "Error513", ERRORES["Error513"])
        
        # Error514: Valores permitidos
        if resultado not in [0, 4, 5, 21]:
            self.agregar_error(id_usuario, resultado, "Error514", ERRORES["Error514"])
        
        # Error237: Si registra fecha válida, validar condiciones
        if pd.notna(fecha_tacto) and str(fecha_tacto) > '1900-01-01':
            if resultado not in [4, 5] or sexo != 'M' or edad < 40:
                self.agregar_error(id_usuario, fecha_tacto, "Error237", ERRORES["Error237"])
        
        # Error512: Si resultado es 21, fecha debe ser comodín
        if resultado == 21:
            comodines_validos = ['1800-01-01', '1805-01-01', '1810-01-01', '1825-01-01', '1830-01-01', '1835-01-01']
            if str(fecha_tacto) not in comodines_validos:
                self.agregar_error(id_usuario, resultado, "Error512", ERRORES["Error512"])
    
    def validar_columna_23(self, fila):
        """Columna 23: Ácido fólico preconcepcional"""
        valor = fila.iloc[23]
        id_usuario = fila.iloc[4]
        
        if valor not in [0, 1, 2, 21]:
            self.agregar_error(id_usuario, valor, "Error515", ERRORES["Error515"])
    
    def validar_peso_talla(self, fila, fecha_corte):
        """Validar peso y talla (columnas 29-32)"""
        fecha_peso_str = fila.iloc[29]
        peso = pd.to_numeric(fila.iloc[30], errors='coerce')
        fecha_talla_str = fila.iloc[31]
        talla = pd.to_numeric(fila.iloc[32], errors='coerce')
        fecha_nacimiento_str = fila.iloc[9]
        id_usuario = fila.iloc[4]

        fecha_peso = pd.to_datetime(fecha_peso_str, errors='coerce')
        fecha_talla = pd.to_datetime(fecha_talla_str, errors='coerce')
        fecha_nacimiento = pd.to_datetime(fecha_nacimiento_str, errors='coerce')
        
        # Validaciones de peso
        if pd.notna(fecha_peso):
            # Error121: Fecha peso mayor a fecha de corte
            if fecha_peso > fecha_corte:
                self.agregar_error(id_usuario, fecha_peso_str, "Error121", ERRORES["Error121"])
            
            # Error171: Fecha peso menor a fecha de nacimiento
            if pd.notna(fecha_nacimiento) and fecha_peso < fecha_nacimiento:
                self.agregar_error(id_usuario, fecha_peso_str, "Error171", ERRORES["Error171"])
            
            # Warning674: Comodín 1800-01-01
            if str(fecha_peso_str) == '1800-01-01':
                self.agregar_warning(id_usuario, fecha_peso_str, "Warning674", ERRORES["Warning674"])
        
        # Error041: Si no registra peso, no debe registrar fecha
        if peso == 999 and str(fecha_peso_str) != '1800-01-01':
            self.agregar_error(id_usuario, peso, "Error041", ERRORES["Error041"])
        
        # Validaciones de peso por edad
        if pd.notna(peso) and peso != 999 and pd.notna(fecha_peso) and pd.notna(fecha_nacimiento):
            edad_en_fecha_peso = self.calcular_edad(fecha_nacimiento, fecha_peso)
            
            if edad_en_fecha_peso is not None:
                if edad_en_fecha_peso < 2 and (peso < 1 or peso > 15):
                    self.agregar_error(id_usuario, peso, "Error680", ERRORES["Error680"])
                elif 2 <= edad_en_fecha_peso < 5 and (peso < 3 or peso > 25):
                    self.agregar_error(id_usuario, peso, "Error681", ERRORES["Error681"])
                elif 5 <= edad_en_fecha_peso < 13 and (peso < 9 or peso > 80):
                    self.agregar_error(id_usuario, peso, "Error682", ERRORES["Error682"])
                elif 13 <= edad_en_fecha_peso < 18 and (peso < 30 or peso > 80):
                    self.agregar_error(id_usuario, peso, "Error683", ERRORES["Error683"])
                elif edad_en_fecha_peso >= 18 and (peso < 35 or peso > 250):
                    self.agregar_error(id_usuario, peso, "Error684", ERRORES["Error684"])
        
        # Validaciones de talla
        if pd.notna(fecha_talla):
            # Error122: Fecha talla mayor a fecha de corte
            if fecha_talla > fecha_corte:
                self.agregar_error(id_usuario, fecha_talla_str, "Error122", ERRORES["Error122"])
            
            # Error172: Fecha talla menor a fecha de nacimiento
            if pd.notna(fecha_nacimiento) and fecha_talla < fecha_nacimiento:
                self.agregar_error(id_usuario, fecha_talla_str, "Error172", ERRORES["Error172"])
            
            # Warning675: Comodín 1800-01-01
            if str(fecha_talla_str) == '1800-01-01':
                self.agregar_warning(id_usuario, fecha_talla_str, "Warning675", ERRORES["Warning675"])
        
        # Error043: Si no registra talla, no debe registrar fecha
        if talla == 999 and str(fecha_talla_str) != '1800-01-01':
            self.agregar_error(id_usuario, talla, "Error043", ERRORES["Error043"])
        
        # Validaciones de talla por edad
        if pd.notna(talla) and talla != 999 and pd.notna(fecha_talla) and pd.notna(fecha_nacimiento):
            edad_en_fecha_talla = self.calcular_edad(fecha_nacimiento, fecha_talla)
            
            if edad_en_fecha_talla is not None:
                if edad_en_fecha_talla < 2 and (talla < 40 or talla > 100):
                    self.agregar_error(id_usuario, talla, "Error685", ERRORES["Error685"])
                elif 2 <= edad_en_fecha_talla < 5 and (talla < 70 or talla > 110):
                    self.agregar_error(id_usuario, talla, "Error686", ERRORES["Error686"])
                elif 5 <= edad_en_fecha_talla < 13 and (talla < 80 or talla > 225):
                    self.agregar_error(id_usuario, talla, "Error687", ERRORES["Error687"])
                elif 13 <= edad_en_fecha_talla < 18 and (talla < 130 or talla > 225):
                    self.agregar_error(id_usuario, talla, "Error688", ERRORES["Error688"])
                elif edad_en_fecha_talla >= 18 and (talla < 130 or talla > 225):
                    self.agregar_error(id_usuario, talla, "Error689", ERRORES["Error689"])
    
    def validar_fila(self, fila, numero_registro, fecha_corte):
        """Valida una fila completa"""
        # Validaciones básicas
        self.validar_columna_0(fila)
        self.validar_columna_1(fila, numero_registro)
        self.validar_columna_2(fila)
        self.validar_columna_3(fila)
        self.validar_columna_4(fila)
        self.validar_columna_9(fila, fecha_corte)
        self.validar_columna_10(fila)
        self.validar_columna_14(fila, fecha_corte)
        self.validar_columna_15(fila)
        self.validar_columna_16(fila, fecha_corte)
        self.validar_columna_17(fila)
        self.validar_columna_18(fila)
        self.validar_columna_19(fila, fecha_corte)
        self.validar_columna_20(fila)
        self.validar_columna_21(fila)
        self.validar_columna_22(fila, fecha_corte)
        self.validar_columna_23(fila)
        
        # Validaciones de peso y talla
        if len(fila) > 32:
            self.validar_peso_talla(fila, fecha_corte)
    
    def validar_dataframe(self, df, fecha_corte):
        """Valida todo el DataFrame"""
        self.errores = []
        self.warnings = []
        
        for index, fila in df.iterrows():
            numero_registro = index + 1
            self.validar_fila(fila, numero_registro, fecha_corte)
        
        return {
            'errores': self.errores,
            'warnings': self.warnings,
            'total_errores': len(self.errores),
            'total_warnings': len(self.warnings)
        }

# Función de conveniencia para usar el validador
def validar_archivo_ese(df, fecha_corte):
    """Función principal para validar un archivo ESE"""
    validador = ValidadorESE()
    return validador.validar_dataframe(df, fecha_corte)