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


@app.route('/test_desmos')
def test_desmos():
    """Página de prueba para Desmos"""
    return render_template('test_desmos.html')


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

        # Validar que todos los campos estén presentes
        required_fields = ['xi', 'xs', 'tol', 'niter', 'funcion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"exito": False, "mensaje": f"[ERROR] Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar tipos de datos
        try:
            xi = float(data['xi'])
            xs = float(data['xs'])
            tol = float(data['tol'])
            niter = int(data['niter'])
        except (ValueError, TypeError):
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores numéricos no son válidos.\n💡 Asegúrate de que xi, xs, tol y niter sean números."}), 400

        # Validar rangos
        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser un número positivo.\n💡 Ejemplo: 1e-5"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser positivo.\n💡 Ejemplo: 100"}), 400

        if xi == xs:
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores xi y xs deben ser diferentes.\n💡 Necesitas un intervalo [xi, xs] válido."}), 400

        tol_str = str(data['tol'])  # Mantener string original
        resultado = capitulo1.biseccion(xi, xs, tol, niter, data['funcion'], tol_str)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 400


@app.route('/api/capitulo1/regla-falsa', methods=['POST'])
def api_regla_falsa():
    try:
        data = request.json

        # Validar campos requeridos
        required_fields = ['xi', 'xs', 'tol', 'niter', 'funcion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"exito": False, "mensaje": f"[ERROR] Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar tipos
        try:
            xi = float(data['xi'])
            xs = float(data['xs'])
            tol = float(data['tol'])
            niter = int(data['niter'])
        except (ValueError, TypeError):
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores numéricos no son válidos.\n💡 Asegúrate de que xi, xs, tol y niter sean números."}), 400

        # Validar rangos
        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser un número positivo.\n💡 Ejemplo: 1e-5"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser positivo.\n💡 Ejemplo: 100"}), 400

        if xi == xs:
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores xi y xs deben ser diferentes.\n💡 Necesitas un intervalo [xi, xs] válido."}), 400

        tol_str = str(data['tol'])
        resultado = capitulo1.regla_falsa(xi, xs, tol, niter, data['funcion'], tol_str)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 400


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

        # Validar campos requeridos
        required_fields = ['x0', 'tol', 'niter', 'funcion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"exito": False, "mensaje": f"[ERROR] Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar tipos
        try:
            x0 = float(data['x0'])
            tol = float(data['tol'])
            niter = int(data['niter'])
        except (ValueError, TypeError):
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores numéricos no son válidos.\n💡 Asegúrate de que x0, tol y niter sean números."}), 400

        # Validar rangos
        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser un número positivo.\n💡 Ejemplo: 1e-5"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser positivo.\n💡 Ejemplo: 100"}), 400

        resultado = capitulo1.newton_raphson(x0, tol, niter, data['funcion'])
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 400


@app.route('/api/capitulo1/secante', methods=['POST'])
def api_secante():
    try:
        data = request.json

        # Validar campos requeridos
        required_fields = ['x0', 'x1', 'tol', 'niter', 'funcion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"exito": False, "mensaje": f"[ERROR] Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar tipos
        try:
            x0 = float(data['x0'])
            x1 = float(data['x1'])
            tol = float(data['tol'])
            niter = int(data['niter'])
        except (ValueError, TypeError):
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores numéricos no son válidos.\n💡 Asegúrate de que x0, x1, tol y niter sean números."}), 400

        # Validar rangos
        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser un número positivo.\n💡 Ejemplo: 1e-5"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser positivo.\n💡 Ejemplo: 100"}), 400

        if x0 == x1:
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores x0 y x1 deben ser diferentes.\n💡 Necesitas dos puntos iniciales distintos."}), 400

        tol_str = str(data['tol'])
        resultado = capitulo1.secante(x0, x1, tol, niter, data['funcion'], tol_str)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo1/raices-multiples', methods=['POST'])
def api_raices_multiples():
    try:
        data = request.json

        # Validar campos requeridos
        required_fields = ['x0', 'tol', 'niter', 'funcion']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"exito": False, "mensaje": f"[ERROR] Faltan campos requeridos: {', '.join(missing_fields)}"}), 400

        # Validar tipos
        try:
            x0 = float(data['x0'])
            tol = float(data['tol'])
            niter = int(data['niter'])
            metodo = int(data.get('metodo', 2))
            multiplicidad = int(data['multiplicidad']) if data.get('multiplicidad') else None
        except (ValueError, TypeError):
            return jsonify({"exito": False, "mensaje": "[ERROR] Los valores numéricos no son válidos.\n💡 Asegúrate de que x0, tol, niter y metodo sean números."}), 400

        # Validar rangos
        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser un número positivo.\n💡 Ejemplo: 1e-5"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser positivo.\n💡 Ejemplo: 100"}), 400

        if metodo not in [1, 2]:
            return jsonify({"exito": False, "mensaje": "[ERROR] El método debe ser 1 (con multiplicidad) o 2 (con segunda derivada)."}), 400

        if metodo == 1 and not multiplicidad:
            return jsonify({"exito": False, "mensaje": "[ERROR] Para el método 1 debes especificar la multiplicidad.\n💡 Ejemplo: 2 para raíz doble, 3 para raíz triple."}), 400

        tol_str = str(data['tol'])
        resultado = capitulo1.raices_multiples(x0, tol, niter, data['funcion'], metodo, multiplicidad, tol_str)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 400


@app.route('/api/capitulo1/grafica', methods=['POST'])
def api_grafica_cap1():
    try:
        data = request.json
        raiz = data.get('raiz', None)

        x_vals, y_vals = capitulo1.generar_puntos_grafica(
            data['funcion'],
            x_min=data.get('x_min', None),
            x_max=data.get('x_max', None),
            raiz=raiz
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
        tol_str = str(data['tol'])  # Mantener string original
        niter = int(data['niter'])

        resultados = {}

        # Bisección
        resultados['biseccion'] = capitulo1.biseccion(xi, xs, tol, niter, funcion, tol_str)

        # Regla falsa
        resultados['regla_falsa'] = capitulo1.regla_falsa(xi, xs, tol, niter, funcion, tol_str)

        # Newton-Raphson
        resultados['newton'] = capitulo1.newton_raphson(x0, tol, niter, funcion)

        # Secante
        resultados['secante'] = capitulo1.secante(xi, xs, tol, niter, funcion, tol_str)

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

        # Validar que se recibió JSON
        if not data:
            return jsonify({"exito": False, "mensaje": "[ERROR] No se recibieron datos"}), 400

        # Validar campos obligatorios
        if 'matriz' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'matriz'"}), 400
        if 'vector_b' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'vector_b'"}), 400
        if 'tol' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'tol' (tolerancia)"}), 400
        if 'niter' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'niter' (iteraciones)"}), 400

        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        # Validar tolerancia y niter
        try:
            tol = float(data['tol'])
            niter = int(data['niter'])
        except ValueError:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia y el número de iteraciones deben ser números válidos"}), 400

        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser mayor que 0"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser mayor que 0"}), 400

        resultado = capitulo2.jacobi(A, b, x0, tol, niter)
        return jsonify(resultado)
    except KeyError as ke:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Falta el campo obligatorio: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 500


@app.route('/api/capitulo2/gauss-seidel', methods=['POST'])
def api_gauss_seidel():
    try:
        data = request.json

        # Validar que se recibió JSON
        if not data:
            return jsonify({"exito": False, "mensaje": "[ERROR] No se recibieron datos"}), 400

        # Validar campos obligatorios
        if 'matriz' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'matriz'"}), 400
        if 'vector_b' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'vector_b'"}), 400
        if 'tol' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'tol' (tolerancia)"}), 400
        if 'niter' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'niter' (iteraciones)"}), 400

        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        # Validar tolerancia y niter
        try:
            tol = float(data['tol'])
            niter = int(data['niter'])
        except ValueError:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia y el número de iteraciones deben ser números válidos"}), 400

        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser mayor que 0"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser mayor que 0"}), 400

        resultado = capitulo2.gauss_seidel(A, b, x0, tol, niter)
        return jsonify(resultado)
    except KeyError as ke:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Falta el campo obligatorio: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 500


@app.route('/api/capitulo2/sor', methods=['POST'])
def api_sor():
    try:
        data = request.json

        # Validar que se recibió JSON
        if not data:
            return jsonify({"exito": False, "mensaje": "[ERROR] No se recibieron datos"}), 400

        # Validar campos obligatorios
        if 'matriz' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'matriz'"}), 400
        if 'vector_b' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'vector_b'"}), 400
        if 'tol' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'tol' (tolerancia)"}), 400
        if 'niter' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'niter' (iteraciones)"}), 400
        if 'w' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'w' (factor de relajación)"}), 400

        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])

        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        x0 = parsear_vector_x0(data.get('x0', ''), len(A))

        # Validar tolerancia, niter y w
        try:
            tol = float(data['tol'])
            niter = int(data['niter'])
            w = float(data['w'])
        except ValueError:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia, iteraciones y factor w deben ser números válidos"}), 400

        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser mayor que 0"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser mayor que 0"}), 400

        if w <= 0 or w >= 2:
            return jsonify({"exito": False, "mensaje": "[ERROR] El factor de relajación w debe estar entre 0 y 2 (0 < w < 2)"}), 400

        resultado = capitulo2.sor(A, b, x0, tol, niter, w)
        return jsonify(resultado)
    except KeyError as ke:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Falta el campo obligatorio: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"exito": False, "mensaje": f"[ERROR] Error inesperado: {str(e)}"}), 500


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

        tol_str = str(data['tol'])  # Mantener string original
        resultados = capitulo2.comparar_metodos_cap2(A, b, x0, float(data['tol']), int(data['niter']), w, tol_str)
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"exito": False, "mensaje": str(e)}), 400


@app.route('/api/capitulo2/grafica-convergencia', methods=['POST'])
def api_grafica_convergencia_cap2():
    """Genera puntos para graficar la convergencia de un método iterativo"""
    try:
        data = request.json
        tabla_datos = data.get('tabla', [])
        tipo_error = data.get('tipo_error', 'absoluto')

        if not tabla_datos:
            return jsonify({"exito": False, "mensaje": "No hay datos para graficar"}), 400

        iteraciones, errores = capitulo2.generar_puntos_grafica_convergencia(tabla_datos, tipo_error)

        return jsonify({
            "exito": True,
            "iteraciones": iteraciones,
            "errores": errores,
            "tipo_error": tipo_error
        })
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
        tol_str = str(data['tol'])  # Mantener string original
        niter = int(data['niter'])

        resultados = []

        # 1. Bisección
        try:
            inicio = time.time()
            res = capitulo1.biseccion(xi, xs, tol, niter, funcion, tol_str)
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
            res = capitulo1.regla_falsa(xi, xs, tol, niter, funcion, tol_str)
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
            res = capitulo1.secante(x0, x1, tol, niter, funcion, tol_str)
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

        # 6. Raíces Múltiples
        try:
            inicio = time.time()
            res = capitulo1.raices_multiples(x0, tol, niter, funcion, 2, None, tol_str)
            tiempo = time.time() - inicio
            if res['exito']:
                resultados.append({
                    'metodo': 'Raíces Múltiples',
                    'raiz': res['raiz'],
                    'iteraciones': res['iteraciones'],
                    'error': res['error_final'],
                    'tiempo': tiempo,
                    'exito': True
                })
        except Exception as e:
            resultados.append({'metodo': 'Raíces Múltiples', 'exito': False, 'error_msg': str(e)})

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

        # Validar que se recibió JSON
        if not data:
            return jsonify({"exito": False, "mensaje": "[ERROR] No se recibieron datos"}), 400

        # Validar campos obligatorios
        if 'matriz' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'matriz'"}), 400
        if 'vector_b' not in data:
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'vector_b'"}), 400
        if 'tol' not in data or not data['tol'] or str(data['tol']).strip() == '':
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'tol' (tolerancia). Debe ingresar un valor como 1e-6 o 0.0001"}), 400
        if 'niter' not in data or not data['niter'] or str(data['niter']).strip() == '':
            return jsonify({"exito": False, "mensaje": "[ERROR] Falta el campo 'niter' (iteraciones). Debe ingresar un número entero positivo"}), 400

        # Validar matriz usando la función del módulo
        A, b, error = capitulo2.validar_matriz(data['matriz'], data['vector_b'])
        if error:
            return jsonify({"exito": False, "mensaje": error}), 400

        n = len(A)
        x0 = parsear_vector_x0(data.get('x0', ''), n)

        # Validar tolerancia y niter
        try:
            tol = float(data['tol'])
            niter = int(data['niter'])
        except ValueError:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia y el número de iteraciones deben ser números válidos"}), 400

        if tol <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] La tolerancia debe ser mayor que 0"}), 400

        if niter <= 0:
            return jsonify({"exito": False, "mensaje": "[ERROR] El número de iteraciones debe ser mayor que 0"}), 400

        # Validar w (opcional, valor por defecto 1.5)
        try:
            w = float(data.get('w', 1.5))
        except ValueError:
            return jsonify({"exito": False, "mensaje": "[ERROR] El factor de relajación w debe ser un número válido"}), 400

        if w <= 0 or w >= 2:
            return jsonify({"exito": False, "mensaje": "[ERROR] El factor de relajación w debe estar entre 0 y 2 (0 < w < 2)"}), 400

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
                    'error_final': res['error_final'],
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
                    'error_final': res['error_final'],
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
                    'error_final': res['error_final'],
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

        # Encontrar el mejor método por diferentes criterios
        mejor_iter = min(exitosos, key=lambda x: x['iteraciones'])
        mejor_error = min(exitosos, key=lambda x: x['error_final'])

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
    import numpy as np
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
                    # Calcular error promedio si está disponible
                    error_promedio = None
                    if 'errores' in res and res['errores']:
                        error_promedio = float(np.mean(res['errores']))

                    resultados.append({
                        'metodo': nombre,
                        'exito': True,
                        'polinomio': res.get('polinomio', 'N/A'),
                        'tiempo': tiempo,
                        'error_promedio': error_promedio,
                        'errores': res.get('errores', [])
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

        # Identificar método más rápido
        mas_rapido = min(exitosos, key=lambda x: x['tiempo'])

        # Identificar método con menor error (solo métodos polinomiales que tienen errores)
        exitosos_con_error = [r for r in exitosos if r.get('error_promedio') is not None]

        menor_error = None
        mejor_metodo = None

        if exitosos_con_error:
            menor_error = min(exitosos_con_error, key=lambda x: x['error_promedio'])

            # Determinar mejor método general (balance entre error y tiempo)
            # Para métodos polinomiales (Vandermonde, Newton, Lagrange), todos dan el mismo resultado
            # así que el mejor es el más rápido entre ellos
            metodos_polinomiales = [r for r in exitosos_con_error if r['metodo'] in ['Vandermonde', 'Newton Interpolante', 'Lagrange']]

            if metodos_polinomiales:
                mejor_metodo = min(metodos_polinomiales, key=lambda x: x['tiempo'])
            else:
                mejor_metodo = menor_error

        return jsonify({
            'exito': True,
            'resultados': resultados,
            'mas_rapido': mas_rapido['metodo'],
            'menor_error': menor_error['metodo'] if menor_error else 'N/A',
            'mejor_metodo': mejor_metodo['metodo'] if mejor_metodo else mas_rapido['metodo'],
            'estadisticas': {
                'total_metodos': len(resultados),
                'exitosos': len(exitosos),
                'fallidos': len(resultados) - len(exitosos),
                'error_minimo': menor_error['error_promedio'] if menor_error else None,
                'tiempo_minimo': mas_rapido['tiempo']
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
