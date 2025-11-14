import numpy as np

def NewGaussSeidel(x0, A, b):
    """
    NewGaussSeidel: Calcula la aproximación siguiente a la solución del sistema
    Ax=b con base en una condición inicial x0, mediante el método de Gauss-Seidel
    
    Parámetros:
    x0: Vector inicial (numpy array)
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    
    Retorna:
    x1: Nueva aproximación del vector solución
    """
    n = len(A)
    x1 = x0.copy()
    
    for i in range(n):
        sum_val = 0
        for j in range(n):
            if j != i:
                sum_val += A[i, j] * x1[j]
        x1[i] = (b[i] - sum_val) / A[i, i]
    
    return x1


def MatGaussSeidel(x0, A, b, Tol, niter):
    """
    MatGaussSeidel: Calcula la solución del sistema Ax=b con base en una 
    condición inicial x0, mediante el método de Gauss-Seidel (Matricial)
    
    Parámetros:
    x0: Vector inicial (numpy array)
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    Tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    
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
        # Gauss-Seidel
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
    print("=" * 60)
    print("MÉTODO DE GAUSS-SEIDEL")
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
    
    # Método de Gauss-Seidel
    print("\n--- Resolviendo sistema con Gauss-Seidel ---")
    E, s = MatGaussSeidel(x0.copy(), A, b, Tol, niter)
    
    # Mostrar progreso de errores
    print("\n--- Progreso de errores por iteración ---")
    for i, error in enumerate(E):
        print(f"Iteración {i+1}: Error = {error:.10f}")
    
    # Verificación
    print("\n--- Verificación ---")
    print(f"A @ s = {A @ s}")
    print(f"b     = {b}")
    print(f"Error absoluto: {np.linalg.norm(A @ s - b)}")
