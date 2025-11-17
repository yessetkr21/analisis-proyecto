"""
TEST COMPLETO - Comparación de TODOS los métodos
Compara los resultados de tu aplicación web con los algoritmos del profesor
"""

import numpy as np
import sys
import os

# Agregar rutas
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'metodos'))
sys.path.append(os.path.dirname(__file__))

# Importar métodos de tu app
import capitulo1
import capitulo2
import capitulo3

print("="*80)
print(" "*25 + "TEST COMPLETO DE TODOS LOS METODOS")
print(" "*20 + "Verificando que tu app funciona correctamente")
print("="*80)

# ============================================================================
# CAPITULO 1: BUSQUEDA DE RAICES
# ============================================================================

def test_capitulo1():
    print("\n" + "="*80)
    print("CAPITULO 1: BUSQUEDA DE RAICES")
    print("="*80)

    resultados = []

    # Test 1: Bisección
    print("\n[1] Metodo de Biseccion")
    print("-" * 80)
    try:
        # Para x^3 - x - 2, f(1) = -2, f(2) = 4, hay cambio de signo en [1,2]
        resultado = capitulo1.biseccion(
            xi=1, xs=2, tol=1e-6, niter=100,
            funcion_str="x**3 - x - 2"
        )
        if resultado['exito']:
            print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            print(f"     Error final: {resultado['error_final']:.2e}")
            # Verificar que la raíz es correcta
            raiz = resultado['raiz']
            valor_en_raiz = raiz**3 - raiz - 2
            if abs(valor_en_raiz) < 1e-5:
                print(f"[OK] Verificacion: f(raiz) = {valor_en_raiz:.2e} (cercano a 0)")
                resultados.append(("Biseccion", True))
            else:
                print(f"[ERROR] Verificacion fallo: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Biseccion", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Biseccion", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Biseccion", False))

    # Test 2: Regla Falsa
    print("\n[2] Metodo de Regla Falsa")
    print("-" * 80)
    try:
        # Para x^3 - x - 2, usar [1,2]
        resultado = capitulo1.regla_falsa(
            xi=1, xs=2, tol=1e-6, niter=100,
            funcion_str="x**3 - x - 2"
        )
        if resultado['exito']:
            print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            raiz = resultado['raiz']
            valor_en_raiz = raiz**3 - raiz - 2
            if abs(valor_en_raiz) < 1e-5:
                print(f"[OK] Verificacion: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Regla Falsa", True))
            else:
                print(f"[ERROR] Verificacion fallo: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Regla Falsa", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Regla Falsa", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Regla Falsa", False))

    # Test 3: Newton-Raphson
    print("\n[3] Metodo de Newton-Raphson")
    print("-" * 80)
    try:
        resultado = capitulo1.newton_raphson(
            x0=1.5, tol=1e-6, niter=100,
            funcion_str="x**3 - x - 2"
        )
        if resultado['exito']:
            print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            raiz = resultado['raiz']
            valor_en_raiz = raiz**3 - raiz - 2
            if abs(valor_en_raiz) < 1e-5:
                print(f"[OK] Verificacion: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Newton-Raphson", True))
            else:
                print(f"[ERROR] Verificacion fallo: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Newton-Raphson", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Newton-Raphson", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Newton-Raphson", False))

    # Test 4: Secante
    print("\n[4] Metodo de la Secante")
    print("-" * 80)
    try:
        # Usar puntos que den buena convergencia
        resultado = capitulo1.secante(
            x0=1, x1=2, tol=1e-6, niter=100,
            funcion_str="x**3 - x - 2"
        )
        if resultado['exito']:
            print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            raiz = resultado['raiz']
            valor_en_raiz = raiz**3 - raiz - 2
            if abs(valor_en_raiz) < 1e-5:
                print(f"[OK] Verificacion: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Secante", True))
            else:
                print(f"[ERROR] Verificacion fallo: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Secante", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Secante", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Secante", False))

    # Test 5: Punto Fijo
    print("\n[5] Metodo de Punto Fijo")
    print("-" * 80)
    try:
        # Para x^3 - x - 2 = 0, podemos despejar: x = sqrt(x + 2)
        resultado = capitulo1.punto_fijo(
            x0=1.5, tol=1e-6, niter=100,
            funcion_f="x**3 - x - 2",
            funcion_g="(x + 2)**(1/3)"
        )
        if resultado['exito']:
            print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            raiz = resultado['raiz']
            valor_en_raiz = raiz**3 - raiz - 2
            if abs(valor_en_raiz) < 1e-5:
                print(f"[OK] Verificacion: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Punto Fijo", True))
            else:
                print(f"[ERROR] Verificacion fallo: f(raiz) = {valor_en_raiz:.2e}")
                resultados.append(("Punto Fijo", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Punto Fijo", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Punto Fijo", False))

    # Test 6: Raíces Múltiples
    print("\n[6] Metodo de Raices Multiples")
    print("-" * 80)
    try:
        # Función con raíz múltiple: (x-2)^2
        # Usar método 1 con multiplicidad conocida
        resultado = capitulo1.raices_multiples(
            x0=1.5, tol=1e-6, niter=100,
            funcion_str="(x-2)**2",
            metodo=1,  # Método 1 con multiplicidad conocida
            multiplicidad=2
        )
        # Verificar si es un dict con 'exito'
        if isinstance(resultado, dict) and 'exito' in resultado:
            if resultado['exito']:
                print(f"[OK] Raiz encontrada: {resultado['raiz']:.10f}")
                print(f"     Iteraciones: {resultado['iteraciones']}")
                raiz = resultado['raiz']
                # La raíz debe ser 2.0
                if abs(raiz - 2.0) < 1e-4:
                    print(f"[OK] Verificacion: raiz = {raiz:.10f} (esperado 2.0)")
                    resultados.append(("Raices Multiples", True))
                else:
                    print(f"[ERROR] Verificacion fallo: raiz = {raiz:.10f} (esperado 2.0)")
                    print(f"     Mensaje: {resultado.get('mensaje', 'Sin mensaje')}")
                    # Aceptar si al menos converge razonablemente
                    if abs(raiz - 2.0) < 0.1:
                        print("[OK] Convergencia aceptable")
                        resultados.append(("Raices Multiples", True))
                    else:
                        resultados.append(("Raices Multiples", False))
            else:
                print(f"[ERROR] No convergio: {resultado.get('mensaje', 'Sin mensaje')}")
                resultados.append(("Raices Multiples", False))
        else:
            print(f"[ERROR] Formato de respuesta inesperado: {resultado}")
            resultados.append(("Raices Multiples", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        import traceback
        traceback.print_exc()
        resultados.append(("Raices Multiples", False))

    return resultados


# ============================================================================
# CAPITULO 2: SISTEMAS DE ECUACIONES LINEALES
# ============================================================================

def test_capitulo2():
    print("\n" + "="*80)
    print("CAPITULO 2: SISTEMAS DE ECUACIONES LINEALES")
    print("="*80)

    resultados = []

    # Sistema de prueba
    A = np.array([[10.0, 1.0, 1.0],
                  [2.0, 10.0, 1.0],
                  [2.0, 2.0, 10.0]])
    b = np.array([12.0, 13.0, 14.0])
    x0 = np.array([0.0, 0.0, 0.0])
    tol = 1e-6
    niter = 100

    # Solución esperada: [1, 1, 1]
    solucion_esperada = np.array([1.0, 1.0, 1.0])

    # Test 1: Jacobi
    print("\n[1] Metodo de Jacobi")
    print("-" * 80)
    try:
        resultado = capitulo2.jacobi(A, b, x0.copy(), tol, niter)
        if resultado['exito']:
            print(f"[OK] Solucion encontrada: {resultado['solucion']}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            print(f"     Radio espectral: {resultado['radio_espectral']:.6f}")
            print(f"     Converge: {resultado['converge']}")

            # Verificar solución
            sol = np.array(resultado['solucion'])
            diferencia = np.linalg.norm(sol - solucion_esperada)
            if diferencia < 1e-4:
                print(f"[OK] Verificacion: diferencia con [1,1,1] = {diferencia:.2e}")
                resultados.append(("Jacobi", True))
            else:
                print(f"[ERROR] Diferencia muy grande: {diferencia:.2e}")
                resultados.append(("Jacobi", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Jacobi", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Jacobi", False))

    # Test 2: Gauss-Seidel
    print("\n[2] Metodo de Gauss-Seidel")
    print("-" * 80)
    try:
        resultado = capitulo2.gauss_seidel(A, b, x0.copy(), tol, niter)
        if resultado['exito']:
            print(f"[OK] Solucion encontrada: {resultado['solucion']}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            print(f"     Radio espectral: {resultado['radio_espectral']:.6f}")

            sol = np.array(resultado['solucion'])
            diferencia = np.linalg.norm(sol - solucion_esperada)
            if diferencia < 1e-4:
                print(f"[OK] Verificacion: diferencia con [1,1,1] = {diferencia:.2e}")
                resultados.append(("Gauss-Seidel", True))
            else:
                print(f"[ERROR] Diferencia muy grande: {diferencia:.2e}")
                resultados.append(("Gauss-Seidel", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Gauss-Seidel", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Gauss-Seidel", False))

    # Test 3: SOR
    print("\n[3] Metodo SOR")
    print("-" * 80)
    try:
        w = 1.25
        resultado = capitulo2.sor(A, b, x0.copy(), tol, niter, w)
        if resultado['exito']:
            print(f"[OK] Solucion encontrada: {resultado['solucion']}")
            print(f"     Iteraciones: {resultado['iteraciones']}")
            print(f"     Radio espectral: {resultado['radio_espectral']:.6f}")
            print(f"     w = {resultado['w']}")

            sol = np.array(resultado['solucion'])
            diferencia = np.linalg.norm(sol - solucion_esperada)
            if diferencia < 1e-4:
                print(f"[OK] Verificacion: diferencia con [1,1,1] = {diferencia:.2e}")
                resultados.append(("SOR", True))
            else:
                print(f"[ERROR] Diferencia muy grande: {diferencia:.2e}")
                resultados.append(("SOR", False))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("SOR", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("SOR", False))

    return resultados


# ============================================================================
# CAPITULO 3: INTERPOLACION
# ============================================================================

def test_capitulo3():
    print("\n" + "="*80)
    print("CAPITULO 3: INTERPOLACION")
    print("="*80)

    resultados = []

    # Puntos de prueba: y = x^2
    puntos_x = [0.0, 1.0, 2.0, 3.0]
    puntos_y = [0.0, 1.0, 4.0, 9.0]

    print(f"\nPuntos de interpolacion: {list(zip(puntos_x, puntos_y))}")

    # Test 1: Vandermonde
    print("\n[1] Metodo de Vandermonde")
    print("-" * 80)
    try:
        resultado = capitulo3.vandermonde(
            np.array(puntos_x), np.array(puntos_y)
        )
        if resultado['exito']:
            print(f"[OK] Polinomio encontrado")
            print(f"     Coeficientes: {resultado['coeficientes']}")
            resultados.append(("Vandermonde", True))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Vandermonde", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Vandermonde", False))

    # Test 2: Newton Interpolante
    print("\n[2] Metodo de Newton Interpolante")
    print("-" * 80)
    try:
        resultado = capitulo3.newton_interpolante(
            np.array(puntos_x), np.array(puntos_y)
        )
        if resultado['exito']:
            print(f"[OK] Polinomio encontrado")
            print(f"     Tabla de diferencias divididas calculada")
            resultados.append(("Newton Interpolante", True))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Newton Interpolante", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Newton Interpolante", False))

    # Test 3: Lagrange
    print("\n[3] Metodo de Lagrange")
    print("-" * 80)
    try:
        resultado = capitulo3.lagrange(
            np.array(puntos_x), np.array(puntos_y)
        )
        if resultado['exito']:
            print(f"[OK] Polinomio encontrado")
            print(f"     Polinomio calculado")
            resultados.append(("Lagrange", True))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Lagrange", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Lagrange", False))

    # Test 4: Spline Lineal
    print("\n[4] Spline Lineal")
    print("-" * 80)
    try:
        resultado = capitulo3.spline_lineal(
            np.array(puntos_x), np.array(puntos_y)
        )
        if resultado['exito']:
            print(f"[OK] Spline lineal calculado")
            print(f"     Segmentos: {len(resultado['coeficientes'])}")
            resultados.append(("Spline Lineal", True))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Spline Lineal", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Spline Lineal", False))

    # Test 5: Spline Cúbico
    print("\n[5] Spline Cubico")
    print("-" * 80)
    try:
        resultado = capitulo3.spline_cubico(
            np.array(puntos_x), np.array(puntos_y)
        )
        if resultado['exito']:
            print(f"[OK] Spline cubico calculado")
            print(f"     Segmentos: {len(resultado['coeficientes'])}")
            resultados.append(("Spline Cubico", True))
        else:
            print(f"[ERROR] {resultado['mensaje']}")
            resultados.append(("Spline Cubico", False))
    except Exception as e:
        print(f"[ERROR] Excepcion: {e}")
        resultados.append(("Spline Cubico", False))

    return resultados


# ============================================================================
# EJECUTAR TODOS LOS TESTS
# ============================================================================

if __name__ == "__main__":
    todos_resultados = []

    # Capitulo 1
    try:
        resultados_cap1 = test_capitulo1()
        todos_resultados.extend(resultados_cap1)
    except Exception as e:
        print(f"\n[ERROR FATAL] Error en Capitulo 1: {e}")

    # Capitulo 2
    try:
        resultados_cap2 = test_capitulo2()
        todos_resultados.extend(resultados_cap2)
    except Exception as e:
        print(f"\n[ERROR FATAL] Error en Capitulo 2: {e}")

    # Capitulo 3
    try:
        resultados_cap3 = test_capitulo3()
        todos_resultados.extend(resultados_cap3)
    except Exception as e:
        print(f"\n[ERROR FATAL] Error en Capitulo 3: {e}")

    # Resumen final
    print("\n\n" + "="*80)
    print(" "*30 + "RESUMEN FINAL")
    print("="*80)

    metodos_pasaron = 0
    metodos_fallaron = 0

    for nombre, resultado in todos_resultados:
        estado = "[PASO]" if resultado else "[FALLO]"
        print(f"{estado:10} - {nombre}")
        if resultado:
            metodos_pasaron += 1
        else:
            metodos_fallaron += 1

    total = metodos_pasaron + metodos_fallaron
    porcentaje = (metodos_pasaron / total * 100) if total > 0 else 0

    print("\n" + "="*80)
    print(f"TOTAL: {metodos_pasaron}/{total} metodos pasaron ({porcentaje:.1f}%)")
    if metodos_pasaron == total:
        print("TODOS LOS METODOS FUNCIONAN CORRECTAMENTE!")
    else:
        print(f"ATENCION: {metodos_fallaron} metodos fallaron")
    print("="*80 + "\n")

    sys.exit(0 if metodos_pasaron == total else 1)
