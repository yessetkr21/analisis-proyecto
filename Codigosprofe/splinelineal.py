import numpy as np
import matplotlib.pyplot as plt

def SplineLineal(x, y):
    """
    SplineLineal: Calcula los coeficientes de los polinomios de interpolación de
    grado 1 (lineal) para el conjunto de n datos (x,y), mediante el método spline.
    
    Para cada segmento [x_i, x_{i+1}], calcula un polinomio lineal:
    P_i(x) = a_i*x + b_i
    
    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)
    
    Retorna:
    Tabla: Matriz con los coeficientes de cada polinomio lineal
           Cada fila i contiene [a_i, b_i] para el segmento i
    """
    n = len(x)
    d = 1  # grado lineal
    
    # Crear matriz A y vector b para el sistema lineal
    A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
    b = np.zeros((d+1)*(n-1))
    
    # Índices para llenar las matrices
    c = 0  # columna
    h = 0  # fila
    
    # Condición 1: El polinomio i pasa por el punto (x_i, y_i)
    # P_i(x_i) = y_i para i = 1, 2, ..., n-1
    for i in range(n-1):
        A[h, c] = x[i]
        A[h, c+1] = 1
        b[h] = y[i]
        c += 2
        h += 1
    
    # Condición 2: El polinomio i pasa por el punto (x_{i+1}, y_{i+1})
    # P_i(x_{i+1}) = y_{i+1} para i = 1, 2, ..., n-1
    c = 0
    for i in range(1, n):
        A[h, c] = x[i]
        A[h, c+1] = 1
        b[h] = y[i]
        c += 2
        h += 1
    
    # Resolver el sistema lineal
    val = np.linalg.solve(A, b)
    
    # Reorganizar los coeficientes en una tabla
    # Cada fila representa un segmento: [a, b] para P(x) = ax + b
    Tabla = val.reshape(n-1, d+1)
    
    return Tabla


def evaluar_spline_lineal(Tabla, x_original, x_eval):
    """
    Evalúa el spline lineal en un punto dado
    
    Parámetros:
    Tabla: Matriz de coeficientes del spline
    x_original: Puntos originales usados para crear el spline
    x_eval: Punto donde evaluar el spline
    
    Retorna:
    resultado: Valor del spline en x_eval
    """
    n = len(x_original)
    
    # Encontrar en qué segmento está x_eval
    for i in range(n-1):
        if x_original[i] <= x_eval <= x_original[i+1]:
            # Evaluar el polinomio lineal del segmento i
            a, b = Tabla[i]
            return a * x_eval + b
    
    # Si está fuera del rango, usar extrapolación
    if x_eval < x_original[0]:
        a, b = Tabla[0]
        return a * x_eval + b
    else:
        a, b = Tabla[-1]
        return a * x_eval + b


def mostrar_coeficientes_spline(Tabla, x):
    """
    Muestra los coeficientes de cada segmento del spline
    """
    n = len(Tabla)
    print("\nCOEFICIENTES DEL SPLINE LINEAL")
    print("=" * 70)
    print(f"{'Segmento':<15} {'Intervalo':<20} {'Polinomio'}")
    print("-" * 70)
    
    for i in range(n):
        a, b = Tabla[i]
        intervalo = f"[{x[i]:.3f}, {x[i+1]:.3f}]"
        polinomio = f"P{i}(x) = {a:.6f}x + {b:.6f}"
        print(f"{i+1:<15} {intervalo:<20} {polinomio}")


def graficar_spline_lineal(x, y, Tabla):
    """
    Grafica los puntos originales y el spline lineal
    """
    plt.figure(figsize=(10, 6))
    
    # Graficar puntos originales
    plt.plot(x, y, 'ro', markersize=10, label='Puntos dados', zorder=5)
    
    # Graficar cada segmento del spline
    n = len(x)
    for i in range(n-1):
        x_seg = np.linspace(x[i], x[i+1], 100)
        y_seg = Tabla[i, 0] * x_seg + Tabla[i, 1]
        
        if i == 0:
            plt.plot(x_seg, y_seg, 'b-', linewidth=2, label='Spline lineal')
        else:
            plt.plot(x_seg, y_seg, 'b-', linewidth=2)
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación con Spline Lineal', fontsize=14)
    plt.legend(fontsize=10)
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("INTERPOLACIÓN CON SPLINE LINEAL")
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
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        y = np.array([1.0, 2.5, 0.5, 2.0, 3.5])
        print(f"Puntos: {list(zip(x, y))}")
    
    # Calcular el spline lineal
    print("\n" + "=" * 70)
    print("CALCULANDO SPLINE LINEAL...")
    print("=" * 70)
    
    Tabla = SplineLineal(x, y)
    
    # Mostrar coeficientes
    mostrar_coeficientes_spline(Tabla, x)
    
    # Verificar que el spline pasa por todos los puntos
    print("\n" + "=" * 70)
    print("VERIFICACIÓN")
    print("=" * 70)
    print(f"{'x':<10} {'y (dado)':<15} {'S(x) (calculado)':<20} {'Error'}")
    print("-" * 70)
    
    for i in range(len(x)):
        y_calc = evaluar_spline_lineal(Tabla, x, x[i])
        error = abs(y[i] - y_calc)
        print(f"{x[i]:<10.4f} {y[i]:<15.6f} {y_calc:<20.6f} {error:.2e}")
    
    # Evaluar en un punto adicional (opcional)
    print("\n" + "=" * 70)
    evaluar_mas = input("¿Deseas evaluar el spline en un punto específico? (s/n): ").strip().lower()
    
    if evaluar_mas == 's':
        x_nuevo = float(input("Ingresa el valor de x: "))
        y_nuevo = evaluar_spline_lineal(Tabla, x, x_nuevo)
        print(f"\nS({x_nuevo}) = {y_nuevo:.6f}")
        
        # Indicar en qué segmento está
        for i in range(len(x)-1):
            if x[i] <= x_nuevo <= x[i+1]:
                print(f"(Este punto está en el segmento {i+1}: [{x[i]:.3f}, {x[i+1]:.3f}])")
                break
    
    # Graficar (opcional)
    print("\n" + "=" * 70)
    graficar = input("¿Deseas graficar la interpolación? (s/n): ").strip().lower()
    
    if graficar == 's':
        graficar_spline_lineal(x, y, Tabla)
    
    print("\n¡Listo! 🎉")
