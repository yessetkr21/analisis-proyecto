"""
Script para ejecutar código del profesor directamente y comparar
"""
import numpy as np
import sys
sys.path.append('Codigosprofe')

# Importar métodos del profesor
from vandermorde import vandermonde_interpolacion, evaluar_polinomio_vandermonde
from newtoninter import Newtonint, evaluar_newton
from lagrange import Lagrange
from splinelineal import SplineLineal
from splinecubico import SplineCubico

print("="*80)
print("EJECUTANDO CÓDIGO DEL PROFESOR - CAPÍTULO 3")
print("="*80)

# Test 1: Vandermonde
print("\n" + "="*80)
print("1. VANDERMONDE")
print("="*80)
x = np.array([-2, -1, 2, 3], dtype=float)
y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)

coef_prof, matriz_prof = vandermonde_interpolacion(x, y)
print(f"\nCoeficientes del profesor:")
for i, c in enumerate(coef_prof):
    print(f"  a[{i}] = {c:.15f}")

print(f"\nVerificación en puntos:")
for i in range(len(x)):
    p_x = evaluar_polinomio_vandermonde(coef_prof, x[i])
    error = abs(y[i] - p_x)
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 2: Newton
print("\n" + "="*80)
print("2. NEWTON")
print("="*80)
tabla_prof = Newtonint(x, y)
print(f"\nTabla de diferencias divididas (primeras 2 columnas):")
print(f"{'i':<5} {'x':<12} {'f(x)':<15} {'DD1':<15} {'DD2':<15}")
for i in range(len(x)):
    row = f"{i:<5} {tabla_prof[i,0]:<12.6f} {tabla_prof[i,1]:<15.10f}"
    if i >= 0 and tabla_prof.shape[1] > 2:
        row += f" {tabla_prof[i,2]:<15.10f}"
    if i >= 1 and tabla_prof.shape[1] > 3:
        row += f" {tabla_prof[i,3]:<15.10f}"
    print(row)

print(f"\nVerificación en puntos:")
for i in range(len(x)):
    p_x = evaluar_newton(tabla_prof, x[i])
    error = abs(y[i] - p_x)
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 3: Lagrange
print("\n" + "="*80)
print("3. LAGRANGE")
print("="*80)
pol_prof = Lagrange(x, y)
print(f"\nCoeficientes del polinomio:")
for i, c in enumerate(pol_prof):
    print(f"  p[{i}] = {c:.15f}")

print(f"\nVerificación en puntos:")
for i in range(len(x)):
    p_x = np.polyval(pol_prof, x[i])
    error = abs(y[i] - p_x)
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 4: Spline Lineal
print("\n" + "="*80)
print("4. SPLINE LINEAL")
print("="*80)
x_spline = np.array([0, 1, 2, 3, 4], dtype=float)
y_spline = np.array([1, 2, 1.5, 3, 2.5], dtype=float)

tabla_spline_lin = SplineLineal(x_spline, y_spline)
print(f"\nCoeficientes de segmentos:")
for i in range(len(tabla_spline_lin)):
    a, b = tabla_spline_lin[i]
    print(f"Seg {i+1}: [{x_spline[i]:.1f}, {x_spline[i+1]:.1f}] -> P(x) = {a:.10f}x + {b:.10f}")

# Test 5: Spline Cúbico
print("\n" + "="*80)
print("5. SPLINE CÚBICO")
print("="*80)
tabla_spline_cub = SplineCubico(x_spline, y_spline)
print(f"\nCoeficientes de segmentos:")
for i in range(len(tabla_spline_cub)):
    a, b, c, d = tabla_spline_cub[i]
    print(f"Seg {i+1}: [{x_spline[i]:.1f}, {x_spline[i+1]:.1f}]")
    print(f"  -> P(x) = {a:.10f}x³ + {b:.10f}x² + {c:.10f}x + {d:.10f}")

print("\n" + "="*80)
print("TODOS LOS RESULTADOS DEL PROFESOR CAPTURADOS")
print("="*80)
