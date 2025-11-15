"""
Métodos numéricos del Capítulo 1: Búsqueda de raíces
Incluye: Bisección, Regla Falsa, Punto Fijo, Newton-Raphson, Secante y Raíces Múltiples
"""

import numpy as np
import sympy as sp
from sympy import symbols, sympify, diff, lambdify
import math


def biseccion(xi, xs, tol, niter, funcion_str):
    """
    Método de Bisección para encontrar raíces de funciones

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones', 'tipo_error'
    """
    # Detectar tipo de error
    tipo_error = "relativo" if str(tol).startswith(("5e", "5E")) else "absoluto"

    # Preparar función
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la función: {str(e)}"}

    # Listas para la tabla
    iteraciones = []
    valores_xm = []
    valores_fm = []
    errores = []

    # Evaluar en los extremos
    fi = f(xi)
    fs = f(xs)

    if fi == 0:
        return {"exito": True, "raiz": xi, "mensaje": f"{xi} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs == 0:
        return {"exito": True, "raiz": xs, "mensaje": f"{xs} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs * fi >= 0:
        return {"exito": False, "mensaje": "El intervalo es inadecuado (f(xi) y f(xs) deben tener signos opuestos)"}

    c = 0
    xm = (xi + xs) / 2
    fe = f(xm)

    iteraciones.append(c)
    valores_xm.append(xm)
    valores_fm.append(fe)
    errores.append(None)

    while c < niter:
        if fi * fe < 0:
            xs = xm
            fs = f(xs)
        else:
            xi = xm
            fi = f(xi)

        xa = xm
        xm = (xi + xs) / 2
        fe = f(xm)

        # Calcular error
        if tipo_error == "relativo":
            error = abs(xm - xa) / abs(xm) if xm != 0 else abs(xm - xa)
        else:
            error = abs(xm - xa)

        c += 1
        iteraciones.append(c)
        valores_xm.append(xm)
        valores_fm.append(fe)
        errores.append(error)

        if error < tol or fe == 0:
            break

    tabla = {
        "Iteracion": iteraciones,
        "Xm": valores_xm,
        "f(Xm)": valores_fm,
        "Error": errores
    }

    mensaje = f"Raíz aproximada: {xm:.10f} con error {error:.2e}" if c < niter else f"Se alcanzó el número máximo de iteraciones ({niter})"

    return {
        "exito": True,
        "raiz": xm,
        "mensaje": mensaje,
        "iteraciones": c,
        "tabla": tabla,
        "tipo_error": tipo_error,
        "error_final": errores[-1] if errores[-1] is not None else 0
    }


def regla_falsa(xi, xs, tol, niter, funcion_str):
    """
    Método de Regla Falsa (Falsa Posición) para encontrar raíces

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones', 'tipo_error'
    """
    # Detectar tipo de error
    tipo_error = "relativo" if str(tol).startswith(("5e", "5E")) else "absoluto"

    # Preparar función
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la función: {str(e)}"}

    # Listas para la tabla
    iteraciones = []
    valores_xm = []
    valores_fm = []
    errores = []

    # Evaluar en los extremos
    fi = f(xi)
    fs = f(xs)

    if fi == 0:
        return {"exito": True, "raiz": xi, "mensaje": f"{xi} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs == 0:
        return {"exito": True, "raiz": xs, "mensaje": f"{xs} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs * fi >= 0:
        return {"exito": False, "mensaje": "El intervalo es inadecuado"}

    c = 0
    xm = xi - fi * (xs - xi) / (fs - fi)
    fe = f(xm)

    iteraciones.append(c)
    valores_xm.append(xm)
    valores_fm.append(fe)
    errores.append(None)

    while c < niter:
        if fi * fe < 0:
            xs = xm
            fs = f(xs)
        else:
            xi = xm
            fi = f(xi)

        xa = xm
        xm = xi - fi * (xs - xi) / (fs - fi)
        fe = f(xm)

        # Calcular error
        if tipo_error == "relativo":
            error = abs(xm - xa) / abs(xm) if xm != 0 else abs(xm - xa)
        else:
            error = abs(xm - xa)

        c += 1
        iteraciones.append(c)
        valores_xm.append(xm)
        valores_fm.append(fe)
        errores.append(error)

        if error < tol or fe == 0:
            break

    tabla = {
        "Iteracion": iteraciones,
        "Xm": valores_xm,
        "f(Xm)": valores_fm,
        "Error": errores
    }

    mensaje = f"Raíz aproximada: {xm:.10f} con error {error:.2e}" if c < niter else f"Se alcanzó el número máximo de iteraciones ({niter})"

    return {
        "exito": True,
        "raiz": xm,
        "mensaje": mensaje,
        "iteraciones": c,
        "tabla": tabla,
        "tipo_error": tipo_error,
        "error_final": errores[-1] if errores[-1] is not None else 0
    }


def punto_fijo(g_str, x0, tol, niter, funcion_f):
    """
    Método de Punto Fijo
    
    Parámetros:
    g_str: Función de iteración g(x) tal que x = g(x)
    x0: Valor inicial
    tol: Tolerancia
    niter: Número máximo de iteraciones
    funcion_f: Función original f(x) = 0 (para referencia)

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    x_sym = sp.Symbol('x')

    try:
        f_expr = sp.sympify(funcion_f)
        g_expr = sp.sympify(g_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
        g = sp.lambdify(x_sym, g_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en las funciones: {str(e)}"}

    iteraciones = []
    xn_vals = []
    gxn_vals = []
    fxn_vals = []
    errores = []

    xn = x0
    c = 0

    while c < niter:
        try:
            fxn = f(xn)
            xn1 = g(xn)
        except Exception as e:
            return {"exito": False, "mensaje": f"Error al evaluar en iteración {c}: {str(e)}"}

        error = abs(xn1 - xn)

        iteraciones.append(c)
        xn_vals.append(xn)
        gxn_vals.append(xn1)
        fxn_vals.append(fxn)
        errores.append(error)

        if c > 0 and error <= tol:
            break

        xn = xn1
        c += 1

    tabla = {
        "Iteracion": iteraciones,
        "Xm": xn_vals,
        "f(Xm)": fxn_vals,
        "Error": errores
    }

    mensaje = f"Punto fijo aproximado: {xn1:.10f} con error {error:.2e}" if error <= tol else f"No convergió en {niter} iteraciones"

    return {
        "exito": error <= tol,
        "raiz": xn1,
        "mensaje": mensaje,
        "iteraciones": c,
        "tabla": tabla,
        "error_final": error
    }


def newton_raphson(x0, tol, niter, funcion_str):
    """
    Método de Newton-Raphson

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    x_sym = sp.Symbol('x')

    try:
        f_expr = sp.sympify(funcion_str)
        df_expr = sp.diff(f_expr, x_sym)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
        df = sp.lambdify(x_sym, df_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la función: {str(e)}"}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    dfn_vals = []
    errores = []

    xn = x0
    c = 0
    error = 100

    fn = f(xn)
    dfn = df(xn)

    iteraciones.append(c)
    xn_vals.append(xn)
    fn_vals.append(fn)
    dfn_vals.append(dfn)
    errores.append(error)

    while error > tol and fn != 0 and dfn != 0 and c < niter:
        try:
            xn = xn - fn / dfn
            fn = f(xn)
            dfn = df(xn)
        except Exception as e:
            return {"exito": False, "mensaje": f"Error en iteración {c}: {str(e)}"}

        c += 1
        error = abs(xn - xn_vals[-1])

        iteraciones.append(c)
        xn_vals.append(xn)
        fn_vals.append(fn)
        dfn_vals.append(dfn)
        errores.append(error)

    tabla = {
        "Iteracion": iteraciones,
        "Xm": xn_vals,
        "f(Xm)": fn_vals,
        "Error": errores
    }

    if fn == 0:
        mensaje = f"{xn:.10f} es raíz exacta de f(x)"
    elif error < tol:
        mensaje = f"Raíz aproximada: {xn:.10f} con error {error:.2e}"
    else:
        mensaje = f"Fracaso en {niter} iteraciones"

    return {
        "exito": fn == 0 or error < tol,
        "raiz": xn,
        "mensaje": mensaje,
        "iteraciones": c,
        "tabla": tabla,
        "error_final": error
    }


def secante(x0, x1, tol, niter, funcion_str):
    """
    Método de la Secante

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    tipo_error = "relativo" if str(tol).startswith(("5e", "5E")) else "absoluto"

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la función: {str(e)}"}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    errores = []

    f0 = f(x0)
    f1 = f(x1)

    k = 0
    error = tol + 1  # Inicializar error
    iteraciones.append(k)
    xn_vals.append(x1)
    fn_vals.append(f1)
    errores.append(None)

    if f0 == 0:
        return {"exito": True, "raiz": x0, "mensaje": f"{x0} es raíz exacta",
                "iteraciones": 0, "tabla": {}, "error_final": 0}
    elif f1 == 0:
        return {"exito": True, "raiz": x1, "mensaje": f"{x1} es raíz exacta",
                "iteraciones": 0, "tabla": {}, "error_final": 0}

    while k < niter:
        denom = f1 - f0
        if denom == 0:
            break

        x2 = x1 - f1 * (x1 - x0) / denom

        if tipo_error == "relativo":
            error = abs(x2 - x1) / abs(x2) if x2 != 0 else abs(x2 - x1)
        else:
            error = abs(x2 - x1)

        x0, f0 = x1, f1
        x1 = x2
        f1 = f(x1)

        k += 1
        iteraciones.append(k)
        xn_vals.append(x1)
        fn_vals.append(f1)
        errores.append(error)

        if f1 == 0 or error < tol:
            break

    tabla = {
        "Iteracion": iteraciones,
        "Xm": xn_vals,
        "f(Xm)": fn_vals,
        "Error": errores
    }

    if f1 == 0:
        mensaje = f"{x1:.10f} es raíz exacta"
    elif error < tol:
        mensaje = f"Raíz aproximada: {x1:.10f} con error {error:.2e}"
    else:
        mensaje = f"Fracaso en {niter} iteraciones"

    return {
        "exito": f1 == 0 or error < tol,
        "raiz": x1,
        "mensaje": mensaje,
        "iteraciones": k,
        "tabla": tabla,
        "tipo_error": tipo_error,
        "error_final": error
    }


def raices_multiples(x0, tol, niter, funcion_str, metodo=2, multiplicidad=None):
    """
    Método de Newton-Raphson para Raíces Múltiples

    metodo: 1 (con multiplicidad conocida) o 2 (con segunda derivada)
    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    tipo_error = "relativo" if str(tol).startswith(("5e", "5E")) else "absoluto"

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        df_expr = sp.diff(f_expr, x_sym)
        ddf_expr = sp.diff(df_expr, x_sym)

        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
        df = sp.lambdify(x_sym, df_expr, modules=['numpy', 'math'])
        ddf = sp.lambdify(x_sym, ddf_expr, modules=['numpy', 'math'])
    except Exception as e:
        return {"exito": False, "mensaje": f"Error en la función: {str(e)}"}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    dfn_vals = []
    errores = []

    c = 0
    xn = x0
    fn = f(xn)
    dfn = df(xn)

    iteraciones.append(c)
    xn_vals.append(xn)
    fn_vals.append(fn)
    dfn_vals.append(dfn)
    errores.append(None)

    error = tol + 1

    while error > tol and c < niter:
        fn = f(xn)
        dfn = df(xn)

        if dfn == 0:
            return {"exito": False, "mensaje": f"La derivada se anula en x={xn}, el método falla"}

        if metodo == 1 and multiplicidad:
            # Método con multiplicidad conocida
            xn1 = xn - multiplicidad * fn / dfn
        else:
            # Método con segunda derivada
            ddfn = ddf(xn)
            denominador = dfn**2 - fn * ddfn

            if abs(denominador) < 1e-15:
                return {"exito": False, "mensaje": "Denominador muy pequeño, el método no puede continuar"}

            xn1 = xn - (fn * dfn) / denominador

        if tipo_error == "relativo":
            error = abs(xn1 - xn) / abs(xn1) if xn1 != 0 else abs(xn1 - xn)
        else:
            error = abs(xn1 - xn)

        c += 1
        xn = xn1
        fn = f(xn)
        dfn = df(xn)

        iteraciones.append(c)
        xn_vals.append(xn)
        fn_vals.append(fn)
        dfn_vals.append(dfn)
        errores.append(error)

        if error < tol or abs(fn) < 1e-15:
            break

    tabla = {
        "Iteracion": iteraciones,
        "Xm": xn_vals,
        "f(Xm)": fn_vals,
        "Error": errores
    }

    # Verificar si encontramos la raíz
    exito = (error < tol) or (abs(fn) < 1e-15)

    if exito:
        mensaje = f"Raíz aproximada: {xn:.10f} con error {error:.2e}"
    else:
        mensaje = f"Se alcanzó el máximo de iteraciones ({niter})"

    # Detectar si es raíz múltiple
    es_multiple = abs(fn) < 1e-10 and abs(dfn) < 1e-6

    return {
        "exito": exito,
        "raiz": xn,
        "mensaje": mensaje,
        "iteraciones": c,
        "tabla": tabla,
        "tipo_error": tipo_error,
        "error_final": error,
        "es_raiz_multiple": es_multiple
    }


def generar_puntos_grafica(funcion_str, x_min, x_max, num_puntos=500):
    """
    Genera puntos para graficar una función
    """
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])

        x_vals = np.linspace(x_min, x_max, num_puntos)
        y_vals = []

        for x in x_vals:
            try:
                y = f(x)
                if np.isfinite(y):
                    y_vals.append(y)
                else:
                    y_vals.append(None)
            except:
                y_vals.append(None)

        return x_vals.tolist(), y_vals
    except Exception as e:
        return None, None
