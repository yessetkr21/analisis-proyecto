import pandas as pd
import math

print("X0:")
x0 = float(input())
print("X1:")
x1 = float(input())
print("Tol:")
Tol_str = input()
Tol = float(Tol_str)
print("Niter:")
Niter = int(input())
print("Function:")
Fun = input()   # puedes poner exp(-x)-x, sin "math."

# Detectar tipo de error
tipo_error = "cifras" if Tol_str.startswith(("5e", "5E")) else "decimales"

# Función evaluadora con acceso a math
def f(x):
    return eval(Fun, {"x": x, **math.__dict__})

# Inicialización de listas
iteracion = []
xn_vals   = []
fxn_vals  = []
err_vals  = []

# Evaluaciones iniciales
f0 = f(x0)
f1 = f(x1)

# Registrar primera fila
k = 0
iteracion.append(k)
xn_vals.append(x1)
fxn_vals.append(f1)
err_vals.append(None)  # No hay error en la primera iteración

# Comprobaciones iniciales
if f0 == 0:
    print(f"{x0} es raíz de f(x)")
elif f1 == 0:
    print(f"{x1} es raíz de f(x)")
else:
    while k < Niter:
        denom = (f1 - f0)
        if denom == 0:
            break

        # Fórmula de la secante
        x2 = x1 - f1 * (x1 - x0) / denom

        # Error según tipo
        if tipo_error == "cifras":
            Error = abs(x2 - x1) / abs(x2) if x2 != 0 else float("inf")
        else:  # decimales correctos
            Error = abs(x2 - x1)

        # Avanzar
        x0, f0 = x1, f1
        x1 = x2
        f1 = f(x1)

        k += 1
        iteracion.append(k)
        xn_vals.append(x1)
        fxn_vals.append(f1)
        err_vals.append(Error)

        # Parada
        if f1 == 0 or Error < Tol:
            break

    # Tabla
    tabla = pd.DataFrame({
        "Iteración": iteracion,
        "x_n": xn_vals,
        "f(x_n)": fxn_vals,
        "Error": err_vals
    })

    print("\nMétodo: Secante")
    print("Criterio de error usado:", "cifras significativas" if tipo_error == "cifras" else "decimales correctos")
    print(tabla.to_string(index=False))

    # Resultado final
    if f1 == 0:
        print(f"\n{x1} es raíz de f(x).")
    elif err_vals[-1] is not None and err_vals[-1] < Tol:
        print(f"\n{x1} es aproximación de una raíz con tolerancia {Tol}.")
    else:
        print(f"\nFracaso en {Niter} iteraciones.")