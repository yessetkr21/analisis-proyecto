"""
Métodos numéricos del Capítulo 1: Búsqueda de raíces
Incluye: Bisección, Regla Falsa, Punto Fijo, Newton-Raphson, Secante y Raíces Múltiples
"""

import numpy as np
import sympy as sp
from sympy import symbols, sympify, diff, lambdify
import math


def biseccion(xi, xs, tol, niter, funcion_str, tol_str=None):
    """
    Método de Bisección para encontrar raíces de funciones

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones', 'tipo_error'
    """
    # Detectar tipo de error usando el string original de tolerancia
    if tol_str is None:
        tol_str = str(tol)

    # Detectar el tipo de error
    if tol_str.startswith(("5e", "5E", "5.0e", "5.0E")):
        tipo_error = "relativo"  # Cifras Significativas
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"  # Decimales Correctos
    else:
        tipo_error = "ninguno"  # No es ninguno de los dos tipos específicos

    # Preparar función
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita.\n💡 Ejemplo correcto: x**3 - 2*x - 5"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar la función: Asegúrate de usar 'x' como variable.\n💡 Ejemplos: x**2-4, sin(x)-x/2, exp(x)-3*x"}

    # Listas para la tabla
    iteraciones = []
    valores_xm = []
    valores_fm = []
    errores = []

    # Evaluar en los extremos
    try:
        fi = f(xi)
        fs = f(xs)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return {"exito": False,
               "mensaje": f"❌ Error al evaluar la función en el intervalo [{xi}, {xs}]\n💡 Posibles causas:\n   • La función no está definida en este intervalo\n   • División por cero en xi o xs\n\n🔧 Solución: Cambia el intervalo [Xi, Xs]"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error inesperado al evaluar f(x): {str(e)}"}

    if fi == 0:
        return {"exito": True, "raiz": xi, "mensaje": f"✅ {xi} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs == 0:
        return {"exito": True, "raiz": xs, "mensaje": f"✅ {xs} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs * fi >= 0:
        return {"exito": False,
               "mensaje": f"❌ Intervalo inadecuado: f({xi}) = {fi:.4f} y f({xs}) = {fs:.4f} tienen el mismo signo.\n\n💡 Para que Bisección funcione:\n   • f(Xi) y f(Xs) deben tener SIGNOS OPUESTOS\n   • Esto garantiza que hay una raíz en el intervalo\n\n🔧 Soluciones:\n   1. Grafica la función para encontrar un intervalo válido\n   2. Busca valores donde la función cambie de signo\n   3. Prueba con otros valores de Xi y Xs\n\n📊 Valores actuales:\n   • f({xi}) = {fi:.6f} {'(positivo)' if fi > 0 else '(negativo)'}\n   • f({xs}) = {fs:.6f} {'(positivo)' if fs > 0 else '(negativo)'}"}

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


def regla_falsa(xi, xs, tol, niter, funcion_str, tol_str=None):
    """
    Método de Regla Falsa (Falsa Posición) para encontrar raíces

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones', 'tipo_error'
    """
    # Detectar tipo de error usando el string original de tolerancia
    if tol_str is None:
        tol_str = str(tol)

    # Detectar el tipo de error
    if tol_str.startswith(("5e", "5E", "5.0e", "5.0E")):
        tipo_error = "relativo"  # Cifras Significativas
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"  # Decimales Correctos
    else:
        tipo_error = "ninguno"  # No es ninguno de los dos tipos específicos

    # Preparar función
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita.\n💡 Ejemplo correcto: x**3 - 2*x - 5"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar la función: Asegúrate de usar 'x' como variable.\n💡 Ejemplos: x**2-4, sin(x)-x/2, exp(x)-3*x"}

    # Listas para la tabla
    iteraciones = []
    valores_xm = []
    valores_fm = []
    errores = []

    # Evaluar en los extremos
    try:
        fi = f(xi)
        fs = f(xs)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return {"exito": False,
               "mensaje": f"❌ Error al evaluar la función en el intervalo [{xi}, {xs}]\n💡 La función no está definida en este intervalo.\n\n🔧 Solución: Cambia el intervalo [Xi, Xs]"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error inesperado al evaluar f(x): {str(e)}"}

    if fi == 0:
        return {"exito": True, "raiz": xi, "mensaje": f"✅ {xi} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs == 0:
        return {"exito": True, "raiz": xs, "mensaje": f"✅ {xs} es raíz exacta de f(x)",
                "iteraciones": 0, "tabla": [], "tipo_error": tipo_error}
    elif fs * fi >= 0:
        return {"exito": False,
               "mensaje": f"❌ Intervalo inadecuado: f({xi}) = {fi:.4f} y f({xs}) = {fs:.4f} tienen el mismo signo.\n\n💡 Para que Regla Falsa funcione:\n   • f(Xi) y f(Xs) deben tener SIGNOS OPUESTOS\n\n🔧 Soluciones:\n   1. Busca valores donde f(x) cambie de signo\n   2. Prueba con otros valores de Xi y Xs\n\n📊 Valores actuales:\n   • f({xi}) = {fi:.6f} {'(+)' if fi > 0 else '(-)'}\n   • f({xs}) = {fs:.6f} {'(+)' if fs > 0 else '(-)'}"}

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

    # Validar funciones
    try:
        f_expr = sp.sympify(funcion_f)
        g_expr = sp.sympify(g_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
        g = sp.lambdify(x_sym, g_expr, modules=['numpy', 'math'])
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita. Ejemplo: x**2 - 4"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar las funciones: Asegúrate de usar 'x' como variable. Ejemplo: g(x) = (x+2)**(1/3)"}

    iteraciones = []
    xn_vals = []
    gxn_vals = []
    fxn_vals = []
    errores = []

    xn = x0
    c = 0
    valores_grandes_consecutivos = 0

    while c < niter:
        try:
            fxn = f(xn)
            xn1 = g(xn)

            # Detectar valores inválidos (NaN, infinito)
            if math.isnan(xn1) or math.isnan(fxn):
                return {"exito": False,
                       "mensaje": f"⚠️ Se obtuvo un valor no numérico (NaN) en la iteración {c}.\n💡 Posibles causas:\n   • g(x) produce valores complejos (ej: raíz cuadrada de número negativo)\n   • División por cero\n   • Logaritmo de número negativo\n\n🔧 Solución: Cambia x0 o reformula g(x)"}

            if math.isinf(xn1) or math.isinf(fxn):
                return {"exito": False,
                       "mensaje": f"⚠️ Se obtuvo un valor infinito en la iteración {c}.\n💡 Posibles causas:\n   • La función g(x) está divergiendo\n   • g(x) no está bien elegida para este problema\n\n🔧 Solución: Verifica que g(x) cumpla |g'(x)| < 1 cerca de la raíz"}

            # Detectar divergencia (valores muy grandes)
            if abs(xn1) > 1e10:
                valores_grandes_consecutivos += 1
                if valores_grandes_consecutivos >= 3:
                    return {"exito": False,
                           "mensaje": f"⚠️ El método está divergiendo (valores muy grandes).\n💡 El problema:\n   • La función g(x) = {g_str} no converge desde x0 = {x0}\n   • La condición |g'(x)| < 1 no se cumple\n\n🔧 Soluciones:\n   1. Cambia la función g(x) (debe cumplir x = g(x))\n   2. Prueba con otro x0 más cercano a la raíz\n   3. Usa otro método (Newton-Raphson, Bisección)"}
            else:
                valores_grandes_consecutivos = 0

        except ZeroDivisionError:
            return {"exito": False,
                   "mensaje": f"⚠️ División por cero en la iteración {c}.\n💡 El problema:\n   • g({xn:.4f}) intenta dividir por cero\n\n🔧 Solución: Reformula g(x) o cambia x0"}
        except ValueError as e:
            return {"exito": False,
                   "mensaje": f"⚠️ Error matemático en iteración {c}: {str(e)}\n💡 Posibles causas:\n   • Raíz cuadrada de número negativo\n   • Logaritmo de número no positivo\n   • Potencia con base negativa y exponente fraccionario\n\n🔧 Solución: Verifica el dominio de g(x) y ajusta x0"}
        except OverflowError:
            return {"exito": False,
                   "mensaje": f"⚠️ Desbordamiento numérico (número muy grande).\n💡 El método está divergiendo.\n\n🔧 Solución: La función g(x) no es adecuada para este problema"}
        except Exception as e:
            return {"exito": False,
                   "mensaje": f"⚠️ Error inesperado en iteración {c}: {str(e)}\n\n🔧 Solución: Verifica que g(x) esté bien escrita"}

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

    if error <= tol:
        mensaje = f"✅ Punto fijo encontrado: {xn1:.10f} con error {error:.2e}"
    else:
        mensaje = f"⚠️ No convergió en {niter} iteraciones (error final: {error:.2e}).\n💡 Posibles causas:\n   • g(x) no cumple la condición de convergencia |g'(x)| < 1\n   • Necesitas más iteraciones\n   • x0 está muy lejos de la raíz\n\n🔧 Soluciones:\n   1. Aumenta el número de iteraciones\n   2. Prueba con otro x0\n   3. Reformula g(x)\n   4. Usa otro método"

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
        derivada_str = str(df_expr)  # Guardar derivada como string
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita.\n💡 Ejemplo correcto: x**3 - 2*x - 5"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar la función.\n💡 Asegúrate de usar 'x' como variable."}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    dfn_vals = []
    errores = []

    xn = x0
    c = 0
    error = 100

    try:
        fn = f(xn)
        dfn = df(xn)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return {"exito": False,
               "mensaje": f"❌ Error al evaluar f(x) en x0={x0}\n💡 La función no está definida en este punto.\n\n🔧 Solución: Cambia el valor inicial x0"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error inesperado al evaluar f(x): {str(e)}"}

    if math.isnan(fn) or math.isnan(dfn):
        return {"exito": False, "mensaje": f"❌ f(x0) o f'(x0) no están definidas en x0={x0}\n\n🔧 Solución: Cambia x0"}

    iteraciones.append(c)
    xn_vals.append(xn)
    fn_vals.append(fn)
    dfn_vals.append(dfn)
    errores.append(error)

    while error > tol and fn != 0 and c < niter:
        # Verificar derivada antes de dividir
        if abs(dfn) < 1e-15:
            return {"exito": False,
                   "mensaje": f"⚠️ La derivada se anula en x={xn:.6f} (f'(x)={dfn:.2e})\n\n💡 Cuando f'(x) ≈ 0:\n   • El método de Newton-Raphson falla\n   • No se puede calcular: x - f(x)/f'(x)\n\n🔧 Soluciones:\n   1. Cambia x0 (valor inicial) a otro punto\n   2. Usa otro método (Bisección, Secante, Regla Falsa)\n   3. Si la raíz es múltiple, usa el método de Raíces Múltiples"}

        try:
            xn = xn - fn / dfn
            fn = f(xn)
            dfn = df(xn)

            # Detectar valores inválidos
            if math.isnan(xn) or math.isnan(fn) or math.isnan(dfn):
                return {"exito": False,
                       "mensaje": f"⚠️ Se obtuvo un valor no numérico (NaN) en la iteración {c+1}.\n\n🔧 Solución: Cambia x0 o verifica el dominio de f(x)"}

            if math.isinf(xn) or math.isinf(fn):
                return {"exito": False,
                       "mensaje": f"⚠️ El método está divergiendo (valores infinitos).\n\n🔧 Solución: Cambia x0 a un valor más cercano a la raíz"}

            # Detectar divergencia
            if abs(xn) > 1e10:
                return {"exito": False,
                       "mensaje": f"⚠️ El método está divergiendo (x={xn:.2e}).\n💡 x0={x0} está muy lejos de la raíz.\n\n🔧 Soluciones:\n   1. Cambia x0 a un valor más cercano\n   2. Usa un método de intervalo (Bisección) para acotar la raíz primero"}

        except ZeroDivisionError:
            return {"exito": False,
                   "mensaje": f"⚠️ División por cero: f'({xn:.6f}) = 0\n\n🔧 Solución: Cambia x0"}
        except (ValueError, OverflowError) as e:
            return {"exito": False,
                   "mensaje": f"⚠️ Error numérico en iteración {c+1}: {str(e)}\n\n🔧 Solución: Cambia x0"}
        except Exception as e:
            return {"exito": False, "mensaje": f"❌ Error inesperado en iteración {c+1}: {str(e)}"}

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
        "error_final": error,
        "derivada": derivada_str  # Mostrar derivada calculada
    }


def secante(x0, x1, tol, niter, funcion_str, tol_str=None):
    """
    Método de la Secante

    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    # Detectar tipo de error usando el string original de tolerancia
    if tol_str is None:
        tol_str = str(tol)

    # Detectar el tipo de error
    if tol_str.startswith(("5e", "5E", "5.0e", "5.0E")):
        tipo_error = "relativo"  # Cifras Significativas
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"  # Decimales Correctos
    else:
        tipo_error = "ninguno"  # No es ninguno de los dos tipos específicos

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita.\n💡 Ejemplo correcto: x**3 - x - 2"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar la función.\n💡 Asegúrate de usar 'x' como variable."}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    errores = []

    # Evaluar f en los puntos iniciales con manejo de errores
    try:
        f0 = f(x0)
        f1 = f(x1)

        # Validar que los valores no sean NaN o infinitos
        if math.isnan(f0) or math.isnan(f1):
            return {"exito": False,
                   "mensaje": f"❌ La función no está definida en x0={x0} o x1={x1}\n💡 Posibles causas:\n   • Raíz de número negativo\n   • Logaritmo de número no positivo\n   • División por cero\n\n🔧 Solución: Cambia los valores iniciales x0 y x1"}

        if math.isinf(f0) or math.isinf(f1):
            return {"exito": False,
                   "mensaje": f"❌ La función diverge a infinito en x0={x0} o x1={x1}\n\n🔧 Solución: Elige valores iniciales más cercanos a la raíz"}

    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return {"exito": False,
               "mensaje": f"❌ Error al evaluar f(x) en los puntos iniciales.\n💡 La función no está definida en x0={x0} o x1={x1}\n\n🔧 Solución: Cambia los valores iniciales"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error inesperado: {str(e)}"}

    k = 0
    error = tol + 1  # Inicializar error
    iteraciones.append(k)
    xn_vals.append(x1)
    fn_vals.append(f1)
    errores.append(None)

    if f0 == 0:
        return {"exito": True, "raiz": x0, "mensaje": f"{x0} es raíz exacta",
                "iteraciones": 0, "tabla": {}, "tipo_error": tipo_error, "error_final": 0}
    elif f1 == 0:
        return {"exito": True, "raiz": x1, "mensaje": f"{x1} es raíz exacta",
                "iteraciones": 0, "tabla": {}, "tipo_error": tipo_error, "error_final": 0}

    valores_grandes_consecutivos = 0

    while k < niter:
        denom = f1 - f0

        # Validar que la recta secante no sea horizontal
        if abs(denom) < 1e-15:
            return {"exito": False,
                   "mensaje": f"⚠️ Los valores de f(x) son muy similares en las dos últimas iteraciones.\n💡 El problema:\n   • f({xn_vals[-1]:.4f}) ≈ f({x0:.4f})\n   • La recta secante es casi horizontal\n   • No se puede calcular la siguiente aproximación\n\n🔧 Soluciones:\n   1. Cambia los valores iniciales x0 y x1 (que estén más separados)\n   2. Usa otro método (Newton-Raphson, Bisección)"}

        try:
            x2 = x1 - f1 * (x1 - x0) / denom

            # Detectar divergencia
            if math.isnan(x2):
                return {"exito": False,
                       "mensaje": f"⚠️ Se obtuvo un valor no numérico (NaN) en la iteración {k+1}.\n\n🔧 Solución: Cambia los valores iniciales x0 y x1"}

            if math.isinf(x2):
                return {"exito": False,
                       "mensaje": f"⚠️ El método está divergiendo (valor infinito).\n\n🔧 Solución: Cambia x0 y x1 a valores más cercanos a la raíz"}

            # Detectar valores muy grandes
            if abs(x2) > 1e10:
                valores_grandes_consecutivos += 1
                if valores_grandes_consecutivos >= 3:
                    return {"exito": False,
                           "mensaje": f"⚠️ El método está divergiendo (x={x2:.2e}).\n💡 Los valores iniciales x0={x0} y x1={x1} están muy lejos de la raíz.\n\n🔧 Soluciones:\n   1. Elige x0 y x1 más cercanos a la raíz\n   2. Usa Bisección primero para acotar la raíz"}
            else:
                valores_grandes_consecutivos = 0

            if tipo_error == "relativo":
                error = abs(x2 - x1) / abs(x2) if x2 != 0 else abs(x2 - x1)
            else:
                error = abs(x2 - x1)

            x0, f0 = x1, f1
            x1 = x2
            f1 = f(x1)

            # Validar f1
            if math.isnan(f1):
                return {"exito": False,
                       "mensaje": f"⚠️ f({x1:.4f}) no está definida (NaN).\n\n🔧 Solución: El método salió del dominio de f(x)"}

            if math.isinf(f1):
                return {"exito": False,
                       "mensaje": f"⚠️ f({x1:.4f}) diverge a infinito.\n\n🔧 Solución: El método está fuera de control"}

        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return {"exito": False,
                   "mensaje": f"⚠️ Error numérico en iteración {k+1}: {str(e)}\n\n🔧 Solución: Cambia los valores iniciales x0 y x1"}
        except Exception as e:
            return {"exito": False, "mensaje": f"❌ Error inesperado en iteración {k+1}: {str(e)}"}

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
        mensaje = f"❌ No se alcanzó la tolerancia en {niter} iteraciones.\n💡 Error actual: {error:.2e} > Tolerancia: {tol:.2e}\n\n🔧 Soluciones:\n   1. Aumenta el número de iteraciones\n   2. Cambia x0 y x1 a valores más cercanos a la raíz\n   3. Aumenta la tolerancia"

    return {
        "exito": f1 == 0 or error < tol,
        "raiz": x1,
        "mensaje": mensaje,
        "iteraciones": k,
        "tabla": tabla,
        "tipo_error": tipo_error,
        "error_final": error
    }


def raices_multiples(x0, tol, niter, funcion_str, metodo=2, multiplicidad=None, tol_str=None):
    """
    Método de Newton-Raphson para Raíces Múltiples

    metodo: 1 (con multiplicidad conocida) o 2 (con segunda derivada)
    Retorna: dict con 'tabla', 'exito', 'raiz', 'mensaje', 'iteraciones'
    """
    # Detectar tipo de error usando el string original de tolerancia
    if tol_str is None:
        tol_str = str(tol)

    # Detectar el tipo de error
    if tol_str.startswith(("5e", "5E", "5.0e", "5.0E")):
        tipo_error = "relativo"  # Cifras Significativas
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"  # Decimales Correctos
    else:
        tipo_error = "ninguno"  # No es ninguno de los dos tipos específicos

    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        df_expr = sp.diff(f_expr, x_sym)
        ddf_expr = sp.diff(df_expr, x_sym)

        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])
        df = sp.lambdify(x_sym, df_expr, modules=['numpy', 'math'])
        ddf = sp.lambdify(x_sym, ddf_expr, modules=['numpy', 'math'])

        derivada_str = str(df_expr)  # Guardar derivadas como string
        derivada2_str = str(ddf_expr)
    except SyntaxError:
        return {"exito": False, "mensaje": "❌ Error de sintaxis en la función. Verifica que esté bien escrita.\n💡 Ejemplo correcto: (x-1)**3"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error al procesar la función.\n💡 Asegúrate de usar 'x' como variable."}

    iteraciones = []
    xn_vals = []
    fn_vals = []
    dfn_vals = []
    errores = []

    c = 0
    xn = x0

    # Evaluar función inicial con manejo de errores
    try:
        fn = f(xn)
        dfn = df(xn)

        # Validar valores iniciales
        if math.isnan(fn) or math.isnan(dfn):
            return {"exito": False,
                   "mensaje": f"❌ La función o su derivada no están definidas en x0={x0}\n\n🔧 Solución: Cambia el valor inicial x0"}

        if math.isinf(fn) or math.isinf(dfn):
            return {"exito": False,
                   "mensaje": f"❌ La función diverge a infinito en x0={x0}\n\n🔧 Solución: Elige un x0 más cercano a la raíz"}

    except (ValueError, ZeroDivisionError, OverflowError) as e:
        return {"exito": False,
               "mensaje": f"❌ Error al evaluar f(x) en x0={x0}\n💡 La función no está definida en este punto.\n\n🔧 Solución: Cambia el valor inicial x0"}
    except Exception as e:
        return {"exito": False, "mensaje": f"❌ Error inesperado: {str(e)}"}

    iteraciones.append(c)
    xn_vals.append(xn)
    fn_vals.append(fn)
    dfn_vals.append(dfn)
    errores.append(None)

    error = tol + 1
    valores_grandes_consecutivos = 0

    while error > tol and c < niter:
        try:
            fn = f(xn)
            dfn = df(xn)

            # Verificar derivada
            if abs(dfn) < 1e-15:
                return {"exito": False,
                       "mensaje": f"⚠️ La derivada se anula en x={xn:.6f} (f'(x)={dfn:.2e})\n\n💡 Cuando f'(x) ≈ 0:\n   • El método para raíces múltiples no puede continuar\n   • No se puede calcular la siguiente iteración\n\n🔧 Soluciones:\n   1. Cambia x0 (valor inicial) a otro punto\n   2. Verifica que la función tenga una raíz múltiple\n   3. Si la raíz es simple, usa Newton-Raphson normal"}

            if metodo == 1 and multiplicidad:
                # Método con multiplicidad conocida
                if multiplicidad <= 0:
                    return {"exito": False,
                           "mensaje": "❌ La multiplicidad debe ser un entero positivo (1, 2, 3, ...)\n\n🔧 Solución: Ingresa una multiplicidad válida o usa el método 2 (con segunda derivada)"}

                xn1 = xn - multiplicidad * fn / dfn
            else:
                # Método con segunda derivada
                ddfn = ddf(xn)

                # Validar segunda derivada
                if math.isnan(ddfn):
                    return {"exito": False,
                           "mensaje": f"⚠️ La segunda derivada no está definida en x={xn:.6f}\n\n🔧 Solución: Cambia x0"}

                denominador = dfn**2 - fn * ddfn

                if abs(denominador) < 1e-15:
                    return {"exito": False,
                           "mensaje": f"⚠️ El denominador del método es muy pequeño en x={xn:.6f}\n💡 El problema:\n   • [f'(x)]² - f(x)·f''(x) ≈ 0\n   • El método no puede continuar\n\n🔧 Soluciones:\n   1. Cambia x0 a otro valor\n   2. Verifica que la función tenga raíz múltiple\n   3. Prueba con multiplicidad conocida (método 1)"}

                xn1 = xn - (fn * dfn) / denominador

            # Detectar valores inválidos
            if math.isnan(xn1):
                return {"exito": False,
                       "mensaje": f"⚠️ Se obtuvo un valor no numérico (NaN) en la iteración {c+1}.\n\n🔧 Solución: Cambia x0 o verifica que f(x) tenga raíz múltiple"}

            if math.isinf(xn1):
                return {"exito": False,
                       "mensaje": f"⚠️ El método está divergiendo (valor infinito).\n\n🔧 Solución: Cambia x0 a un valor más cercano a la raíz"}

            # Detectar divergencia
            if abs(xn1) > 1e10:
                valores_grandes_consecutivos += 1
                if valores_grandes_consecutivos >= 3:
                    return {"exito": False,
                           "mensaje": f"⚠️ El método está divergiendo (x={xn1:.2e}).\n💡 x0={x0} está muy lejos de la raíz.\n\n🔧 Soluciones:\n   1. Cambia x0 a un valor más cercano\n   2. Verifica que la función tenga una raíz múltiple\n   3. Usa Bisección primero para localizar la raíz"}
            else:
                valores_grandes_consecutivos = 0

            if tipo_error == "relativo":
                error = abs(xn1 - xn) / abs(xn1) if xn1 != 0 else abs(xn1 - xn)
            else:
                error = abs(xn1 - xn)

            c += 1
            xn = xn1
            fn = f(xn)
            dfn = df(xn)

            # Validar nuevos valores
            if math.isnan(fn) or math.isnan(dfn):
                return {"exito": False,
                       "mensaje": f"⚠️ f({xn:.4f}) o f'({xn:.4f}) no están definidas.\n\n🔧 Solución: El método salió del dominio de f(x)"}

            if math.isinf(fn) or math.isinf(dfn):
                return {"exito": False,
                       "mensaje": f"⚠️ La función diverge a infinito en x={xn:.4f}.\n\n🔧 Solución: El método está fuera de control"}

        except (ValueError, ZeroDivisionError, OverflowError) as e:
            return {"exito": False,
                   "mensaje": f"⚠️ Error numérico en iteración {c+1}: {str(e)}\n\n🔧 Solución: Cambia el valor inicial x0"}
        except Exception as e:
            return {"exito": False, "mensaje": f"❌ Error inesperado en iteración {c+1}: {str(e)}"}

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
        mensaje = f"❌ No se alcanzó la tolerancia en {niter} iteraciones.\n💡 Error actual: {error:.2e} > Tolerancia: {tol:.2e}\n\n🔧 Soluciones:\n   1. Aumenta el número de iteraciones\n   2. Cambia x0 a un valor más cercano a la raíz\n   3. Verifica que la función tenga una raíz múltiple\n   4. Si la raíz es simple, usa Newton-Raphson normal"

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
        "es_raiz_multiple": es_multiple,
        "derivada": derivada_str,  # Mostrar derivadas calculadas
        "derivada2": derivada2_str
    }


def generar_puntos_grafica(funcion_str, x_min=None, x_max=None, raiz=None, num_puntos=500):
    """
    Genera puntos para graficar una función
    Si se proporciona raiz, centra la gráfica alrededor de ella
    """
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(funcion_str)
        f = sp.lambdify(x_sym, f_expr, modules=['numpy', 'math'])

        # Si hay raíz, centrar la gráfica alrededor de ella
        if raiz is not None and (x_min is None or x_max is None):
            # Crear un rango centrado en la raíz
            margen = max(abs(raiz) * 0.5, 5)  # Al menos ±5 unidades
            x_min = raiz - margen
            x_max = raiz + margen
        elif x_min is None or x_max is None:
            # Valores por defecto
            x_min = -10
            x_max = 10

        x_vals = np.linspace(x_min, x_max, num_puntos)
        y_vals = []

        for x in x_vals:
            try:
                y = f(x)
                # Limitar valores muy grandes para mejor visualización
                if np.isfinite(y):
                    if abs(y) > 1e6:
                        y_vals.append(None)
                    else:
                        y_vals.append(y)
                else:
                    y_vals.append(None)
            except:
                y_vals.append(None)

        return x_vals.tolist(), y_vals
    except Exception as e:
        return None, None
