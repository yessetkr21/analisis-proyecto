"""
Métodos numéricos del Capítulo 2: Sistemas de ecuaciones lineales iterativos
Incluye: Jacobi, Gauss-Seidel y SOR
"""

import numpy as np


def jacobi(A, b, x0, tol, niter):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales

    Parámetros:
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    x0: Vector inicial (numpy array)
    tol: Tolerancia para el error
    niter: Número máximo de iteraciones

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'errores', 'tabla', 'radio_espectral', 'converge'
    """
    try:
        n = len(A)
        c = 0
        error = tol + 1
        errores = []
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

        while error > tol and c < niter:
            # Jacobi: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D) @ b
            x1 = T @ x0 + C

            # Calcular error (norma infinito)
            error = np.linalg.norm(x1 - x0, np.inf)
            errores.append(error)

            c += 1
            tabla_datos.append({
                "iter": c,
                "x": x1.copy().tolist(),
                "error": error
            })

            x0 = x1

        converge = radio_espectral < 1

        return {
            "exito": error < tol,
            "solucion": x0.tolist(),
            "iteraciones": c,
            "errores": errores,
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": error
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def gauss_seidel(A, b, x0, tol, niter):
    """
    Método de Gauss-Seidel para resolver sistemas de ecuaciones lineales

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'errores', 'tabla', 'radio_espectral', 'converge'
    """
    try:
        n = len(A)
        c = 0
        error = tol + 1
        errores = []
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

        while error > tol and c < niter:
            # Gauss-Seidel: x^(k+1) = T * x^(k) + C
            C = np.linalg.inv(D - L) @ b
            x1 = T @ x0 + C

            # Calcular error (norma infinito)
            error = np.linalg.norm(x1 - x0, np.inf)
            errores.append(error)

            c += 1
            tabla_datos.append({
                "iter": c,
                "x": x1.copy().tolist(),
                "error": error
            })

            x0 = x1

        converge = radio_espectral < 1

        return {
            "exito": error < tol,
            "solucion": x0.tolist(),
            "iteraciones": c,
            "errores": errores,
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "mensaje": f"Solución encontrada en {c} iteraciones" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": error
        }
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}"}


def sor(A, b, x0, tol, niter, w):
    """
    Método SOR (Successive Over-Relaxation) para resolver sistemas de ecuaciones lineales

    Parámetros adicionales:
    w: Factor de relajación (0 < w < 2)
       w < 1: Subrelajación
       w = 1: Gauss-Seidel
       w > 1: Sobrerelajación

    Retorna: dict con 'exito', 'solucion', 'iteraciones', 'errores', 'tabla', 'radio_espectral', 'converge', 'w'
    """
    try:
        if w <= 0 or w >= 2:
            return {"exito": False, "mensaje": "El factor de relajación w debe estar entre 0 y 2"}

        n = len(A)
        c = 0
        error = tol + 1
        errores = []
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

        while error > tol and c < niter:
            # SOR: x^(k+1) = T * x^(k) + C
            C = w * np.linalg.inv(D - w*L) @ b
            x1 = T @ x0 + C

            # Calcular error (norma infinito)
            error = np.linalg.norm(x1 - x0, np.inf)
            errores.append(error)

            c += 1
            tabla_datos.append({
                "iter": c,
                "x": x1.copy().tolist(),
                "error": error
            })

            x0 = x1

        converge = radio_espectral < 1

        return {
            "exito": error < tol,
            "solucion": x0.tolist(),
            "iteraciones": c,
            "errores": errores,
            "tabla": tabla_datos,
            "radio_espectral": float(radio_espectral),
            "converge": converge,
            "w": w,
            "mensaje": f"Solución encontrada en {c} iteraciones con w={w}" if error < tol else f"No convergió en {niter} iteraciones",
            "error_final": error
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


def comparar_metodos_cap2(A, b, x0, tol, niter, w=1.5):
    """
    Compara los tres métodos del capítulo 2 para un mismo problema

    Retorna: dict con resultados de cada método y análisis comparativo
    """
    resultados = {}

    # Ejecutar Jacobi
    res_jacobi = jacobi(A, b, x0.copy(), tol, niter)
    resultados['jacobi'] = res_jacobi

    # Ejecutar Gauss-Seidel
    res_seidel = gauss_seidel(A, b, x0.copy(), tol, niter)
    resultados['gauss_seidel'] = res_seidel

    # Ejecutar SOR
    res_sor = sor(A, b, x0.copy(), tol, niter, w)
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
