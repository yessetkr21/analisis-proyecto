"""
Script para ejecutar TU código y comparar con el profesor
"""
import numpy as np
import sys
sys.path.append('app/metodos')

# Importar TUS métodos
import capitulo3

print("="*80)
print("EJECUTANDO TU CÓDIGO - CAPÍTULO 3")
print("="*80)

# Test 1: Vandermonde
print("\n" + "="*80)
print("1. VANDERMONDE")
print("="*80)
x = np.array([-2, -1, 2, 3], dtype=float)
y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)

resultado = capitulo3.vandermonde(x, y)
coef_app = np.array(resultado['coeficientes'])
print(f"\nCoeficientes de TU APP:")
for i, c in enumerate(coef_app):
    print(f"  a[{i}] = {c:.15f}")

print(f"\nVerificación en puntos:")
errores_app = resultado['errores']
for i in range(len(x)):
    p_x = np.polyval(coef_app, x[i])
    error = errores_app[i]
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 2: Newton
print("\n" + "="*80)
print("2. NEWTON")
print("="*80)
resultado = capitulo3.newton_interpolante(x, y)
tabla_app = np.array(resultado['tabla'])
print(f"\nTabla de diferencias divididas (primeras 2 columnas):")
print(f"{'i':<5} {'x':<12} {'f(x)':<15} {'DD1':<15} {'DD2':<15}")
for i in range(len(x)):
    row = f"{i:<5} {tabla_app[i,0]:<12.6f} {tabla_app[i,1]:<15.10f}"
    if i >= 0 and tabla_app.shape[1] > 2:
        row += f" {tabla_app[i,2]:<15.10f}"
    if i >= 1 and tabla_app.shape[1] > 3:
        row += f" {tabla_app[i,3]:<15.10f}"
    print(row)

print(f"\nVerificación en puntos:")
errores_app = resultado['errores']
for i in range(len(x)):
    p_x = capitulo3.evaluar_newton(tabla_app, x[i])
    error = errores_app[i]
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 3: Lagrange
print("\n" + "="*80)
print("3. LAGRANGE")
print("="*80)
resultado = capitulo3.lagrange(x, y)
pol_app = np.array(resultado['coeficientes'])
print(f"\nCoeficientes del polinomio:")
for i, c in enumerate(pol_app):
    print(f"  p[{i}] = {c:.15f}")

print(f"\nVerificación en puntos:")
errores_app = resultado['errores']
for i in range(len(x)):
    p_x = np.polyval(pol_app, x[i])
    error = errores_app[i]
    print(f"x={x[i]:6.2f}: y_real={y[i]:15.10f}, P(x)={p_x:15.10f}, error={error:.2e}")

# Test 4: Spline Lineal
print("\n" + "="*80)
print("4. SPLINE LINEAL")
print("="*80)
x_spline = np.array([0, 1, 2, 3, 4], dtype=float)
y_spline = np.array([1, 2, 1.5, 3, 2.5], dtype=float)

resultado = capitulo3.spline_lineal(x_spline, y_spline)
tabla_spline_lin = np.array(resultado['coeficientes'])
print(f"\nCoeficientes de segmentos:")
for i in range(len(tabla_spline_lin)):
    a, b = tabla_spline_lin[i]
    print(f"Seg {i+1}: [{x_spline[i]:.1f}, {x_spline[i+1]:.1f}] -> P(x) = {a:.10f}x + {b:.10f}")

# Test 5: Spline Cúbico
print("\n" + "="*80)
print("5. SPLINE CÚBICO")
print("="*80)
resultado = capitulo3.spline_cubico(x_spline, y_spline)
tabla_spline_cub = np.array(resultado['coeficientes'])
print(f"\nCoeficientes de segmentos:")
for i in range(len(tabla_spline_cub)):
    a, b, c, d = tabla_spline_cub[i]
    print(f"Seg {i+1}: [{x_spline[i]:.1f}, {x_spline[i+1]:.1f}]")
    print(f"  -> P(x) = {a:.10f}x³ + {b:.10f}x² + {c:.10f}x + {d:.10f}")

print("\n" + "="*80)
print("TODOS LOS RESULTADOS DE TU APP CAPTURADOS")
print("="*80)
