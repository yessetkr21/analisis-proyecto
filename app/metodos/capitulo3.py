"""
Métodos numéricos del Capítulo 3: Interpolación
Incluye: Vandermonde, Newton, Lagrange, Spline Lineal y Spline Cúbico
"""

import numpy as np
import sympy as sp
 
 
def vandermonde(x, y):
    """
    Método de Vandermonde para interpolación polinomial

    Retorna: dict con 'exito', 'coeficientes', 'polinomio_str', 'puntos_grafic a'
    """
    try:
        n = len(x)
        grado = n - 1

        # Construir matriz de Vandermonde
        A = np.zeros((n, n))
        for i in range(n):
            A[:, i] = x ** (grado - i)

        # Resolver sistema A*a = y
        coeficientes = np.linalg.solve(A, y)

        # Crear string del polinomio
        polinomio_str = crear_string_polinomio(coeficientes)

        # Generar puntos para graficar
        x_plot = np.linspace(min(x) - 0.5, max(x) + 0.5, 200)
        y_plot = evaluar_polinomio(coeficientes, x_plot)

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = evaluar_polinomio(coeficientes, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "coeficientes": coeficientes.tolist(),
            "polinomio_str": polinomio_str,
            "puntos_grafica": {"x": x_plot.tolist(), "y": y_plot.tolist()},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores,
            "matriz_vandermonde": A.tolist()
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def newton_interpolante(x, y):
    """
    Método de Newton con diferencias divididas para interpolación

    Retorna: dict con 'exito', 'tabla', 'coeficientes', 'polinomio_str', 'puntos_grafica'
    """
    try:
        n = len(x)
        Tabla = np.zeros((n, n + 1))
        Tabla[:, 0] = x
        Tabla[:, 1] = y

        # Calcular diferencias divididas
        for j in range(2, n + 1):
            for i in range(j - 1, n):
                Tabla[i, j] = (Tabla[i, j-1] - Tabla[i-1, j-1]) / (Tabla[i, 0] - Tabla[i-j+1, 0])

        # Extraer coeficientes (diagonal de diferencias divididas)
        coeficientes = []
        for i in range(n):
            coeficientes.append(Tabla[i, i+1])

        # Crear string del polinomio de Newton
        polinomio_str = crear_string_newton(coeficientes, x)

        # Generar puntos para graficar
        x_plot = np.linspace(min(x) - 0.5, max(x) + 0.5, 200)
        y_plot = np.array([evaluar_newton(Tabla, xi) for xi in x_plot])

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = evaluar_newton(Tabla, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "tabla": Tabla.tolist(),
            "coeficientes": coeficientes,
            "polinomio_str": polinomio_str,
            "puntos_grafica": {"x": x_plot.tolist(), "y": y_plot.tolist()},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def lagrange(x, y):
    """
    Método de Lagrange para interpolación polinomial

    Retorna: dict con 'exito', 'coeficientes', 'polinomio_str', 'puntos_grafica'
    """
    try:
        n = len(x)

        # Calcular polinomio de Lagrange
        coeficientes = np.zeros(n)

        for i in range(n):
            Li = np.array([1.0])
            den = 1.0

            for j in range(n):
                if j != i:
                    # Multiplicar por (t - x[j])
                    paux = np.array([1.0, -x[j]])
                    Li = np.convolve(Li, paux)
                    den = den * (x[i] - x[j])

            # Sumar y[i] * Li / den al polinomio total
            coeficientes = coeficientes + (y[i] * Li / den)

        # Rellenar con ceros si es necesario
        if len(coeficientes) < n:
            coeficientes = np.append(coeficientes, np.zeros(n - len(coeficientes)))

        # Crear string del polinomio
        polinomio_str = crear_string_polinomio(coeficientes)

        # Generar puntos para graficar
        x_plot = np.linspace(min(x) - 0.5, max(x) + 0.5, 200)
        y_plot = np.polyval(coeficientes, x_plot)

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = np.polyval(coeficientes, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "coeficientes": coeficientes.tolist(),
            "polinomio_str": polinomio_str,
            "puntos_grafica": {"x": x_plot.tolist(), "y": y_plot.tolist()},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def spline_lineal(x, y):
    """
    Spline lineal (interpolación por segmentos lineales)

    Retorna: dict con 'exito', 'coeficientes', 'segmentos', 'puntos_grafica'
    """
    try:
        n = len(x)
        d = 1  # grado lineal

        # Crear matriz A y vector b
        A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
        b_vec = np.zeros((d+1)*(n-1))

        c = 0  # columna
        h = 0  # fila

        # Condición 1: P_i(x_i) = y_i
        for i in range(n-1):
            A[h, c] = x[i]
            A[h, c+1] = 1
            b_vec[h] = y[i]
            c += 2
            h += 1

        # Condición 2: P_i(x_{i+1}) = y_{i+1}
        c = 0
        for i in range(1, n):
            A[h, c] = x[i]
            A[h, c+1] = 1
            b_vec[h] = y[i]
            c += 2
            h += 1

        # Resolver sistema
        val = np.linalg.solve(A, b_vec)
        Tabla = val.reshape(n-1, d+1)

        # Crear lista de segmentos
        segmentos = []
        for i in range(n-1):
            a, b_coef = Tabla[i]
            segmentos.append({
                "intervalo": [float(x[i]), float(x[i+1])],
                "coeficientes": [float(a), float(b_coef)],
                "polinomio": f"{a:.6f}x + {b_coef:.6f}"
            })

        # Generar puntos para graficar
        x_plot = []
        y_plot = []
        for i in range(n-1):
            x_seg = np.linspace(x[i], x[i+1], 50)
            y_seg = Tabla[i, 0] * x_seg + Tabla[i, 1]
            x_plot.extend(x_seg.tolist())
            y_plot.extend(y_seg.tolist())

        return {
            "exito": True,
            "coeficientes": Tabla.tolist(),
            "segmentos": segmentos,
            "puntos_grafica": {"x": x_plot, "y": y_plot},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()}
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def spline_cubico(x, y):
    """
    Spline cúbico natural (interpolación por segmentos cúbicos)

    Retorna: dict con 'exito', 'coeficientes', 'segmentos', 'puntos_grafica'
    """
    try:
        n = len(x)
        d = 3  # grado cúbico

        # Crear matriz A y vector b
        A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
        b_vec = np.zeros((d+1)*(n-1))

        # Potencias de x
        x2 = x**2
        x3 = x**3

        c = 0  # columna
        h = 0  # fila

        # Condición 1: P_i(x_i) = y_i
        for i in range(n-1):
            A[h, c] = x3[i]
            A[h, c+1] = x2[i]
            A[h, c+2] = x[i]
            A[h, c+3] = 1
            b_vec[h] = y[i]
            c += 4
            h += 1

        # Condición 2: P_i(x_{i+1}) = y_{i+1}
        c = 0
        for i in range(1, n):
            A[h, c] = x3[i]
            A[h, c+1] = x2[i]
            A[h, c+2] = x[i]
            A[h, c+3] = 1
            b_vec[h] = y[i]
            c += 4
            h += 1

        # Condición 3: Primera derivada continua
        c = 0
        for i in range(1, n-1):
            A[h, c] = 3*x2[i]
            A[h, c+1] = 2*x[i]
            A[h, c+2] = 1
            A[h, c+4] = -3*x2[i]
            A[h, c+5] = -2*x[i]
            A[h, c+6] = -1
            b_vec[h] = 0
            c += 4
            h += 1

        # Condición 4: Segunda derivada continua
        c = 0
        for i in range(1, n-1):
            A[h, c] = 6*x[i]
            A[h, c+1] = 2
            A[h, c+4] = -6*x[i]
            A[h, c+5] = -2
            b_vec[h] = 0
            c += 4
            h += 1

        # Condición 5: Spline natural (segunda derivada nula en extremos)
        A[h, 0] = 6*x[0]
        A[h, 1] = 2
        b_vec[h] = 0
        h += 1

        A[h, c] = 6*x[-1]
        A[h, c+1] = 2
        b_vec[h] = 0

        # Resolver sistema
        val = np.linalg.solve(A, b_vec)
        Tabla = val.reshape(n-1, d+1)

        # Crear lista de segmentos
        segmentos = []
        for i in range(n-1):
            a, b, c_coef, d_coef = Tabla[i]
            segmentos.append({
                "intervalo": [float(x[i]), float(x[i+1])],
                "coeficientes": [float(a), float(b), float(c_coef), float(d_coef)],
                "polinomio": f"{a:.6f}x³ + {b:.6f}x² + {c_coef:.6f}x + {d_coef:.6f}"
            })

        # Generar puntos para graficar
        x_plot = []
        y_plot = []
        for i in range(n-1):
            x_seg = np.linspace(x[i], x[i+1], 50)
            a, b, c_coef, d_coef = Tabla[i]
            y_seg = a * x_seg**3 + b * x_seg**2 + c_coef * x_seg + d_coef
            x_plot.extend(x_seg.tolist())
            y_plot.extend(y_seg.tolist())

        return {
            "exito": True,
            "coeficientes": Tabla.tolist(),
            "segmentos": segmentos,
            "puntos_grafica": {"x": x_plot, "y": y_plot},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()}
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def validar_puntos(puntos_str):
    """
    Valida y convierte string de puntos a arrays numpy

    Formato: "x1,y1;x2,y2;x3,y3"
    """
    try:
        pares = puntos_str.strip().split(';')
        x = []
        y = []

        for par in pares:
            coords = par.split(',')
            if len(coords) != 2:
                return None, None, "Formato incorrecto. Use: x1,y1;x2,y2;..."

            x.append(float(coords[0].strip()))
            y.append(float(coords[1].strip()))

        x = np.array(x)
        y = np.array(y)

        if len(x) < 2:
            return None, None, "Se necesitan al menos 2 puntos"
        if len(x) > 8:
            return None, None, "Máximo 8 puntos permitidos"

        # Verificar que no haya x repetidos
        if len(set(x)) != len(x):
            return None, None, "No puede haber valores de x repetidos"

        return x, y, None
    except Exception as e:
        return None, None, f"Error al procesar puntos: {str(e)}"


def comparar_metodos_cap3(x, y):
    """
    Compara todos los métodos de interpolación para un mismo conjunto de datos

    Retorna: dict con resultados de cada método y análisis comparativo
    """
    resultados = {}

    # Ejecutar todos los métodos
    resultados['vandermonde'] = vandermonde(x, y)
    resultados['newton'] = newton_interpolante(x, y)
    resultados['lagrange'] = lagrange(x, y)
    resultados['spline_lineal'] = spline_lineal(x, y)
    resultados['spline_cubico'] = spline_cubico(x, y)

    # Calcular errores promedio en puntos originales
    errores_metodos = {}
    for metodo, res in resultados.items():
        if res.get('exito') and 'errores' in res:
            errores_metodos[metodo] = np.mean(res['errores'])

    # Determinar mejor método (menor error)
    if errores_metodos:
        mejor_metodo = min(errores_metodos, key=errores_metodos.get)
        resultados['comparacion'] = {
            "mejor_metodo": mejor_metodo,
            "errores_promedio": errores_metodos,
            "analisis": f"El método {mejor_metodo} tuvo el menor error promedio"
        }
    else:
        resultados['comparacion'] = {
            "mejor_metodo": "No determinado",
            "analisis": "No se pudo calcular errores de comparación"
        }

    return resultados


# Funciones auxiliares
def crear_string_polinomio(coeficientes):
    """Crea una representación en string de un polinomio"""
    n = len(coeficientes)
    grado = n - 1
    terminos = []

    for i, coef in enumerate(coeficientes):
        potencia = grado - i
        if abs(coef) > 1e-10:
            if potencia == 0:
                terminos.append(f"{coef:.6f}")
            elif potencia == 1:
                terminos.append(f"{coef:.6f}x")
            else:
                terminos.append(f"{coef:.6f}x^{potencia}")

    return " + ".join(terminos).replace("+ -", "- ") if terminos else "0"


def crear_string_newton(coeficientes, x):
    """Crea representación en string del polinomio de Newton"""
    n = len(coeficientes)
    terminos = [f"{coeficientes[0]:.6f}"]

    for i in range(1, n):
        producto = " * ".join([f"(x - {x[j]:.3f})" for j in range(i)])
        terminos.append(f"{coeficientes[i]:.6f} * {producto}")

    return " + ".join(terminos).replace("+ -", "- ")


def evaluar_polinomio(coeficientes, x):
    """Evalúa un polinomio en x"""
    return np.polyval(coeficientes, x)


def evaluar_newton(Tabla, x_eval):
    """Evalúa el polinomio de Newton en x_eval"""
    n = len(Tabla)
    x = Tabla[:, 0]
    resultado = Tabla[0, 1]
    producto = 1.0

    for i in range(1, n):
        producto *= (x_eval - x[i-1])
        resultado += Tabla[i, i+1] * producto

    return resultado


def ejecutar_metodo(metodo, puntos_str):
    """
    Ejecuta un método de interpolación específico

    Parámetros:
    metodo: Nombre del método ('vandermonde', 'newton', 'lagrange', 'spline-lineal', 'spline-cubico')
    puntos_str: String con puntos en formato "x1,y1;x2,y2;..."

    Retorna: dict con resultado del método
    """
    x, y, error = validar_puntos(puntos_str)

    if error:
        return {"exito": False, "mensaje": error}

    # Mapeo de métodos
    metodos_map = {
        'vandermonde': vandermonde,
        'newton': newton_interpolante,
        'lagrange': lagrange,
        'spline-lineal': spline_lineal,
        'spline-cubico': spline_cubico
    }

    if metodo not in metodos_map:
        return {"exito": False, "mensaje": f"Método '{metodo}' no reconocido"}

    # Ejecutar método
    resultado = metodos_map[metodo](x, y)

    # Agregar representación del polinomio para el informe
    if resultado.get('exito'):
        if 'polinomio_str' in resultado:
            resultado['polinomio'] = resultado['polinomio_str']
        elif 'segmentos' in resultado:
            # Para splines, mostrar el primer segmento
            resultado['polinomio'] = resultado['segmentos'][0]['polinomio']

    return resultado
