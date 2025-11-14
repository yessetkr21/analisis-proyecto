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
            await graficarFuncion(data.funcion, resultado);
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
                <p><strong>Raíz encontrada:</strong> ${resultado.raiz?.toFixed(10) || 'N/A'}</p>
                <p><strong>Iteraciones:</strong> ${resultado.iteraciones}</p>
                <p><strong>Error final:</strong> ${resultado.error_final?.toExponential(4) || 'N/A'}</p>
            </div>
        `;

        if (resultado.tabla) {
            html += crearTabla(resultado.tabla);
        }
    }

    resultadosDiv.innerHTML = html;
}

// Crear tabla de resultados
function crearTabla(tabla) {
    if (!tabla.iter || tabla.iter.length === 0) return '';

    let html = '<div class="table-container"><table><thead><tr>';

    // Encabezados
    for (let key in tabla) {
        html += `<th>${key}</th>`;
    }
    html += '</tr></thead><tbody>';

    // Filas
    const numFilas = tabla.iter.length;
    for (let i = 0; i < numFilas; i++) {
        html += '<tr>';
        for (let key in tabla) {
            const valor = tabla[key][i];
            html += `<td>${valor !== null && valor !== undefined ?
                (typeof valor === 'number' ? valor.toExponential(6) : valor) :
                '-'}</td>`;
        }
        html += '</tr>';
    }

    html += '</tbody></table></div>';
    return html;
}

// Graficar función con Plotly
async function graficarFuncion(funcion, resultado) {
    try {
        const response = await fetch('/api/capitulo1/grafica', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({funcion})
        });

        const data = await response.json();

        if (data.exito) {
            const trace1 = {
                x: data.x,
                y: data.y,
                type: 'scatter',
                name: 'f(x)',
                line: {color: '#3498db', width: 2}
            };

            const traces = [trace1];

            // Añadir punto de la raíz
            if (resultado.raiz) {
                traces.push({
                    x: [resultado.raiz],
                    y: [0],
                    mode: 'markers',
                    name: 'Raíz',
                    marker: {size: 12, color: '#e74c3c'}
                });
            }

            const layout = {
                title: 'Gráfica de f(x)',
                xaxis: {title: 'x'},
                yaxis: {title: 'f(x)'},
                hovermode: 'closest'
            };

            Plotly.newPlot('grafica', traces, layout, {responsive: true});
        }
    } catch (error) {
        console.error('Error al graficar:', error);
    }
}

// Comparar todos los métodos
async function compararMetodos() {
    const formData = {
        funcion: document.getElementById('comp-funcion').value,
        xi: document.getElementById('comp-xi').value,
        xs: document.getElementById('comp-xs').value,
        x0: document.getElementById('comp-x0').value,
        tol: document.getElementById('comp-tol').value,
        niter: document.getElementById('comp-niter').value
    };

    mostrarLoading('comparacion', true);

    try {
        const response = await fetch('/api/capitulo1/comparar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });

        const resultado = await response.json();
        mostrarComparacion(resultado);
    } catch (error) {
        console.error('Error:', error);
    } finally {
        mostrarLoading('comparacion', false);
    }
}

// Mostrar comparación
function mostrarComparacion(resultado) {
    const div = document.getElementById('resultados-comparacion');
    div.classList.add('show');

    let html = '<h3>Resultados de la Comparación</h3>';
    html += `<div class="mejor-metodo">Mejor Método: ${resultado.mejor_metodo}</div>`;

    html += '<div class="comparacion-grid">';
    resultado.metodos_exitosos.forEach(metodo => {
        html += `
            <div class="comparacion-card">
                <h4>${metodo.nombre}</h4>
                <p><strong>Raíz:</strong> ${metodo.raiz.toFixed(10)}</p>
                <p><strong>Iteraciones:</strong> ${metodo.iteraciones}</p>
                <p><strong>Error:</strong> ${metodo.error_final.toExponential(4)}</p>
            </div>
        `;
    });
    html += '</div>';

    div.innerHTML = html;
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
    resultadosDiv.innerHTML = `<div class="result-message error">Error: ${mensaje}</div>`;
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
