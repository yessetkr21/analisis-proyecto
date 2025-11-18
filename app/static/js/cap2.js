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

    // VALIDACIONES FRONTEND
    const validacion = validarDatosCapitulo2(data, metodo);
    if (!validacion.valido) {
        mostrarError(metodo, validacion.mensaje);
        return;
    }

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
        mostrarError(metodo, `Error de conexión: ${error.message}`);
    } finally {
        mostrarLoading(metodo, false);
    }
}

// Función de validación para Capítulo 2
function validarDatosCapitulo2(data, metodo) {
    // 1. Validar que la matriz no esté vacía
    if (!data.matriz || data.matriz.trim() === '') {
        return { valido: false, mensaje: '[ERROR] Error: La matriz A es obligatoria. Ejemplo: 10,1,1;2,10,1;2,2,10' };
    }

    // 2. Validar que el vector b no esté vacío
    if (!data.vector_b || data.vector_b.trim() === '') {
        return { valido: false, mensaje: '[ERROR] Error: El vector b es obligatorio. Ejemplo: 12,13,14' };
    }

    // 3. Validar tolerancia
    if (!data.tol || data.tol.trim() === '') {
        return { valido: false, mensaje: '[ERROR] Error: La tolerancia es obligatoria. Ejemplo: 1e-6 o 0.0001' };
    }

    // Validar que la tolerancia sea un número válido
    const tol = parseFloat(data.tol);
    if (isNaN(tol) || tol <= 0) {
        return { valido: false, mensaje: `[ERROR] Error: La tolerancia debe ser un número positivo. Valor ingresado: "${data.tol}"` };
    }

    if (tol >= 1) {
        return { valido: false, mensaje: '[ERROR] Error: La tolerancia debe ser menor que 1 (ejemplo: 1e-6, 0.0001)' };
    }

    // 4. Validar iteraciones máximas
    if (!data.niter || data.niter.trim() === '') {
        return { valido: false, mensaje: '[ERROR] Error: El número de iteraciones es obligatorio. Ejemplo: 100' };
    }

    const niter = parseInt(data.niter);
    if (isNaN(niter) || niter <= 0) {
        return { valido: false, mensaje: `[ERROR] Error: Las iteraciones deben ser un número entero positivo. Valor ingresado: "${data.niter}"` };
    }

    if (niter > 10000) {
        return { valido: false, mensaje: '[ERROR] Error: Número de iteraciones muy grande (máximo: 10000)' };
    }

    // 5. Validar formato de matriz
    const filas = data.matriz.trim().split(';');
    if (filas.length === 0) {
        return { valido: false, mensaje: '[ERROR] Error: La matriz debe tener al menos una fila. Separa filas con ";"' };
    }

    if (filas.length > 7) {
        return { valido: false, mensaje: `[ERROR] Error: La matriz no puede tener más de 7 filas. Filas ingresadas: ${filas.length}` };
    }

    // Validar que todas las filas tengan el mismo número de elementos
    const nCols = filas[0].split(',').length;
    for (let i = 1; i < filas.length; i++) {
        const cols = filas[i].split(',').length;
        if (cols !== nCols) {
            return { valido: false, mensaje: `[ERROR] Error: Todas las filas deben tener el mismo número de columnas. Fila 1: ${nCols} cols, Fila ${i+1}: ${cols} cols` };
        }
    }

    // Validar que sea matriz cuadrada
    if (filas.length !== nCols) {
        return { valido: false, mensaje: `[ERROR] Error: La matriz debe ser cuadrada. Dimensión actual: ${filas.length}x${nCols}` };
    }

    // 6. Validar formato del vector b
    const elementosB = data.vector_b.trim().split(',');
    if (elementosB.length !== filas.length) {
        return { valido: false, mensaje: `[ERROR] Error: El vector b debe tener ${filas.length} elementos (igual al número de filas de A). Elementos en b: ${elementosB.length}` };
    }

    // 7. Validar factor w para SOR
    if (metodo === 'sor') {
        if (!data.w || data.w.trim() === '') {
            return { valido: false, mensaje: '[ERROR] Error: El factor de relajación w es obligatorio para SOR. Valor recomendado: 1.5' };
        }

        const w = parseFloat(data.w);
        if (isNaN(w) || w <= 0 || w >= 2) {
            return { valido: false, mensaje: `[ERROR] Error: El factor w debe estar entre 0 y 2. Valor ingresado: "${data.w}"` };
        }
    }

    return { valido: true };
}

// Guardar resultados globalmente para poder actualizar precisión
if (!window.lastResults) {
    window.lastResults = {};
}

// Mostrar resultados
function mostrarResultados(metodo, resultado) {
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    resultadosDiv.classList.add('show');

    // Guardar resultado para poder cambiar precisión después
    window.lastResults[metodo] = resultado;

    let html = '';

    if (!resultado.exito) {
        html = `<div class="result-message error">${resultado.mensaje}</div>`;
    } else {
        const decimalesSolucion = mostrarAltaPrecision ? 12 : 6;
        html = `
            <div class="result-message success">${resultado.mensaje}</div>
            <div class="result-stats">
                <p><strong>Radio Espectral:</strong> ${resultado.radio_espectral?.toFixed(6) || 'N/A'}</p>
                <p><strong>¿Converge?:</strong> ${resultado.converge ? '✓ Sí (ρ < 1)' : '✗ No (ρ ≥ 1)'}</p>
                <p><strong>Iteraciones:</strong> ${resultado.iteraciones}</p>
                <p><strong>Error final:</strong> ${resultado.error_final?.toExponential(4) || 'N/A'}</p>
                <p><strong>Solución:</strong> [${resultado.solucion?.map(v => v.toFixed(decimalesSolucion)).join(', ') || 'N/A'}]</p>
            </div>
        `;

        if (resultado.tabla) {
            html += crearTablaIteraciones(resultado.tabla, metodo);
        }
    }

    resultadosDiv.innerHTML = html;

    // Graficar convergencia si el resultado fue exitoso
    if (resultado.exito && resultado.tabla) {
        graficarConvergencia(resultado, metodo);
    }
}

// Variable global para controlar precisión de decimales
let mostrarAltaPrecision = false;

// Crear tabla de iteraciones simplificada (como el código del profesor)
function crearTablaIteraciones(tabla, metodo) {
    if (!tabla || tabla.length === 0) return '';

    let html = '';

    // Botón para alternar precisión
    html += `
    <div style="margin-bottom: 10px; text-align: right;">
        <button onclick="alternarPrecision('${metodo}')" class="btn-precision" id="btn-precision-${metodo}">
            🔍 Mostrar más decimales
        </button>
    </div>
    `;

    html += '<div class="table-container"><table id="tabla-' + metodo + '"><thead><tr>';
    html += '<th>Iteración</th>';

    // Encabezados para cada variable
    const numVars = tabla[0].x.length;
    for (let i = 0; i < numVars; i++) {
        html += `<th>x${i+1}</th>`;
    }
    // Solo un error
    html += '<th>Error</th>';
    html += '</tr></thead><tbody>';

    // Filas - usar precisión según estado
    const decimales = mostrarAltaPrecision ? 12 : 6;
    tabla.forEach(fila => {
        html += '<tr>';
        html += `<td><strong>${fila.iter}</strong></td>`;
        fila.x.forEach(val => {
            html += `<td class="valor-x">${val.toFixed(decimales)}</td>`;
        });
        // Mostrar el error
        html += `<td>${fila.error !== null && fila.error !== undefined ? fila.error.toExponential(4) : '-'}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table></div>';

    // Agregar nota sobre el error
    html += `
    <div class="metricas-legend">
        <p><strong>Error:</strong> ||x<sup>(n)</sup> - x<sup>(n-1)</sup>||<sub>∞</sub> (norma infinito)</p>
    </div>
    `;

    return html;
}

// Función para alternar entre 6 y 12 decimales
function alternarPrecision(metodo) {
    mostrarAltaPrecision = !mostrarAltaPrecision;

    // Obtener los datos originales del último resultado
    const resultadosDiv = document.getElementById(`resultados-${metodo}`);
    if (!resultadosDiv || !window.lastResults || !window.lastResults[metodo]) {
        console.error('No hay datos para actualizar');
        return;
    }

    const resultado = window.lastResults[metodo];

    // Regenerar solo la tabla
    const decimales = mostrarAltaPrecision ? 12 : 6;
    const tabla = resultado.tabla;

    // Actualizar solo los valores de x en la tabla
    const tablaDom = document.getElementById(`tabla-${metodo}`);
    if (tablaDom) {
        const filas = tablaDom.querySelectorAll('tbody tr');
        filas.forEach((fila, index) => {
            const celdas = fila.querySelectorAll('.valor-x');
            celdas.forEach((celda, i) => {
                celda.textContent = tabla[index].x[i].toFixed(decimales);
            });
        });
    }

    // Actualizar texto del botón
    const btn = document.getElementById(`btn-precision-${metodo}`);
    if (btn) {
        btn.textContent = mostrarAltaPrecision ? '🔍 Mostrar menos decimales' : '🔍 Mostrar más decimales';
    }
}

// Generar informe comparativo del Capítulo 2
async function generarInformeCap2() {
    const form = document.getElementById('form-informe-cap2');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // VALIDACIONES FRONTEND
    const validacion = validarDatosCapitulo2(data, 'informe');
    if (!validacion.valido) {
        mostrarErrorInforme('informe-cap2', validacion.mensaje);
        return;
    }

    // Validar factor w para el informe (necesario para SOR)
    if (!data.w || data.w.trim() === '') {
        mostrarErrorInforme('informe-cap2', '[ERROR] Error: El factor w es obligatorio para ejecutar SOR en el informe. Valor recomendado: 1.5');
        return;
    }

    const w = parseFloat(data.w);
    if (isNaN(w) || w <= 0 || w >= 2) {
        mostrarErrorInforme('informe-cap2', `[ERROR] Error: El factor w debe estar entre 0 y 2. Valor ingresado: "${data.w}"`);
        return;
    }

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
        mostrarErrorInforme('informe-cap2', `Error de conexión: ${error.message}`);
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

    // Información sobre el cálculo del error
    html += `<div class="info-box" style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2196F3; color: #1565c0;">`;
    html += `<p style="color: #1565c0; margin: 0;"><strong>📌 Criterio de convergencia:</strong> Error calculado con norma infinito ||x<sup>(n)</sup> - x<sup>(n-1)</sup>||<sub>∞</sub></p>`;
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

    // Análisis y conclusiones
    html += '<div class="informe-analisis">';
    html += '<h4>🏆 Análisis y Conclusiones</h4>';
    html += '<div class="conclusiones">';
    html += `<p><strong>⚡ Método más rápido (menos iteraciones):</strong> <span class="highlight">${resultado.mejor_iteraciones}</span></p>`;
    html += `<p><strong>🎯 Método con menor error final:</strong> <span class="highlight">${resultado.mejor_error}</span></p>`;
    html += `<p><strong>✅ Métodos exitosos:</strong> ${resultado.estadisticas.exitosos} de ${resultado.estadisticas.total_metodos}</p>`;

    if (resultado.estadisticas.fallidos > 0) {
        html += `<p><strong>⚠️ Métodos que fallaron:</strong> ${resultado.estadisticas.fallidos}</p>`;
        html += '<p class="nota">Nota: Para garantizar convergencia, la matriz debe ser diagonalmente dominante o simétrica definida positiva.</p>';
    }

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

        // Generar puntos para graficar
        const tabla_datos = resultado.tabla;
        const iteraciones = [];
        const errores = [];

        tabla_datos.forEach(fila => {
            if (fila.error !== null && fila.error !== undefined) {
                iteraciones.push(fila.iter);
                errores.push(fila.error);
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
        desmosCalculator.setExpression({
            id: 'titulo',
            latex: `\\text{Convergencia (Norma Infinito)}`,
            color: '#000000',
            hidden: true
        });

    } catch (error) {
        console.error('Error al graficar convergencia:', error);
    }
}

// Función para toggle del botón de ayuda
function toggleAyudaGeneral() {
    const content = document.getElementById('ayuda-general-content');
    const button = document.querySelector('.ayuda-toggle');

    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        button.textContent = 'Ocultar ayuda (Click aqui)';
        button.style.background = '#27ae60';
    } else {
        content.style.display = 'none';
        button.textContent = 'Formato de Entrada (Click para ayuda)';
        button.style.background = '#3498db';
    }
}
