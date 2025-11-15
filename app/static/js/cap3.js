// JavaScript para Capítulo 3: Interpolación

// Cambiar entre métodos
function cambiarMetodo(metodo) {
    document.querySelectorAll('.metodo-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(metodo).classList.add('active');

    document.querySelectorAll('.metodo-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Ejecutar método
async function ejecutarMetodo(metodo) {
    const form = document.getElementById(`form-${metodo}`);
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    mostrarLoading(metodo, true);
    ocultarResultados(metodo);

    try {
        const response = await fetch(`/api/capitulo3/${metodo}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        mostrarResultados(metodo, resultado);

        if (resultado.exito && resultado.puntos_grafica) {
            graficarInterpolacion(resultado);
        }
    } catch (error) {
        mostrarError(metodo, error.message);
    } finally {
        mostrarLoading(metodo, false);
    }
}

// Mostrar resultados
function mostrarResultados(metodo, resultado) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    resultadosDiv.classList.add('show');

    let html = '';

    if (!resultado.exito) {
        html = `<div class="result-message error">${resultado.mensaje}</div>`;
    } else {
        html = `<div class="result-message success">Interpolación exitosa</div>`;
        
        // Mostrar polinomio
        if (resultado.polinomio_str) {
            html += `<div class="polinomio-box">
                <h4>📐 Polinomio Interpolador</h4>
                <p class="polinomio">${resultado.polinomio_str}</p>
            </div>`;
        }

        // Mostrar segmentos para splines
        if (resultado.segmentos) {
            html += '<div class="segmentos-box">';
            html += '<h4>📊 Segmentos del Spline</h4>';
            resultado.segmentos.forEach((seg, i) => {
                html += `<div class="segmento">
                    <strong>Segmento ${i+1}:</strong> [${seg.intervalo[0].toFixed(3)}, ${seg.intervalo[1].toFixed(3)}]<br>
                    <code>${seg.polinomio}</code>
                </div>`;
            });
            html += '</div>';
        }

        // Gráfica
        html += '<div id="grafica-' + metodo + '" class="grafica-container"></div>';
    }

    resultadosDiv.innerHTML = html;
}

// Graficar interpolación
function graficarInterpolacion(resultado) {
    const puntos_orig = resultado.puntos_originales;
    const puntos_graf = resultado.puntos_grafica;

    const trace1 = {
        x: puntos_orig.x,
        y: puntos_orig.y,
        mode: 'markers',
        type: 'scatter',
        name: 'Puntos dados',
        marker: { size: 10, color: 'red' }
    };

    const trace2 = {
        x: puntos_graf.x,
        y: puntos_graf.y,
        mode: 'lines',
        type: 'scatter',
        name: 'Interpolación',
        line: { color: 'blue', width: 2 }
    };

    const layout = {
        title: 'Interpolación',
        xaxis: { title: 'x' },
        yaxis: { title: 'y' },
        showlegend: true
    };

    // El contenedor se crea dinámicamente en mostrarResultados
    const metodo = Object.keys(resultado).includes('matriz_vandermonde') ? 'vandermonde' :
                   Object.keys(resultado).includes('tabla') ? 'newton' : 'lagrange';
    
    // Buscar el contenedor correcto
    const containers = ['vandermonde', 'newton', 'lagrange', 'spline-lineal', 'spline-cubico'];
    for (let cont of containers) {
        const elem = document.getElementById(`grafica-${cont}`);
        if (elem && elem.offsetParent !== null) {
            Plotly.newPlot(`grafica-${cont}`, [trace1, trace2], layout);
            break;
        }
    }
}

// Generar informe comparativo del Capítulo 3
async function generarInforme() {
    const form = document.getElementById('form-informe');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    mostrarLoading('informe', true);
    document.getElementById('resultados-informe').classList.remove('show');

    try {
        const response = await fetch('/api/capitulo3/informe', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        mostrarInforme(resultado);
    } catch (error) {
        mostrarError('informe', error.message);
    } finally {
        mostrarLoading('informe', false);
    }
}

function mostrarInforme(resultado) {
    const resultadosDiv = document.getElementById('resultados-informe');
    resultadosDiv.classList.add('show');

    if (!resultado.exito) {
        resultadosDiv.innerHTML = `<div class="result-message error">${resultado.mensaje}</div>`;
        return;
    }

    let html = '<div class="informe-container">';
    html += '<h3>📊 Informe Comparativo - Capítulo 3</h3>';

    // Tabla comparativa
    html += '<div class="table-container"><table>';
    html += '<thead><tr>';
    html += '<th>Método</th><th>Estado</th><th>Polinomio/Spline</th><th>Tiempo (s)</th>';
    html += '</tr></thead><tbody>';

    resultado.resultados.forEach(r => {
        if (r.exito) {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #27ae60;">✓ Exitoso</span></td>`;
            html += `<td><code style="font-size: 0.85em;">${r.polinomio ? r.polinomio.substring(0, 50) + '...' : 'N/A'}</code></td>`;
            html += `<td>${(r.tiempo * 1000).toFixed(2)} ms</td>`;
            html += '</tr>';
        } else {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #e74c3c;">✗ Falló</span></td>`;
            html += `<td colspan="2">${r.error_msg || 'Error desconocido'}</td>`;
            html += '</tr>';
        }
    });

    html += '</tbody></table></div>';

    // Análisis y conclusiones
    html += '<div class="informe-analisis">';
    html += '<h4>🏆 Análisis y Conclusiones</h4>';
    html += '<div class="conclusiones">';
    html += `<p><strong>⚡ Método más rápido:</strong> <span class="highlight">${resultado.mas_rapido}</span></p>`;
    html += `<p><strong>📈 Métodos exitosos:</strong> ${resultado.estadisticas.exitosos} de ${resultado.estadisticas.total_metodos}</p>`;

    html += '<div class="recomendaciones">';
    html += '<h5>💡 Recomendaciones</h5>';
    html += '<ul>';
    html += '<li><strong>Vandermonde, Newton y Lagrange:</strong> Generan el mismo polinomio interpolador (de grado n-1)</li>';
    html += '<li><strong>Spline Lineal:</strong> Conecta puntos con líneas rectas, más simple pero menos suave</li>';
    html += '<li><strong>Spline Cúbico:</strong> Más suave y natural, recomendado para datos con variación continua</li>';
    html += '</ul>';
    html += '</div>';

    if (resultado.estadisticas.fallidos > 0) {
        html += `<p><strong>⚠️ Métodos que fallaron:</strong> ${resultado.estadisticas.fallidos}</p>`;
    }

    html += '</div></div>';
    html += '</div>';

    // Estilos
    html += `
    <style>
    .informe-container {
        margin-top: 20px;
    }
    .informe-analisis {
        background: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        border-left: 4px solid #9b59b6;
    }
    .conclusiones p {
        margin: 10px 0;
        font-size: 1.05em;
    }
    .highlight {
        color: #9b59b6;
        font-weight: bold;
        font-size: 1.1em;
    }
    .recomendaciones {
        background: white;
        padding: 15px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .recomendaciones ul {
        margin: 10px 0;
        padding-left: 25px;
    }
    .recomendaciones li {
        margin: 8px 0;
        line-height: 1.5;
    }
    .polinomio-box, .segmentos-box {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 6px;
        margin: 15px 0;
    }
    .polinomio {
        font-family: 'Courier New', monospace;
        font-size: 0.95em;
        color: #2c3e50;
        overflow-x: auto;
    }
    .segmento {
        background: white;
        padding: 10px;
        margin: 8px 0;
        border-radius: 4px;
        border-left: 3px solid #9b59b6;
    }
    .grafica-container {
        margin: 20px 0;
        min-height: 400px;
    }
    </style>
    `;

    resultadosDiv.innerHTML = html;
}

// Funciones auxiliares
function mostrarLoading(metodo, mostrar) {
    const loadingDiv = document.getElementById(`loading-${metodo}`);
    if (loadingDiv) {
        loadingDiv.style.display = mostrar ? 'block' : 'none';
    }
}

function ocultarResultados(metodo) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    if (resultadosDiv) {
        resultadosDiv.classList.remove('show');
    }
}

function mostrarError(metodo, mensaje) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    if (resultadosDiv) {
        resultadosDiv.classList.add('show');
        resultadosDiv.innerHTML = `<div class="result-message error">Error: ${mensaje}</div>`;
    }
}
