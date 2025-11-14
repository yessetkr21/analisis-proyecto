import numpy as np

def NewJacobiSeid(x0, A, b, met):
    """
    NewJacobiSeid: Calcula la aproximación siguiente a la solución del sistema
    Ax=b con base en una condición inicial x0, mediante el método de Jacobi o
    de Gauss Seidel, depende del método elegido, se elige 0 o 1 en met
    respectivamente
    
    Parámetros:
    x0: Vector inicial (numpy array)
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    met: Método a usar (0 para Jacobi, 1 para Gauss-Seidel)
    
    Retorna:
    x1: Nueva aproximación del vector solución
    """
    n = len(A)
    x1 = x0.copy()
    
    for i in range(n):
        sum_val = 0
        for j in range(n):
            if j != i and met == 0:
                sum_val += A[i, j] * x0[j]
            elif j != i and met == 1:
                sum_val += A[i, j] * x1[j]
        x1[i] = (b[i] - sum_val) / A[i, i]
    
    return x1


def MatJacobiSeid(x0, A, b, Tol, niter, met):
    """
    MatJacobiSeid: Calcula la solución del sistema
    Ax=b con base en una condición inicial x0, mediante el método de Jacobi o
    de Gauss Seidel (Matricial), depende del método elegido, se elige 0 o 1 en met
    respectivamente
    
    Parámetros:
    x0: Vector inicial (numpy array)
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    Tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    met: Método a usar (0 para Jacobi, 1 para Gauss-Seidel)
    
    Retorna:
    E: Vector de errores en cada iteración
    s: Solución aproximada
    """
    c = 0
    error = Tol + 1
    E = []
    
    # Descomposición de la matriz A
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    
    while error > Tol and c < niter:
        if met == 0:  # Jacobi
            T = np.linalg.inv(D) @ (L + U)
            C = np.linalg.inv(D) @ b
            x1 = T @ x0 + C
        elif met == 1:  # Gauss-Seidel
            T = np.linalg.inv(D - L) @ U
            C = np.linalg.inv(D - L) @ b
            x1 = T @ x0 + C
        
        # Calcular error
        E.append(np.linalg.norm(x1 - x0, np.inf))
        error = E[c]
        x0 = x1
        c += 1
    
    if error < Tol:
        s = x0
        print(f"\nSolución encontrada:")
        print(s)
        print(f"Es una aproximación de la solución del sistema con una tolerancia = {Tol}")
        print(f"Iteraciones realizadas: {c}")
    else:
        s = x0
        print(f"Fracasó en {niter} iteraciones")
    
    return np.array(E), s


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo 1: Sistema de ecuaciones 3x3
    print("=" * 60)
    print("EJEMPLO - MÉTODO DE JACOBI Y GAUSS-SEIDEL")
    print("=" * 60)
    
    # Sistema de ecuaciones:
    # 10x + y + z = 12
    # 2x + 10y + z = 13
    # 2x + 2y + 10z = 14
    
    A = np.array([[10.0, 1.0, 1.0],
                  [2.0, 10.0, 1.0],
                  [2.0, 2.0, 10.0]])
    
    b = np.array([12.0, 13.0, 14.0])
    x0 = np.array([0.0, 0.0, 0.0])
    Tol = 1e-6
    niter = 100
    
    # Método de Jacobi (met = 0)
    print("\n--- MÉTODO DE JACOBI ---")
    E_jacobi, s_jacobi = MatJacobiSeid(x0.copy(), A, b, Tol, niter, met=0)
    
    # Método de Gauss-Seidel (met = 1)
    print("\n--- MÉTODO DE GAUSS-SEIDEL ---")
    E_seidel, s_seidel = MatJacobiSeid(x0.copy(), A, b, Tol, niter, met=1)
    
    # Comparación
    print("\n" + "=" * 60)
    print("COMPARACIÓN DE RESULTADOS")
    print("=" * 60)
    print(f"Iteraciones con Jacobi: {len(E_jacobi)}")
    print(f"Iteraciones con Gauss-Seidel: {len(E_seidel)}")
    print(f"\nSolución con Jacobi: {s_jacobi}")
    print(f"Solución con Gauss-Seidel: {s_seidel}")
    
    # Verificación
    print("\nVerificación A @ s = b:")
    print(f"Jacobi:       {A @ s_jacobi}")
    print(f"Gauss-Seidel: {A @ s_seidel}")
    print(f"Vector b:     {b}")
