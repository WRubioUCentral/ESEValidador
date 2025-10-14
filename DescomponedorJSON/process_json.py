import json
import csv
import os
from datetime import datetime
from collections import Counter

# Create outputs folder if it doesn't exist
os.makedirs('outputs', exist_ok=True)

# Cutoff date for age calculation
cutoff_date_str = "2025-09-30"
cutoff_date = datetime.strptime(cutoff_date_str, "%Y-%m-%d")

# List to hold user details
users = []

# Counters for groupings
servicio_counts = Counter()
prestador_counts = Counter()
diagnostico_counts = Counter()

# Process each JSON file in the inputs folder
for filename in os.listdir('inputs'):
    if filename.endswith('.json'):
        filepath = os.path.join('inputs', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for user in data['usuarios']:
                user_id = user['numDocumentoIdentificacion']
                birth_str = user['fechaNacimiento']
                birth = datetime.strptime(birth_str, "%Y-%m-%d")
                age = cutoff_date.year - birth.year - ((cutoff_date.month, cutoff_date.day) < (birth.month, birth.day))
                codSexo = user['codSexo']
                tipoUsuario = user['tipoUsuario']
                codDiagnosticoPrincipal = user['servicios']['codDiagnosticoPrincipal']
                causaMotivoAtencion = user['servicios']['causaMotivoAtencion']
                count = len(user['servicios']['consultas'])
                users.append({
                    'Usuario': user_id,
                    'Edad': age,
                    'codSexo': codSexo,
                    'tipoUsuario': tipoUsuario,
                    'Procedimientos': count,
                    'Diagnostico': codDiagnosticoPrincipal,
                    'MotivoAtencion': causaMotivoAtencion
                })
                # Count for groupings
                for consulta in user['servicios']['consultas']:
                    codServicio = consulta['codServicio']
                    codPrestador = consulta['codPrestador']
                    codDiagnosticoPrincipal = consulta['codDiagnosticoPrincipal']
                    servicio_counts[codServicio] += 1
                    prestador_counts[codPrestador] += 1
                    diagnostico_counts[codDiagnosticoPrincipal] += 1

# Write user details to CSV
with open('outputs/usuarios_detalles.csv', 'w', newline='', encoding='utf-8') as csvfile:
    if users:
        fieldnames = ['Usuario', 'Edad', 'codSexo', 'tipoUsuario', 'Procedimientos']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)

# Write servicio counts
with open('outputs/servicios_por_codServicio.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['codServicio', 'Conteo'])
    for cod, count in servicio_counts.items():
        writer.writerow([cod, count])

# Write prestador counts
with open('outputs/servicios_por_codPrestador.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['codPrestador', 'Conteo'])
    for cod, count in prestador_counts.items():
        writer.writerow([cod, count])

# Write diagnostico counts
with open('outputs/servicios_por_codDiagnosticoPrincipal.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['codDiagnosticoPrincipal', 'Conteo'])
    for cod, count in diagnostico_counts.items():
        writer.writerow([cod, count])

print("CSV files generated successfully in outputs/")
