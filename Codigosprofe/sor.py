import numpy as np

def SOR(x0, A, b, Tol, niter, w):
    """
    SOR: Calcula la solución del sistema Ax=b con base en una condición inicial x0,
    mediante el método Gauss Seidel (relajado), depende del valor de w entre (0,2)
    
    Parámetros:
    x0: Vector inicial (numpy array)
    A: Matriz de coeficientes (numpy array)
    b: Vector de términos independientes (numpy array)
    Tol: Tolerancia para el error
    niter: Número máximo de iteraciones
    w: Factor de relajación (debe estar entre 0 y 2)
        w < 1: Subrelajación
        w = 1: Gauss-Seidel estándar
        w > 1: Sobrerelajación
    
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
        # Método SOR
        T = np.linalg.inv(D - w*L) @ ((1-w)*D + w*U)
        C = w * np.linalg.inv(D - w*L) @ b
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
        print(f"Factor de relajación w = {w}")
    else:
        s = x0
        print(f"Fracasó en {niter} iteraciones")
    
    return np.array(E), s


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("MÉTODO SOR (Successive Over-Relaxation)")
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
    
    # Probar con diferentes valores de w
    valores_w = [0.5, 1.0, 1.25, 1.5]
    
    resultados = []
    
    for w in valores_w:
        print(f"\n{'='*60}")
        print(f"Probando con w = {w}")
        print('='*60)
        E, s = SOR(x0.copy(), A, b, Tol, niter, w)
        resultados.append((w, len(E), s))
    
    # Comparación de resultados
    print("\n" + "="*60)
    print("COMPARACIÓN DE RESULTADOS CON DIFERENTES w")
    print("="*60)
    print(f"{'w':<10} {'Iteraciones':<15} {'Solución'}")
    print("-"*60)
    for w, iters, sol in resultados:
        sol_str = np.array2string(sol, precision=6, separator=', ')
        print(f"{w:<10.2f} {iters:<15} {sol_str}")
    
    # Verificación con w óptimo
    print("\n" + "="*60)
    print("VERIFICACIÓN (con w = 1.25)")
    print("="*60)
    w_optimo = 1.25
    E_opt, s_opt = SOR(x0.copy(), A, b, Tol, niter, w_optimo)
    print(f"\nA @ s = {A @ s_opt}")
    print(f"b     = {b}")
    print(f"Error absoluto: {np.linalg.norm(A @ s_opt - b)}")
