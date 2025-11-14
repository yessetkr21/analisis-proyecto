import pandas as pd
import numpy as np
import math
from sympy import symbols, sympify, diff, lambdify

print("=" * 80)
print("MÉTODO DE NEWTON-RAPHSON PARA RAÍCES MÚLTIPLES")
print("=" * 80)

print("\nEste método es útil cuando la raíz tiene multiplicidad m > 1")
print("Es decir, cuando f(x) = (x - r)^m * g(x), donde g(r) ≠ 0")
print("\nFórmula modificada: x_{n+1} = x_n - m * f(x_n) / f'(x_n)")
print("O fórmula general: x_{n+1} = x_n - f(x_n) * f'(x_n) / [f'(x_n)^2 - f(x_n)*f''(x_n)]")

print("\n" + "=" * 80)
print("ENTRADA DE DATOS")
print("=" * 80)

print("\n¿Qué método deseas usar?")
print("1. Newton-Raphson modificado (conociendo la multiplicidad m)")
print("2. Newton-Raphson con segunda derivada (sin conocer m)")

metodo = input("\nElige una opción (1 o 2): ").strip()

print("\nX0 (valor inicial):")
x0 = float(input())

print("Tol (tolerancia):")
Tol_str = input()
Tol = float(Tol_str)

print("Niter (número máximo de iteraciones):")
Niter = int(input())

print("Function f(x) (usa 'x' como variable):")
Fun = input()

# Detectar tipo de error automáticamente
if Tol_str.startswith("5e") or Tol_str.startswith("5E"):
    tipo_error = "cifras"
else:
    tipo_error = "decimales"

# Crear símbolo para cálculo simbólico
x_sym = symbols('x')
f_sym = sympify(Fun)

# Calcular derivadas simbólicamente
f_prime_sym = diff(f_sym, x_sym)
f_double_prime_sym = diff(f_prime_sym, x_sym)

# Convertir a funciones evaluables
f = lambdify(x_sym, f_sym, modules=['numpy', 'math'])
f_prime = lambdify(x_sym, f_prime_sym, modules=['numpy', 'math'])
f_double_prime = lambdify(x_sym, f_double_prime_sym, modules=['numpy', 'math'])

print(f"\nf(x) = {f_sym}")
print(f"f'(x) = {f_prime_sym}")

if metodo == "1":
    # Método 1: Newton-Raphson modificado con multiplicidad conocida
    print("\nMultiplicidad m de la raíz:")
    m = int(input())
    print(f"\nUsando fórmula: x_{{n+1}} = x_n - {m} * f(x_n) / f'(x_n)")
else:
    # Método 2: Fórmula con segunda derivada
    print(f"f''(x) = {f_double_prime_sym}")
    print("\nUsando fórmula: x_{{n+1}} = x_n - f(x_n)*f'(x_n) / [f'(x_n)² - f(x_n)*f''(x_n)]")

# Listas para la tabla
iteraciones = []
valores_xn = []
valores_fn = []
valores_fprime = []
errores = []

print("\n" + "=" * 80)
print("RESOLVIENDO...")
print("=" * 80)

c = 0
xn = x0
fn = f(xn)
fpn = f_prime(xn)

iteraciones.append(c)
valores_xn.append(xn)
valores_fn.append(fn)
valores_fprime.append(fpn)
errores.append(None)

Error = Tol + 1

while Error > Tol and c < Niter:
    fn = f(xn)
    fpn = f_prime(xn)
    
    if fpn == 0:
        print(f"\nError: f'(x_{c}) = 0, no se puede continuar")
        print("La derivada se anula, el método falla")
        break
    
    # Calcular siguiente aproximación según el método elegido
    if metodo == "1":
        # Método con multiplicidad conocida
        xn1 = xn - m * fn / fpn
    else:
        # Método con segunda derivada
        fppn = f_double_prime(xn)
        denominador = fpn**2 - fn * fppn
        
        if abs(denominador) < 1e-15:
            print(f"\nError: Denominador muy pequeño en iteración {c}")
            print("El método no puede continuar")
            break
        
        xn1 = xn - (fn * fpn) / denominador
    
    # Calcular error
    if tipo_error == "cifras":
        Error = abs(xn1 - xn) / abs(xn1) if xn1 != 0 else abs(xn1 - xn)
    else:
        Error = abs(xn1 - xn)
    
    c += 1
    xn = xn1
    fn = f(xn)
    fpn = f_prime(xn)
    
    iteraciones.append(c)
    valores_xn.append(xn)
    valores_fn.append(fn)
    valores_fprime.append(fpn)
    errores.append(Error)
    
    # Verificar convergencia
    if Error < Tol:
        print(f"\n¡Convergencia alcanzada!")
        print(f"Raíz aproximada: x = {xn}")
        print(f"f({xn}) = {fn}")
        print(f"Error: {Error}")
        print(f"Iteraciones: {c}")
        break
    elif abs(fn) < 1e-15:
        print(f"\n¡Raíz encontrada!")
        print(f"Raíz: x = {xn}")
        print(f"f({xn}) = {fn}")
        print(f"Iteraciones: {c}")
        break

if c >= Niter:
    print(f"\n¡Número máximo de iteraciones alcanzado!")
    print(f"Raíz aproximada: x = {xn}")
    print(f"f({xn}) = {fn}")
    print(f"Error final: {Error}")

# Crear DataFrame con los resultados
if metodo == "1":
    tabla = pd.DataFrame({
        "Iter": iteraciones,
        "x_n": valores_xn,
        "f(x_n)": valores_fn,
        "f'(x_n)": valores_fprime,
        "Error": errores
    })
else:
    valores_fdoubleprime = [f_double_prime(x) for x in valores_xn]
    tabla = pd.DataFrame({
        "Iter": iteraciones,
        "x_n": valores_xn,
        "f(x_n)": valores_fn,
        "f'(x_n)": valores_fprime,
        "f''(x_n)": valores_fdoubleprime,
        "Error": errores
    })

print("\n" + "=" * 80)
print("TABLA DE ITERACIONES")
print("=" * 80)
print(f"Método de error usado: {tipo_error}")
print(f"Tolerancia: {Tol}")
print("\n")
print(tabla.to_string(index=False))

print("\n" + "=" * 80)
print("INFORMACIÓN SOBRE RAÍCES MÚLTIPLES")
print("=" * 80)
print("\n¿Qué es una raíz múltiple?")
print("Una raíz r tiene multiplicidad m si:")
print("  f(r) = f'(r) = f''(r) = ... = f^(m-1)(r) = 0")
print("  pero f^(m)(r) ≠ 0")
print("\nEjemplo: f(x) = (x-2)³ tiene una raíz triple en x=2")
print("\nEl Newton-Raphson estándar converge lentamente para raíces múltiples.")
print("Estos métodos modificados mejoran la convergencia:")
print("\n  Método 1: Si conoces m, usa x_{n+1} = x_n - m*f(x_n)/f'(x_n)")
print("  Método 2: Si no conoces m, usa la fórmula con f''(x_n)")

# Verificar si es raíz múltiple
if abs(fn) < 1e-10 and abs(fpn) < 1e-6:
    print("\n" + "=" * 80)
    print("⚠️  POSIBLE RAÍZ MÚLTIPLE DETECTADA")
    print("=" * 80)
    print(f"f({xn}) ≈ 0 y f'({xn}) ≈ 0")
    print("Esto indica que la raíz probablemente tiene multiplicidad > 1")

print("\n¡Listo! 🎉")
