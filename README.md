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

