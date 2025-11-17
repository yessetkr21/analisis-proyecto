import numpy as np
import matplotlib.pyplot as plt

def SplineCubico(x, y):
    """
    SplineCubico: Calcula los coeficientes de los polinomios de interpolación de
    grado 3 (cúbico) para el conjunto de n datos (x,y), mediante el método spline.
    
    Para cada segmento [x_i, x_{i+1}], calcula un polinomio cúbico:
    P_i(x) = a_i*x^3 + b_i*x^2 + c_i*x + d_i
    
    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)
    
    Retorna:
    Tabla: Matriz con los coeficientes de cada polinomio cúbico
           Cada fila i contiene [a_i, b_i, c_i, d_i] para el segmento i
    """
    n = len(x)
    d = 3  # grado cúbico
    
    # Crear matriz A y vector b para el sistema lineal
    A = np.zeros(((d+1)*(n-1), (d+1)*(n-1)))
    b = np.zeros((d+1)*(n-1))
    
    # Potencias de x
    cua = x**2  # x^2
    cub = x**3  # x^3
    
    # Índices para llenar las matrices
    c = 0  # columna
    h = 0  # fila
    
    # Condición 1: El polinomio i pasa por el punto (x_i, y_i)
    # P_i(x_i) = y_i para i = 1, 2, ..., n-1
    for i in range(n-1):
        A[h, c] = cub[i]
        A[h, c+1] = cua[i]
        A[h, c+2] = x[i]
        A[h, c+3] = 1
        b[h] = y[i]
        c += 4
        h += 1
    
    # Condición 2: El polinomio i pasa por el punto (x_{i+1}, y_{i+1})
    # P_i(x_{i+1}) = y_{i+1} para i = 1, 2, ..., n-1
    c = 0
    for i in range(1, n):
        A[h, c] = cub[i]
        A[h, c+1] = cua[i]
        A[h, c+2] = x[i]
        A[h, c+3] = 1
        b[h] = y[i]
        c += 4
        h += 1
    
    # Condición 3: Primera derivada continua en los puntos interiores
    # P'_i(x_{i+1}) = P'_{i+1}(x_{i+1}) para i = 1, 2, ..., n-2
    c = 0
    for i in range(1, n-1):
        A[h, c] = 3*cua[i]
        A[h, c+1] = 2*x[i]
        A[h, c+2] = 1
        A[h, c+4] = -3*cua[i]
        A[h, c+5] = -2*x[i]
        A[h, c+6] = -1
        b[h] = 0
        c += 4
        h += 1
    
    # Condición 4: Segunda derivada continua en los puntos interiores
    # P''_i(x_{i+1}) = P''_{i+1}(x_{i+1}) para i = 1, 2, ..., n-2
    c = 0
    for i in range(1, n-1):
        A[h, c] = 6*x[i]
        A[h, c+1] = 2
        A[h, c+4] = -6*x[i]
        A[h, c+5] = -2
        b[h] = 0
        c += 4
        h += 1
    
    # Condición 5: Segunda derivada nula en los extremos (spline natural)
    # P''_1(x_1) = 0
    A[h, 0] = 6*x[0]
    A[h, 1] = 2
    b[h] = 0
    h += 1
    
    # P''_{n-1}(x_n) = 0
    A[h, c] = 6*x[-1]
    A[h, c+1] = 2
    b[h] = 0
    
    # Resolver el sistema lineal
    val = np.linalg.solve(A, b)
    
    # Reorganizar los coeficientes en una tabla
    # Cada fila representa un segmento: [a, b, c, d] para P(x) = ax^3 + bx^2 + cx + d
    Tabla = val.reshape(n-1, d+1)
    
    return Tabla


def evaluar_spline_cubico(Tabla, x_original, x_eval):
    """
    Evalúa el spline cúbico en un punto dado
    
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
            # Evaluar el polinomio cúbico del segmento i
            a, b, c, d = Tabla[i]
            return a * x_eval**3 + b * x_eval**2 + c * x_eval + d
    
    # Si está fuera del rango, usar extrapolación
    if x_eval < x_original[0]:
        a, b, c, d = Tabla[0]
        return a * x_eval**3 + b * x_eval**2 + c * x_eval + d
    else:
        a, b, c, d = Tabla[-1]
        return a * x_eval**3 + b * x_eval**2 + c * x_eval + d


def mostrar_coeficientes_spline_cubico(Tabla, x):
    """
    Muestra los coeficientes de cada segmento del spline cúbico
    """
    n = len(Tabla)
    print("\nCOEFICIENTES DEL SPLINE CÚBICO")
    print("=" * 90)
    print(f"{'Seg':<5} {'Intervalo':<20} {'Polinomio'}")
    print("-" * 90)
    
    for i in range(n):
        a, b, c, d = Tabla[i]
        intervalo = f"[{x[i]:.3f}, {x[i+1]:.3f}]"
        polinomio = f"P{i}(x) = {a:.6f}x³ + {b:.6f}x² + {c:.6f}x + {d:.6f}"
        print(f"{i+1:<5} {intervalo:<20} {polinomio}")


def graficar_spline_cubico(x, y, Tabla):
    """
    Grafica los puntos originales y el spline cúbico
    """
    plt.figure(figsize=(10, 6))
    
    # Graficar puntos originales
    plt.plot(x, y, 'ro', markersize=10, label='Puntos dados', zorder=5)
    
    # Graficar cada segmento del spline
    n = len(x)
    for i in range(n-1):
        x_seg = np.linspace(x[i], x[i+1], 100)
        a, b, c, d = Tabla[i]
        y_seg = a * x_seg**3 + b * x_seg**2 + c * x_seg + d
        
        if i == 0:
            plt.plot(x_seg, y_seg, 'b-', linewidth=2, label='Spline cúbico')
        else:
            plt.plot(x_seg, y_seg, 'b-', linewidth=2)
    
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación con Spline Cúbico (Natural)', fontsize=14)
    plt.legend(fontsize=10)
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 90)
    print("INTERPOLACIÓN CON SPLINE CÚBICO")
    print("=" * 90)
    
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
    
    # Calcular el spline cúbico
    print("\n" + "=" * 90)
    print("CALCULANDO SPLINE CÚBICO...")
    print("=" * 90)
    
    Tabla = SplineCubico(x, y)
    
    # Mostrar coeficientes
    mostrar_coeficientes_spline_cubico(Tabla, x)
    
    # Verificar que el spline pasa por todos los puntos
    print("\n" + "=" * 90)
    print("VERIFICACIÓN")
    print("=" * 90)
    print(f"{'x':<10} {'y (dado)':<15} {'S(x) (calculado)':<20} {'Error'}")
    print("-" * 90)
    
    for i in range(len(x)):
        y_calc = evaluar_spline_cubico(Tabla, x, x[i])
        error = abs(y[i] - y_calc)
        print(f"{x[i]:<10.4f} {y[i]:<15.6f} {y_calc:<20.6f} {error:.2e}")
    
    # Evaluar en un punto adicional (opcional)
    print("\n" + "=" * 90)
    evaluar_mas = input("¿Deseas evaluar el spline en un punto específico? (s/n): ").strip().lower()
    
    if evaluar_mas == 's':
        x_nuevo = float(input("Ingresa el valor de x: "))
        y_nuevo = evaluar_spline_cubico(Tabla, x, x_nuevo)
        print(f"\nS({x_nuevo}) = {y_nuevo:.6f}")
        
        # Indicar en qué segmento está
        for i in range(len(x)-1):
            if x[i] <= x_nuevo <= x[i+1]:
                print(f"(Este punto está en el segmento {i+1}: [{x[i]:.3f}, {x[i+1]:.3f}])")
                break
    
    # Graficar (opcional)
    print("\n" + "=" * 90)
    graficar = input("¿Deseas graficar la interpolación? (s/n): ").strip().lower()
    
    if graficar == 's':
        graficar_spline_cubico(x, y, Tabla)
    
    print("\n¡Listo! 🎉")
