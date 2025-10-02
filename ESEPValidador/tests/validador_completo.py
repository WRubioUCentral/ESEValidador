import pandas as pd

def validar_archivo_ese(df: pd.DataFrame, fecha_corte: str) -> dict:
    """
    Valida un DataFrame según las reglas definidas.

    Args:
        df (pd.DataFrame): El DataFrame a validar.
        fecha_corte (str): La fecha de corte para las validaciones.

    Returns:
        dict: Un diccionario con los resultados de la validación, incluyendo errores y warnings.
    """
    errores = []
    warnings = []

    # Validaciones de ejemplo (añadir más validaciones según sea necesario)
    for index, row in df.iterrows():
        # Ejemplo de error: tipo_registro debe ser 1 o 2
        if row['tipo_registro'] not in [1, 2]:
            errores.append({
                'usuario': index + 1,
                'codigo': 'E001',
                'dato_erroneo': row['tipo_registro'],
                'explicacion': 'El tipo de registro debe ser 1 o 2.'
            })

        # Ejemplo de warning: sexo debe ser M o F
        if row['sexo'] not in ['M', 'F']:
            warnings.append({
                'usuario': index + 1,
                'codigo': 'W001',
                'dato_erroneo': row['sexo'],
                'explicacion': 'El sexo debe ser M o F.'
            })

    resultados = {
        'total_errores': len(errores),
        'total_warnings': len(warnings),
        'errores': errores,
        'warnings': warnings
    }

    return resultados