import pandas as pd
import numpy as np
import math

print("Xi:")
Xi = float(input())
print("Xs:")
Xs = float(input())
print("Tol:")
Tol_str = input()   # leer como string para analizar
Tol = float(Tol_str)
print("Niter:")
Niter = int(input())
print("Function:")
Fun = input()

# Detectar tipo de error automáticamente según Tol_str
if Tol_str.startswith("5e") or Tol_str.startswith("5E"):
    tipo_error = "cifras"
else:
    tipo_error = "decimales"

# Listas para la tabla
iteraciones = []
valores_Xm = []
valores_fm = []
errores = []

x = Xi
fi = eval(Fun)
x = Xs
fs = eval(Fun)

if fi == 0:
    print(Xi, "es raíz de f(x)")
elif fs == 0:
    print(Xs, "es raíz de f(x)")
elif fs * fi < 0:
    c = 0
    Xm = (Xi + Xs) / 2
    x = Xm
    fe = eval(Fun)

    iteraciones.append(c)
    valores_Xm.append(Xm)
    valores_fm.append(fe)
    errores.append(None)  # No hay error en la primera iteración

    while True:
        if fi * fe < 0:
            Xs = Xm
            x = Xs
            fs = eval(Fun)
        else:
            Xi = Xm
            x = Xi
            fi = eval(Fun)

        Xa = Xm
        Xm = (Xi + Xs) / 2
        x = Xm
        fe = eval(Fun)

        # Cálculo del error según el tipo detectado
        if tipo_error == "cifras":
            Error = abs(Xm - Xa) / abs(Xm)
        else:
            Error = abs(Xm - Xa)

        c += 1
        iteraciones.append(c)
        valores_Xm.append(Xm)
        valores_fm.append(fe)
        errores.append(Error)

        # Condiciones de parada
        if Error < Tol or fe == 0 or c >= Niter:
            break

    # Crear DataFrame con los resultados
    tabla = pd.DataFrame({
        "Iteración": iteraciones,
        "Xm": valores_Xm,
        "f(Xm)": valores_fm,
        "Error": errores
    })

    print("\nMétodo de error usado:", tipo_error)
    print(tabla.to_string(index=False))
else:
    print("El intervalo es inadecuado")