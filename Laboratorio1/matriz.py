import os

import numpy as np


def crear_matriz_binaria(
    nombre_archivo,
    filas,
    columnas,
    tipo_dato,
    tamano_bloque=10000,
):
    # Verificamos si la matriz ya fue creada anteriormente
    if os.path.exists(nombre_archivo):
        print(f"El archivo '{nombre_archivo}' ya existe. Saltando creación.")
        return

    # Creamos la matriz directamente en el disco
    print("Creando matriz directamente en disco...")
    matriz = np.memmap(
        nombre_archivo, dtype=tipo_dato, mode="w+", shape=(filas, columnas)
    )

    # Vamos llenando la matriz por bloques para no cargarla toda en memoria
    for i in range(0, filas, tamano_bloque):
        # Calculamos hasta qué fila llega el bloque actual
        fin = min(i + tamano_bloque, filas)

        # Llenamos el bloque con números aleatorios entre 0 y 1
        matriz[i:fin, :] = np.random.randint(
            0, 2, size=(fin - i, columnas), dtype=tipo_dato
        )

        # Guardamos los cambios en el archivo
        matriz.flush()

    # Cerramos la matriz que estaba conectada al archivo
    del matriz
    print(f"Matriz creada exitosamente: {nombre_archivo}")


def mostrar_informacion_matriz(
    nombre_archivo,
    filas,
    columnas,
    tipo_dato,
):
    # Abrimos la matriz que está guardada en el disco
    matriz_lectura = np.memmap(
        nombre_archivo, dtype=tipo_dato, mode="r", shape=(filas, columnas)
    )

    # Obtenemos las dimensiones directamente de la matriz
    filas_matriz, columnas_matriz = matriz_lectura.shape

    # Calculamos la cantidad total de elementos
    total_elementos = matriz_lectura.size

    # Obtenemos el tamaño real del archivo
    tamano_bytes = os.path.getsize(nombre_archivo)
    tamano_gb = tamano_bytes / (1024**3)

    print("\n--- Información de la matriz ---")
    print(f"Archivo: {nombre_archivo}")
    print(f"Filas: {filas_matriz}")
    print(f"Columnas: {columnas_matriz}")
    print(f"Total de elementos: {total_elementos}")
    print(f"Tipo de dato: {matriz_lectura.dtype}")
    print(f"Tamaño del archivo: {tamano_gb:.2f} GB")

    # Cerramos la matriz
    del matriz_lectura


def consultar_celda(
    num_fila,
    num_columna,
    nombre_archivo,
    filas,
    columnas,
    tipo_dato,
):
    # Abrimos la matriz que está guardada en el archivo
    matriz_lectura = np.memmap(
        nombre_archivo, dtype=tipo_dato, mode="r", shape=(filas, columnas)
    )

    # Obtenemos el valor de la posición indicada
    valor = matriz_lectura[num_fila, num_columna]

    # Cerramos el archivo
    del matriz_lectura

    # Mostramos el valor encontrado
    print(f"Valor en ({num_fila}, {num_columna}): {valor}")
    return valor


def exportar_fila_a_txt(
    num_fila,
    nombre_archivo,
    filas,
    columnas,
    tipo_dato,
):
    # Abrimos la matriz guardada en el archivo
    matriz_lectura = np.memmap(
        nombre_archivo, dtype=tipo_dato, mode="r", shape=(filas, columnas)
    )

    # Seleccionamos la fila que queremos guardar
    fila_seleccionada = matriz_lectura[num_fila, :]
    nombre_txt = f"fila_{num_fila}.txt"

    print(f"Guardando datos en '{nombre_txt}'...")

    # Convertimos la fila en una cadena de texto
    cadena_fila = np.array2string(
        fila_seleccionada,
        threshold=columnas,
        max_line_width=columnas + 10,
        separator="",
    )[1:-1]

    # Creamos el archivo TXT y guardamos la fila
    with open(nombre_txt, "w") as f:
        f.write(cadena_fila + ",")

    # Cerramos la matriz
    del matriz_lectura
    print("¡Fila exportada con éxito!")


def main():
    # Definimos los datos principales de la matriz
    nombre_archivo = "matriz_binaria.dat"
    filas = 100000
    columnas = 100000
    tipo_dato = "uint8"

    # Creamos la matriz
    crear_matriz_binaria(nombre_archivo, filas, columnas, tipo_dato)

    # Mostramos las opciones que puede elegir el usuario
    print("\n--- Opciones de Consulta ---")
    print("1. Consultar información de la matriz)")
    print("2. Consultar una celda específica (fila, columna)")
    print("3. Exportar una fila completa a TXT")

    # Le pedimos al usuario que seleccione una opción
    opcion = input("Selecciona una opción (1 o 2): ")

    match opcion:
        case "1":
            # Verificamos la información de la matriz
            mostrar_informacion_matriz(nombre_archivo, filas, columnas, tipo_dato)

        case "2":
            # Pedimos la fila y columna que quiere consultar
            f = int(input(f"Fila (0-{filas - 1}): "))
            c = int(input(f"Columna (0-{columnas - 1}): "))

            # Consultamos el valor de esa posición
            consultar_celda(f, c, nombre_archivo, filas, columnas, tipo_dato)

        case "3":
            # Pedimos la fila que quiere exportar
            f = int(input(f"Fila a exportar (0-{filas - 1}): "))

            # Exportamos la fila a un archivo TXT
            exportar_fila_a_txt(f, nombre_archivo, filas, columnas, tipo_dato)


# Ejecutamos el programa empezando desde main()
if __name__ == "__main__":
    main()
