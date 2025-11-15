// JavaScript para Capítulo 2: Sistemas de Ecuaciones Lineales

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
        const response = await fetch(`/api/capitulo2/${metodo}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        mostrarResultados(metodo, resultado);
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
        html = `
            <div class="result-message success">${resultado.mensaje}</div>
            <div class="result-stats">
                <p><strong>Radio Espectral:</strong> ${resultado.radio_espectral?.toFixed(6) || 'N/A'}</p>
                <p><strong>¿Converge?:</strong> ${resultado.converge ? '✓ Sí (ρ < 1)' : '✗ No (ρ ≥ 1)'}</p>
                <p><strong>Iteraciones:</strong> ${resultado.iteraciones}</p>
                <p><strong>Error final:</strong> ${resultado.error_final?.toExponential(4) || 'N/A'}</p>
                <p><strong>Solución:</strong> [${resultado.solucion?.map(v => v.toFixed(6)).join(', ') || 'N/A'}]</p>
            </div>
        `;

        if (resultado.tabla) {
            html += crearTablaIteraciones(resultado.tabla);
        }
    }

    resultadosDiv.innerHTML = html;
}

// Crear tabla de iteraciones
function crearTablaIteraciones(tabla) {
    if (!tabla || tabla.length === 0) return '';

    let html = '<div class="table-container"><table><thead><tr>';
    html += '<th>Iteración</th>';
    
    // Encabezados para cada variable
    const numVars = tabla[0].x.length;
    for (let i = 0; i < numVars; i++) {
        html += `<th>x${i+1}</th>`;
    }
    html += '<th>Error</th>';
    html += '</tr></thead><tbody>';

    // Filas
    tabla.forEach(fila => {
        html += '<tr>';
        html += `<td>${fila.iter}</td>`;
        fila.x.forEach(val => {
            html += `<td>${val.toFixed(6)}</td>`;
        });
        html += `<td>${fila.error !== null ? fila.error.toExponential(4) : '-'}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    return html;
}

// Generar informe comparativo del Capítulo 2
async function generarInforme() {
    const form = document.getElementById('form-informe');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    mostrarLoading('informe', true);
    document.getElementById('resultados-informe').classList.remove('show');

    try {
        const response = await fetch('/api/capitulo2/informe', {
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
    html += '<h3>📊 Informe Comparativo - Capítulo 2</h3>';

    // Tabla comparativa
    html += '<div class="table-container"><table>';
    html += '<thead><tr>';
    html += '<th>Método</th><th>Estado</th><th>Iteraciones</th><th>Error Final</th><th>Radio Espectral</th><th>Converge</th><th>Tiempo (s)</th>';
    html += '</tr></thead><tbody>';

    resultado.resultados.forEach(r => {
        if (r.exito) {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #27ae60;">✓ Exitoso</span></td>`;
            html += `<td>${r.iteraciones}</td>`;
            html += `<td>${r.error.toExponential(4)}</td>`;
            html += `<td>${r.radio_espectral.toFixed(6)}</td>`;
            html += `<td>${r.converge ? '✓ Sí' : '✗ No'}</td>`;
            html += `<td>${(r.tiempo * 1000).toFixed(2)} ms</td>`;
            html += '</tr>';
        } else {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #e74c3c;">✗ Falló</span></td>`;
            html += `<td colspan="5">${r.error_msg || 'No convergió'}</td>`;
            html += '</tr>';
        }
    });

    html += '</tbody></table></div>';

    // Análisis y conclusiones
    html += '<div class="informe-analisis">';
    html += '<h4>🏆 Análisis y Conclusiones</h4>';
    html += '<div class="conclusiones">';
    html += `<p><strong>⚡ Método más rápido (menos iteraciones):</strong> <span class="highlight">${resultado.mejor_iteraciones}</span></p>`;
    html += `<p><strong>🎯 Mejor método (menor error):</strong> <span class="highlight">${resultado.mejor_error}</span></p>`;
    html += `<p><strong>📈 Métodos exitosos:</strong> ${resultado.estadisticas.exitosos} de ${resultado.estadisticas.total_metodos}</p>`;

    if (resultado.estadisticas.fallidos > 0) {
        html += `<p><strong>⚠️ Métodos que fallaron:</strong> ${resultado.estadisticas.fallidos}</p>`;
        html += '<p class="nota">Nota: Para garantizar convergencia, la matriz debe ser diagonalmente dominante o simétrica definida positiva.</p>';
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
        border-left: 4px solid #3498db;
    }
    .conclusiones p {
        margin: 10px 0;
        font-size: 1.05em;
    }
    .highlight {
        color: #3498db;
        font-weight: bold;
        font-size: 1.1em;
    }
    .nota {
        font-size: 0.9em;
        color: #666;
        font-style: italic;
        margin-top: 15px;
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
