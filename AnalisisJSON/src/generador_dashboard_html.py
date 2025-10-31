"""
Módulo para generar dashboard interactivo en HTML con JavaScript y Chart.js
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from src.cargador_rips import CargadorRIPS
from collections import Counter
from datetime import datetime


class GeneradorDashboardHTML:
    """Genera dashboard interactivo en HTML/JavaScript"""

    def __init__(self, cargador: CargadorRIPS):
        """
        Inicializa el generador

        Args:
            cargador: Instancia de CargadorRIPS
        """
        self.cargador = cargador

    def generar_dashboard(self, datos_consolidados: List[Dict[str, Any]], nombre_archivo: str):
        """
        Genera dashboard HTML interactivo

        Args:
            datos_consolidados: Lista con datos de todos los RIPS
            nombre_archivo: Nombre del archivo HTML a generar
        """
        # Analizar y preparar datos
        datos_json = self._preparar_datos_json(datos_consolidados)

        # Generar HTML
        html_content = self._generar_html(datos_json)

        # Guardar archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"\nDashboard HTML interactivo generado: {nombre_archivo}")
        print(f"  Abrir en navegador para visualizar")

    def _preparar_datos_json(self, datos_consolidados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepara los datos en formato JSON para el dashboard"""
        usuarios_data = []
        consultas_data = []
        procedimientos_data = []
        diagnosticos = Counter()
        procedimientos_cups = Counter()
        municipios = Counter()
        prestadores = Counter()
        meses = Counter()

        for rips in datos_consolidados:
            datos = rips["datos"]
            num_factura = datos.get("numFactura", "")
            usuarios = self.cargador.extraer_usuarios(datos)

            for usuario in usuarios:
                tipo_doc = usuario.get("tipoDocumentoIdentificacion", "")
                num_doc = usuario.get("numDocumentoIdentificacion", "")
                sexo = usuario.get("codSexo", "")
                tipo_usuario = usuario.get("tipoUsuario", "")
                fecha_nac = usuario.get("fechaNacimiento", "")
                edad = self.cargador.calcular_edad(fecha_nac)
                municipio = usuario.get("codMunicipioResidencia", "")
                municipio_nombre = self.cargador.obtener_nombre_municipio(municipio)
                pais = usuario.get("codPaisResidencia", "170")
                pais_nombre = self.cargador.obtener_nombre_pais(pais)

                # Determinar régimen
                regimen = "CONTRIBUTIVO" if tipo_usuario in ["01", "02", "03"] else "SUBSIDIADO" if tipo_usuario == "04" else "OTRO"

                # Curso de vida
                if edad is not None:
                    if edad < 6:
                        curso_vida = "Primera Infancia"
                    elif edad < 12:
                        curso_vida = "Infancia"
                    elif edad < 18:
                        curso_vida = "Adolescencia"
                    elif edad < 29:
                        curso_vida = "Juventud"
                    elif edad < 60:
                        curso_vida = "Adultez"
                    else:
                        curso_vida = "Vejez"
                else:
                    curso_vida = "Desconocido"

                nombre_completo = f"{usuario.get('primerNombre', '')} {usuario.get('segundoNombre', '')} {usuario.get('primerApellido', '')} {usuario.get('segundoApellido', '')}".strip()

                usuario_info = {
                    "factura": num_factura,
                    "tipo_doc": tipo_doc,
                    "num_doc": num_doc,
                    "nombre": nombre_completo,
                    "sexo": "Masculino" if sexo == "M" else "Femenino" if sexo == "F" else sexo,
                    "edad": edad,
                    "municipio": municipio,
                    "municipio_nombre": municipio_nombre,
                    "pais": pais_nombre,
                    "regimen": regimen,
                    "curso_vida": curso_vida,
                    "total_consultas": 0,
                    "total_procedimientos": 0,
                    "diagnosticos": []
                }

                municipios[municipio_nombre] += 1

                # Procesar consultas
                consultas = self.cargador.extraer_consultas(usuario)
                usuario_info["total_consultas"] = len(consultas)

                for consulta in consultas:
                    prestador = consulta.get("codPrestador", "")
                    prestador_nombre = self.cargador.obtener_nombre_prestador(prestador)
                    prestadores[prestador_nombre] += 1

                    dx_principal = consulta.get("codDiagnosticoPrincipal", "")
                    if dx_principal:
                        info_dx = self.cargador.obtener_info_diagnostico(dx_principal)
                        dx_nombre = f"[{dx_principal}] {info_dx.get('nombre', '')}"
                        diagnosticos[dx_nombre] += 1
                        if dx_nombre not in usuario_info["diagnosticos"]:
                            usuario_info["diagnosticos"].append(dx_nombre)

                    fecha_atencion = consulta.get("fechaInicioAtencion", "")
                    if fecha_atencion:
                        mes = fecha_atencion[:7] if len(fecha_atencion) >= 7 else ""
                        if mes:
                            meses[mes] += 1

                    consultas_data.append({
                        "factura": num_factura,
                        "usuario": num_doc,
                        "nombre": nombre_completo,
                        "fecha": fecha_atencion,
                        "codigo": consulta.get("codConsulta", ""),
                        "prestador": prestador_nombre,
                        "diagnostico": dx_nombre if dx_principal else "",
                        "municipio": municipio_nombre,
                        "regimen": regimen
                    })

                # Procesar procedimientos
                procedimientos = self.cargador.extraer_procedimientos(usuario)
                usuario_info["total_procedimientos"] = len(procedimientos)

                for proc in procedimientos:
                    prestador = proc.get("codPrestador", "")
                    prestador_nombre = self.cargador.obtener_nombre_prestador(prestador)
                    prestadores[prestador_nombre] += 1

                    cod_proc = proc.get("codProcedimiento", "")
                    nombre_proc = self.cargador.obtener_nombre_cups(cod_proc)
                    proc_completo = f"[{cod_proc}] {nombre_proc}"
                    procedimientos_cups[proc_completo] += 1

                    fecha_atencion = proc.get("fechaInicioAtencion", "")
                    if fecha_atencion:
                        mes = fecha_atencion[:7] if len(fecha_atencion) >= 7 else ""
                        if mes:
                            meses[mes] += 1

                    procedimientos_data.append({
                        "factura": num_factura,
                        "usuario": num_doc,
                        "nombre": nombre_completo,
                        "fecha": fecha_atencion,
                        "codigo": cod_proc,
                        "nombre_proc": nombre_proc,
                        "prestador": prestador_nombre,
                        "municipio": municipio_nombre,
                        "regimen": regimen
                    })

                usuarios_data.append(usuario_info)

        return {
            "usuarios": usuarios_data,
            "consultas": consultas_data,
            "procedimientos": procedimientos_data,
            "estadisticas": {
                "total_usuarios": len(usuarios_data),
                "total_consultas": len(consultas_data),
                "total_procedimientos": len(procedimientos_data),
                "diagnosticos_top": [{"nombre": k, "cantidad": v} for k, v in diagnosticos.most_common(15)],
                "procedimientos_top": [{"nombre": k, "cantidad": v} for k, v in procedimientos_cups.most_common(15)],
                "municipios_top": [{"nombre": k, "cantidad": v} for k, v in municipios.most_common(10)],
                "prestadores_top": [{"nombre": k, "cantidad": v} for k, v in prestadores.most_common(10)],
                "tendencia_mensual": [{"mes": k, "cantidad": v} for k, v in sorted(meses.items())]
            }
        }

    def _generar_html(self, datos_json: Dict[str, Any]) -> str:
        """Genera el contenido HTML del dashboard"""
        datos_json_str = json.dumps(datos_json, ensure_ascii=False, indent=2)

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Interactivo RIPS - Análisis de Salud</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}

        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .filters {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .filter-group {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .filter-item {{
            display: flex;
            flex-direction: column;
        }}

        .filter-item label {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
            font-size: 0.9em;
        }}

        .filter-item select, .filter-item input {{
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}

        .filter-item select:focus, .filter-item input:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}

        .stat-card .number {{
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}

        .stat-card .label {{
            color: #666;
            font-size: 1em;
            font-weight: 600;
        }}

        .stat-card .icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}

        .chart-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .chart-card h3 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}

        .chart-container {{
            position: relative;
            height: 350px;
        }}

        .table-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .table-card h3 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        tr:hover {{
            background: #f5f5f5;
        }}

        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: background 0.3s;
            margin-right: 10px;
        }}

        .btn:hover {{
            background: #5568d3;
        }}

        .btn-secondary {{
            background: #6c757d;
        }}

        .btn-secondary:hover {{
            background: #5a6268;
        }}

        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Dashboard Interactivo RIPS</h1>
            <p class="subtitle">Análisis de Registros Individuales de Prestación de Servicios de Salud</p>
            <p class="subtitle">Resolución 2275 de 2023</p>
        </header>

        <div class="filters">
            <h3 style="color: #667eea; margin-bottom: 15px;">🔍 Filtros de Segmentación</h3>
            <div class="filter-group">
                <div class="filter-item">
                    <label>Sexo</label>
                    <select id="filtroSexo" onchange="aplicarFiltros()">
                        <option value="">Todos</option>
                        <option value="Masculino">Masculino</option>
                        <option value="Femenino">Femenino</option>
                    </select>
                </div>

                <div class="filter-item">
                    <label>Régimen</label>
                    <select id="filtroRegimen" onchange="aplicarFiltros()">
                        <option value="">Todos</option>
                        <option value="CONTRIBUTIVO">Contributivo</option>
                        <option value="SUBSIDIADO">Subsidiado</option>
                        <option value="OTRO">Otro</option>
                    </select>
                </div>

                <div class="filter-item">
                    <label>Curso de Vida</label>
                    <select id="filtroCursoVida" onchange="aplicarFiltros()">
                        <option value="">Todos</option>
                        <option value="Primera Infancia">Primera Infancia (0-5)</option>
                        <option value="Infancia">Infancia (6-11)</option>
                        <option value="Adolescencia">Adolescencia (12-17)</option>
                        <option value="Juventud">Juventud (18-28)</option>
                        <option value="Adultez">Adultez (29-59)</option>
                        <option value="Vejez">Vejez (60+)</option>
                    </select>
                </div>

                <div class="filter-item">
                    <label>Municipio</label>
                    <select id="filtroMunicipio" onchange="aplicarFiltros()">
                        <option value="">Todos</option>
                    </select>
                </div>

                <div class="filter-item">
                    <label>Buscar Usuario</label>
                    <input type="text" id="buscarUsuario" placeholder="Nombre o documento" onkeyup="aplicarFiltros()">
                </div>
            </div>
            <div style="margin-top: 15px;">
                <button class="btn" onclick="aplicarFiltros()">Aplicar Filtros</button>
                <button class="btn btn-secondary" onclick="limpiarFiltros()">Limpiar Filtros</button>
                <button class="btn btn-secondary" onclick="exportarDatos()">Exportar Datos</button>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="icon">👥</div>
                <div class="label">Total Usuarios</div>
                <div class="number" id="statUsuarios">0</div>
            </div>
            <div class="stat-card">
                <div class="icon">🏥</div>
                <div class="label">Total Consultas</div>
                <div class="number" id="statConsultas">0</div>
            </div>
            <div class="stat-card">
                <div class="icon">⚕️</div>
                <div class="label">Total Procedimientos</div>
                <div class="number" id="statProcedimientos">0</div>
            </div>
            <div class="stat-card">
                <div class="icon">📋</div>
                <div class="label">Total Servicios</div>
                <div class="number" id="statServicios">0</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <h3>Distribución por Sexo</h3>
                <div class="chart-container">
                    <canvas id="chartSexo"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h3>Distribución por Curso de Vida</h3>
                <div class="chart-container">
                    <canvas id="chartCursoVida"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h3>Top 10 Diagnósticos</h3>
                <div class="chart-container">
                    <canvas id="chartDiagnosticos"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h3>Top 10 Procedimientos</h3>
                <div class="chart-container">
                    <canvas id="chartProcedimientos"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h3>Distribución por Régimen</h3>
                <div class="chart-container">
                    <canvas id="chartRegimen"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h3>Tendencia Mensual de Servicios</h3>
                <div class="chart-container">
                    <canvas id="chartTendencia"></canvas>
                </div>
            </div>
        </div>

        <div class="table-card">
            <h3>Detalle de Usuarios</h3>
            <div style="overflow-x: auto;">
                <table id="tablaUsuarios">
                    <thead>
                        <tr>
                            <th>Documento</th>
                            <th>Nombre</th>
                            <th>Sexo</th>
                            <th>Edad</th>
                            <th>Curso de Vida</th>
                            <th>Municipio</th>
                            <th>Régimen</th>
                            <th>Consultas</th>
                            <th>Procedimientos</th>
                        </tr>
                    </thead>
                    <tbody id="tablaUsuariosBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Datos del sistema
        const datosOriginales = {datos_json_str};
        let datosFiltrados = JSON.parse(JSON.stringify(datosOriginales));
        let charts = {{}};

        // Inicializar dashboard
        window.onload = function() {{
            inicializarFiltros();
            aplicarFiltros();
        }};

        function inicializarFiltros() {{
            // Poblar select de municipios
            const municipios = new Set();
            datosOriginales.usuarios.forEach(u => {{
                if (u.municipio_nombre) municipios.add(u.municipio_nombre);
            }});

            const selectMunicipio = document.getElementById('filtroMunicipio');
            Array.from(municipios).sort().forEach(m => {{
                const option = document.createElement('option');
                option.value = m;
                option.textContent = m;
                selectMunicipio.appendChild(option);
            }});
        }}

        function aplicarFiltros() {{
            const filtroSexo = document.getElementById('filtroSexo').value;
            const filtroRegimen = document.getElementById('filtroRegimen').value;
            const filtroCursoVida = document.getElementById('filtroCursoVida').value;
            const filtroMunicipio = document.getElementById('filtroMunicipio').value;
            const buscarUsuario = document.getElementById('buscarUsuario').value.toLowerCase();

            // Filtrar usuarios
            let usuariosFiltrados = datosOriginales.usuarios.filter(u => {{
                if (filtroSexo && u.sexo !== filtroSexo) return false;
                if (filtroRegimen && u.regimen !== filtroRegimen) return false;
                if (filtroCursoVida && u.curso_vida !== filtroCursoVida) return false;
                if (filtroMunicipio && u.municipio_nombre !== filtroMunicipio) return false;
                if (buscarUsuario && !u.nombre.toLowerCase().includes(buscarUsuario) && !u.num_doc.includes(buscarUsuario)) return false;
                return true;
            }});

            datosFiltrados.usuarios = usuariosFiltrados;

            // Recalcular estadísticas
            actualizarEstadisticas();
            actualizarGraficos();
            actualizarTabla();
        }}

        function limpiarFiltros() {{
            document.getElementById('filtroSexo').value = '';
            document.getElementById('filtroRegimen').value = '';
            document.getElementById('filtroCursoVida').value = '';
            document.getElementById('filtroMunicipio').value = '';
            document.getElementById('buscarUsuario').value = '';
            aplicarFiltros();
        }}

        function actualizarEstadisticas() {{
            const usuarios = datosFiltrados.usuarios;
            const totalUsuarios = usuarios.length;
            const totalConsultas = usuarios.reduce((sum, u) => sum + u.total_consultas, 0);
            const totalProcedimientos = usuarios.reduce((sum, u) => sum + u.total_procedimientos, 0);

            document.getElementById('statUsuarios').textContent = totalUsuarios.toLocaleString();
            document.getElementById('statConsultas').textContent = totalConsultas.toLocaleString();
            document.getElementById('statProcedimientos').textContent = totalProcedimientos.toLocaleString();
            document.getElementById('statServicios').textContent = (totalConsultas + totalProcedimientos).toLocaleString();
        }}

        function actualizarGraficos() {{
            // Destruir gráficos anteriores
            Object.values(charts).forEach(chart => chart?.destroy());
            charts = {{}};

            const usuarios = datosFiltrados.usuarios;

            // Gráfico de sexo
            const distSexo = {{}};
            usuarios.forEach(u => {{
                distSexo[u.sexo] = (distSexo[u.sexo] || 0) + 1;
            }});

            charts.sexo = new Chart(document.getElementById('chartSexo'), {{
                type: 'pie',
                data: {{
                    labels: Object.keys(distSexo),
                    datasets: [{{
                        data: Object.values(distSexo),
                        backgroundColor: ['#4472C4', '#ED7D31', '#A5A5A5']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom'
                        }}
                    }}
                }}
            }});

            // Gráfico de curso de vida
            const distCursoVida = {{}};
            usuarios.forEach(u => {{
                distCursoVida[u.curso_vida] = (distCursoVida[u.curso_vida] || 0) + 1;
            }});

            charts.cursoVida = new Chart(document.getElementById('chartCursoVida'), {{
                type: 'bar',
                data: {{
                    labels: Object.keys(distCursoVida),
                    datasets: [{{
                        label: 'Cantidad',
                        data: Object.values(distCursoVida),
                        backgroundColor: '#667eea'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});

            // Gráfico de diagnósticos
            const diagnosticos = datosOriginales.estadisticas.diagnosticos_top.slice(0, 10);
            charts.diagnosticos = new Chart(document.getElementById('chartDiagnosticos'), {{
                type: 'bar',
                data: {{
                    labels: diagnosticos.map(d => d.nombre.substring(0, 40) + '...'),
                    datasets: [{{
                        label: 'Cantidad',
                        data: diagnosticos.map(d => d.cantidad),
                        backgroundColor: '#70AD47'
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});

            // Gráfico de procedimientos
            const procedimientos = datosOriginales.estadisticas.procedimientos_top.slice(0, 10);
            charts.procedimientos = new Chart(document.getElementById('chartProcedimientos'), {{
                type: 'bar',
                data: {{
                    labels: procedimientos.map(p => p.nombre.substring(0, 40) + '...'),
                    datasets: [{{
                        label: 'Cantidad',
                        data: procedimientos.map(p => p.cantidad),
                        backgroundColor: '#FFC000'
                    }}]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});

            // Gráfico de régimen
            const distRegimen = {{}};
            usuarios.forEach(u => {{
                distRegimen[u.regimen] = (distRegimen[u.regimen] || 0) + 1;
            }});

            charts.regimen = new Chart(document.getElementById('chartRegimen'), {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(distRegimen),
                    datasets: [{{
                        data: Object.values(distRegimen),
                        backgroundColor: ['#4472C4', '#ED7D31', '#A5A5A5']
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'bottom'
                        }}
                    }}
                }}
            }});

            // Gráfico de tendencia
            const tendencia = datosOriginales.estadisticas.tendencia_mensual;
            charts.tendencia = new Chart(document.getElementById('chartTendencia'), {{
                type: 'line',
                data: {{
                    labels: tendencia.map(t => t.mes),
                    datasets: [{{
                        label: 'Servicios',
                        data: tendencia.map(t => t.cantidad),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }}
                }}
            }});
        }}

        function actualizarTabla() {{
            const tbody = document.getElementById('tablaUsuariosBody');
            tbody.innerHTML = '';

            datosFiltrados.usuarios.slice(0, 100).forEach(u => {{
                const row = tbody.insertRow();
                row.insertCell(0).textContent = u.num_doc;
                row.insertCell(1).textContent = u.nombre;
                row.insertCell(2).textContent = u.sexo;
                row.insertCell(3).textContent = u.edad || 'N/A';
                row.insertCell(4).textContent = u.curso_vida;
                row.insertCell(5).textContent = u.municipio_nombre;
                row.insertCell(6).textContent = u.regimen;
                row.insertCell(7).textContent = u.total_consultas;
                row.insertCell(8).textContent = u.total_procedimientos;
            }});

            if (datosFiltrados.usuarios.length > 100) {{
                const row = tbody.insertRow();
                const cell = row.insertCell(0);
                cell.colSpan = 9;
                cell.style.textAlign = 'center';
                cell.style.fontStyle = 'italic';
                cell.textContent = `Mostrando 100 de ${{datosFiltrados.usuarios.length}} registros`;
            }}
        }}

        function exportarDatos() {{
            const csv = generarCSV();
            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'datos_rips_filtrados.csv';
            link.click();
        }}

        function generarCSV() {{
            let csv = 'Documento,Nombre,Sexo,Edad,Curso de Vida,Municipio,Régimen,Consultas,Procedimientos\\n';
            datosFiltrados.usuarios.forEach(u => {{
                csv += `"${{u.num_doc}}","${{u.nombre}}","${{u.sexo}}","${{u.edad}}","${{u.curso_vida}}","${{u.municipio_nombre}}","${{u.regimen}}","${{u.total_consultas}}","${{u.total_procedimientos}}"\\n`;
            }});
            return csv;
        }}
    </script>
</body>
</html>"""
        return html
