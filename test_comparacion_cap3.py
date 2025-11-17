"""
Test de comparación entre los códigos del profesor y la aplicación web - Capítulo 3
Este script verifica que los resultados de interpolación sean idénticos
"""

import numpy as np
import sys
import os

# Agregar rutas
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'metodos'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Codigosprofe'))

# Importar métodos de tu app
import capitulo3

# Importar métodos del profesor
from vandermorde import vandermonde_interpolacion, evaluar_polinomio_vandermonde
from newtoninter import Newtonint, evaluar_newton
from lagrange import Lagrange
from splinelineal import SplineLineal
from splinecubico import SplineCubico


def comparar_arrays(arr1, arr2, nombre="Arrays", tolerancia=1e-10):
    """Compara dos arrays numpy y reporta diferencias"""
    if isinstance(arr1, list):
        arr1 = np.array(arr1)
    if isinstance(arr2, list):
        arr2 = np.array(arr2)

    # Asegurar que tienen la misma forma
    if arr1.shape != arr2.shape:
        print(f"[ERROR] {nombre}: DIMENSIONES DIFERENTES (Profesor: {arr1.shape}, Tu app: {arr2.shape})")
        return False

    diferencia = np.linalg.norm(arr1 - arr2)

    if diferencia < tolerancia:
        print(f"[OK] {nombre}: IGUALES (diferencia: {diferencia:.2e})")
        return True
    else:
        print(f"[ERROR] {nombre}: DIFERENTES (diferencia: {diferencia:.2e})")
        print(f"   Profesor: {arr1}")
        print(f"   Tu app:   {arr2}")
        return False


def test_vandermonde():
    """Prueba el método de Vandermonde"""
    print("\n" + "="*70)
    print("TEST 1: MÉTODO DE VANDERMONDE")
    print("="*70)

    # Puntos de ejemplo
    x = np.array([-2, -1, 2, 3], dtype=float)
    y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)

    print(f"\nPuntos de interpolación:")
    print(f"x: {x}")
    print(f"y: {y}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    coef_prof, matriz_prof = vandermonde_interpolacion(x, y)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo3.vandermonde(x, y)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar coeficientes
    coef_app = np.array(resultado_app['coeficientes'])
    todos_correctos &= comparar_arrays(coef_prof, coef_app, "Coeficientes del polinomio")

    # Comparar matriz de Vandermonde
    matriz_app = np.array(resultado_app['matriz_vandermonde'])
    todos_correctos &= comparar_arrays(matriz_prof, matriz_app, "Matriz de Vandermonde")

    # Verificar en puntos originales
    print("\n" + "-"*70)
    print("VERIFICACIÓN: Evaluar en puntos originales")
    print("-"*70)
    for i in range(len(x)):
        p_prof = evaluar_polinomio_vandermonde(coef_prof, x[i])
        p_app = np.polyval(coef_app, x[i])
        error_prof = abs(y[i] - p_prof)
        error_app = abs(y[i] - p_app)
        print(f"x[{i}] = {x[i]:6.2f}: P(x) = {p_app:12.6f}, y = {y[i]:12.6f}, error = {error_app:.2e}")

    return todos_correctos


def test_newton():
    """Prueba el método de Newton"""
    print("\n" + "="*70)
    print("TEST 2: MÉTODO DE NEWTON")
    print("="*70)

    # Puntos de ejemplo
    x = np.array([-2, -1, 2, 3], dtype=float)
    y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)

    print(f"\nPuntos de interpolación:")
    print(f"x: {x}")
    print(f"y: {y}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    tabla_prof = Newtonint(x, y)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo3.newton_interpolante(x, y)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar tabla de diferencias divididas
    tabla_app = np.array(resultado_app['tabla'])
    todos_correctos &= comparar_arrays(tabla_prof, tabla_app, "Tabla de diferencias divididas")

    # Verificar en puntos originales
    print("\n" + "-"*70)
    print("VERIFICACIÓN: Evaluar en puntos originales")
    print("-"*70)
    for i in range(len(x)):
        p_prof = evaluar_newton(tabla_prof, x[i])
        p_app = evaluar_newton(tabla_app, x[i])
        error = abs(p_prof - p_app)
        print(f"x[{i}] = {x[i]:6.2f}: P_prof(x) = {p_prof:12.6f}, P_app(x) = {p_app:12.6f}, diff = {error:.2e}")

    return todos_correctos


def test_lagrange():
    """Prueba el método de Lagrange"""
    print("\n" + "="*70)
    print("TEST 3: MÉTODO DE LAGRANGE")
    print("="*70)

    # Puntos de ejemplo
    x = np.array([-2, -1, 2, 3], dtype=float)
    y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)

    print(f"\nPuntos de interpolación:")
    print(f"x: {x}")
    print(f"y: {y}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    pol_prof = Lagrange(x, y)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo3.lagrange(x, y)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar coeficientes
    pol_app = np.array(resultado_app['coeficientes'])
    todos_correctos &= comparar_arrays(pol_prof, pol_app, "Coeficientes del polinomio")

    # Verificar en puntos originales
    print("\n" + "-"*70)
    print("VERIFICACIÓN: Evaluar en puntos originales")
    print("-"*70)
    for i in range(len(x)):
        p_prof = np.polyval(pol_prof, x[i])
        p_app = np.polyval(pol_app, x[i])
        error = abs(y[i] - p_app)
        print(f"x[{i}] = {x[i]:6.2f}: P(x) = {p_app:12.6f}, y = {y[i]:12.6f}, error = {error:.2e}")

    return todos_correctos


def test_spline_lineal():
    """Prueba el método de Spline Lineal"""
    print("\n" + "="*70)
    print("TEST 4: SPLINE LINEAL")
    print("="*70)

    # Puntos de ejemplo
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1, 2, 1.5, 3, 2.5], dtype=float)

    print(f"\nPuntos de interpolación:")
    print(f"x: {x}")
    print(f"y: {y}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    tabla_prof = SplineLineal(x, y)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo3.spline_lineal(x, y)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar coeficientes
    tabla_app = np.array(resultado_app['coeficientes'])
    todos_correctos &= comparar_arrays(tabla_prof, tabla_app, "Coeficientes del spline")

    # Mostrar segmentos
    print("\n" + "-"*70)
    print("SEGMENTOS DEL SPLINE")
    print("-"*70)
    for i, seg in enumerate(resultado_app['segmentos']):
        print(f"Segmento {i+1}: {seg['intervalo']} -> {seg['polinomio']}")

    return todos_correctos


def test_spline_cubico():
    """Prueba el método de Spline Cúbico"""
    print("\n" + "="*70)
    print("TEST 5: SPLINE CÚBICO")
    print("="*70)

    # Puntos de ejemplo
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1, 2, 1.5, 3, 2.5], dtype=float)

    print(f"\nPuntos de interpolación:")
    print(f"x: {x}")
    print(f"y: {y}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    tabla_prof = SplineCubico(x, y)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo3.spline_cubico(x, y)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar coeficientes
    tabla_app = np.array(resultado_app['coeficientes'])
    todos_correctos &= comparar_arrays(tabla_prof, tabla_app, "Coeficientes del spline")

    # Mostrar segmentos
    print("\n" + "-"*70)
    print("SEGMENTOS DEL SPLINE CÚBICO")
    print("-"*70)
    for i, seg in enumerate(resultado_app['segmentos']):
        print(f"Segmento {i+1}: {seg['intervalo']} -> {seg['polinomio']}")

    return todos_correctos


if __name__ == "__main__":
    print("\n")
    print("="*70)
    print(" "*15 + "TESTS DE COMPARACION - CAPITULO 3")
    print(" "*15 + "Codigo del Profesor vs Tu App")
    print("="*70)

    resultados = []

    # Ejecutar todos los tests
    resultados.append(("Vandermonde", test_vandermonde()))
    resultados.append(("Newton", test_newton()))
    resultados.append(("Lagrange", test_lagrange()))
    resultados.append(("Spline Lineal", test_spline_lineal()))
    resultados.append(("Spline Cúbico", test_spline_cubico()))

    # Resumen final
    print("\n")
    print("="*70)
    print(" "*24 + "RESUMEN FINAL")
    print("="*70)

    for nombre, resultado in resultados:
        estado = "[PASO]" if resultado else "[FALLO]"
        print(f"{estado:12} - {nombre}")

    todos_pasaron = all(r[1] for r in resultados)

    print("\n" + "="*70)
    if todos_pasaron:
        print("TODOS LOS TESTS PASARON!")
        print("Tu aplicacion produce los mismos resultados que el codigo del profesor")
    else:
        print("ALGUNOS TESTS FALLARON")
        print("Revisa las diferencias reportadas arriba")
    print("="*70 + "\n")

    sys.exit(0 if todos_pasaron else 1)
