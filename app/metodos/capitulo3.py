"""
Métodos numéricos del Capítulo 3: Interpolación
Incluye: Vandermonde, Newton, Lagrange, Spline Lineal y Spline Cúbico

Basado en los códigos del profesor con mejoras para la aplicación web
"""

import numpy as np
import sympy as sp


def vandermonde(x, y):
    """
    Interpolación usando la matriz de Vandermonde

    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)

    Retorna:
    dict con 'exito', 'coeficientes', 'polinomio_str', 'puntos_grafica', etc.
    """
    try:
        n = len(x)
        grado = n - 1

        # Construir la matriz de Vandermonde
        # A = [x^n, x^{n-1}, ..., x, 1]
        A = np.zeros((n, grado + 1))
        for i in range(grado + 1):
            A[:, i] = x ** (grado - i)

        # Resolver el sistema A*a = y
        coeficientes = np.linalg.solve(A, y)

        # Crear string del polinomio
        polinomio_str = crear_string_polinomio_vandermonde(coeficientes)

        # Generar puntos para graficar
        x_min, x_max = x.min(), x.max()
        margen = (x_max - x_min) * 0.1 if x_max != x_min else 1
        x_plot = np.linspace(x_min - margen, x_max + margen, 300)
        y_plot = evaluar_polinomio_vandermonde(coeficientes, x_plot)

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = evaluar_polinomio_vandermonde(coeficientes, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "coeficientes": coeficientes.tolist(),
            "polinomio_str": polinomio_str,
            "puntos_grafica": {"x": x_plot.tolist(), "y": y_plot.tolist()},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores,
            "matriz_vandermonde": A.tolist(),
            "grado": grado,
            "tipo": "polinomial"
        }
    except np.linalg.LinAlgError:
        return {"exito": False, "mensaje": "❌ Error: La matriz de Vandermonde es singular. Verifica que no haya valores de x repetidos."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error: {str(e)}"}


def newton_interpolante(x, y):
    """
    Método de Newton con diferencias divididas

    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)

    Retorna:
    dict con 'exito', 'tabla', 'coeficientes', 'polinomio_str', 'puntos_grafica'
    """
    try:
        n = len(x)

        # Crear tabla de diferencias divididas
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
        x_min, x_max = x.min(), x.max()
        margen = (x_max - x_min) * 0.1 if x_max != x_min else 1
        x_plot = np.linspace(x_min - margen, x_max + margen, 300)
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
            "errores": errores,
            "grado": n - 1,
            "tipo": "polinomial"
        }
    except ZeroDivisionError:
        return {"exito": False, "mensaje": "❌ Error: División por cero. Verifica que no haya valores de x repetidos."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error: {str(e)}"}


def lagrange(x, y):
    """
    Método de Lagrange para interpolación polinomial

    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)

    Retorna:
    dict con 'exito', 'coeficientes', 'polinomio_str', 'puntos_grafica'
    """
    try:
        n = len(x)
        Tabla = np.zeros((n, n))

        # Calcular cada polinomio base de Lagrange
        for i in range(n):
            Li = np.array([1.0])
            den = 1.0

            for j in range(n):
                if j != i:
                    # Multiplica por (t - x[j])
                    paux = np.array([1.0, -x[j]])
                    Li = np.convolve(Li, paux)
                    den = den * (x[i] - x[j])

            # Guarda y[i] * Li / den en la tabla
            Tabla[i, :] = (y[i] * Li / den)[:n]  # Asegurar longitud n

        # Suma todos los polinomios de Lagrange
        coeficientes = np.sum(Tabla, axis=0)

        # Crear string del polinomio
        polinomio_str = crear_string_polinomio_standard(coeficientes)

        # Generar puntos para graficar
        x_min, x_max = x.min(), x.max()
        margen = (x_max - x_min) * 0.1 if x_max != x_min else 1
        x_plot = np.linspace(x_min - margen, x_max + margen, 300)
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
            "errores": errores,
            "grado": n - 1,
            "tipo": "polinomial"
        }
    except ZeroDivisionError:
        return {"exito": False, "mensaje": "❌ Error: División por cero. Verifica que no haya valores de x repetidos."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error: {str(e)}"}


def spline_lineal(x, y):
    """
    Spline lineal (interpolación por segmentos lineales)

    Para cada segmento [x_i, x_{i+1}], calcula un polinomio lineal:
    P_i(x) = a_i*x + b_i

    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)

    Retorna:
    dict con 'exito', 'coeficientes', 'segmentos', 'puntos_grafica'
    """
    try:
        n = len(x)
        d = 1  # grado lineal

        # Crear matriz A y vector b para el sistema lineal
        A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
        b_vec = np.zeros((d+1)*(n-1))

        c = 0  # columna
        h = 0  # fila

        # Condición 1: El polinomio i pasa por el punto (x_i, y_i)
        # P_i(x_i) = y_i para i = 1, 2, ..., n-1
        for i in range(n-1):
            A[h, c] = x[i]
            A[h, c+1] = 1
            b_vec[h] = y[i]
            c += 2
            h += 1

        # Condición 2: El polinomio i pasa por el punto (x_{i+1}, y_{i+1})
        # P_i(x_{i+1}) = y_{i+1} para i = 1, 2, ..., n-1
        c = 0
        for i in range(1, n):
            A[h, c] = x[i]
            A[h, c+1] = 1
            b_vec[h] = y[i]
            c += 2
            h += 1

        # Resolver el sistema lineal
        val = np.linalg.solve(A, b_vec)

        # Reorganizar los coeficientes en una tabla
        # Cada fila representa un segmento: [a, b] para P(x) = ax + b
        Tabla = val.reshape(n-1, d+1)

        # Crear lista de segmentos
        segmentos = []
        for i in range(n-1):
            a, b_coef = Tabla[i]
            segmentos.append({
                "intervalo": [float(x[i]), float(x[i+1])],
                "coeficientes": [float(a), float(b_coef)],
                "polinomio": f"{a:.6f}x {'+' if b_coef >= 0 else '-'} {abs(b_coef):.6f}"
            })

        # Generar puntos para graficar
        x_plot = []
        y_plot = []
        for i in range(n-1):
            x_seg = np.linspace(x[i], x[i+1], 50)
            y_seg = Tabla[i, 0] * x_seg + Tabla[i, 1]
            x_plot.extend(x_seg.tolist())
            y_plot.extend(y_seg.tolist())

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = evaluar_spline_lineal(Tabla, x, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "coeficientes": Tabla.tolist(),
            "segmentos": segmentos,
            "puntos_grafica": {"x": x_plot, "y": y_plot},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores,
            "num_segmentos": n - 1,
            "tipo": "spline",
            "grado_spline": 1
        }
    except np.linalg.LinAlgError:
        return {"exito": False, "mensaje": "❌ Error: El sistema de ecuaciones es singular."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error: {str(e)}"}


def spline_cubico(x, y):
    """
    Spline cúbico natural (interpolación por segmentos cúbicos)

    Para cada segmento [x_i, x_{i+1}], calcula un polinomio cúbico:
    P_i(x) = a_i*x^3 + b_i*x^2 + c_i*x + d_i

    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)

    Retorna:
    dict con 'exito', 'coeficientes', 'segmentos', 'puntos_grafica'
    """
    try:
        n = len(x)
        d = 3  # grado cúbico

        # Crear matriz A y vector b para el sistema lineal
        A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
        b_vec = np.zeros((d+1)*(n-1))

        # Potencias de x
        x2 = x**2
        x3 = x**3

        c = 0  # columna
        h = 0  # fila

        # Condición 1: P_i(x_i) = y_i para i = 1, 2, ..., n-1
        for i in range(n-1):
            A[h, c] = x3[i]
            A[h, c+1] = x2[i]
            A[h, c+2] = x[i]
            A[h, c+3] = 1
            b_vec[h] = y[i]
            c += 4
            h += 1

        # Condición 2: P_i(x_{i+1}) = y_{i+1} para i = 1, 2, ..., n-1
        c = 0
        for i in range(1, n):
            A[h, c] = x3[i]
            A[h, c+1] = x2[i]
            A[h, c+2] = x[i]
            A[h, c+3] = 1
            b_vec[h] = y[i]
            c += 4
            h += 1

        # Condición 3: Primera derivada continua en los puntos interiores
        # P'_i(x_{i+1}) = P'_{i+1}(x_{i+1}) para i = 1, 2, ..., n-2
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

        # Condición 4: Segunda derivada continua en los puntos interiores
        # P''_i(x_{i+1}) = P''_{i+1}(x_{i+1}) para i = 1, 2, ..., n-2
        c = 0
        for i in range(1, n-1):
            A[h, c] = 6*x[i]
            A[h, c+1] = 2
            A[h, c+4] = -6*x[i]
            A[h, c+5] = -2
            b_vec[h] = 0
            c += 4
            h += 1

        # Condición 5: Spline natural (segunda derivada nula en los extremos)
        # P''_1(x_1) = 0
        A[h, 0] = 6*x[0]
        A[h, 1] = 2
        b_vec[h] = 0
        h += 1

        # P''_{n-1}(x_n) = 0
        A[h, c] = 6*x[-1]
        A[h, c+1] = 2
        b_vec[h] = 0

        # Resolver el sistema lineal
        val = np.linalg.solve(A, b_vec)

        # Reorganizar los coeficientes en una tabla
        # Cada fila representa un segmento: [a, b, c, d] para P(x) = ax^3 + bx^2 + cx + d
        Tabla = val.reshape(n-1, d+1)

        # Crear lista de segmentos
        segmentos = []
        for i in range(n-1):
            a, b, c_coef, d_coef = Tabla[i]
            segmentos.append({
                "intervalo": [float(x[i]), float(x[i+1])],
                "coeficientes": [float(a), float(b), float(c_coef), float(d_coef)],
                "polinomio": formatear_polinomio_cubico(a, b, c_coef, d_coef)
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

        # Verificación en puntos originales
        errores = []
        for i in range(len(x)):
            y_calc = evaluar_spline_cubico(Tabla, x, x[i])
            errores.append(abs(y[i] - y_calc))

        return {
            "exito": True,
            "coeficientes": Tabla.tolist(),
            "segmentos": segmentos,
            "puntos_grafica": {"x": x_plot, "y": y_plot},
            "puntos_originales": {"x": x.tolist(), "y": y.tolist()},
            "errores": errores,
            "num_segmentos": n - 1,
            "tipo": "spline",
            "grado_spline": 3
        }
    except np.linalg.LinAlgError:
        return {"exito": False, "mensaje": "❌ Error: El sistema de ecuaciones es singular."}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error: {str(e)}"}


# ===== FUNCIONES AUXILIARES =====

def evaluar_polinomio_vandermonde(coeficientes, x_eval):
    """
    Evalúa el polinomio de Vandermonde en los puntos dados

    Parámetros:
    coeficientes: Coeficientes del polinomio [a_n, a_{n-1}, ..., a_1, a_0]
    x_eval: Puntos donde evaluar (puede ser escalar o array)

    Retorna:
    Valores del polinomio en x_eval
    """
    grado = len(coeficientes) - 1
    resultado = np.zeros_like(x_eval, dtype=float)

    for i, coef in enumerate(coeficientes):
        potencia = grado - i
        resultado += coef * (x_eval ** potencia)

    return resultado


def evaluar_newton(Tabla, x_eval):
    """
    Evalúa el polinomio de Newton en un punto dado

    Parámetros:
    Tabla: Tabla de diferencias divididas
    x_eval: Punto donde evaluar el polinomio

    Retorna:
    Valor del polinomio en x_eval
    """
    n = len(Tabla)
    x = Tabla[:, 0]
    resultado = Tabla[0, 1]
    producto = 1.0

    for i in range(1, n):
        producto *= (x_eval - x[i-1])
        resultado += Tabla[i, i+1] * producto

    return resultado


def evaluar_spline_lineal(Tabla, x_original, x_eval):
    """
    Evalúa el spline lineal en un punto dado

    Parámetros:
    Tabla: Matriz de coeficientes del spline
    x_original: Puntos originales usados para crear el spline
    x_eval: Punto donde evaluar el spline

    Retorna:
    Valor del spline en x_eval
    """
    n = len(x_original)

    # Encontrar en qué segmento está x_eval
    for i in range(n-1):
        if x_original[i] <= x_eval <= x_original[i+1]:
            # Evaluar el polinomio lineal del segmento i
            a, b = Tabla[i]
            return a * x_eval + b

    # Si está fuera del rango, usar extrapolación
    if x_eval < x_original[0]:
        a, b = Tabla[0]
        return a * x_eval + b
    else:
        a, b = Tabla[-1]
        return a * x_eval + b


def evaluar_spline_cubico(Tabla, x_original, x_eval):
    """
    Evalúa el spline cúbico en un punto dado

    Parámetros:
    Tabla: Matriz de coeficientes del spline
    x_original: Puntos originales usados para crear el spline
    x_eval: Punto donde evaluar el spline

    Retorna:
    Valor del spline en x_eval
    """
    n = len(x_original)

    # Encontrar en qué segmento está x_eval
    for i in range(n-1):
        if x_original[i] <= x_eval <= x_original[i+1]:
            # Evaluar el polinomio cúbico del segmento i
            a, b, c, d = Tabla[i]
            return a * x_eval**3 + b * x_eval**2 + c * x_eval + d

    # Si está fuera del rango, usar extrapolación
    if x_eval < x_original[0]:
        a, b, c, d = Tabla[0]
        return a * x_eval**3 + b * x_eval**2 + c * x_eval + d
    else:
        a, b, c, d = Tabla[-1]
        return a * x_eval**3 + b * x_eval**2 + c * x_eval + d


def crear_string_polinomio_vandermonde(coeficientes):
    """
    Crea una representación en string de un polinomio de Vandermonde

    Formato: a_n*x^n + a_{n-1}*x^{n-1} + ... + a_1*x + a_0
    """
    grado = len(coeficientes) - 1
    terminos = []

    for i, coef in enumerate(coeficientes):
        potencia = grado - i
        if abs(coef) > 1e-10:  # Ignorar coeficientes muy pequeños
            # Formatear coeficiente
            coef_str = f"{coef:.6f}"

            if potencia == 0:
                terminos.append(coef_str)
            elif potencia == 1:
                terminos.append(f"{coef_str}x")
            else:
                terminos.append(f"{coef_str}x^{potencia}")

    if not terminos:
        return "0"

    # Unir términos y limpiar formato
    resultado = " + ".join(terminos)
    resultado = resultado.replace("+ -", "- ")

    return resultado


def crear_string_polinomio_standard(coeficientes):
    """
    Crea representación en string de un polinomio estándar (formato numpy.polyval)
    """
    n = len(coeficientes)
    grado = n - 1
    terminos = []

    for i, coef in enumerate(coeficientes):
        potencia = grado - i
        if abs(coef) > 1e-10:
            coef_str = f"{coef:.6f}"

            if potencia == 0:
                terminos.append(coef_str)
            elif potencia == 1:
                terminos.append(f"{coef_str}x")
            else:
                terminos.append(f"{coef_str}x^{potencia}")

    if not terminos:
        return "0"

    resultado = " + ".join(terminos)
    resultado = resultado.replace("+ -", "- ")

    return resultado


def crear_string_newton(coeficientes, x):
    """
    Crea representación en string del polinomio de Newton

    Formato: a_0 + a_1(x-x_0) + a_2(x-x_0)(x-x_1) + ...
    """
    n = len(coeficientes)

    if n == 0:
        return "0"

    terminos = [f"{coeficientes[0]:.6f}"]

    for i in range(1, n):
        # Crear producto de (x - x_j) para j = 0, ..., i-1
        factores = []
        for j in range(i):
            # MATLAB simplifica (x - 0) a solo x
            if abs(x[j]) < 1e-10:
                factores.append("x")
            elif x[j] > 0:
                factores.append(f"(x - {x[j]:.3f})")
            else:
                factores.append(f"(x + {abs(x[j]):.3f})")

        producto = "".join(factores)

        # Formatear coeficiente
        if abs(coeficientes[i]) > 1e-10:
            terminos.append(f"{coeficientes[i]:.6f}{producto}")

    resultado = " + ".join(terminos)
    resultado = resultado.replace("+ -", "- ")

    return resultado


def formatear_polinomio_cubico(a, b, c, d):
    """Formatea un polinomio cúbico de manera legible"""
    terminos = []

    if abs(a) > 1e-10:
        terminos.append(f"{a:.6f}x³")
    if abs(b) > 1e-10:
        terminos.append(f"{b:.6f}x²")
    if abs(c) > 1e-10:
        terminos.append(f"{c:.6f}x")
    if abs(d) > 1e-10:
        terminos.append(f"{d:.6f}")

    if not terminos:
        return "0"

    resultado = " + ".join(terminos)
    resultado = resultado.replace("+ -", "- ")

    return resultado


def validar_puntos(puntos_str):
    """
    Valida y convierte string de puntos a arrays numpy

    Formato esperado: "x1,y1;x2,y2;x3,y3;..."

    Retorna: (x, y, error_mensaje)
    """
    try:
        if not puntos_str or not puntos_str.strip():
            return None, None, "❌ Error: No se proporcionaron puntos.\n💡 Formato: x1,y1;x2,y2;x3,y3"

        pares = puntos_str.strip().split(';')
        x = []
        y = []

        for i, par in enumerate(pares):
            if not par.strip():
                continue

            coords = par.split(',')
            if len(coords) != 2:
                return None, None, f"❌ Error: Formato incorrecto en el punto {i+1}: '{par}'\n💡 Cada punto debe tener formato: x,y"

            try:
                x_val = float(coords[0].strip())
                y_val = float(coords[1].strip())
                x.append(x_val)
                y.append(y_val)
            except ValueError:
                return None, None, f"❌ Error: Valores no numéricos en el punto {i+1}: '{par}'\n💡 Asegúrate de que x e y sean números"

        if len(x) < 2:
            return None, None, f"❌ Error: Se necesitan al menos 2 puntos para interpolar.\n💡 Puntos recibidos: {len(x)}"

        if len(x) > 8:
            return None, None, f"❌ Error: Máximo 8 puntos permitidos.\n💡 Puntos recibidos: {len(x)}"

        x = np.array(x)
        y = np.array(y)

        # Verificar que no haya x repetidos
        if len(set(x)) != len(x):
            return None, None, "❌ Error: No puede haber valores de x repetidos.\n💡 Cada punto debe tener un valor x único"

        # Verificar que no haya NaN o infinitos
        if np.any(np.isnan(x)) or np.any(np.isnan(y)):
            return None, None, "❌ Error: Los puntos contienen valores NaN (no numéricos)"

        if np.any(np.isinf(x)) or np.any(np.isinf(y)):
            return None, None, "❌ Error: Los puntos contienen valores infinitos"

        return x, y, None

    except Exception as e:
        return None, None, f"❌ Error al procesar puntos: {str(e)}\n💡 Formato correcto: x1,y1;x2,y2;x3,y3"


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
        return {"exito": False, "mensaje": f"❌ Error: Método '{metodo}' no reconocido"}

    # Ejecutar método
    resultado = metodos_map[metodo](x, y)

    # Agregar representación del polinomio para el informe
    if resultado.get('exito'):
        if 'polinomio_str' in resultado:
            resultado['polinomio'] = resultado['polinomio_str']
        elif 'segmentos' in resultado and resultado['segmentos']:
            # Para splines, mostrar información de todos los segmentos
            num_seg = len(resultado['segmentos'])
            resultado['polinomio'] = f"{num_seg} segmentos de grado {resultado.get('grado_spline', 'N/A')}"

    return resultado


def comparar_metodos_cap3(x, y):
    """
    Compara todos los métodos de interpolación para un mismo conjunto de datos

    NO USADO actualmente - el informe se genera desde app.py
    Esta función se mantiene para compatibilidad

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
