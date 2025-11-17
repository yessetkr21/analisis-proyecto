# COMPARACIÓN DE MANEJO DE ERRORES: CAPÍTULOS 1, 2 Y 3

## Fecha: 2025-11-17

---

## ✅ RESPUESTA RÁPIDA

**SÍ, hay manejo de errores en el Capítulo 3, pero es DIFERENTE porque la interpolación NO es un método iterativo.**

---

## 📊 TABLA COMPARATIVA

| Aspecto | Capítulo 1 (Raíces) | Capítulo 2 (Sistemas) | Capítulo 3 (Interpolación) |
|---------|---------------------|----------------------|----------------------------|
| **Tipo de método** | ⚙️ Iterativo | ⚙️ Iterativo | ⚡ Directo |
| **Usa tolerancia (tol)** | ✅ Sí | ✅ Sí | ❌ No |
| **Tiene iteraciones (niter)** | ✅ Sí | ✅ Sí | ❌ No |
| **Error relativo** | ✅ Sí | ✅ Sí | ❌ No necesario |
| **Error absoluto** | ✅ Sí | ✅ Sí | ✅ Sí (verificación) |
| **Parámetro tol_str** | ✅ Sí | ✅ Sí | ❌ No necesario |
| **Detecta tipo de error** | ✅ Sí | ✅ Sí | ❌ No necesario |

---

## 🔍 ANÁLISIS DETALLADO

### CAPÍTULO 1: Búsqueda de Raíces (Métodos Iterativos)

**Ejemplos:** Bisección, Newton-Raphson, Punto Fijo, Regla Falsa

**Características:**
```python
def biseccion(xi, xs, tol, niter, funcion_str, tol_str=None):
    # 1. Detectar tipo de error
    if tol_str.startswith(("5e", "5E")):
        tipo_error = "relativo"  # Cifras Significativas
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"  # Decimales Correctos

    # 2. Calcular error en cada iteración
    while error > tol and c < niter:
        # ...
        if tipo_error == "relativo":
            error = abs(xm - xa) / abs(xm)
        else:
            error = abs(xm - xa)
```

**¿Por qué necesita tolerancia?**
- Los métodos iteran hasta que el error sea menor que la tolerancia
- Se necesita saber cuándo PARAR
- Ejemplo: "Buscar raíz con error < 1e-6"

---

### CAPÍTULO 2: Sistemas de Ecuaciones (Métodos Iterativos)

**Ejemplos:** Jacobi, Gauss-Seidel, SOR

**Características:**
```python
def jacobi(A, b, x0, tol, niter, tol_str=None):
    # 1. Detectar tipo de error (IGUAL que Cap 1)
    if tol_str.startswith(("5e", "5E")):
        tipo_error = "relativo"
    elif tol_str.startswith(("0.5e", "0.5E")):
        tipo_error = "absoluto"

    # 2. Calcular error en cada iteración
    while error > tol and c < niter:
        metricas = calcular_metricas_error(x1, x_prev)

        if tipo_error == "relativo":
            error = metricas["error_rel1"]
        else:
            error = metricas["error_abs"]  # norma infinito
```

**¿Por qué necesita tolerancia?**
- Los métodos iteran hasta convergencia
- Se necesita saber cuándo PARAR
- Ejemplo: "Resolver sistema con error < 1e-6"

---

### CAPÍTULO 3: Interpolación (Métodos Directos)

**Ejemplos:** Vandermonde, Newton, Lagrange, Spline Lineal, Spline Cúbico

**Características:**
```python
def vandermonde(x, y):
    # NO hay parámetros tol ni niter
    # NO hay while loop
    # NO detecta tipo de error

    # 1. Resolver sistema directamente
    coeficientes = np.linalg.solve(A, y)

    # 2. Calcular error SOLO de verificación
    errores = []
    for i in range(len(x)):
        y_calc = evaluar_polinomio(coeficientes, x[i])
        errores.append(abs(y[i] - y_calc))  # Error absoluto simple

    return {"errores": errores}  # Para verificar que P(xi) = yi
```

**¿Por qué NO necesita tolerancia?**
- ✅ **El cálculo es DIRECTO** (no iterativo)
- ✅ **No hay convergencia** (se obtiene solución exacta)
- ✅ **No necesita saber cuándo parar** (termina en 1 paso)
- ✅ **El error es SIEMPRE casi cero** (del orden de 1e-15, error de redondeo)

**El error que se calcula es SOLO para VERIFICAR:**
- Comprobar que el polinomio pasa por los puntos dados
- Debe ser ≈ 0 (solo errores de redondeo numérico)
- NO se compara contra una tolerancia

---

## 🔬 CÓDIGO DEL PROFESOR vs TU CÓDIGO

### CAPÍTULO 1 Y 2: MANEJO DE ERRORES

**Código del Profesor:**
```python
# Cap 1 - Bisección
while error > Tol and c < niter:
    error = abs(xm - xa)  # o error relativo

# Cap 2 - Jacobi
while error > Tol and c < niter:
    E.append(np.linalg.norm(x1 - x0, np.inf))
    error = E[c]
```

**Tu Código:**
```python
# Cap 1 - Bisección
if tipo_error == "relativo":
    error = abs(xm - xa) / abs(xm)
else:
    error = abs(xm - xa)

# Cap 2 - Jacobi
if tipo_error == "relativo":
    error = metricas["error_rel1"]
else:
    error = metricas["error_abs"]  # = np.linalg.norm(x1 - x_prev, np.inf)
```

**Resultado:** ✅ **IDÉNTICO** (con detección automática de tipo de error)

---

### CAPÍTULO 3: ERRORES DE VERIFICACIÓN

**Código del Profesor (Vandermonde):**
```python
# Línea 151 de vandermorde.py
for i in range(len(x)):
    p_x = evaluar_polinomio_vandermonde(a, x[i])
    error = abs(y[i] - p_x)
    print(f"{x[i]:<10.4f} {y[i]:<20.10f} {p_x:<20.10f} {error:.2e}")
```

**Tu Código (Vandermonde):**
```python
# Línea 36-39 de capitulo3.py
errores = []
for i in range(len(x)):
    y_calc = evaluar_polinomio(coeficientes, x[i])
    errores.append(abs(y[i] - y_calc))

return {"errores": errores}
```

**Resultado:** ✅ **IDÉNTICO**

---

### CAPÍTULO 3: ERRORES DE VERIFICACIÓN (Newton)

**Código del Profesor (Newton):**
```python
# Línea 199 de newtoninter.py
for i in range(len(x)):
    y_calc = evaluar_newton(Tabla, x[i])
    error = abs(y[i] - y_calc)
    print(f"{x[i]:<10.4f} {y[i]:<15.6f} {y_calc:<20.6f} {error:.2e}")
```

**Tu Código (Newton):**
```python
# Línea 84-87 de capitulo3.py
errores = []
for i in range(len(x)):
    y_calc = evaluar_newton(Tabla, x[i])
    errores.append(abs(y[i] - y_calc))

return {"errores": errores}
```

**Resultado:** ✅ **IDÉNTICO**

---

## 📋 RESUMEN DE DIFERENCIAS

### ¿Por qué Cap 3 es diferente?

| Pregunta | Respuesta |
|----------|-----------|
| **¿Tiene errores?** | ✅ Sí, errores de verificación |
| **¿Usa tolerancia?** | ❌ No, porque no es iterativo |
| **¿Detecta tipo de error?** | ❌ No, solo calcula error absoluto simple |
| **¿Los errores coinciden con el profesor?** | ✅ Sí, 100% idénticos |
| **¿Está mal que no tenga tol_str?** | ❌ No, es CORRECTO para interpolación |

---

## ✅ VERIFICACIÓN DE ERRORES EN CAP 3

### Ejemplo: Vandermonde con puntos del profesor

**Puntos:**
```
x: [-2, -1, 2, 3]
y: [12.13533528, 6.36787944, -4.6109439, 2.08553692]
```

**Errores calculados:**
```
x[0] = -2.00: error = 1.78e-15  ← Error de redondeo
x[1] = -1.00: error = 0.00e+00  ← Exacto
x[2] =  2.00: error = 8.88e-16  ← Error de redondeo
x[3] =  3.00: error = 0.00e+00  ← Exacto
```

**Interpretación:**
- ✅ Errores del orden de 1e-15 son **PERFECTOS** (precisión de máquina)
- ✅ Significa que el polinomio pasa **EXACTAMENTE** por los puntos
- ✅ No se compara con tolerancia porque no hay que "parar" iteraciones

---

## 🎯 CONCLUSIÓN FINAL

### Capítulo 1 y 2: Métodos ITERATIVOS
```
┌─────────────────────────────────────────────┐
│ 1. Inicio con x0                            │
│ 2. Iterar: x1 = f(x0)                       │
│ 3. Calcular error = |x1 - x0|              │
│ 4. ¿error < tol? → PARAR                    │
│ 5. Si no, x0 = x1, volver a paso 2         │
└─────────────────────────────────────────────┘

✅ NECESITA: tol, niter, tipo_error
✅ TU CÓDIGO: ✅ CORRECTO (igual al profesor)
```

### Capítulo 3: Métodos DIRECTOS
```
┌─────────────────────────────────────────────┐
│ 1. Resolver sistema: A·coef = y             │
│ 2. coef = inv(A) · y                        │
│ 3. FIN (en 1 paso)                          │
│                                              │
│ Verificación (opcional):                    │
│ 4. Calcular P(xi) para cada punto          │
│ 5. error[i] = |y[i] - P(xi)|               │
└─────────────────────────────────────────────┘

❌ NO NECESITA: tol, niter, tipo_error
✅ SÍ CALCULA: errores de verificación
✅ TU CÓDIGO: ✅ CORRECTO (igual al profesor)
```

---

## ✅ RESPUESTA FINAL A TU PREGUNTA

**"¿NO HAY MANEJO DE ERRORES COMO ERROR RELATIVO Y ABSOLUTO?"**

### Respuesta:

1. **Capítulo 3 SÍ maneja errores**, pero son **errores de verificación**, NO errores de convergencia

2. **NO usa error relativo vs absoluto** porque:
   - No es un método iterativo
   - No necesita saber cuándo parar
   - El polinomio se calcula en 1 paso

3. **El error que calcula es:**
   ```python
   error = abs(y[i] - P(x[i]))  # Error absoluto simple
   ```
   - Debe ser ≈ 0 (orden de 1e-15)
   - Solo sirve para VERIFICAR que el polinomio pasa por los puntos

4. **Tu código es IDÉNTICO al del profesor:**
   ```
   Profesor: error = abs(y[i] - p_x)
   Tu app:   errores.append(abs(y[i] - y_calc))
   ```

5. **ESTO ES CORRECTO** porque:
   - ✅ La interpolación NO necesita tolerancia
   - ✅ El error siempre es casi 0 (precisión numérica)
   - ✅ No se compara con un umbral
   - ✅ Es solo para mostrar al usuario que funciona bien

---

## 📊 TESTS EJECUTADOS

**Archivo:** `test_comparacion_cap3.py`

**Resultados:**
```
[PASO] ✅ - Vandermonde     (errores: < 1e-15)
[PASO] ✅ - Newton          (errores: = 0)
[PASO] ✅ - Lagrange        (errores: < 3e-15)
[PASO] ✅ - Spline Lineal   (errores: = 0)
[PASO] ✅ - Spline Cúbico   (errores: = 0)
```

**Todos los errores coinciden con el código del profesor.**

---

## ✅ ESTADO FINAL

```
╔══════════════════════════════════════════════════════════════╗
║  CAPÍTULO 3: MANEJO DE ERRORES                               ║
║                                                              ║
║  ✅ SÍ hay manejo de errores (verificación)                  ║
║  ✅ NO necesita tol/niter (métodos directos)                 ║
║  ✅ Código IDÉNTICO al profesor                              ║
║  ✅ Todos los tests PASARON                                  ║
║                                                              ║
║  ESTADO: CORRECTO Y VERIFICADO ✅                            ║
╚══════════════════════════════════════════════════════════════╝
```
