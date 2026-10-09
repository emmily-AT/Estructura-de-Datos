# Laboratorio 3

Estudio experimental que compara tres estructuras de datos para administrar registros de estudiantes: **Lista (arreglo dinámico)**, **Árbol Binario de Búsqueda (ABB)** y **Árbol B+**. Se mide cómo escalan en tiempo de ejecución al crecer el tamaño de los datos (N).

## 1. Problema

Cada estudiante tiene: `id` (único), `nombre`, `edad` y `promedio`. El sistema debe permitir:

1. **Buscar** un estudiante por ID.
2. **Insertar** un nuevo estudiante.
3. **Listar** todos los estudiantes en orden ascendente de ID.

Además se evalúa la **búsqueda por rango** de IDs.

### Descripción de los módulos

**`modelo.py`**
Contiene únicamente la clase `Estudiante`, que representa el registro con el que trabaja todo el sistema. El `id` es la clave de búsqueda y el método `__str__` da un formato legible para imprimir.

**`estructuras.py`**
Es el núcleo del laboratorio. Reúne las tres estructuras de datos con la misma interfaz (`insertar`, `buscar`, `buscar_por_rango`, `listar_ascendente`) para poder compararlas en igualdad de condiciones:
- `SistemaLista`: arreglo dinámico con búsqueda lineal y ordenamiento al listar.
- `SistemaABB`: árbol binario de búsqueda sin balanceo, con recorridos iterativos.
- `SistemaBPlus`: árbol B+ de orden configurable, con hojas enlazadas para rangos y listados rápidos.

**`experimentos.py`**
Es el motor del estudio estadístico. Genera los datos de prueba (IDs aleatorios y ordenados), mide los tiempos de cada operación para cada N con 15 repeticiones, elimina outliers con IQR, calcula media, desviación estándar e IC95, y produce el CSV, las tablas en consola y las gráficas log-log.

**`main.py`**
Es el punto de entrada. Lanza el experimento completo, maneja la interrupción por teclado y los errores inesperados, y muestra un mensaje final con los archivos generados.

## 2. Estructuras implementadas

| Estructura | Inserción | Búsqueda por ID | Rango | Listado ascendente |
|---|---|---|---|---|
| Lista | O(1) (append) | O(N) lineal | O(N + K log K) | O(N log N) (TimSort) |
| ABB (sin balanceo) | O(h) | O(h) | O(h + K) | O(N) inorden |
| Árbol B+ (orden 16) | O(log_B N) | O(log_B N) | O(log_B N + K) | O(N) por hojas enlazadas |

Notas:
- `h` es la altura del ABB: ~log N con IDs aleatorios, pero **O(N)** con IDs ordenados (árbol degenerado).
- `K` es la cantidad de elementos dentro del rango.
- El ABB y el recorrido del B+ son **iterativos** (pila explícita), sin recursión.
- El B+ guarda los registros solo en las hojas, enlazadas por el puntero `siguiente`, y divide nodos llenos de forma proactiva durante el descenso.

## 3. Metodología experimental

| Parámetro | Valor |
|---|---|
| Tamaños N | 100, 500, 1000, 2500, 5000, 7500, 10000 |
| Búsquedas exactas (M) | 1000 por ejecución |
| Consultas por rango | 50, con ancho N/10 |
| Repeticiones | 15 por configuración (N, escenario, estructura) |
| Escenarios | `aleatorio` (IDs sin repetir en [1, 10N]) y `ordenado` (IDs 1..N) |
| Orden del B+ | 16 |
| Reloj | `time.perf_counter()` |

Operaciones medidas: inserción de N estudiantes, M búsquedas exactas, 50 búsquedas por rango y listado ascendente completo.

**Tratamiento estadístico**
- Se eliminan outliers por **rango intercuartílico (IQR)**: se descarta lo que cae fuera de [Q1 − 1.5·IQR, Q3 + 1.5·IQR].
- Con los datos limpios se calcula la **media**, la **desviación estándar muestral** (`ddof=1`) y el **intervalo de confianza al 95 %** (1.96 · σ/√n).
- Las gráficas usan **escala log-log** con barras de error de desviación estándar.

**Limitación a tener en cuenta:** en el escenario `ordenado`, para el ABB con N > 2500 la búsqueda exacta se mide con solo 100 consultas y el tiempo se **extrapola** multiplicando por M/100. Se hizo para evitar tiempos excesivos con el árbol degenerado, por lo que ese valor es una estimación y no una medición directa.



**Resumen para N = 10 000 (promedio, ms)**

| Escenario | Estructura | Inserción | Búsqueda exacta (M=1000) | Rango (50) | Listado |
|---|---|---|---|---|---|
| Aleatorio | Lista | 0.35 | 63.47 | 11.85 | 1.22 |
| Aleatorio | ABB | 7.48 | 0.67 | 0.64 | 0.71 |
| Aleatorio | B+ | 10.76 | 0.90 | 0.32 | 0.07 |
| Ordenado | Lista | 0.34 | 62.32 | 10.21 | 0.30 |
| Ordenado | ABB | 1240.12 | 157.71 | 9.85 | 0.59 |
| Ordenado | B+ | 9.84 | 0.90 | 2.66 | 0.08 |

**Conclusiones**
- **Lista:** la inserción es la más rápida, pero la búsqueda lineal escala mal (~63 ms por 1000 búsquedas con N = 10 000).
- **ABB:** con IDs aleatorios es muy competitivo, pero con IDs ordenados se degenera en una lista enlazada: la inserción pasa a ~1.2 s y la búsqueda se vuelve más lenta que en la lista.
- **B+:** mantiene tiempos estables en ambos escenarios gracias al auto-balanceo, y es el mejor en rango y listado por sus hojas enlazadas.
- La inserción del B+ es algo más costosa que la del ABB aleatorio por el trabajo de dividir nodos.

## 4. Entorno de ejecución

| Componente | Detalle |
|---|---|
| Sistema operativo | macOS (Darwin 25.5.0, arm64) |
| CPU | Arquitectura ARM, 8 núcleos lógicos |
| Python | 3.14.6 |
| Pandas | 3.0.6 |
| NumPy | 2.5.2 |
| Matplotlib | 3.11.2 |


## 5. Uso de Inteligencia Artificial

En este laboratorio se utilizó la IA como herramienta de apoyo, para:
- Redactar este README a partir del código y los resultados.
- Apoyar la explicación de la metodología estadística y del comportamiento de las estructuras.

La ejecución de las pruebas y la revisión de resultados fueron realizados y verificados por mi antes de la implementación. 
