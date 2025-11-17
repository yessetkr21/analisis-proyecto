
# Interfaz gráfica para Newton-Raphson
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sympy as sp

def newton_raphson(X0, Tol, Niter, Fun):
	fn = []
	xn = []
	E = []
	N = []
	x = X0
	x_sym = sp.Symbol('x')
	try:
		f_expr = sp.sympify(Fun)
		df_expr = sp.diff(f_expr, x_sym)
		f_lambda = sp.lambdify(x_sym, f_expr, modules=["math"])
		df_lambda = sp.lambdify(x_sym, df_expr, modules=["math"])
		f = f_lambda(x)
		derivada = df_lambda(x)
	except Exception as e:
		return None, f"Error en la función: {e}"
	c = 0
	Error = 100
	fn.append(f)
	xn.append(x)
	E.append(Error)
	N.append(c)
	while Error > Tol and f != 0 and derivada != 0 and c < Niter:
		try:
			x = x - f / derivada
			f = f_lambda(x)
			derivada = df_lambda(x)
		except Exception as e:
			return None, f"Error durante la iteración: {e}"
		fn.append(f)
		xn.append(x)
		c += 1
		Error = abs(xn[c] - xn[c - 1])
		N.append(c)
		E.append(Error)
	resultado = {
		"Iteración": N,
		"xn": xn,
		"f(xn)": fn,
		"Error": E
	}
	if f == 0:
		mensaje = f"{x} es raíz de f(x)"
	elif Error < Tol:
		mensaje = f"{x} es una aproximación de una raíz de f(x) con tolerancia {Tol}"
	else:
		mensaje = f"Fracaso en {Niter} iteraciones"
	return pd.DataFrame(resultado), mensaje

def ejecutar():
	try:
		X0 = float(entry_x0.get())
		Tol = float(entry_tol.get())
		Niter = int(entry_niter.get())
		Fun = entry_fun.get()
	except Exception:
		messagebox.showerror("Error", "Verifica los datos ingresados.")
		return
	df_result, mensaje = newton_raphson(X0, Tol, Niter, Fun)
	label_result.config(text=mensaje)
	for i in tree.get_children():
		tree.delete(i)
	if df_result is not None:
		for idx, row in df_result.iterrows():
			tree.insert("", "end", values=(row["Iteración"], row["xn"], row["f(xn)"], row["Error"]))

root = tk.Tk()
root.title("Método de Newton-Raphson")
root.geometry("900x500")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)

# Entradas
tk.Label(frame, text="X0:").grid(row=0, column=0)
entry_x0 = tk.Entry(frame)
entry_x0.grid(row=0, column=1)

tk.Label(frame, text="Tolerancia:").grid(row=1, column=0)
entry_tol = tk.Entry(frame)
entry_tol.grid(row=1, column=1)

tk.Label(frame, text="Niter:").grid(row=2, column=0)
entry_niter = tk.Entry(frame)
entry_niter.grid(row=2, column=1)

tk.Label(frame, text="Función f(x):").grid(row=3, column=0)
entry_fun = tk.Entry(frame, width=40)
entry_fun.grid(row=3, column=1, columnspan=2)
tk.Label(frame, text="Ejemplo: x**2-2").grid(row=3, column=3)

btn = tk.Button(frame, text="Calcular", command=ejecutar)
btn.grid(row=4, column=0, columnspan=2, pady=10)

label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.pack(pady=5)

columns = ("Iteración", "xn", "f(xn)", "Error")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
	tree.heading(col, text=col)
	tree.column(col, width=120)
tree.pack(side=tk.LEFT, padx=10, pady=10)

# Tabla de ayuda de sintaxis
help_frame = tk.Frame(root)
help_frame.pack(side=tk.LEFT, padx=10, pady=10)
tk.Label(help_frame, text="Ayuda de Sintaxis para f(x)", font=("Arial", 12, "bold")).pack()
help_columns = ("Operación", "Ejemplo")
help_tree = ttk.Treeview(help_frame, columns=help_columns, show="headings", height=8)
for col in help_columns:
	help_tree.heading(col, text=col)
	help_tree.column(col, width=150)
help_tree.pack()
ayuda = [
	("Seno", "sin(x)"),
	("Coseno", "cos(x)"),
	("Tangente", "tan(x)"),
	("Logaritmo", "log(x)"),
	("Exponencial", "exp(x)"),
	("Raíz cuadrada", "sqrt(x)"),
	("Potencia", "x**2"),
	("Valor absoluto", "abs(x)")
]
for op, ej in ayuda:
	help_tree.insert("", "end", values=(op, ej))

tk.Label(help_frame, text="* Usa funciones como en Python/sympy.", font=("Arial", 9)).pack()

root.mainloop()
