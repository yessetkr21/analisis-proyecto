# Aplicación de Métodos Numéricos - Proyecto Final

Aplicación web interactiva para ejecutar y comparar métodos numéricos vistos durante el curso de Análisis Numérico.

## Características

- **Capítulo 1 - Búsqueda de Raíces**: Bisección, Regla Falsa, Punto Fijo, Newton-Raphson, Secante y Raíces Múltiples
- **Capítulo 2 - Sistemas de Ecuaciones**: Jacobi, Gauss-Seidel y SOR
- **Capítulo 3 - Interpolación**: Vandermonde, Newton Interpolante, Lagrange, Spline Lineal y Spline Cúbico

### Funcionalidades Principales

- ✅ Interfaz dividida por capítulos
- ✅ Visualización de resultados en tablas y gráficas interactivas
- ✅ Sistema de ayuda al usuario con ejemplos
- ✅ Validación y prevención de errores
- ✅ Informes automáticos de comparación entre métodos
- ✅ Identificación automática del mejor método según criterios de error e iteraciones

## Estructura del Proyecto

```
proyecto-analisis-numerico/
├── app/
│   ├── metodos/
│   │   ├── __init__.py
│   │   ├── capitulo1.py  (Métodos de raíces)
│   │   ├── capitulo2.py  (Sistemas de ecuaciones)
│   │   └── capitulo3.py  (Interpolación)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── cap1.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── capitulo1.html
│   │   ├── capitulo2.html
│   │   └── capitulo3.html
│   └── app.py
├── requirements.txt
└── README.md
```

## Instalación y Ejecución

### 1. Instalar dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
cd app
python app.py
```

La aplicación se iniciará en: **http://localhost:5000**

### 3. Acceder a los capítulos

- **Página principal**: http://localhost:5000
- **Capítulo 1**: http://localhost:5000/capitulo1
- **Capítulo 2**: http://localhost:5000/capitulo2
- **Capítulo 3**: http://localhost:5000/capitulo3

## Uso de la Aplicación

### Capítulo 1: Búsqueda de Raíces

#### Formato de Entrada de Funciones

Usa sintaxis matemática estándar de Python/SymPy:

| Operación | Sintaxis | Ejemplo |
|-----------|----------|---------|
| Potencia | `x**n` | `x**2 - 4` |
| Raíz cuadrada | `sqrt(x)` | `sqrt(x) - 2` |
| Exponencial | `exp(x)` | `exp(x) - 2*x` |
| Logaritmo natural | `log(x)` | `log(x) + x` |
| Seno | `sin(x)` | `sin(x) - x/2` |
| Coseno | `cos(x)` | `cos(x) + x` |
| Tangente | `tan(x)` | `tan(x) - x` |

**Ejemplos de funciones válidas:**
- `x**3 - 2*x - 5`
- `exp(x) - 3*x`
- `sin(x) - x/2`
- `log(x) + x - 1`

#### Parámetros Comunes

- **Xi, Xs**: Límites del intervalo (para métodos de intervalo)
- **x0, x1**: Valores iniciales
- **Tol**: Tolerancia del error
  - Para error relativo: usar notación científica como `5e-7`
  - Para error absoluto: usar número decimal como `0.00001`
- **Niter**: Número máximo de iteraciones

#### Uso del Informe de Comparación

1. Ingresa los parámetros del problema
2. Haz clic en "Comparar Todos los Métodos"
3. La aplicación ejecutará todos los métodos y mostrará:
   - Cuál fue el mejor método (menor número de iteraciones)
   - Tabla comparativa con resultados de cada método
   - Gráfica de la función con las raíces encontradas

### Capítulo 2: Sistemas de Ecuaciones Lineales

#### Formato de Entrada

**Matriz A (coeficientes):**
Usa punto y coma (`;`) para separar filas y comas (`,`) para separar columnas:

```
10,1,1;2,10,1;2,2,10
```

Esto representa:
```
10   1   1
 2  10   1
 2   2  10
```

**Vector b:**
Separa los elementos con comas:
```
12,13,14
```

**Vector inicial x0 (opcional):**
Si no se proporciona, se usa el vector cero.
```
0,0,0
```

#### Parámetros del Método SOR

- **w (Factor de relajación)**: debe estar entre 0 y 2
  - `w < 1`: Subrelajación (convergencia más lenta pero más estable)
  - `w = 1`: Equivalente a Gauss-Seidel
  - `w > 1`: Sobrerelajación (convergencia más rápida)
  - Valor recomendado inicial: `1.5`

#### Interpretación de Resultados

- **Radio Espectral**: Indica si el método convergerá
  - Si < 1: El método converge
  - Si ≥ 1: El método no converge
- **Error**: Norma infinito de la diferencia entre iteraciones
- **Diagonal Dominante**: Si la matriz es diagonalmente dominante, todos los métodos convergen

#### Uso del Informe de Comparación

1. Ingresa la matriz A y el vector b
2. Haz clic en "Comparar Todos los Métodos"
3. La aplicación mostrará:
   - Qué método convergió más rápido
   - Radio espectral de cada método
   - Si la matriz es diagonalmente dominante
   - Solución y número de iteraciones de cada método

### Capítulo 3: Interpolación

#### Formato de Entrada de Puntos

Usa punto y coma (`;`) para separar puntos y coma (`,`) para separar x e y:

```
0,1;1,2.5;2,0.5;3,2;4,3.5
```

Esto representa los puntos:
```
(0, 1)
(1, 2.5)
(2, 0.5)
(3, 2)
(4, 3.5)
```

**Restricciones:**
- Mínimo: 2 puntos
- Máximo: 8 puntos
- No puede haber valores de x repetidos

#### Diferencias entre Métodos

- **Vandermonde, Newton, Lagrange**: Generan el mismo polinomio interpolador (de grado n-1)
- **Spline Lineal**: Interpolación por segmentos lineales (más simple, menos suave)
- **Spline Cúbico**: Interpolación por segmentos cúbicos (más suave, más natural)

#### Uso del Informe de Comparación

1. Ingresa los puntos (x,y)
2. Haz clic en "Comparar Todos los Métodos"
3. La aplicación mostrará:
   - Mejor método según error promedio en puntos originales
   - Gráficas superpuestas de todos los métodos
   - Polinomios o ecuaciones de cada segmento
   - Comparación visual de la suavidad

## Ejemplos de Uso

### Ejemplo 1: Encontrar raíz de f(x) = x³ - 2x - 5

```
Método: Bisección
Función: x**3 - 2*x - 5
Xi: 2
Xs: 3
Tolerancia: 0.00001
Niter: 100
```

### Ejemplo 2: Resolver sistema 3x3 con Jacobi

```
Método: Jacobi
Matriz A: 10,1,1;2,10,1;2,2,10
Vector b: 12,13,14
x0: 0,0,0
Tolerancia: 0.000001
Niter: 100
```

### Ejemplo 3: Interpolación con Spline Cúbico

```
Método: Spline Cúbico
Puntos: 0,1;1,2;2,1.5;3,3;4,2.5
```

## Solución de Problemas

### La aplicación no inicia

- Verifica que todas las dependencias estén instaladas: `pip list`
- Asegúrate de estar en la carpeta `app/` al ejecutar `python app.py`

### Error "Puerto ya en uso"

Si el puerto 5000 está ocupado, edita `app.py` y cambia:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
Por otro puerto, por ejemplo:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error en funciones matemáticas

- Usa siempre `x` como variable
- Usa `**` para potencias, no `^`
- Para funciones como `sin`, `cos`, `exp`, escríbelas en minúsculas

### Gráficas no se muestran

- Verifica que tengas acceso a internet (Plotly se carga desde CDN)
- O descarga Plotly localmente y modifica las plantillas HTML

## Créditos

Proyecto Final - Análisis Numérico
Universidad: [Tu Universidad]
Año: 2025

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.
