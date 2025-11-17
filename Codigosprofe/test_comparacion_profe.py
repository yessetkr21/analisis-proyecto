"""
Test de comparación entre los códigos del profesor y la aplicación web
Este script verifica que los resultados sean idénticos
"""

import numpy as np
import sys
import os

# Agregar rutas
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'metodos'))
sys.path.append(os.path.dirname(__file__))

# Importar métodos de tu app
import capitulo2

# Importar métodos del profesor
from jacobi import MatJacobiSeid
from seidel import MatGaussSeidel
from sor import SOR


def comparar_arrays(arr1, arr2, nombre="Arrays", tolerancia=1e-10):
    """Compara dos arrays numpy y reporta diferencias"""
    if isinstance(arr1, list):
        arr1 = np.array(arr1)
    if isinstance(arr2, list):
        arr2 = np.array(arr2)

    diferencia = np.linalg.norm(arr1 - arr2)

    if diferencia < tolerancia:
        print(f"[OK] {nombre}: IGUALES (diferencia: {diferencia:.2e})")
        return True
    else:
        print(f"[ERROR] {nombre}: DIFERENTES (diferencia: {diferencia:.2e})")
        print(f"   Profesor: {arr1}")
        print(f"   Tu app:   {arr2}")
        return False


def test_jacobi():
    """Prueba el método de Jacobi"""
    print("\n" + "="*70)
    print("TEST 1: MÉTODO DE JACOBI")
    print("="*70)

    # Sistema de ecuaciones del ejemplo del profesor
    A = np.array([[10.0, 1.0, 1.0],
                  [2.0, 10.0, 1.0],
                  [2.0, 2.0, 10.0]])

    b = np.array([12.0, 13.0, 14.0])
    x0 = np.array([0.0, 0.0, 0.0])
    Tol = 1e-6
    niter = 100

    print(f"\nSistema de ecuaciones:")
    print(f"Matriz A:\n{A}")
    print(f"Vector b: {b}")
    print(f"x0: {x0}")
    print(f"Tolerancia: {Tol}")
    print(f"Iteraciones máximas: {niter}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    E_prof, s_prof = MatJacobiSeid(x0.copy(), A, b, Tol, niter, met=0)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo2.jacobi(A, b, x0.copy(), Tol, niter)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar número de iteraciones
    iter_prof = len(E_prof)
    iter_app = resultado_app['iteraciones']
    if iter_prof == iter_app:
        print(f"[OK] Iteraciones: IGUALES ({iter_prof})")
    else:
        print(f"[ERROR] Iteraciones: DIFERENTES (Profesor: {iter_prof}, Tu app: {iter_app})")
        todos_correctos = False

    # Comparar solución
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], "Solución final")

    # Comparar errores
    errores_prof = list(E_prof)
    errores_app = resultado_app['errores']
    todos_correctos &= comparar_arrays(errores_prof, errores_app, "Errores por iteración")

    # Verificación final
    print("\n" + "-"*70)
    print("VERIFICACIÓN: A @ solución = b")
    print("-"*70)
    verificacion_prof = A @ s_prof
    verificacion_app = A @ np.array(resultado_app['solucion'])
    comparar_arrays(verificacion_prof, b, "Profesor (A@s vs b)")
    comparar_arrays(verificacion_app, b, "Tu app (A@s vs b)")

    return todos_correctos


def test_gauss_seidel():
    """Prueba el método de Gauss-Seidel"""
    print("\n" + "="*70)
    print("TEST 2: MÉTODO DE GAUSS-SEIDEL")
    print("="*70)

    # Sistema de ecuaciones del ejemplo del profesor
    A = np.array([[10.0, 1.0, 1.0],
                  [2.0, 10.0, 1.0],
                  [2.0, 2.0, 10.0]])

    b = np.array([12.0, 13.0, 14.0])
    x0 = np.array([0.0, 0.0, 0.0])
    Tol = 1e-6
    niter = 100

    print(f"\nSistema de ecuaciones:")
    print(f"Matriz A:\n{A}")
    print(f"Vector b: {b}")
    print(f"x0: {x0}")
    print(f"Tolerancia: {Tol}")
    print(f"Iteraciones máximas: {niter}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    E_prof, s_prof = MatGaussSeidel(x0.copy(), A, b, Tol, niter)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo2.gauss_seidel(A, b, x0.copy(), Tol, niter)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar número de iteraciones
    iter_prof = len(E_prof)
    iter_app = resultado_app['iteraciones']
    if iter_prof == iter_app:
        print(f"[OK] Iteraciones: IGUALES ({iter_prof})")
    else:
        print(f"[ERROR] Iteraciones: DIFERENTES (Profesor: {iter_prof}, Tu app: {iter_app})")
        todos_correctos = False

    # Comparar solución
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], "Solución final")

    # Comparar errores
    errores_prof = list(E_prof)
    errores_app = resultado_app['errores']
    todos_correctos &= comparar_arrays(errores_prof, errores_app, "Errores por iteración")

    # Verificación final
    print("\n" + "-"*70)
    print("VERIFICACIÓN: A @ solución = b")
    print("-"*70)
    verificacion_prof = A @ s_prof
    verificacion_app = A @ np.array(resultado_app['solucion'])
    comparar_arrays(verificacion_prof, b, "Profesor (A@s vs b)")
    comparar_arrays(verificacion_app, b, "Tu app (A@s vs b)")

    return todos_correctos


def test_sor():
    """Prueba el método SOR"""
    print("\n" + "="*70)
    print("TEST 3: MÉTODO SOR")
    print("="*70)

    # Sistema de ecuaciones del ejemplo del profesor
    A = np.array([[10.0, 1.0, 1.0],
                  [2.0, 10.0, 1.0],
                  [2.0, 2.0, 10.0]])

    b = np.array([12.0, 13.0, 14.0])
    x0 = np.array([0.0, 0.0, 0.0])
    Tol = 1e-6
    niter = 100
    w = 1.25

    print(f"\nSistema de ecuaciones:")
    print(f"Matriz A:\n{A}")
    print(f"Vector b: {b}")
    print(f"x0: {x0}")
    print(f"Tolerancia: {Tol}")
    print(f"Iteraciones máximas: {niter}")
    print(f"Factor de relajación w: {w}")

    # Ejecutar método del profesor
    print("\n--- Ejecutando método del PROFESOR ---")
    E_prof, s_prof = SOR(x0.copy(), A, b, Tol, niter, w)

    # Ejecutar método de tu app
    print("\n--- Ejecutando método de TU APP ---")
    resultado_app = capitulo2.sor(A, b, x0.copy(), Tol, niter, w)

    # Comparar resultados
    print("\n" + "-"*70)
    print("COMPARACIÓN DE RESULTADOS")
    print("-"*70)

    todos_correctos = True

    # Comparar número de iteraciones
    iter_prof = len(E_prof)
    iter_app = resultado_app['iteraciones']
    if iter_prof == iter_app:
        print(f"[OK] Iteraciones: IGUALES ({iter_prof})")
    else:
        print(f"[ERROR] Iteraciones: DIFERENTES (Profesor: {iter_prof}, Tu app: {iter_app})")
        todos_correctos = False

    # Comparar solución
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], "Solución final")

    # Comparar errores
    errores_prof = list(E_prof)
    errores_app = resultado_app['errores']
    todos_correctos &= comparar_arrays(errores_prof, errores_app, "Errores por iteración")

    # Verificación final
    print("\n" + "-"*70)
    print("VERIFICACIÓN: A @ solución = b")
    print("-"*70)
    verificacion_prof = A @ s_prof
    verificacion_app = A @ np.array(resultado_app['solucion'])
    comparar_arrays(verificacion_prof, b, "Profesor (A@s vs b)")
    comparar_arrays(verificacion_app, b, "Tu app (A@s vs b)")

    return todos_correctos


def test_caso_adicional():
    """Prueba con un sistema diferente para asegurar robustez"""
    print("\n" + "="*70)
    print("TEST 4: CASO ADICIONAL (Sistema 4x4)")
    print("="*70)

    # Sistema más grande
    A = np.array([[4.0, -1.0, 0.0, 0.0],
                  [-1.0, 4.0, -1.0, 0.0],
                  [0.0, -1.0, 4.0, -1.0],
                  [0.0, 0.0, -1.0, 4.0]])

    b = np.array([15.0, 10.0, 10.0, 10.0])
    x0 = np.array([0.0, 0.0, 0.0, 0.0])
    Tol = 1e-6
    niter = 100

    print(f"\nSistema 4x4")
    print(f"Matriz A:\n{A}")
    print(f"Vector b: {b}")

    todos_correctos = True

    # Test Jacobi
    print("\n--- JACOBI ---")
    E_prof, s_prof = MatJacobiSeid(x0.copy(), A, b, Tol, niter, met=0)
    resultado_app = capitulo2.jacobi(A, b, x0.copy(), Tol, niter)
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], "Jacobi 4x4")

    # Test Gauss-Seidel
    print("\n--- GAUSS-SEIDEL ---")
    E_prof, s_prof = MatJacobiSeid(x0.copy(), A, b, Tol, niter, met=1)
    resultado_app = capitulo2.gauss_seidel(A, b, x0.copy(), Tol, niter)
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], "Gauss-Seidel 4x4")

    # Test SOR
    print("\n--- SOR ---")
    w = 1.1
    E_prof, s_prof = SOR(x0.copy(), A, b, Tol, niter, w)
    resultado_app = capitulo2.sor(A, b, x0.copy(), Tol, niter, w)
    todos_correctos &= comparar_arrays(s_prof, resultado_app['solucion'], f"SOR 4x4 (w={w})")

    return todos_correctos


if __name__ == "__main__":
    print("\n")
    print("="*70)
    print(" "*20 + "TESTS DE COMPARACION")
    print(" "*15 + "Codigo del Profesor vs Tu App")
    print("="*70)

    resultados = []

    # Ejecutar todos los tests
    resultados.append(("Jacobi", test_jacobi()))
    resultados.append(("Gauss-Seidel", test_gauss_seidel()))
    resultados.append(("SOR", test_sor()))
    resultados.append(("Caso adicional 4x4", test_caso_adicional()))

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
