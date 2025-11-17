// JavaScript para Capítulo 1: Búsqueda de Raíces

// Cambiar entre métodos
function cambiarMetodo(metodo) {
    // Ocultar todos los paneles
    document.querySelectorAll('.metodo-panel').forEach(panel => {
        panel.classList.remove('active');
    });

    // Mostrar el panel seleccionado
    document.getElementById(metodo).classList.add('active');

    // Actualizar botones activos
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
        const response = await fetch(`/api/capitulo1/${metodo}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const resultado = await response.json();
        mostrarResultados(metodo, resultado);

        if (resultado.exito) {
            // Obtener el nombre de la función según el método
            let nombreFuncion = data.funcion || data.funcion_f || '';
            await graficarFuncion(nombreFuncion, resultado, metodo);
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
        // Formatear mensaje de error con saltos de línea y emojis
        const mensajeFormateado = resultado.mensaje
            .replace(/\n/g, '<br>')
            .replace(/•/g, '&bull;')
            .replace(/💡/g, '<span style="color: #f39c12; font-size: 1.2em;">💡</span>')
            .replace(/🔧/g, '<span style="color: #3498db; font-size: 1.2em;">🔧</span>')
            .replace(/⚠️/g, '<span style="color: #e74c3c; font-size: 1.2em;">⚠️</span>')
            .replace(/❌/g, '<span style="color: #c0392b; font-size: 1.2em;">❌</span>')
            .replace(/📊/g, '<span style="font-size: 1.2em;">📊</span>');
        html = `<div class="result-message error" style="text-align: left; line-height: 1.8;">${mensajeFormateado}</div>`;
    } else {
        // Determinar el mensaje del tipo de error
        let tipoErrorMsg = '';
        if (resultado.tipo_error === 'relativo') {
            tipoErrorMsg = '<p><strong>📊 Tipo de error:</strong> <span style="color: #3498db;">Cifras Significativas (Error Relativo)</span></p>';
        } else if (resultado.tipo_error === 'absoluto') {
            tipoErrorMsg = '<p><strong>📊 Tipo de error:</strong> <span style="color: #27ae60;">Decimales Correctos (Error Absoluto)</span></p>';
        } else if (resultado.tipo_error === 'ninguno') {
            tipoErrorMsg = '<p><strong>📊 Tipo de error:</strong> <span style="color: #e67e22;">Ninguno (Tolerancia genérica - Error Absoluto)</span></p>';
        }

        // Agregar información de derivadas si están disponibles
        let derivadaInfo = '';
        if (resultado.derivada) {
            derivadaInfo += `
                <div class="derivada-info" style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #3498db;">
                    <h4 style="color: #2c3e50; margin-bottom: 10px;">🧮 Derivadas Calculadas Automáticamente:</h4>
                    <p style="margin: 5px 0;"><strong>f'(x) =</strong> <code style="background: #e8f4f8; padding: 4px 8px; border-radius: 4px; color: #c0392b;">${resultado.derivada}</code></p>
                    ${resultado.derivada2 ? `<p style="margin: 5px 0;"><strong>f''(x) =</strong> <code style="background: #e8f4f8; padding: 4px 8px; border-radius: 4px; color: #c0392b;">${resultado.derivada2}</code></p>` : ''}
                    <p style="font-size: 0.9em; color: #666; margin-top: 10px; font-style: italic;">💡 Estas derivadas fueron calculadas automáticamente por el sistema</p>
                </div>
            `;
        }

        html = `
            <div class="result-message success">${resultado.mensaje}</div>
            <div class="result-stats">
                <p><strong>Raíz encontrada:</strong> ${resultado.raiz?.toFixed(10) || 'N/A'}</p>
                <p><strong>Iteraciones:</strong> ${resultado.iteraciones}</p>
                <p><strong>Error final:</strong> ${resultado.error_final?.toExponential(4) || 'N/A'}</p>
                ${tipoErrorMsg}
            </div>
            ${derivadaInfo}
        `;

        if (resultado.tabla) {
            html += crearTabla(resultado.tabla);
        }
    }

    resultadosDiv.innerHTML = html;
}

// Función para formatear números de manera inteligente
function formatNumero(num) {
    // Si es exactamente cero
    if (num === 0) return '0.000000';

    const absNum = Math.abs(num);

    // Si es muy pequeño (menor a 1e-4), usar notación científica
    if (absNum < 1e-4 && absNum > 0) {
        return num.toExponential(6);
    }

    // Si es muy grande (mayor a 1e6), usar notación científica
    if (absNum > 1e6) {
        return num.toExponential(6);
    }

    // Para números normales, usar 6 decimales
    return num.toFixed(6);
}

// Crear tabla de resultados (formato del profesor)
function crearTabla(tabla) {
    if (!tabla.Iteracion || tabla.Iteracion.length === 0) return '';

    let html = '<div class="table-container"><table><thead><tr>';
    html += '<th>Iteración</th>';
    html += '<th>Xm</th>';
    html += '<th>f(Xm)</th>';
    html += '<th>Error</th>';
    html += '</tr></thead><tbody>';

    // Filas
    const numFilas = tabla.Iteracion.length;
    for (let i = 0; i < numFilas; i++) {
        html += '<tr>';

        // Iteración
        html += `<td>${tabla.Iteracion[i]}</td>`;

        // Xm - formato inteligente
        const xm = tabla.Xm[i];
        if (xm !== null && xm !== undefined) {
            html += `<td>${formatNumero(xm)}</td>`;
        } else {
            html += '<td>-</td>';
        }

        // f(Xm) - formato inteligente (notación científica para valores muy pequeños)
        const fxm = tabla['f(Xm)'][i];
        if (fxm !== null && fxm !== undefined) {
            html += `<td>${formatNumero(fxm)}</td>`;
        } else {
            html += '<td>-</td>';
        }

        // Error - formato inteligente
        const error = tabla.Error[i];
        if (error === null || error === undefined) {
            html += '<td>NaN</td>';
        } else {
            html += `<td>${formatNumero(error)}</td>`;
        }

        html += '</tr>';
    }

    html += '</tbody></table></div>';
    return html;
}

// Objeto para almacenar calculadoras de Desmos por método
let desmosCalculators = {};

// Graficar función con Desmos
async function graficarFuncion(funcion, resultado, metodo) {
    try {
        // Obtener el contenedor específico del método
        const graficaDiv = document.getElementById(`grafica-${metodo}`);
        if (!graficaDiv) {
            console.error(`No se encontró contenedor de gráfica para método: ${metodo}`);
            return;
        }

        // Crear calculadora de Desmos para este método si no existe
        if (!desmosCalculators[metodo]) {
            // Solo limpiar el contenedor si vamos a crear una nueva calculadora
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
            // Si ya existe, solo limpiar las expresiones (NO el contenedor HTML)
            desmosCalculators[metodo].setBlank();
        }

        // Usar la calculadora específica del método
        const desmosCalculator = desmosCalculators[metodo];

        // Convertir la función de Python a formato Desmos
        let funcionDesmos = funcion
            .replace(/\*\*/g, '^')                    // x**2 -> x^2
            .replace(/exp\(/g, 'e^(')                 // exp(x) -> e^(x)
            .replace(/log\(/g, 'ln(')                 // log(x) -> ln(x)
            .replace(/sqrt\(/g, '\\sqrt(')            // sqrt(x) -> \sqrt(x)
            .replace(/sin\(/g, '\\sin(')              // sin(x) -> \sin(x)
            .replace(/cos\(/g, '\\cos(')              // cos(x) -> \cos(x)
            .replace(/tan\(/g, '\\tan(')              // tan(x) -> \tan(x)
            .replace(/abs\(/g, '\\abs(')              // abs(x) -> \abs(x)
            .replace(/(\d+)\*/g, '$1')                // 2*x -> 2x, 3*sin -> 3sin
            .replace(/\*(\d+)/g, '$1')                // x*2 -> x2
            .replace(/\*/g, '\\cdot ')                // Operador multiplicación restante
            .trim();

        // Agregar la función principal
        desmosCalculator.setExpression({
            id: 'funcion',
            latex: `y=${funcionDesmos}`,
            color: '#2E7D32',
            lineWidth: 3
        });

        // Agregar línea y=0
        desmosCalculator.setExpression({
            id: 'eje-x',
            latex: 'y=0',
            color: '#757575',
            lineStyle: Desmos.Styles.DASHED,
            lineWidth: 1.5
        });

        // Marcar la raíz si existe
        if (resultado.raiz) {
            const raiz = resultado.raiz;

            // Punto de la raíz
            desmosCalculator.setExpression({
                id: 'raiz',
                latex: `(${raiz}, 0)`,
                color: '#C62828',
                pointSize: 12,
                label: `Raíz ≈ ${raiz.toFixed(6)}`,
                showLabel: true,
                labelSize: Desmos.LabelSizes.MEDIUM
            });

            // Ajustar el viewport para centrar la raíz
            const margen = Math.max(Math.abs(raiz) * 0.5, 5);
            desmosCalculator.setMathBounds({
                left: raiz - margen,
                right: raiz + margen,
                bottom: -10,
                top: 10
            });
        }

        // Añadir título con texto
        desmosCalculator.setExpression({
            id: 'titulo',
            latex: `f(x) = ${funcionDesmos}`,
            color: '#000000',
            hidden: true
        });

    } catch (error) {
        console.error('Error al graficar con Desmos:', error);

        // Fallback a Plotly si Desmos falla
        console.log('Intentando con Plotly...');
        graficarConPlotly(funcion, resultado, metodo);
    }
}

// Función de respaldo con Plotly (por si Desmos falla)
async function graficarConPlotly(funcion, resultado, metodo) {
    try {
        const response = await fetch('/api/capitulo1/grafica', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                funcion: funcion,
                raiz: resultado.raiz || null
            })
        });

        const data = await response.json();

        if (data.exito) {
            const trace1 = {
                x: data.x,
                y: data.y,
                type: 'scatter',
                name: 'f(x)',
                line: {color: '#3498db', width: 3},
                mode: 'lines'
            };

            const traces = [trace1];

            if (resultado.raiz) {
                traces.push({
                    x: [resultado.raiz],
                    y: [0],
                    mode: 'markers',
                    name: `Raíz ≈ ${resultado.raiz.toFixed(6)}`,
                    marker: {size: 14, color: '#e74c3c'}
                });
            }

            const layout = {
                title: `Gráfica de f(x) = ${funcion}`,
                xaxis: {title: 'x'},
                yaxis: {title: 'f(x)'}
            };

            Plotly.newPlot(`grafica-${metodo}`, traces, layout, {responsive: true});
        }
    } catch (error) {
        console.error('Error con Plotly:', error);
    }
}

// Utilidades
function mostrarLoading(metodo, mostrar) {
    const loading = document.getElementById(`loading-${metodo}`);
    if (loading) {
        loading.classList.toggle('show', mostrar);
    }
}

function ocultarResultados(metodo) {
    const resultados = document.getElementById(`resultados-${metodo}`);
    if (resultados) {
        resultados.classList.remove('show');
    }
}

function mostrarError(metodo, mensaje) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    resultadosDiv.classList.add('show');

    // Convertir saltos de línea a <br> y mantener formato
    const mensajeFormateado = mensaje
        .replace(/\n/g, '<br>')
        .replace(/•/g, '&bull;')
        .replace(/💡/g, '<span style="color: #f39c12; font-size: 1.2em;">💡</span>')
        .replace(/🔧/g, '<span style="color: #3498db; font-size: 1.2em;">🔧</span>')
        .replace(/⚠️/g, '<span style="color: #e74c3c; font-size: 1.2em;">⚠️</span>')
        .replace(/❌/g, '<span style="color: #c0392b; font-size: 1.2em;">❌</span>')
        .replace(/📊/g, '<span style="font-size: 1.2em;">📊</span>');

    resultadosDiv.innerHTML = `<div class="result-message error" style="text-align: left; line-height: 1.8;">${mensajeFormateado}</div>`;
}

// Toggle ayuda general
function toggleAyudaGeneral() {
    const content = document.getElementById('ayuda-general-content');
    const button = document.querySelector('.ayuda-toggle');

    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.textContent = '📖 Ocultar ayuda (Click aquí)';
        button.style.background = '#27ae60';
    } else {
        content.style.display = 'none';
        button.textContent = '📖 ¿Cómo escribir funciones? (Click para ayuda)';
        button.style.background = '#3498db';
    }
}

// Toggle ayuda
function toggleAyuda(id) {
    const content = document.getElementById(id);
    content.classList.toggle('show');
}

// Validar entrada
function validarNumero(input) {
    const valor = parseFloat(input.value);
    if (isNaN(valor)) {
        input.style.borderColor = '#e74c3c';
        return false;
    }
    input.style.borderColor = '#27ae60';
    return true;
}

// ===== FUNCIÓN PARA GENERAR INFORME COMPARATIVO =====
async function generarInforme() {
    const form = document.getElementById('form-informe');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    mostrarLoading('informe', true);
    document.getElementById('resultados-informe').classList.remove('show');

    try {
        const response = await fetch('/api/capitulo1/informe', {
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
    html += '<h3>📊 Resultados de la Comparación</h3>';

    // Tabla comparativa
    html += '<div class="table-container"><table>';
    html += '<thead><tr>';
    html += '<th>Método</th><th>Estado</th><th>Raíz</th><th>Iteraciones</th><th>Error Final</th><th>Tiempo (s)</th>';
    html += '</tr></thead><tbody>';

    resultado.resultados.forEach(r => {
        if (r.exito) {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #27ae60;">✓ Exitoso</span></td>`;
            html += `<td>${r.raiz.toFixed(10)}</td>`;
            html += `<td>${r.iteraciones}</td>`;
            html += `<td>${r.error.toExponential(4)}</td>`;
            html += `<td>${(r.tiempo * 1000).toFixed(2)} ms</td>`;
            html += '</tr>';
        } else {
            html += '<tr>';
            html += `<td><strong>${r.metodo}</strong></td>`;
            html += `<td><span style="color: #e74c3c;">✗ Falló</span></td>`;
            html += `<td colspan="4">${r.error_msg || 'No convergió'}</td>`;
            html += '</tr>';
        }
    });

    html += '</tbody></table></div>';

    // Análisis y conclusiones
    html += '<div class="informe-analisis">';
    html += '<h4>🏆 Análisis y Conclusiones</h4>';
    html += '<div class="conclusiones">';
    html += `<p><strong>🎯 Mejor método (menor error):</strong> <span class="highlight">${resultado.mejor_error}</span></p>`;
    html += `<p><strong>⚡ Método más rápido (menos iteraciones):</strong> <span class="highlight">${resultado.mejor_iteraciones}</span></p>`;
    html += `<p><strong>📈 Métodos exitosos:</strong> ${resultado.estadisticas.exitosos} de ${resultado.estadisticas.total_metodos}</p>`;

    if (resultado.estadisticas.fallidos > 0) {
        html += `<p><strong>⚠️ Métodos que fallaron:</strong> ${resultado.estadisticas.fallidos}</p>`;
        html += '<p class="nota">Nota: Algunos métodos pueden fallar dependiendo de la función y los parámetros iniciales.</p>';
    }

    html += '</div></div>';

    html += '</div>';

    // Estilos adicionales para el informe
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
        border-left: 4px solid #27ae60;
    }
    .conclusiones p {
        margin: 10px 0;
        font-size: 1.05em;
    }
    .highlight {
        color: #27ae60;
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
