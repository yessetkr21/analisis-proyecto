import numpy as np
import matplotlib.pyplot as plt

def Lagrange(x, y):
    """
    Lagrange: Calcula los coeficientes del polinomio de interpolación de
    grado n-1 para el conjunto de n datos (x,y), mediante el método de
    Lagrange.
    
    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)
    
    Retorna:
    pol: Coeficientes del polinomio interpolador (de mayor a menor grado)
    """
    n = len(x)
    Tabla = np.zeros((n, n))
    
    for i in range(n):
        Li = np.array([1.0])
        den = 1.0
        
        for j in range(n):
            if j != i:
                # Multiplica por (t - x[j])
                paux = np.array([1.0, -x[j]])
                Li = np.convolve(Li, paux)
                den = den * (x[i] - x[j])
        
        # Guarda y[i] * Li / den en la tabla
        Tabla[i, :] = y[i] * Li / den
    
    # Suma todos los polinomios de Lagrange
    pol = np.sum(Tabla, axis=0)
    
    return pol


def evaluar_polinomio(pol, x_eval):
    """
    Evalúa el polinomio en los puntos dados
    
    Parámetros:
    pol: Coeficientes del polinomio
    x_eval: Puntos donde evaluar el polinomio
    
    Retorna:
    y_eval: Valores del polinomio en los puntos dados
    """
    return np.polyval(pol, x_eval)


def mostrar_polinomio(pol):
    """
    Muestra el polinomio en formato legible
    """
    n = len(pol)
    grado = n - 1
    terminos = []
    
    for i, coef in enumerate(pol):
        potencia = grado - i
        if abs(coef) > 1e-10:  # Ignorar coeficientes muy pequeños
            if potencia == 0:
                terminos.append(f"{coef:.6f}")
            elif potencia == 1:
                terminos.append(f"{coef:.6f}x")
            else:
                terminos.append(f"{coef:.6f}x^{potencia}")
    
    return " + ".join(terminos).replace("+ -", "- ")


def graficar_interpolacion(x, y, pol):
    """
    Grafica los puntos originales y el polinomio interpolador
    """
    # Crear puntos para graficar el polinomio suavemente
    x_plot = np.linspace(min(x) - 1, max(x) + 1, 500)
    y_plot = evaluar_polinomio(pol, x_plot)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', markersize=10, label='Puntos dados')
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio de Lagrange')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación con Polinomio de Lagrange', fontsize=14)
    plt.legend(fontsize=10)
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("INTERPOLACIÓN CON POLINOMIO DE LAGRANGE")
    print("=" * 70)
    
    # Opción de entrada de datos
    print("\n¿Cómo deseas ingresar los datos?")
    print("1. Usar ejemplo predefinido")
    print("2. Ingresar datos manualmente")
    
    opcion = input("\nElige una opción (1 o 2): ").strip()
    
    if opcion == "2":
        # Entrada manual de datos
        print("\n--- Entrada de datos ---")
        n = int(input("¿Cuántos puntos deseas interpolar?: "))
        
        x = np.zeros(n)
        y = np.zeros(n)
        
        print(f"\nIngresa {n} puntos (x, y):")
        for i in range(n):
            x[i] = float(input(f"  x[{i}] = "))
            y[i] = float(input(f"  y[{i}] = "))
    else:
        # Ejemplo predefinido
        print("\n--- Usando ejemplo predefinido ---")
        x = np.array([1.0, 2.0, 3.0, 4.0])
        y = np.array([0.5, 2.0, 1.5, 3.0])
        print(f"Puntos: {list(zip(x, y))}")
    
    # Calcular el polinomio de Lagrange
    print("\n" + "=" * 70)
    print("CALCULANDO POLINOMIO DE LAGRANGE...")
    print("=" * 70)
    
    pol = Lagrange(x, y)
    
    # Mostrar resultados
    print(f"\nCoeficientes del polinomio (de mayor a menor grado):")
    print(pol)
    
    print(f"\nPolinomio interpolador:")
    print(f"P(x) = {mostrar_polinomio(pol)}")
    
    # Verificar que el polinomio pasa por todos los puntos
    print("\n" + "=" * 70)
    print("VERIFICACIÓN")
    print("=" * 70)
    print(f"{'x':<10} {'y (dado)':<15} {'P(x) (calculado)':<20} {'Error'}")
    print("-" * 70)
    
    for i in range(len(x)):
        y_calc = evaluar_polinomio(pol, x[i])
        error = abs(y[i] - y_calc)
        print(f"{x[i]:<10.4f} {y[i]:<15.6f} {y_calc:<20.6f} {error:.2e}")
    
    # Evaluar en un punto adicional (opcional)
    print("\n" + "=" * 70)
    evaluar_mas = input("¿Deseas evaluar el polinomio en un punto específico? (s/n): ").strip().lower()
    
    if evaluar_mas == 's':
        x_nuevo = float(input("Ingresa el valor de x: "))
        y_nuevo = evaluar_polinomio(pol, x_nuevo)
        print(f"\nP({x_nuevo}) = {y_nuevo:.6f}")
    
    # Graficar (opcional)
    print("\n" + "=" * 70)
    graficar = input("¿Deseas graficar la interpolación? (s/n): ").strip().lower()
    
    if graficar == 's':
        graficar_interpolacion(x, y, pol)
    
    print("\n¡Listo! 🎉")
