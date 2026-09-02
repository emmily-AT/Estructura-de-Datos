# Estructura de Datos - Laboratorio 1

**Nombre:** Emmily Andrea Alvarez Tobón

## Descripción

Este repositorio contiene el desarrollo del **Laboratorio 1 de Estructura de Datos**.

El laboratorio consiste en la creación y manejo de una matriz binaria de gran tamaño, utilizando almacenamiento en disco para evitar que toda la matriz tenga que mantenerse en la memoria RAM.

La matriz tiene **100000 filas y 100000 columnas**, con valores de tipo `uint8`, que corresponden a valores binarios (`0` y `1`).

Para solucionar el problema de memoria se utiliza `NumPy` junto con `np.memmap`, que permite trabajar con una matriz almacenada directamente en un archivo del disco.

## Objetivos

El código desarrollado debe resolver los siguientes problemas planteados en el laboratorio:

* **Consumo excesivo de RAM.**
* **Escritura lenta a disco.**
* **Optimización en la manipulación, creación, almacenamiento y lectura de datos.**


## Solución implementada

Para manejar la matriz de gran tamaño se utiliza `np.memmap`.

Esta herramienta permite acceder a los datos del archivo como si fueran una matriz de NumPy, sin necesidad de cargar toda la información en la RAM.

Además, durante la creación de la matriz se trabaja por **bloques de 10000 filas**:

```python
for i in range(0, filas, tamano_bloque):
```

De esta manera, los datos se generan y escriben por partes en lugar de crear toda la matriz en memoria.

Cada bloque contiene valores aleatorios entre `0` y `1`, que corresponden a los valores de la matriz binaria.

## Archivos del repositorio

| Archivo              | Descripción                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `matriz.py`          | Código principal del laboratorio. Contiene las funciones para crear, consultar, verificar y exportar información de la matriz. |
| `README.md`          | Documento con la explicación del laboratorio, funcionamiento del código y forma de verificar la matriz.                        |

## Funciones

| Función                        | Descripción                                                                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crear_matriz_binaria()`       | Crea la matriz binaria y la almacena directamente en el disco utilizando `np.memmap`. La matriz se genera por bloques para reducir el consumo de RAM. |
| `mostrar_informacion_matriz()` | Abre la matriz almacenada y muestra sus filas, columnas, cantidad de elementos, tipo de dato y tamaño del archivo.                                    |
| `consultar_celda()`            | Permite consultar el valor almacenado en una posición específica de la matriz indicando la fila y la columna.                                         |
| `exportar_fila_a_txt()`        | Selecciona una fila completa de la matriz y la guarda en un archivo `.txt`.                                                                           |
| `main()`                       | Contiene el flujo principal del programa y permite al usuario seleccionar la operación que desea realizar.                                            |

## Requisitos

Para ejecutar el programa se necesita:

* **Python 3.10 o superior**, debido al uso de `match/case`.
* **NumPy**.
* Aproximadamente **10 GB de espacio disponible en disco** para almacenar la matriz.

