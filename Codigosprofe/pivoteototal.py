# -*- coding: utf-8 -*-
# Eliminación Gaussiana con pivoteo total para el sistema 5x5 dado
# Imprime: x (orden interno), mark, xor (reordenado al orden original),
# E1_es = ||A*xor - b||_inf y las probabilidades como porcentaje.

import numpy as np

def gauss_piv_total(A, b, tol=1e-12):
    A = A.astype(float)
    b = b.astype(float).reshape(-1, 1)
    n = A.shape[0]
    Ab = np.hstack([A, b])
    mark = list(range(1, n+1))  # 1-based como en MATLAB

    for k in range(n-1):
        # buscar máximo en submatriz
        sub = np.abs(Ab[k:n, k:n])
        idx_flat = np.argmax(sub)
        max_r, max_c = divmod(idx_flat, sub.shape[1])
        maxrow = max_r + k
        maxcol = max_c + k

        if abs(Ab[maxrow, maxcol]) < tol:
            raise ValueError("El sistema no tiene solución única.")

        # intercambio de filas y columnas
        if maxrow != k:
            Ab[[k, maxrow], :] = Ab[[maxrow, k], :]
        if maxcol != k:
            Ab[:, [k, maxcol]] = Ab[:, [maxcol, k]]
            mark[k], mark[maxcol] = mark[maxcol], mark[k]

        # eliminación
        for i in range(k+1, n):
            M = Ab[i, k] / Ab[k, k]
            Ab[i, k:n+1] = Ab[i, k:n+1] - M * Ab[k, k:n+1]

    # sustitución regresiva
    x_int = np.zeros(n, float)
    for i in range(n-1, -1, -1):
        s = float(np.dot(Ab[i, i+1:n], x_int[i+1:n]))
        x_int[i] = (Ab[i, n] - s) / Ab[i, i]
    return x_int, mark, Ab

if __name__ == "__main__":
    # MATRIZ Y VECTOR EXACTOS DEL EJERCICIO
    A = np.array([[10, 5, 10, 15, -20],
                  [ 1,-5,  2,  3,  -4],
                  [ 6, 8, 14, 11,  -1],
                  [11, 3,  6,-20,   0],
                  [ 1, 8, -1,  0, -10]], dtype=float)
    b = np.array([10, 20, 30, 40, 50], dtype=float)

    # Resolver
    x, mark, _ = gauss_piv_total(A, b)

    # Reordenar al orden original usando 'mark' (1-based).
    xor = np.zeros_like(x)
    for i, m in enumerate(mark):
        xor[m-1] = x[i]

    # Error escalar en norma infinito
    E1_es = np.linalg.norm(A @ xor - b, ord=np.inf)

    # ---- Salidas base
    print("x =")
    print(x)
    print("\nmark =")
    print(mark)
    print("\nxor =")
    print(xor)
    print("\nE1_es =")
    print(E1_es)

    # ---- Probabilidades: |xor_i| / sum|xor|, impresas como %
    abs_xor = np.abs(xor)
    total_abs = float(np.sum(abs_xor))
    probs = abs_xor / total_abs

    print("\nProbabilidades (|xor_i| / sum|xor|):")
    for i, p in enumerate(probs, start=1):
        print(f"p(x{i}) = {p*100:.6f}%")
    print(f"Suma de probabilidades = {np.sum(probs)*100:.6f}%")
    print(f"Suma |xor| = {total_abs:.6f}")
