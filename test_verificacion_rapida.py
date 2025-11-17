"""
Script rápido para verificar que nuestro código produce los mismos resultados
que el código del profesor
"""

import numpy as np
import sys
sys.path.append('app/metodos')

import capitulo2

# Sistema de ecuaciones del profesor
A = np.array([[10.0, 1.0, 1.0],
              [2.0, 10.0, 1.0],
              [2.0, 2.0, 10.0]])

b = np.array([12.0, 13.0, 14.0])
x0 = np.array([0.0, 0.0, 0.0])
Tol = 1e-6
niter = 100

print("="*70)
print(" "*20 + "VERIFICACIÓN RÁPIDA")
print("="*70)

# Test Jacobi
print("\n--- JACOBI ---")
res_jacobi = capitulo2.jacobi(A, b, x0.copy(), Tol, niter)
print(f"Iteraciones: {res_jacobi['iteraciones']}")
print(f"Solución: {res_jacobi['solucion']}")
print(f"Errores: {res_jacobi['errores']}")

# Test Gauss-Seidel
print("\n--- GAUSS-SEIDEL ---")
res_seidel = capitulo2.gauss_seidel(A, b, x0.copy(), Tol, niter)
print(f"Iteraciones: {res_seidel['iteraciones']}")
print(f"Solución: {res_seidel['solucion']}")
print(f"Errores: {res_seidel['errores']}")

# Test SOR
print("\n--- SOR (w=1.25) ---")
res_sor = capitulo2.sor(A, b, x0.copy(), Tol, niter, 1.25)
print(f"Iteraciones: {res_sor['iteraciones']}")
print(f"Solución: {res_sor['solucion']}")
print(f"Errores: {res_sor['errores']}")

print("\n" + "="*70)
print("COMPARACIÓN CON RESULTADOS DEL PROFESOR:")
print("="*70)
print("Jacobi:")
print(f"  Esperado: 13 iteraciones, [1.00000007, 1.00000008, 1.0000001]")
print(f"  Obtenido: {res_jacobi['iteraciones']} iteraciones, {res_jacobi['solucion']}")
print("\nGauss-Seidel:")
print(f"  Esperado: 6 iteraciones, [1.00000002, 0.99999998, 1.0]")
print(f"  Obtenido: {res_seidel['iteraciones']} iteraciones, {res_seidel['solucion']}")
print("\nSOR (w=1.25):")
print(f"  Esperado: 12 iteraciones, [0.99999983, 0.99999988, 1.00000003]")
print(f"  Obtenido: {res_sor['iteraciones']} iteraciones, {res_sor['solucion']}")
print("="*70)
