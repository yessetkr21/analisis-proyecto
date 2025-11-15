"""
Aplicación Flask para Métodos Numéricos
Proyecto final de Análisis Numérico
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import sys
import os

# Agregar directorio de métodos al path
sys.path.append(os.path.dirname(__file__))

from metodos import capitulo1, capitulo2, capitulo3

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# ===== FUNCIONES AUXILIARES =====

def parsear_vector_x0(x0_str, n):
    """
    Parsea el vector inicial x0 desde un string

    Parámetros:
    x0_str: String con valores separados por comas (ej: "0,0,0" o "1,2,3")
    n: Longitud esperada del vector

    Retorna: numpy array con el vector x0
    """
    # Si el string está vacío o es None, retornar vector de ceros
    if not x0_str or not x0_str.strip():
        return np.zeros(n)

    try:
        # Limpiar el string y separar por comas
        valores = [x.strip() for x in x0_str.strip().split(',') if x.strip()]

        # Convertir a float
        x0 = np.array([float(v) for v in valores])

        # Validar longitud
        if len(x0) != n:
            return np.zeros(n)

        return x0
    except (ValueError, TypeError):
        # Si hay error en la conversión, retornar vector de ceros
        return np.zeros(n)


def parsear_matriz(matriz_str, b_str):
    """
    Parsea matriz y vector b desde strings

    Parámetros:
    matriz_str: String con matriz en formato "1,2,3;4,5,6;7,8,9"
    b_str: String con vector en formato "1,2,3"

    Retorna: tuple (A, b) como numpy arrays
    """
    try:
        # Procesar matriz
        filas = matriz_str.strip().split(';')
        A = []
        for fila in filas:
            elementos = [float(x.strip()) for x in fila.split(',')]
            A.append(elementos)
        A = np.array(A)

        # Procesar vector b
        b = np.array([float(x.strip()) for x in b_str.strip().split(',')])

        return A, b
    except Exception as e:
        raise ValueError(f"Error al parsear matriz: {str(e)}")


# ===== RUTAS PRINCIPALES =====

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/capitulo1')
def pagina_capitulo1():
    """Página del Capítulo 1: Búsqueda de raíces"""
    return render_template('capitulo1.html')


@app.route('/capitulo2')
def pagina_capitulo2():
    """Página del Capítulo 2: Sistemas de ecuaciones"""
    return render_template('capitulo2.html')


@app.route('/capitulo3')
def pagina_capitulo3():
    """Página del Capítulo 3: Interpolación"""
    return render_template('capitulo3.html')


# ===== API ENDPOINTS - CAPÍTULO 1 =====

@app.route('/api/capitulo1/biseccion', methods=['POST'])
def api_biseccion():
    try:
        data = request.json
        resultado = capitulo1.biseccion(
            float(data['xi']),
            float(data['xs']),
            float(data['tol']),
            int(data['niter']),
            data['funcion']
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/regla-falsa', methods=['POST'])
def api_regla_falsa():
    try:
        data = request.json
        resultado = capitulo1.regla_falsa(
            float(data['xi']),
            float(data['xs']),
            float(data['tol']),
            int(data['niter']),
            data['funcion']
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/punto-fijo', methods=['POST'])
def api_punto_fijo():
    try:
        data = request.json
        resultado = capitulo1.punto_fijo(
            data['funcion_g'],
            float(data['x0']),
            float(data['tol']),
            int(data['niter']),
            data['funcion_f']
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/newton', methods=['POST'])
def api_newton():
    try:
        data = request.json
        resultado = capitulo1.newton_raphson(
            float(data['x0']),
            float(data['tol']),
            int(data['niter']),
            data['funcion']
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/secante', methods=['POST'])
def api_secante():
    try:
        data = request.json
        resultado = capitulo1.secante(
            float(data['x0']),
            float(data['x1']),
            float(data['tol']),
            int(data['niter']),
            data['funcion']
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/raices-multiples', methods=['POST'])
def api_raices_multiples():
    try:
        data = request.json
        metodo = int(data.get('metodo', 2))
        multiplicidad = int(data['multiplicidad']) if data.get('multiplicidad') else None

        resultado = capitulo1.raices_multiples(
            float(data['x0']),
            float(data['tol']),
            int(data['niter']),
            data['funcion'],
            metodo,
            multiplicidad
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/grafica', methods=['POST'])
def api_grafica_cap1():
    try:
        data = request.json
        x_vals, y_vals = capitulo1.generar_puntos_grafica(
            data['funcion'],
            float(data.get('x_min', -10)),
            float(data.get('x_max', 10))
        )

        if x_vals is None:
            return jsonify({"exito": False, "mensaje": "Error al generar gráfica"}), 400

        return jsonify({
            "exito": True,
            "x": x_vals,
            "y": y_vals
        })
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/comparar', methods=['POST'])
def api_comparar_cap1():
    """Compara todos los métodos del capítulo 1 con los mismos parámetros"""
    try:
        data = request.json
        funcion = data['funcion']
        xi = float(data['xi'])
        xs = float(data['xs'])
        x0 = float(data.get('x0', (xi + xs) / 2))
        tol = float(data['tol'])
        niter = int(data['niter'])

        resultados = {}

        # Bisección
        resultados['biseccion'] = capitulo1.biseccion(xi, xs, tol, niter, funcion)

        # Regla falsa
        resultados['regla_falsa'] = capitulo1.regla_falsa(xi, xs, tol, niter, funcion)

        # Newton-Raphson
        resultados['newton'] = capitulo1.newton_raphson(x0, tol, niter, funcion)

        # Secante
        resultados['secante'] = capitulo1.secante(xi, xs, tol, niter, funcion)

        # Punto fijo (requiere función g, usar solo si se proporciona)
        if 'funcion_g' in data:
            resultados['punto_fijo'] = capitulo1.punto_fijo(x0, tol, niter, funcion, data['funcion_g'])

        # Análisis comparativo
        metodos_exitosos = []
        for metodo, res in resultados.items():
            if res.get('exito'):
                metodos_exitosos.append({
                    'nombre': metodo,
                    'iteraciones': res.get('iteraciones', 0),
                    'error_final': res.get('error_final', 0),
                    'raiz': res.get('raiz', 0)
                })

        # Ordenar por número de iteraciones
        metodos_exitosos.sort(key=lambda x: x['iteraciones'])

        mejor_metodo = metodos_exitosos[0]['nombre'] if metodos_exitosos else "Ninguno"

        return jsonify({
            "exito": True,
            "resultados": resultados,
            "mejor_metodo": mejor_metodo,
            "metodos_exitosos": metodos_exitosos
        })
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


# ===== API ENDPOINTS - CAPÍTULO 2 =====

@app.route('/api/capitulo2/jacobi', methods=['POST'])
def api_jacobi():
    try:
        data = request.json
        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        resultado = capitulo2.jacobi(A, b, x0, float(data['tol']), int(data['niter']))
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo2/gauss-seidel', methods=['POST'])
def api_gauss_seidel():
    try:
        data = request.json
        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        resultado = capitulo2.gauss_seidel(A, b, x0, float(data['tol']), int(data['niter']))
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo2/sor', methods=['POST'])
def api_sor():
    try:
        data = request.json
        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        resultado = capitulo2.sor(A, b, x0, float(data['tol']), int(data['niter']), float(data['w']))
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo2/comparar', methods=['POST'])
def api_comparar_cap2():
    """Compara los tres métodos del capítulo 2"""
    try:
        data = request.json
        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))
        w = float(data.get('w', 1.5))

        resultados = capitulo2.comparar_metodos_cap2(A, b, x0, float(data['tol']), int(data['niter']), w)
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


# ===== API ENDPOINTS - CAPÍTULO 3 =====

@app.route('/api/capitulo3/vandermonde', methods=['POST'])
def api_vandermonde():
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultado = capitulo3.vandermonde(x, y)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo3/newton', methods=['POST'])
def api_newton_interpolante():
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultado = capitulo3.newton_interpolante(x, y)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo3/lagrange', methods=['POST'])
def api_lagrange():
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultado = capitulo3.lagrange(x, y)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo3/spline-lineal', methods=['POST'])
def api_spline_lineal():
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultado = capitulo3.spline_lineal(x, y)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo3/spline-cubico', methods=['POST'])
def api_spline_cubico():
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultado = capitulo3.spline_cubico(x, y)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo3/comparar', methods=['POST'])
def api_comparar_cap3():
    """Compara todos los métodos de interpolación"""
    try:
        data = request.json
        x, y, error = capitulo3.validar_puntos(data['puntos'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        resultados = capitulo3.comparar_metodos_cap3(x, y)
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


# ===== MANEJO DE ERRORES =====

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ===== ENDPOINTS DE INFORMES COMPARATIVOS =====

@app.route('/api/capitulo1/informe', methods=['POST'])
def informe_capitulo1():
    """Genera informe comparativo de todos los métodos del Capítulo 1"""
    import time
    try:
        data = request.get_json()
        funcion = data['funcion']
        xi = float(data['xi'])
        xs = float(data['xs'])
        x0 = float(data['x0'])
        x1 = float(data['x1'])
        tol = float(data['tol'])
        niter = int(data['niter'])

        resultados = []

        # 1. Bisección
        try:
            inicio = time.time()
            res = capitulo1.biseccion(xi, xs, tol, niter, funcion)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Bisección',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Bisección', 'exito': False, 'error_msg': str(e)})

        # 2. Regla Falsa
        try:
            inicio = time.time()
            res = capitulo1.regla_falsa(xi, xs, tol, niter, funcion)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Regla Falsa',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Regla Falsa', 'exito': False, 'error_msg': str(e)})

        # 3. Punto Fijo (usar g(x) = x - f(x)/3 como ejemplo)
        try:
            inicio = time.time()
            # Para punto fijo, usar una transformación simple
            g_funcion = f"x - ({funcion})/3"
            res = capitulo1.punto_fijo(g_funcion, x0, tol, niter, funcion)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Punto Fijo',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Punto Fijo', 'exito': False, 'error_msg': str(e)})

        # 4. Newton-Raphson
        try:
            inicio = time.time()
            res = capitulo1.newton_raphson(x0, tol, niter, funcion)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Newton-Raphson',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Newton-Raphson', 'exito': False, 'error_msg': str(e)})

        # 5. Secante
        try:
            inicio = time.time()
            res = capitulo1.secante(x0, x1, tol, niter, funcion)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Secante',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Secante', 'exito': False, 'error_msg': str(e)})

        # Filtrar solo métodos exitosos
        exitosos = [r for r in resultados if r.get('exito', False)]

        if not exitosos:
            return jsonify({
                'exito': False,
                'mensaje': 'Ningún método convergió. Intenta con otros parámetros.',
                'resultados': resultados
            })

        # Encontrar el mejor método (menor error)
        mejor = min(exitosos, key=lambda x: x['error'])
        mas_rapido = min(exitosos, key=lambda x: x['iteraciones'])

        return jsonify({
            'exito': True,
            'resultados': resultados,
            'mejor_error': mejor['metodo'],
            'mejor_iteraciones': mas_rapido['metodo'],
            'estadisticas': {
                'total_metodos': len(resultados),
                'exitosos': len(exitosos),
                'fallidos': len(resultados) - len(exitosos)
            }
        })

    except Exception as e:
        return jsonify({'exito': False, 'mensaje': f'Error: {str(e)}'})


@app.route('/api/capitulo2/informe', methods=['POST'])
def informe_capitulo2():
    """Genera informe comparativo de todos los métodos del Capítulo 2"""
    import time
    try:
        data = request.get_json()
        A, b = parsear_matriz(data['matriz'], data['vector_b'])
        n = len(A)
        x0 = parsear_vector_x0(data.get('x0', ''), n)
        tol = float(data['tol'])
        niter = int(data['niter'])
        w = float(data.get('w', 1.5))

        resultados = []

        # 1. Jacobi
        try:
            inicio = time.time()
            res = capitulo2.jacobi(A.copy(), b.copy(), x0.copy(), tol, niter)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Jacobi',
                    'exito': True,
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'radio_espectral': res['radio_espectral'],
                    'converge': res['converge'],
                    'tiempo': tiempo
                })
        except Exception as e:
            resultados.append({'metodo': 'Jacobi', 'exito': False, 'error_msg': str(e)})

        # 2. Gauss-Seidel
        try:
            inicio = time.time()
            res = capitulo2.gauss_seidel(A.copy(), b.copy(), x0.copy(), tol, niter)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Gauss-Seidel',
                    'exito': True,
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'radio_espectral': res['radio_espectral'],
                    'converge': res['converge'],
                    'tiempo': tiempo
                })
        except Exception as e:
            resultados.append({'metodo': 'Gauss-Seidel', 'exito': False, 'error_msg': str(e)})

        # 3. SOR
        try:
            inicio = time.time()
            res = capitulo2.sor(A.copy(), b.copy(), x0.copy(), tol, niter, w)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': f'SOR (w={w})',
                    'exito': True,
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'radio_espectral': res['radio_espectral'],
                    'converge': res['converge'],
                    'tiempo': tiempo
                })
        except Exception as e:
            resultados.append({'metodo': 'SOR', 'exito': False, 'error_msg': str(e)})

        # Filtrar solo métodos exitosos
        exitosos = [r for r in resultados if r.get('exito', False)]

        if not exitosos:
            return jsonify({
                'exito': False,
                'mensaje': 'Ningún método convergió. Verifica que la matriz sea adecuada.',
                'resultados': resultados
            })

        # Encontrar el mejor método
        mejor_iter = min(exitosos, key=lambda x: x['iteraciones'])
        mejor_error = min(exitosos, key=lambda x: x['error'])

        return jsonify({
            'exito': True,
            'resultados': resultados,
            'mejor_iteraciones': mejor_iter['metodo'],
            'mejor_error': mejor_error['metodo'],
            'estadisticas': {
                'total_metodos': len(resultados),
                'exitosos': len(exitosos),
                'fallidos': len(resultados) - len(exitosos)
            }
        })

    except Exception as e:
        return jsonify({'exito': False, 'mensaje': f'Error: {str(e)}'})


@app.route('/api/capitulo3/informe', methods=['POST'])
def informe_capitulo3():
    """Genera informe comparativo de todos los métodos del Capítulo 3"""
    import time
    try:
        data = request.get_json()
        puntos_str = data['puntos']

        resultados = []
        metodos = ['vandermonde', 'newton', 'lagrange', 'spline-lineal', 'spline-cubico']
        nombres = ['Vandermonde', 'Newton Interpolante', 'Lagrange', 'Spline Lineal', 'Spline Cúbico']

        for metodo, nombre in zip(metodos, nombres):
            try:
                inicio = time.time()
                res = capitulo3.ejecutar_metodo(metodo, puntos_str)
                tiempo = time.time() - inicio

                if res['exito']:
                    resultados.append({
                        'metodo': nombre,
                        'exito': True,
                        'polinomio': res.get('polinomio', 'N/A'),
                        'tiempo': tiempo
                    })
            except Exception as e:
                resultados.append({'metodo': nombre, 'exito': False, 'error_msg': str(e)})

        exitosos = [r for r in resultados if r.get('exito', False)]

        if not exitosos:
            return jsonify({
                'exito': False,
                'mensaje': 'Ningún método pudo interpolar los puntos.',
                'resultados': resultados
            })

        mas_rapido = min(exitosos, key=lambda x: x['tiempo'])

        return jsonify({
            'exito': True,
            'resultados': resultados,
            'mas_rapido': mas_rapido['metodo'],
            'estadisticas': {
                'total_metodos': len(resultados),
                'exitosos': len(exitosos),
                'fallidos': len(resultados) - len(exitosos)
            }
        })

    except Exception as e:
        return jsonify({'exito': False, 'mensaje': f'Error: {str(e)}'})


if __name__ == '__main__':
    print("="*60)
    print("Aplicación de Métodos Numéricos")
    print("="*60)
    print("\nIniciando servidor...")
    print("Accede a: http://localhost:5000")
    print("\nCapítulos disponibles:")
    print("  - Capítulo 1: http://localhost:5000/capitulo1")
    print("  - Capítulo 2: http://localhost:5000/capitulo2")
    print("  - Capítulo 3: http://localhost:5000/capitulo3")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000)
