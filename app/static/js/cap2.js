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

        // Graficar convergencia si el resultado fue exitoso
        if (resultado.exito && resultado.tabla) {
            await graficarConvergencia(resultado, metodo);
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

    // Graficar convergencia si el resultado fue exitoso
    if (resultado.exito && resultado.tabla) {
        graficarConvergencia(resultado, metodo);
    }
}

// Crear tabla de iteraciones con 5 métricas de error
function crearTablaIteraciones(tabla) {
    if (!tabla || tabla.length === 0) return '';

    let html = '<div class="table-container"><table><thead><tr>';
    html += '<th>Iteración</th>';
    
    // Encabezados para cada variable
    const numVars = tabla[0].x.length;
    for (let i = 0; i < numVars; i++) {
        html += `<th>x${i+1}</th>`;
    }
    // Encabezados de las 5 métricas de error
    html += '<th>E. Absoluto</th>';
    html += '<th>E. Relativo 1</th>';
    html += '<th>E. Relativo 2</th>';
    html += '<th>E. Relativo 3</th>';
    html += '<th>E. Relativo 4</th>';
    html += '</tr></thead><tbody>';

    // Filas
    tabla.forEach(fila => {
        html += '<tr>';
        html += `<td><strong>${fila.iter}</strong></td>`;
        fila.x.forEach(val => {
            html += `<td>${val.toFixed(6)}</td>`;
        });
        // Mostrar las 5 métricas de error
        html += `<td>${fila.error_abs !== null ? fila.error_abs.toExponential(4) : '-'}</td>`;
        html += `<td>${fila.error_rel1 !== null ? fila.error_rel1.toExponential(4) : '-'}</td>`;
        html += `<td>${fila.error_rel2 !== null ? fila.error_rel2.toExponential(4) : '-'}</td>`;
        html += `<td>${fila.error_rel3 !== null ? fila.error_rel3.toExponential(4) : '-'}</td>`;
        html += `<td>${fila.error_rel4 !== null ? fila.error_rel4.toExponential(4) : '-'}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    
    // Agregar leyenda de métricas
    html += `
    <div class="metricas-legend">
        <h4>Explicación de Métricas de Error (norma infinito):</h4>
        <ul>
            <li><strong>E. Absoluto:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>||<sub>∞</sub></li>
            <li><strong>E. Relativo 1:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>|| / ||x<sup>(n)</sup>||<sub>∞</sub></li>
            <li><strong>E. Relativo 2:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>|| / ||x<sup>(n-1)</sup>||<sub>∞</sub></li>
            <li><strong>E. Relativo 3:</strong> Equivalente a E. Relativo 1</li>
            <li><strong>E. Relativo 4:</strong> Equivalente a E. Relativo 2</li>
        </ul>
    </div>
    `;
    
    return html;
}

// Generar informe comparativo del Capítulo 2
async function generarInformeCap2() {
    const form = document.getElementById('form-informe-cap2');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    mostrarLoading('informe-cap2', true);
    document.getElementById('resultados-informe-cap2').classList.remove('show');

    try {
        const response = await fetch('/api/capitulo2/informe', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        mostrarInformeCap2(resultado);
    } catch (error) {
        mostrarErrorInforme('informe-cap2', error.message);
    } finally {
        mostrarLoading('informe-cap2', false);
    }
}

function mostrarInformeCap2(resultado) {
    const resultadosDiv = document.getElementById('resultados-informe-cap2');
    resultadosDiv.classList.add('show');

    if (!resultado.exito) {
        resultadosDiv.innerHTML = `<div class="result-message error">${resultado.mensaje}</div>`;
        return;
    }

    let html = '<div class="informe-container">';
    html += '<h3>📊 Informe Comparativo - Capítulo 2</h3>';

    // Información sobre el tipo de error usado
    const tipoErrorLabel = resultado.tipo_error_usado === 'relativo' ? 'Cifras Significativas (5e-X)' :
                           resultado.tipo_error_usado === 'absoluto' ? 'Decimales Correctos (0.5e-X)' :
                           'Tolerancia Genérica';
    html += `<div class="info-box" style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2196F3;">`;
    html += `<p><strong>📌 Tipo de error usado para convergencia:</strong> ${tipoErrorLabel}</p>`;
    html += '</div>';

    // Tabla comparativa principal
    html += '<h4>📋 Tabla Comparativa de Resultados</h4>';
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
            html += `<td>${r.error_final.toExponential(4)}</td>`;
            html += `<td>${r.radio_espectral.toFixed(6)}</td>`;
            html += `<td>${r.converge ? '✓ Sí (ρ<1)' : '✗ No (ρ≥1)'}</td>`;
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

    // Tabla de todas las métricas de error
    const exitosos = resultado.resultados.filter(r => r.exito);
    if (exitosos.length > 0 && exitosos[0].error_abs !== null) {
        html += '<h4 style="margin-top: 30px;">📊 Comparación de las 5 Métricas de Error</h4>';
        html += '<div class="table-container"><table>';
        html += '<thead><tr>';
        html += '<th>Método</th><th>E. Absoluto</th><th>E. Relativo 1</th><th>E. Relativo 2</th><th>E. Relativo 3</th><th>E. Relativo 4</th>';
        html += '</tr></thead><tbody>';

        exitosos.forEach(r => {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td>${r.error_abs !== null ? r.error_abs.toExponential(4) : 'N/A'}</td>`;
            html += `<td>${r.error_rel1 !== null ? r.error_rel1.toExponential(4) : 'N/A'}</td>`;
            html += `<td>${r.error_rel2 !== null ? r.error_rel2.toExponential(4) : 'N/A'}</td>`;
            html += `<td>${r.error_rel3 !== null ? r.error_rel3.toExponential(4) : 'N/A'}</td>`;
            html += `<td>${r.error_rel4 !== null ? r.error_rel4.toExponential(4) : 'N/A'}</td>`;
            html += '</tr>';
        });

        html += '</tbody></table></div>';
    }

    // Análisis y conclusiones
    html += '<div class="informe-analisis">';
    html += '<h4>🏆 Análisis y Conclusiones</h4>';
    html += '<div class="conclusiones">';
    html += `<p><strong>⚡ Método más rápido (menos iteraciones):</strong> <span class="highlight">${resultado.mejor_iteraciones}</span></p>`;
    html += `<p><strong>🎯 Mejor método (menor error absoluto):</strong> <span class="highlight">${resultado.mejor_error_abs}</span></p>`;
    html += `<p><strong>📈 Mejor método (menor error relativo 1):</strong> <span class="highlight">${resultado.mejor_error_rel1}</span></p>`;
    html += `<p><strong>📊 Mejor método (menor error relativo 2):</strong> <span class="highlight">${resultado.mejor_error_rel2}</span></p>`;
    html += `<p><strong>✅ Métodos exitosos:</strong> ${resultado.estadisticas.exitosos} de ${resultado.estadisticas.total_metodos}</p>`;

    if (resultado.estadisticas.fallidos > 0) {
        html += `<p><strong>⚠️ Métodos que fallaron:</strong> ${resultado.estadisticas.fallidos}</p>`;
        html += '<p class="nota">Nota: Para garantizar convergencia, la matriz debe ser diagonalmente dominante o simétrica definida positiva.</p>';
    }

    html += '</div>';

    // Agregar leyenda de métricas
    html += '<div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">';
    html += '<h5 style="margin-top: 0;">📖 Explicación de las Métricas de Error:</h5>';
    html += '<ul style="margin: 10px 0; padding-left: 20px;">';
    html += '<li><strong>E. Absoluto:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>||<sub>∞</sub></li>';
    html += '<li><strong>E. Relativo 1:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>|| / ||x<sup>(n)</sup>||<sub>∞</sub></li>';
    html += '<li><strong>E. Relativo 2:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>|| / ||x<sup>(n-1)</sup>||<sub>∞</sub></li>';
    html += '<li><strong>E. Relativo 3:</strong> Equivalente a E. Relativo 1</li>';
    html += '<li><strong>E. Relativo 4:</strong> Equivalente a E. Relativo 2</li>';
    html += '</ul>';
    html += '</div>';

    html += '</div>';
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
    .info-box {
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    `;

    resultadosDiv.innerHTML = html;
}

function mostrarErrorInforme(metodo, mensaje) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    if (resultadosDiv) {
        resultadosDiv.classList.add('show');
        resultadosDiv.innerHTML = `<div class="result-message error">Error: ${mensaje}</div>`;
    }
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

// Objeto para almacenar calculadoras de Desmos por método
let desmosCalculators = {};

// Graficar convergencia con Desmos
async function graficarConvergencia(resultado, metodo) {
    try {
        // Verificar que exista la tabla de datos
        if (!resultado.tabla || resultado.tabla.length === 0) {
            console.log('No hay datos para graficar');
            return;
        }

        // Obtener el contenedor específico del método
        const graficaDiv = document.getElementById(`grafica-${metodo}`);
        if (!graficaDiv) {
            console.error(`No se encontró contenedor de gráfica para método: ${metodo}`);
            return;
        }

        // Determinar el tipo de error según el resultado
        const tipoError = resultado.tipo_error || 'absoluto';

        // Generar puntos para graficar
        const tabla_datos = resultado.tabla;
        const iteraciones = [];
        const errores = [];

        tabla_datos.forEach(fila => {
            if (fila.error_abs !== null && fila.error_abs !== undefined) {
                iteraciones.push(fila.iter);
                // Seleccionar el tipo de error apropiado
                if (tipoError === 'relativo') {
                    errores.push(fila.error_rel1);
                } else {
                    errores.push(fila.error_abs);
                }
            }
        });

        if (iteraciones.length === 0) {
            console.log('No hay suficientes datos para graficar');
            return;
        }

        // Crear calculadora de Desmos si no existe
        if (!desmosCalculators[metodo]) {
            graficaDiv.innerHTML = '';
            desmosCalculators[metodo] = Desmos.GraphingCalculator(graficaDiv, {
                keypad: false,
                settingsMenu: false,
                expressionsTopbar: false,
                border: false,
                lockViewport: false,
                expressions: true,
                zoomButtons: true,
                expressionsCollapsed: false
            });
        } else {
            desmosCalculators[metodo].setBlank();
        }

        const desmosCalculator = desmosCalculators[metodo];

        // Crear puntos para la gráfica (iteración, error)
        const puntos = iteraciones.map((iter, idx) => `(${iter}, ${errores[idx]})`).join(', ');

        // Agregar puntos de convergencia
        desmosCalculator.setExpression({
            id: 'puntos',
            latex: `L = [${puntos}]`,
            color: '#2E7D32',
            pointSize: 8,
            lineWidth: 2,
            lines: true,
            points: true
        });

        // Agregar línea de tolerancia si existe
        if (resultado.error_final !== undefined) {
            const tol = parseFloat(resultado.error_final);
            desmosCalculator.setExpression({
                id: 'tolerancia',
                latex: `y = ${tol}`,
                color: '#C62828',
                lineStyle: Desmos.Styles.DASHED,
                lineWidth: 2
            });
        }

        // Ajustar vista
        const maxError = Math.max(...errores.filter(e => e !== null));
        const minError = Math.min(...errores.filter(e => e !== null && e > 0));

        desmosCalculator.setMathBounds({
            left: -0.5,
            right: Math.max(...iteraciones) + 1,
            bottom: minError > 0 ? minError * 0.1 : 0,
            top: maxError * 1.2
        });

        // Agregar título
        const tipoErrorLabel = tipoError === 'relativo' ? 'Error Relativo' : 'Error Absoluto';
        desmosCalculator.setExpression({
            id: 'titulo',
            latex: `\\text{Convergencia: ${tipoErrorLabel}}`,
            color: '#000000',
            hidden: true
        });

    } catch (error) {
        console.error('Error al graficar convergencia:', error);
    }
}
