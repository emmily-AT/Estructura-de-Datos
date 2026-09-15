# Librería estándar de Python utilizada para generar hashes
import hashlib

# Librería utilizada para representar gráficamente el árbol en la consola. Se cambia el nombre de Node para diferenciarlo de la clase Node creada para el árbol de Merkle.
from binarytree import Node as NodoBinario


class Node:
    """Representa un nodo del árbol de Merkle."""

    def __init__(self, value):
        """Inicializa un nodo con su valor y sus hijos."""
        self.value = value
        self.left = None
        self.right = None


def transacciones(n):
    """Solicita las transacciones y genera su hash SHA-256.
    Args: n: Cantidad de transacciones que se van a ingresar.
    Returns: Lista con los hashes de las transacciones."""

    hashes = []
    for i in range(n):
        t = input(f"Ingrese la transacción #{i + 1}: ")
        # Se genera el hash SHA-256 de la transacción.
        hash = hashlib.sha256(t.encode()).hexdigest()
        hashes.append(hash)

    return hashes


def construir_nivel(nodos):
    """Construye un nivel superior del árbol de Merkle.
    Args: nodos: Lista de nodos del nivel actual.
    Returns: Lista de nodos correspondientes al nivel superior."""

    # Si hay número impar de nodos, se duplica el último
    if len(nodos) % 2 != 0:
        nodos.append(nodos[-1])

    nivel_superior = []

    # Se recorren los nodos de dos en dos para formar parejas.
    for i in range(0, len(nodos), 2):
        izq, der = nodos[i], nodos[i + 1]
        # Se concatenan los hashes de los nodos hijos.
        combinado = izq.value + der.value
        # Se genera el hash del nuevo nodo padre.
        nuevo_hash = hashlib.sha256(combinado.encode()).hexdigest()
        nuevo_nodo = Node(nuevo_hash)
        # Se conectan los nodos hijos con su nodo padre.
        nuevo_nodo.left = izq
        nuevo_nodo.right = der
        nivel_superior.append(nuevo_nodo)
    return nivel_superior


def arbol(hashes):
    """Construye el árbol de Merkle a partir de los hashes.
    Args: hashes: Lista de hashes de las transacciones.
    Returns: Nodo raíz del árbol de Merkle."""
    # Se crea un nodo por cada hash de las transacciones.
    nodos = [Node(h) for h in hashes]
    # Se construyen niveles hasta obtener un único nodo.
    while len(nodos) > 1:
        nodos = construir_nivel(nodos)
    return nodos[0]


def modificar_bloque(hojas, raiz):
    """Modifica una transacción y reconstruye el árbol.
    Args: hojas: Lista de hashes de las transacciones. raiz: Raíz original del árbol."""

    print("\nModificación de bloque\n")
    bloque = int(input("Que bloque desea modificar (0-4): "))
    transacion = input("Ingrese la transacción modificada: ")
    # Se genera el hash de la nueva transacción.
    hojas[bloque] = hashlib.sha256(transacion.encode()).hexdigest()
    # Se reconstruye el árbol con la transacción modificada.
    raiz_modificada = arbol(hojas)
    print(f"\nRaíz original: {raiz.value}")
    print(f"Raíz modificada: {raiz_modificada.value}")
    # Se muestra el árbol después de la modificación.
    imprimir_arbol(raiz_modificada)


def convertir_a_binario(nodo, longitud_hash=8):
    """Convierte recursivamente un Node (Merkle) a un Node de binarytree."""

    # Caso base de la recursividad.
    if nodo is None:
        return None
    # Se utiliza una parte del hash para facilitar la visualización.
    nodo_bin = NodoBinario(nodo.value[:longitud_hash])
    # Se convierten recursivamente los hijos.
    nodo_bin.left = convertir_a_binario(nodo.left, longitud_hash)
    nodo_bin.right = convertir_a_binario(nodo.right, longitud_hash)
    return nodo_bin


def imprimir_arbol(nodo):
    """Muestra gráficamente el árbol de Merkle."""
    # Se convierte y se muestra el árbol al formato de binarytree.
    raiz_binaria = convertir_a_binario(nodo)
    print(raiz_binaria)


def prueba_inclusion(nodo):
    """Realiza una prueba de inclusión de una transacción.
    La función busca los nodos hermanos de la transacción y utiliza sus hashes para reconstruir la raíz."""
    print("\nPrueba de inclusión bloque 3\n")
    # Lista que almacenará los nodos hermanos encontrados.
    prueba = []
    bloque = input("Ingrese la transacción 3: ")
    bloque = hashlib.sha256(bloque.encode()).hexdigest()
    # Se inicia la reconstrucción desde el hash de la transacción.
    raiz_prueba = bloque

    # Se buscan los hermanos necesarios para la prueba.
    if buscar_hermanos(nodo, bloque, prueba):
        for lado, hermano in prueba:
            # El orden de concatenación depende de la posición del nodo hermano.
            if lado == "izquierda":
                comb = hermano + raiz_prueba
            else:
                comb = raiz_prueba + hermano
            # Se calcula el hash del nivel superior.
            raiz_prueba = hashlib.sha256(comb.encode()).hexdigest()
        # Se compara la raíz reconstruida con la raíz original.
        print(f"La transacción 3 es válida: {raiz_prueba} == {nodo.value}")

    else:
        print(f"La transacción 3 NO es válida: {raiz_prueba} != {nodo.value}")


def buscar_hermanos(nodo, bloque, prueba):
    """Busca recursivamente los hermanos de una transacción.
    Args: nodo: Nodo actual que se está recorriendo.
        bloque: Hash de la transacción que se busca.
        prueba: Lista donde se almacenan los hermanos.
    Returns: True si se encuentra el bloque; False en caso contrario."""

    # Si el nodo no tiene hijos, es una hoja.
    if nodo.left is None and nodo.right is None:
        return nodo.value == bloque

    # Se busca primero en el hijo izquierdo. Si se encuentra allí, el hermano está a la derecha.
    if buscar_hermanos(nodo.left, bloque, prueba):
        prueba.append(("derecha", nodo.right.value))
        return True

    # Si no se encuentra a la izquierda, se busca a la derecha. Si no se encuentra a la izquierda, se busca a la derecha.
    if buscar_hermanos(nodo.right, bloque, prueba):
        prueba.append(("izquierda", nodo.left.value))
        return True

    return False


def menu():
    """Controla el flujo principal del programa."""
    print("\nConstruir árbol\n")
    n = int(input("Ingrese el número de transacciones: "))
    # Se obtienen los hashes de las transacciones.
    hojas = transacciones(n)
    # Se construye el árbol de Merkle.
    raiz = arbol(hojas)
    print(f"Raiz: {raiz.value}")
    imprimir_arbol(raiz)

    # Opciones del experimento
    while True:
        opc = input(
            "\nSeleccione un experimento: \n1. Modificar un bloque \n2. Prueba de inclusión para el bloque 3 \n3. Salir\n"
        )
        match opc:
            case "1":
                modificar_bloque(hojas, raiz)
            case "2":
                prueba_inclusion(raiz)
            case "3":
                break


# Inicia la ejecución del programa.
menu()
