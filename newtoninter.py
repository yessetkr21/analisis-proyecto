import numpy as np
import matplotlib.pyplot as plt

def Newtonint(x, y):
    """
    Newtonint: Calcula los coeficientes del polinomio de interpolación de
    grado n-1 para el conjunto de n datos (x,y), mediante el método de Newton
    con diferencias divididas.
    
    Parámetros:
    x: Array con los valores de x (puntos conocidos)
    y: Array con los valores de y (valores de la función en esos puntos)
    
    Retorna:
    Tabla: Matriz de diferencias divididas
           Columna 0: valores de x
           Columna 1: valores de y
           Columnas 2 en adelante: diferencias divididas de orden 1, 2, 3, ...
    """
    n = len(x)
    Tabla = np.zeros((n, n + 1))
    Tabla[:, 0] = x
    Tabla[:, 1] = y
    
    for j in range(2, n + 1):
        for i in range(j - 1, n):
            Tabla[i, j] = (Tabla[i, j-1] - Tabla[i-1, j-1]) / (Tabla[i, 0] - Tabla[i-j+1, 0])
    
    return Tabla


def evaluar_newton(Tabla, x_eval):
    """
    Evalúa el polinomio de Newton en un punto dado
    
    Parámetros:
    Tabla: Tabla de diferencias divididas
    x_eval: Punto donde evaluar el polinomio
    
    Retorna:
    resultado: Valor del polinomio en x_eval
    """
    n = len(Tabla)
    x = Tabla[:, 0]
    resultado = Tabla[0, 1]
    producto = 1.0
    
    for i in range(1, n):
        producto *= (x_eval - x[i-1])
        resultado += Tabla[i, i+1] * producto
    
    return resultado


def mostrar_tabla_diferencias(Tabla):
    """
    Muestra la tabla de diferencias divididas de forma clara
    """
    n = len(Tabla)
    print("\nTABLA DE DIFERENCIAS DIVIDIDAS")
    print("=" * 80)
    
    # Encabezados
    headers = ["x", "f(x)"]
    for i in range(1, n):
        headers.append(f"DD{i}")
    
    # Imprimir encabezados
    print(f"{'i':<5}", end="")
    for header in headers:
        print(f"{header:>12}", end="")
    print()
    print("-" * 80)
    
    # Imprimir filas
    for i in range(n):
        print(f"{i:<5}", end="")
        for j in range(n + 1):
            if j <= i + 1:
                print(f"{Tabla[i, j]:>12.6f}", end="")
            else:
                print(f"{'':>12}", end="")
        print()


def obtener_coeficientes_newton(Tabla):
    """
    Extrae los coeficientes del polinomio de Newton
    (las diferencias divididas de la diagonal)
    """
    n = len(Tabla)
    coeficientes = np.zeros(n)
    coeficientes[0] = Tabla[0, 1]
    
    for i in range(1, n):
        coeficientes[i] = Tabla[i, i+1]
    
    return coeficientes


def mostrar_polinomio_newton(Tabla):
    """
    Muestra el polinomio de Newton en formato legible
    """
    n = len(Tabla)
    x = Tabla[:, 0]
    coefs = obtener_coeficientes_newton(Tabla)
    
    print(f"\nPOLINOMIO DE NEWTON:")
    print("=" * 80)
    print(f"P(x) = {coefs[0]:.6f}", end="")
    
    for i in range(1, n):
        print(f" + {coefs[i]:.6f}", end="")
        for j in range(i):
            print(f"(x - {x[j]:.3f})", end="")
    print()


def graficar_newton(x, y, Tabla):
    """
    Grafica los puntos originales y el polinomio de Newton
    """
    # Crear puntos para graficar el polinomio suavemente
    x_plot = np.linspace(min(x) - 1, max(x) + 1, 500)
    y_plot = np.array([evaluar_newton(Tabla, xi) for xi in x_plot])
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', markersize=10, label='Puntos dados')
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label='Polinomio de Newton')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Interpolación con Polinomio de Newton (Diferencias Divididas)', fontsize=14)
    plt.legend(fontsize=10)
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 80)
    print("INTERPOLACIÓN CON POLINOMIO DE NEWTON (DIFERENCIAS DIVIDIDAS)")
    print("=" * 80)
    
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
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y = np.array([0.5, 2.0, 1.5, 3.0, 2.5])
        print(f"Puntos: {list(zip(x, y))}")
    
    # Calcular el polinomio de Newton
    print("\n" + "=" * 80)
    print("CALCULANDO POLINOMIO DE NEWTON...")
    print("=" * 80)
    
    Tabla = Newtonint(x, y)
    
    # Mostrar tabla de diferencias divididas
    mostrar_tabla_diferencias(Tabla)
    
    # Mostrar coeficientes
    coeficientes = obtener_coeficientes_newton(Tabla)
    print(f"\nCoeficientes del polinomio de Newton:")
    for i, coef in enumerate(coeficientes):
        print(f"  a[{i}] = {coef:.6f}")
    
    # Mostrar polinomio
    mostrar_polinomio_newton(Tabla)
    
    # Verificar que el polinomio pasa por todos los puntos
    print("\n" + "=" * 80)
    print("VERIFICACIÓN")
    print("=" * 80)
    print(f"{'x':<10} {'y (dado)':<15} {'P(x) (calculado)':<20} {'Error'}")
    print("-" * 80)
    
    for i in range(len(x)):
        y_calc = evaluar_newton(Tabla, x[i])
        error = abs(y[i] - y_calc)
        print(f"{x[i]:<10.4f} {y[i]:<15.6f} {y_calc:<20.6f} {error:.2e}")
    
    # Evaluar en un punto adicional (opcional)
    print("\n" + "=" * 80)
    evaluar_mas = input("¿Deseas evaluar el polinomio en un punto específico? (s/n): ").strip().lower()
    
    if evaluar_mas == 's':
        x_nuevo = float(input("Ingresa el valor de x: "))
        y_nuevo = evaluar_newton(Tabla, x_nuevo)
        print(f"\nP({x_nuevo}) = {y_nuevo:.6f}")
    
    # Graficar (opcional)
    print("\n" + "=" * 80)
    graficar = input("¿Deseas graficar la interpolación? (s/n): ").strip().lower()
    
    if graficar == 's':
        graficar_newton(x, y, Tabla)
    
    print("\n¡Listo! 🎉")
