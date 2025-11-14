import numpy as np
import matplotlib.pyplot as plt

def vandermonde_interpolacion(x, y, grado=None):
    """
    Interpolación usando la matriz de Vandermonde
    
    Parámetros:
    x: Puntos conocidos (array)
    y: Valores en esos puntos (array)
    grado: Grado del polinomio (si None, usa n-1 donde n es el número de puntos)
    
    Retorna:
    a: Coeficientes del polinomio [a_n, a_{n-1}, ..., a_1, a_0]
        donde P(x) = a_n*x^n + a_{n-1}*x^{n-1} + ... + a_1*x + a_0
    """
    n = len(x)
    if grado is None:
        grado = n - 1
    
    # Construir la matriz de Vandermonde
    # A = [x^n, x^{n-1}, ..., x, 1]
    A = np.zeros((n, grado + 1))
    for i in range(grado + 1):
        A[:, i] = x ** (grado - i)
    
    # Resolver el sistema A*a = y
    a = np.linalg.solve(A, y)
    
    return a, A


def evaluar_polinomio_vandermonde(a, x_eval):
    """
    Evalúa el polinomio de Vandermonde en los puntos dados
    
    Parámetros:
    a: Coeficientes del polinomio
    x_eval: Puntos donde evaluar
    
    Retorna:
    p: Valores del polinomio en x_eval
    """
    grado = len(a) - 1
    p = np.zeros_like(x_eval)
    
    for i, coef in enumerate(a):
        p += coef * (x_eval ** (grado - i))
    
    return p


def mostrar_polinomio_vandermonde(a):
    """
    Muestra el polinomio en formato legible
    """
    grado = len(a) - 1
    terminos = []
    
    for i, coef in enumerate(a):
        potencia = grado - i
        if abs(coef) > 1e-10:
            if potencia == 0:
                terminos.append(f"{coef:.10f}")
            elif potencia == 1:
                terminos.append(f"{coef:.10f}x")
            else:
                terminos.append(f"{coef:.10f}x^{potencia}")
    
    return " + ".join(terminos).replace("+ -", "- ")


# Programa principal
if __name__ == "__main__":
    print("=" * 80)
    print("INTERPOLACIÓN CON MATRIZ DE VANDERMONDE")
    print("=" * 80)
    
    # Opción de entrada de datos
    print("\n¿Qué ejemplo deseas usar?")
    print("1. Ejemplo 1 (4 puntos, grado 3)")
    print("2. Ejemplo 2 (5 puntos, grado 4)")
    print("3. Ingresar datos manualmente")
    
    opcion = input("\nElige una opción (1, 2 o 3): ").strip()
    
    if opcion == "1":
        # Ejemplo 1: del profesor
        print("\n--- Ejemplo 1 (grado 3) ---")
        x = np.array([-2, -1, 2, 3], dtype=float)
        y = np.array([12.13533528, 6.367879441, -4.610943901, 2.085536923], dtype=float)
        grado = 3
        
    elif opcion == "2":
        # Ejemplo 2: del profesor
        print("\n--- Ejemplo 2 (grado 4) ---")
        x = np.array([1.8, 2, 3, 4, 5], dtype=float)
        y = np.exp(-x/1.8) + 1/(x**2 - 3)
        grado = 4
        print(f"Puntos (x, y):")
        for i in range(len(x)):
            print(f"  ({x[i]:.2f}, {y[i]:.10f})")
        
    else:
        # Entrada manual
        print("\n--- Entrada manual ---")
        n = int(input("¿Cuántos puntos deseas interpolar?: "))
        grado = int(input(f"¿Qué grado de polinomio? (máximo {n-1}): "))
        
        x = np.zeros(n)
        y = np.zeros(n)
        
        print(f"\nIngresa {n} puntos (x, y):")
        for i in range(n):
            x[i] = float(input(f"  x[{i}] = "))
            y[i] = float(input(f"  y[{i}] = "))
    
    # Calcular interpolación con Vandermonde
    print("\n" + "=" * 80)
    print("CALCULANDO INTERPOLACIÓN...")
    print("=" * 80)
    
    a, A = vandermonde_interpolacion(x, y, grado)
    
    # Mostrar matriz de Vandermonde
    print("\nMatriz de Vandermonde A:")
    print(A)
    
    # Mostrar vector b (y)
    print("\nVector b (y):")
    print(y)
    
    # Mostrar coeficientes
    print("\nCoeficientes del polinomio a = inv(A) * b:")
    for i, coef in enumerate(a):
        print(f"  a[{i}] = {coef:.10f}")
    
    # Mostrar polinomio
    print(f"\nPolinomio interpolador:")
    print(f"P(x) = {mostrar_polinomio_vandermonde(a)}")
    
    # Verificación
    print("\n" + "=" * 80)
    print("VERIFICACIÓN EN LOS PUNTOS DADOS")
    print("=" * 80)
    print(f"{'x':<10} {'y (dado)':<20} {'P(x) (calculado)':<20} {'Error'}")
    print("-" * 80)
    
    for i in range(len(x)):
        p_x = evaluar_polinomio_vandermonde(a, x[i])
        error = abs(y[i] - p_x)
        print(f"{x[i]:<10.4f} {y[i]:<20.10f} {p_x:<20.10f} {error:.2e}")
    
    # Evaluar en puntos específicos (para ejemplo 2)
    if opcion == "2":
        print("\n" + "=" * 80)
        print("ERRORES EN PUNTOS ESPECÍFICOS")
        print("=" * 80)
        
        # Evaluar en x = 2.5
        x_test1 = 2.5
        p_test1 = evaluar_polinomio_vandermonde(a, x_test1)
        y_real1 = np.exp(-x_test1/1.8) + 1/(x_test1**2 - 3)
        error1 = abs(p_test1 - y_real1)
        print(f"En x = {x_test1}:")
        print(f"  P({x_test1}) = {p_test1:.10f}")
        print(f"  f({x_test1}) = {y_real1:.10f}")
        print(f"  Error = {error1:.10f}")
        
        # Evaluar en x = 6
        x_test2 = 6.0
        p_test2 = evaluar_polinomio_vandermonde(a, x_test2)
        y_real2 = np.exp(-x_test2/1.8) + 1/(x_test2**2 - 3)
        error2 = abs(p_test2 - y_real2)
        print(f"\nEn x = {x_test2}:")
        print(f"  P({x_test2}) = {p_test2:.10f}")
        print(f"  f({x_test2}) = {y_real2:.10f}")
        print(f"  Error = {error2:.10f}")
    
    # Graficar
    print("\n" + "=" * 80)
    print("GENERANDO GRÁFICA...")
    print("=" * 80)
    
    # Crear puntos para graficar
    x_min, x_max = x.min(), x.max()
    xpol = np.linspace(x_min, x_max, 500)
    p = evaluar_polinomio_vandermonde(a, xpol)
    
    plt.figure(figsize=(12, 6))
    
    # Graficar puntos dados
    plt.plot(x, y, 'r*', markersize=15, label='Puntos dados', linewidth=2)
    
    # Graficar polinomio interpolador
    plt.plot(xpol, p, 'b-', linewidth=2, label='Polinomio interpolador')
    
    # Si es el ejemplo 2, graficar la función real
    if opcion == "2":
        xpol_real = np.linspace(x_min, x_max, 500)
        freal = np.exp(-xpol_real/1.8) + 1/(xpol_real**2 - 3)
        plt.plot(xpol_real, freal, 'c--', linewidth=2, label='Función real')
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title(f'Interpolación con Matriz de Vandermonde (grado {grado})', fontsize=14)
    plt.legend(fontsize=10)
    plt.show()
    
    print("\n¡Listo! 🎉")
