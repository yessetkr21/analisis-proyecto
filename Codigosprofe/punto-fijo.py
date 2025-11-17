import pandas as pd
import sympy as sp
import math

def punto_fijo(X0, Tol, Niter, Fun_f, Fun_g):
    """
    Método de punto fijo para encontrar raíces de funciones usando iteración x_{n+1} = g(x_n).

    Parámetros
    ----------
    X0 : float
        Valor inicial.
    Tol : float
        Tolerancia para el error absoluto entre iteraciones consecutivas.
    Niter : int
        Máximo de iteraciones.
    Fun_f : str
        Expresión de la función original f(x) = 0 en sintaxis Sympy.
    Fun_g : str
        Expresión de la función g(x) en sintaxis Sympy para la iteración x_{n+1} = g(x_n).
    """
    # Símbolo y funciones evaluables
    x_sym = sp.Symbol('x')
    try:
        f_expr = sp.sympify(Fun_f)
        g_expr = sp.sympify(Fun_g)
        f_lambda = sp.lambdify(x_sym, f_expr, modules=["math"])
        g_lambda = sp.lambdify(x_sym, g_expr, modules=["math"])
    except Exception as e:
        return None, {"ok": False, "msg": f"Error en las funciones: {e}"}

    # Listas para la tabla
    iteraciones, xn_vals, gxn_vals, fxn_vals, errores = [], [], [], [], []
    
    x_n = X0
    c = 0
    
    while c < Niter:
        try:
            # Calcular f(x_n) y g(x_n)
            f_xn = f_lambda(x_n)
            x_n1 = g_lambda(x_n)
        except Exception as e:
            return None, {"ok": False, "msg": f"Error al evaluar funciones en iteración {c}: {e}"}

        # Calcular error
        if c > 0:
            Error = abs(x_n1 - x_n)
        else:
            Error = abs(x_n1 - x_n)  # Error inicial

        # Guardar fila
        iteraciones.append(c)
        xn_vals.append(x_n)
        gxn_vals.append(x_n1)
        fxn_vals.append(f_xn)
        errores.append(Error)

        # Criterio de paro por tolerancia
        if c > 0 and Error <= Tol:
            break

        # Actualizar para siguiente iteración
        x_n = x_n1
        c += 1

    # Construir DataFrame
    resultado_df = pd.DataFrame({
        'Iteración': iteraciones,
        'x_n': xn_vals,
        'g(x_n)': gxn_vals,
        'f(x_n)': fxn_vals,
        'Error': errores
    })

    # Mensaje/resumen
    xn_final = xn_vals[-1] if xn_vals else X0
    gxn_final = gxn_vals[-1] if gxn_vals else g_lambda(X0)
    err_final = errores[-1] if errores else float('inf')
    
    if c > 0 and err_final <= Tol:
        msg = f"{gxn_final} es una aproximación del punto fijo con tolerancia {Tol}"
        return resultado_df, {"ok": True, "msg": msg, "iter": c, "xn": gxn_final, "gxn": gxn_final, "err": err_final}
    else:
        return resultado_df, {"ok": False, "msg": f"No convergió en {Niter} iteraciones", 
                              "iter": c, "xn": gxn_final, "gxn": gxn_final, "err": err_final}

def main():
    print("=" * 60)
    print("MÉTODO DE PUNTO FIJO")
    print("=" * 60)

    try:
        print("\nIngrese los datos:")
        X0 = float(input("Valor inicial x0: "))
        Tol = float(input("Tolerancia (ej. 1e-5): "))
        Niter = int(input("Número máximo de iteraciones: "))
        Fun_f = input("Función original f(x) = 0 (sintaxis Sympy, ej. exp(x)/x + 3): ")
        Fun_g = input("Función g(x) para iteración x_{n+1} = g(x_n) (sintaxis Sympy, ej. -exp(x)/3): ")

        print("\nDatos ingresados:")
        print(f"Valor inicial: x0 = {X0}")
        print(f"Tolerancia: {Tol}")
        print(f"Máximo de iteraciones: {Niter}")
        print(f"Función original: f(x) = {Fun_f}")
        print(f"Función de iteración: g(x) = {Fun_g}")
        print()

        # Ejecutar punto fijo
        resultado, info = punto_fijo(X0, Tol, Niter, Fun_f, Fun_g)

        if resultado is not None:
            # Formato de salida
            print("RESULTADOS:")
            print("=" * 100)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', 15)

            resultado_formateado = resultado.copy()
            for col in ['x_n', 'g(x_n)', 'f(x_n)', 'Error']:
                resultado_formateado[col] = resultado_formateado[col].apply(lambda x: f"{x:.10f}")
            print(resultado_formateado.to_string(index=False))
            print("=" * 100)

            # Resumen final
            if info.get("ok", False):
                print(f"\n✅ Éxito: {info['msg']}")
            else:
                print(f"\n⚠️  Aviso: {info['msg']}")
            print(f"Iteraciones usadas: {info['iter']}")
            print(f"Punto fijo aproximado: x = {info['xn']:.10f}")
            print(f"g(x) final: {info['gxn']:.10f}")
            print(f"Error final: {info['err']:.10f}")
        else:
            print(f"ERROR: {info['msg']}")

    except ValueError:
        print("ERROR: Entrada inválida. Revisa los números ingresados.")
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

if __name__ == "__main__":
    main()