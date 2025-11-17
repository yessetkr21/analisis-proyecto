"""
Métodos numéricos del Capítulo 2: Sistemas de ecuaciones lineales iterativos
Incluye: Jacobi, Gauss-Seidel y SOR
"""

import numpy as np


def calcular_metricas_error(x_actual, x_anterior):
    """
    Calcula las 5 métricas de error para sistemas de ecuaciones
    
    Retorna dict con:
    - error_abs: ||x^(n) - x^(n-1)||_∞
    - error_rel1: ||x^(n) - x^(n-1)|| / ||x^(n)||_∞
    - error_rel2: ||x^(n) - x^(n-1)|| / ||x^(n-1)||_∞
    - error_rel3: ||x^(n) - x^(n-1)|| / ||x^(n)||_∞ (alternativo)
    - error_rel4: ||x^(n) - x^(n-1)|| / ||x^(n-1)||_∞ (alternativo)
    """
    diff = np.linalg.norm(x_actual - x_anterior, np.inf)
    norm_actual = np.linalg.norm(x_actual, np.inf)
    norm_anterior = np.linalg.norm(x_anterior, np.inf)
    
    error_abs = float(diff)
    
    # Error relativo 1: diferencia / norma actual
    if norm_actual != 0:
        error_rel1 = float(diff / norm_actual)
    else:
        error_rel1 = float(diff)
    
    # Error relativo 2: diferencia / norma anterior
    if norm_anterior != 0:
        error_rel2 = float(diff / norm_anterior)
    else:
        error_rel2 = float(diff)
    
    # Error relativo 3 y 4 son equivalentes a 1 y 2
    error_rel3 = error_rel1
    error_rel4 = error_rel2
    
    return {
        "error_abs": error_abs,
        "error_rel1": error_rel1,
        "error_rel2": error_rel2,
        "error_rel3": error_rel3,
        "error_rel4": error_rel4
    }


def jacobi(A, b, x0, tol, niter, tol_str=None):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    tol_str: String de tolerancia para detectar tipo de error

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge', 'tipo_error'
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

    try:
        n = len(A)
        c = 0
        error = tol + 1
        tabla_datos = []

        # Descomposición de la matriz A
        D = np.diag(np.diag(A))
        L = -np.tril(A, -1)
        U = -np.triu(A, 1)

        # Calcular matriz de iteración T y radio espectral
        T = np.linalg.inv(D) @ (L + U)
        radio_espectral = max(abs(np.linalg.eigvals(T)))

        # Guardar estado inicial
        tabla_datos.append({
            "iter": 0,
            "x": x0.copy().tolist(),
            "error_abs": None,
            "error_rel1": None,
            "error_rel2": None,
            "error_rel3": None,
            "error_rel4": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # Jacobi: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D) @ b
            x1 = T @ x_prev + C

            # Calcular las 5 métricas de error
            metricas = calcular_metricas_error(x1, x_prev)

            # Seleccionar error según tipo
            if tipo_error == "relativo":
                error = metricas["error_rel1"]
            else:
                error = metricas["error_abs"]

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error_abs": metricas["error_abs"],
                "error_rel1": metricas["error_rel1"],
                "error_rel2": metricas["error_rel2"],
                "error_rel3": metricas["error_rel3"],
                "error_rel4": metricas["error_rel4"]
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "tipo_error": tipo_error,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": float(error)
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def gauss_seidel(A, b, x0, tol, niter, tol_str=None):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    tol_str: String de tolerancia para detectar tipo de error

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge', 'tipo_error'
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

    try:
        n = len(A)
        c = 0
        error = tol + 1
        tabla_datos = []

        # Descomposición de la matriz A
        D = np.diag(np.diag(A))
        L = -np.tril(A, -1)
        U = -np.triu(A, 1)

        # Calcular matriz de iteración T y radio espectral
        T = np.linalg.inv(D - L) @ U
        radio_espectral = max(abs(np.linalg.eigvals(T)))

        # Guardar estado inicial
        tabla_datos.append({
            "iter": 0,
            "x": x0.copy().tolist(),
            "error_abs": None,
            "error_rel1": None,
            "error_rel2": None,
            "error_rel3": None,
            "error_rel4": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # Gauss-Seidel: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D - L) @ b
            x1 = T @ x_prev + C

            # Calcular las 5 métricas de error
            metricas = calcular_metricas_error(x1, x_prev)

            # Seleccionar error según tipo
            if tipo_error == "relativo":
                error = metricas["error_rel1"]
            else:
                error = metricas["error_abs"]

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error_abs": metricas["error_abs"],
                "error_rel1": metricas["error_rel1"],
                "error_rel2": metricas["error_rel2"],
                "error_rel3": metricas["error_rel3"],
                "error_rel4": metricas["error_rel4"]
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "tipo_error": tipo_error,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": float(error)
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def sor(A, b, x0, tol, niter, w, tol_str=None):
    """
    Método SOR (Successive Over-Relaxation) para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    w: Factor de relajación (0 < w < 2)
       w < 1: Subrelajación
       w = 1: Gauss-Seidel
       w > 1: Sobrerelajación
    tol_str: String de tolerancia para detectar tipo de error

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge', 'w', 'tipo_error'
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

    try:
        if w <= 0 or w >= 2:
            return {"exito": False, "mensaje": "El factor de relajación w debe estar entre 0 y 2"}

        n = len(A)
        c = 0
        error = tol + 1
        tabla_datos = []

        # Descomposición de la matriz A
        D = np.diag(np.diag(A))
        L = -np.tril(A, -1)
        U = -np.triu(A, 1)

        # Calcular matriz de iteración T y radio espectral
        T = np.linalg.inv(D - w*L) @ ((1-w)*D + w*U)
        radio_espectral = max(abs(np.linalg.eigvals(T)))

        # Guardar estado inicial
        tabla_datos.append({
            "iter": 0,
            "x": x0.copy().tolist(),
            "error_abs": None,
            "error_rel1": None,
            "error_rel2": None,
            "error_rel3": None,
            "error_rel4": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # SOR: x^(k+1) = T * x^(k) + C
            C = w * np.linalg.inv(D - w*L) @ b
            x1 = T @ x_prev + C

            # Calcular las 5 métricas de error
            metricas = calcular_metricas_error(x1, x_prev)

            # Seleccionar error según tipo
            if tipo_error == "relativo":
                error = metricas["error_rel1"]
            else:
                error = metricas["error_abs"]

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error_abs": metricas["error_abs"],
                "error_rel1": metricas["error_rel1"],
                "error_rel2": metricas["error_rel2"],
                "error_rel3": metricas["error_rel3"],
                "error_rel4": metricas["error_rel4"]
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "w": float(w),
            "tipo_error": tipo_error,
            "mensaje": f"Solución encontrada en {c} iteraciones con w={w}" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": float(error)
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def validar_matriz(matriz_str, b_str):
    """
    Valida y convierte strings de matriz y vector b a numpy arrays

    Formato esperado:
    Matriz: "1,2,3;4,5,6;7,8,9" (filas separadas por ;, elementos por ,)
    Vector b: "1,2,3" (elementos separados por ,)
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

        # Validar dimensiones
        n_filas, n_cols = A.shape
        if n_filas != n_cols:
            return None, None, "La matriz debe ser cuadrada"
        if len(b) != n_filas:
            return None, None, f"El vector b debe tener {n_filas} elementos"
        if n_filas > 7:
            return None, None, "La matriz no puede tener más de 7x7 elementos"

        # Validar que la diagonal no tenga ceros
        if np.any(np.diag(A) == 0):
            return None, None, "La matriz no puede tener ceros en la diagonal"

        return A, b, None
    except Exception as e:
        return None, None, f"Error al procesar los datos: {str(e)}"


def es_diagonalmente_dominante(A):
    """
    Verifica si una matriz es diagonalmente dominante
    """
    n = len(A)
    for i in range(n):
        suma_fila = sum(abs(A[i, j]) for j in range(n) if j != i)
        if abs(A[i, i]) <= suma_fila:
            return False
    return True


def generar_puntos_grafica_convergencia(tabla_datos, tipo_error="absoluto"):
    """
    Genera puntos para graficar la convergencia de un método iterativo

    Parámetros:
    tabla_datos: Lista de diccionarios con datos de cada iteración
    tipo_error: Tipo de error a graficar ("absoluto" o "relativo")

    Retorna:
    iteraciones: Lista de números de iteración
    errores: Lista de valores de error correspondientes
    """
    iteraciones = []
    errores = []

    for dato in tabla_datos:
        iter_num = dato.get("iter", 0)

        # Seleccionar el tipo de error apropiado
        if tipo_error == "relativo":
            error_val = dato.get("error_rel1")
        else:
            error_val = dato.get("error_abs")

        # Solo agregar si el error no es None
        if error_val is not None:
            iteraciones.append(iter_num)
            errores.append(error_val)

    return iteraciones, errores


def comparar_metodos_cap2(A, b, x0, tol, niter, w=1.5, tol_str=None):
    """
    Compara los tres métodos del capítulo 2 para un mismo problema

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    w: Factor de relajación para SOR
    tol_str: String de tolerancia para detectar tipo de error

    Retorna: dict con resultados de cada método y análisis comparativo
    """
    resultados = {}

    # Ejecutar Jacobi
    res_jacobi = jacobi(A, b, x0.copy(), tol, niter, tol_str)
    resultados['jacobi'] = res_jacobi

    # Ejecutar Gauss-Seidel
    res_seidel = gauss_seidel(A, b, x0.copy(), tol, niter, tol_str)
    resultados['gauss_seidel'] = res_seidel

    # Ejecutar SOR
    res_sor = sor(A, b, x0.copy(), tol, niter, w, tol_str)
    resultados['sor'] = res_sor

    # Análisis comparativo
    metodos_exitosos = []
    if res_jacobi.get('exito'):
        metodos_exitosos.append(('Jacobi', res_jacobi['iteraciones'], res_jacobi['error_final']))
    if res_seidel.get('exito'):
        metodos_exitosos.append(('Gauss-Seidel', res_seidel['iteraciones'], res_seidel['error_final']))
    if res_sor.get('exito'):
        metodos_exitosos.append(('SOR', res_sor['iteraciones'], res_sor['error_final']))

    if metodos_exitosos:
        # Ordenar por número de iteraciones (menor es mejor)
        metodos_exitosos.sort(key=lambda x: (x[1], x[2]))
        mejor_metodo = metodos_exitosos[0][0]
    else:
        mejor_metodo = "Ninguno convergió"

    # Verificar diagonal dominante
    es_dd = es_diagonalmente_dominante(A)

    resultados['comparacion'] = {
        "mejor_metodo": mejor_metodo,
        "metodos_exitosos": [m[0] for m in metodos_exitosos],
        "es_diagonalmente_dominante": es_dd,
        "analisis": f"El método más eficiente fue {mejor_metodo}" if mejor_metodo != "Ninguno convergió" else "Ningún método convergió. La matriz podría no cumplir condiciones de convergencia."
    }

    return resultados
