import pandas as pd
import numpy as np
import math

print("=" * 70)
print("MÉTODO DE LA REGLA FALSA (FALSA POSICIÓN)")
print("=" * 70)

print("\nXi (límite inferior):")
Xi = float(input())
print("Xs (límite superior):")
Xs = float(input())
print("Tol (tolerancia):")
Tol_str = input()   # leer como string para analizar
Tol = float(Tol_str)
print("Niter (número máximo de iteraciones):")
Niter = int(input())
print("Function (función f(x), usa 'x' como variable):")
Fun = input()

# Detectar tipo de error automáticamente según Tol_str
if Tol_str.startswith("5e") or Tol_str.startswith("5E"):
    tipo_error = "cifras"
else:
    tipo_error = "decimales"

# Listas para la tabla
iteraciones = []
valores_Xi = []
valores_Xs = []
valores_Xm = []
valores_fi = []
valores_fs = []
valores_fm = []
errores = []

# Evaluar en los extremos del intervalo
x = Xi
fi = eval(Fun)
x = Xs
fs = eval(Fun)

print("\n" + "=" * 70)
print("RESOLVIENDO...")
print("=" * 70)

if fi == 0:
    print(f"\n{Xi} es raíz de f(x)")
    print(f"f({Xi}) = {fi}")
elif fs == 0:
    print(f"\n{Xs} es raíz de f(x)")
    print(f"f({Xs}) = {fs}")
elif fs * fi < 0:
    c = 0
    
    # Primera iteración usando la fórmula de la regla falsa
    # Xm = Xi - fi * (Xs - Xi) / (fs - fi)
    # o equivalentemente: Xm = (Xi*fs - Xs*fi) / (fs - fi)
    Xm = Xi - fi * (Xs - Xi) / (fs - fi)
    x = Xm
    fe = eval(Fun)

    iteraciones.append(c)
    valores_Xi.append(Xi)
    valores_Xs.append(Xs)
    valores_Xm.append(Xm)
    valores_fi.append(fi)
    valores_fs.append(fs)
    valores_fm.append(fe)
    errores.append(None)  # No hay error en la primera iteración

    while True:
        # Actualizar el intervalo según el signo de f(Xm)
        if fi * fe < 0:
            # La raíz está entre Xi y Xm
            Xs = Xm
            x = Xs
            fs = eval(Fun)
        else:
            # La raíz está entre Xm y Xs
            Xi = Xm
            x = Xi
            fi = eval(Fun)

        Xa = Xm
        
        # Calcular nuevo Xm usando la fórmula de la regla falsa
        Xm = Xi - fi * (Xs - Xi) / (fs - fi)
        x = Xm
        fe = eval(Fun)

        # Cálculo del error según el tipo detectado
        if tipo_error == "cifras":
            Error = abs(Xm - Xa) / abs(Xm)
        else:
            Error = abs(Xm - Xa)

        c += 1
        iteraciones.append(c)
        valores_Xi.append(Xi)
        valores_Xs.append(Xs)
        valores_Xm.append(Xm)
        valores_fi.append(fi)
        valores_fs.append(fs)
        valores_fm.append(fe)
        errores.append(Error)

        # Condiciones de parada
        if Error < Tol:
            print(f"\n¡Convergencia alcanzada!")
            print(f"Raíz aproximada: x = {Xm}")
            print(f"f({Xm}) = {fe}")
            print(f"Error: {Error}")
            print(f"Iteraciones: {c}")
            break
        elif fe == 0:
            print(f"\n¡Raíz exacta encontrada!")
            print(f"Raíz: x = {Xm}")
            print(f"f({Xm}) = {fe}")
            print(f"Iteraciones: {c}")
            break
        elif c >= Niter:
            print(f"\n¡Número máximo de iteraciones alcanzado!")
            print(f"Raíz aproximada: x = {Xm}")
            print(f"f({Xm}) = {fe}")
            print(f"Error final: {Error}")
            break

    # Crear DataFrame con los resultados
    tabla = pd.DataFrame({
        "Iter": iteraciones,
        "Xi": valores_Xi,
        "Xs": valores_Xs,
        "Xm": valores_Xm,
        "f(Xi)": valores_fi,
        "f(Xs)": valores_fs,
        "f(Xm)": valores_fm,
        "Error": errores
    })

    print("\n" + "=" * 70)
    print("TABLA DE ITERACIONES")
    print("=" * 70)
    print(f"Método de error usado: {tipo_error}")
    print(f"Tolerancia: {Tol}")
    print("\n")
    print(tabla.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("DIFERENCIA ENTRE BISECCIÓN Y REGLA FALSA")
    print("=" * 70)
    print("• BISECCIÓN: Xm = (Xi + Xs) / 2  (punto medio)")
    print("• REGLA FALSA: Xm = Xi - fi*(Xs - Xi)/(fs - fi)  (interpolación lineal)")
    print("\nLa Regla Falsa generalmente converge más rápido porque usa")
    print("la interpolación lineal entre los puntos en lugar del punto medio.")
    
else:
    print("\n" + "=" * 70)
    print("ERROR: El intervalo es inadecuado")
    print("=" * 70)
    print(f"f({Xi}) = {fi}")
    print(f"f({Xs}) = {fs}")
    print(f"f({Xi}) * f({Xs}) = {fi * fs}")
    print("\nPara que el método funcione, f(Xi) y f(Xs) deben tener signos opuestos.")
    print("Es decir: f(Xi) * f(Xs) < 0")

print("\n¡Listo! 🎉")
