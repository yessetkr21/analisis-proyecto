"""
Métodos numéricos del Capítulo 2: Sistemas de ecuaciones lineales iterativos
Incluye: Jacobi, Gauss-Seidel y SOR
"""

import numpy as np


def calcular_error(x_actual, x_anterior):
    """
    Calcula el error entre dos iteraciones usando la norma infinito
    Similar al código del profesor (línea 73 de jacobi.py)

    Retorna:
    - error: ||x^(n) - x^(n-1)||_∞
    """
    return float(np.linalg.norm(x_actual - x_anterior, np.inf))


def jacobi(A, b, x0, tol, niter):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error (norma infinito)
    niter: Número máximo de iteraciones

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge'
    """
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
            "error": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # Jacobi: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D) @ b
            x1 = T @ x_prev + C

            # Calcular error (norma infinito como el profesor)
            error = calcular_error(x1, x_prev)

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error": error
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        # Extraer lista de errores
        errores_lista = []
        for dato in tabla_datos:
            error_val = dato.get("error")
            if error_val is not None:
                errores_lista.append(error_val)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "errores": errores_lista,  # Lista de errores para comparación
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": float(error)
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def gauss_seidel(A, b, x0, tol, niter):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error (norma infinito)
    niter: Número máximo de iteraciones

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge'
    """
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
            "error": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # Gauss-Seidel: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D - L) @ b
            x1 = T @ x_prev + C

            # Calcular error (norma infinito como el profesor)
            error = calcular_error(x1, x_prev)

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error": error
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        # Extraer lista de errores
        errores_lista = []
        for dato in tabla_datos:
            error_val = dato.get("error")
            if error_val is not None:
                errores_lista.append(error_val)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "errores": errores_lista,  # Lista de errores para comparación
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": float(error)
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def sor(A, b, x0, tol, niter, w):
    """
    Método SOR (Successive Over-Relaxation) para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error (norma infinito)
    niter: Número máximo de iteraciones
    w: Factor de relajación (0 < w < 2)
       w < 1: Subrelajación
       w = 1: Gauss-Seidel
       w > 1: Sobrerelajación

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'tabla', 'radio_espectral', 'converge', 'w'
    """
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
            "error": None
        })

        x_prev = x0.copy()

        while error > tol and c < niter:
            # SOR: x^(k+1) = T * x^(k) + C
            C = w * np.linalg.inv(D - w*L) @ b
            x1 = T @ x_prev + C

            # Calcular error (norma infinito como el profesor)
            error = calcular_error(x1, x_prev)

            c += 1
            tabla_datos.append({
                "iter": int(c),
                "x": x1.copy().tolist(),
                "error": error
            })

            x_prev = x1.copy()

        converge = bool(radio_espectral < 1)

        # Extraer lista de errores
        errores_lista = []
        for dato in tabla_datos:
            error_val = dato.get("error")
            if error_val is not None:
                errores_lista.append(error_val)

        return {
            "exito": bool(error < tol),
            "solucion": x_prev.tolist(),
            "iteraciones": int(c),
            "tabla": tabla_datos,
            "errores": errores_lista,  # Lista de errores para comparación
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "w": float(w),
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
        # Validar que no estén vacíos
        if not matriz_str or matriz_str.strip() == '':
            return None, None, "[ERROR] La matriz A no puede estar vacia. Formato: 10,1,1;2,10,1;2,2,10"

        if not b_str or b_str.strip() == '':
            return None, None, "[ERROR] El vector b no puede estar vacio. Formato: 12,13,14"

        # Procesar matriz
        filas = matriz_str.strip().split(';')
        A = []

        for i, fila in enumerate(filas):
            try:
                elementos = [float(x.strip()) for x in fila.split(',')]
                A.append(elementos)
            except ValueError as ve:
                return None, None, f"[ERROR] Error en fila {i+1} de la matriz: Valor no numerico encontrado. Verifica que todos los elementos sean numeros."

        A = np.array(A)

        # Procesar vector b
        try:
            b = np.array([float(x.strip()) for x in b_str.strip().split(',')])
        except ValueError:
            return None, None, "[ERROR] Error en vector b: Todos los elementos deben ser numeros. Formato: 12,13,14"

        # Validar dimensiones
        n_filas, n_cols = A.shape

        if n_filas != n_cols:
            return None, None, f"[ERROR] La matriz debe ser cuadrada. Dimension actual: {n_filas}x{n_cols}"

        if len(b) != n_filas:
            return None, None, f"[ERROR] El vector b debe tener {n_filas} elementos (igual a las filas de A). Elementos actuales en b: {len(b)}"

        if n_filas > 7:
            return None, None, f"[ERROR] La matriz no puede tener mas de 7x7 elementos. Tamano actual: {n_filas}x{n_cols}"

        if n_filas < 2:
            return None, None, "[ERROR] La matriz debe tener al menos 2x2 elementos"

        # Validar que la diagonal no tenga ceros
        diagonal = np.diag(A)
        if np.any(diagonal == 0):
            indices_cero = [i+1 for i, val in enumerate(diagonal) if val == 0]
            return None, None, f"[ERROR] La matriz tiene ceros en la diagonal (posiciones: {indices_cero}). Los metodos iterativos requieren diagonal no nula."

        # Validar que no haya valores infinitos o NaN
        if np.any(np.isinf(A)) or np.any(np.isnan(A)):
            return None, None, "[ERROR] La matriz contiene valores infinitos o NaN"

        if np.any(np.isinf(b)) or np.any(np.isnan(b)):
            return None, None, "[ERROR] El vector b contiene valores infinitos o NaN"

        return A, b, None

    except Exception as e:
        return None, None, f"[ERROR] Error al procesar los datos: {str(e)}"


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
