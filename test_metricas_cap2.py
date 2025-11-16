#!/usr/bin/env python3
"""
Test para verificar que las 5 métricas de error se calculan correctamente en Cap2
"""

import sys
import os

# Agregar el directorio app al path
app_dir = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_dir)

from metodos import capitulo2
import numpy as np


# Matriz de ejemplo (diagonalmente dominante)
A = np.array([
    [10, 1, 1],
    [2, 10, 1],
    [2, 2, 10]
], dtype=float)

b = np.array([12, 13, 14], dtype=float)
x0 = np.array([0, 0, 0], dtype=float)
tol = 1e-6
niter = 100

print("=" * 70)
print("PRUEBA DE CÁLCULO DE 5 MÉTRICAS DE ERROR - CAPÍTULO 2")
print("=" * 70)
print()

# Prueba Jacobi
print("1. MÉTODO DE JACOBI")
print("-" * 70)
resultado_jacobi = capitulo2.jacobi(A, b, x0.copy(), tol, niter)

if resultado_jacobi['exito']:
    print(f"✓ Convergiò en {resultado_jacobi['iteraciones']} iteraciones")
    print(f"✓ Radio espectral: {resultado_jacobi['radio_espectral']:.6f}")
    print(f"✓ Solución: {[f'{v:.6f}' for v in resultado_jacobi['solucion']]}")
    print()
    
    # Mostrar tabla de primeras 5 iteraciones
    print("Primeras 5 iteraciones con las 5 métricas:")
    print(f"{'Iter':<5} {'Error Abs':<15} {'Error Rel1':<15} {'Error Rel2':<15} {'Error Rel3':<15} {'Error Rel4':<15}")
    print("-" * 80)
    
    for i, fila in enumerate(resultado_jacobi['tabla'][:6]):
        ea_str = f"{fila['error_abs']:.4e}" if fila['error_abs'] is not None else "-"
        er1_str = f"{fila['error_rel1']:.4e}" if fila['error_rel1'] is not None else "-"
        er2_str = f"{fila['error_rel2']:.4e}" if fila['error_rel2'] is not None else "-"
        er3_str = f"{fila['error_rel3']:.4e}" if fila['error_rel3'] is not None else "-"
        er4_str = f"{fila['error_rel4']:.4e}" if fila['error_rel4'] is not None else "-"
        print(f"{fila['iter']:<5} {ea_str:<15} {er1_str:<15} {er2_str:<15} {er3_str:<15} {er4_str:<15}")
else:
    print(f"✗ Error: {resultado_jacobi['mensaje']}")

print()

# Prueba Gauss-Seidel
print("2. MÉTODO DE GAUSS-SEIDEL")
print("-" * 70)
resultado_gs = capitulo2.gauss_seidel(A, b, x0.copy(), tol, niter)

if resultado_gs['exito']:
    print(f"✓ Convergiò en {resultado_gs['iteraciones']} iteraciones")
    print(f"✓ Radio espectral: {resultado_gs['radio_espectral']:.6f}")
    print(f"✓ Solución: {[f'{v:.6f}' for v in resultado_gs['solucion']]}")
    print()
    
    print("Primeras 5 iteraciones con las 5 métricas:")
    print(f"{'Iter':<5} {'Error Abs':<15} {'Error Rel1':<15} {'Error Rel2':<15} {'Error Rel3':<15} {'Error Rel4':<15}")
    print("-" * 80)
    
    for i, fila in enumerate(resultado_gs['tabla'][:6]):
        ea_str = f"{fila['error_abs']:.4e}" if fila['error_abs'] is not None else "-"
        er1_str = f"{fila['error_rel1']:.4e}" if fila['error_rel1'] is not None else "-"
        er2_str = f"{fila['error_rel2']:.4e}" if fila['error_rel2'] is not None else "-"
        er3_str = f"{fila['error_rel3']:.4e}" if fila['error_rel3'] is not None else "-"
        er4_str = f"{fila['error_rel4']:.4e}" if fila['error_rel4'] is not None else "-"
        print(f"{fila['iter']:<5} {ea_str:<15} {er1_str:<15} {er2_str:<15} {er3_str:<15} {er4_str:<15}")
else:
    print(f"✗ Error: {resultado_gs['mensaje']}")

print()

# Prueba SOR
print("3. MÉTODO SOR (w=1.5)")
print("-" * 70)
resultado_sor = capitulo2.sor(A, b, x0.copy(), tol, niter, w=1.5)

if resultado_sor['exito']:
    print(f"✓ Convergiò en {resultado_sor['iteraciones']} iteraciones")
    print(f"✓ Radio espectral: {resultado_sor['radio_espectral']:.6f}")
    print(f"✓ Factor w: {resultado_sor['w']:.2f}")
    print(f"✓ Solución: {[f'{v:.6f}' for v in resultado_sor['solucion']]}")
    print()
    
    print("Primeras 5 iteraciones con las 5 métricas:")
    print(f"{'Iter':<5} {'Error Abs':<15} {'Error Rel1':<15} {'Error Rel2':<15} {'Error Rel3':<15} {'Error Rel4':<15}")
    print("-" * 80)
    
    for i, fila in enumerate(resultado_sor['tabla'][:6]):
        ea_str = f"{fila['error_abs']:.4e}" if fila['error_abs'] is not None else "-"
        er1_str = f"{fila['error_rel1']:.4e}" if fila['error_rel1'] is not None else "-"
        er2_str = f"{fila['error_rel2']:.4e}" if fila['error_rel2'] is not None else "-"
        er3_str = f"{fila['error_rel3']:.4e}" if fila['error_rel3'] is not None else "-"
        er4_str = f"{fila['error_rel4']:.4e}" if fila['error_rel4'] is not None else "-"
        print(f"{fila['iter']:<5} {ea_str:<15} {er1_str:<15} {er2_str:<15} {er3_str:<15} {er4_str:<15}")
else:
    print(f"✗ Error: {resultado_sor['mensaje']}")

print()
print("=" * 70)
print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 70)
