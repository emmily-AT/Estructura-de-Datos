from modelo import Estudiante


# ==========================================
# 1. LISTA / ARREGLO
# ==========================================
class SistemaLista:
    """Estructura lineal basada en arreglos dinámicos para almacenar estudiantes."""

    def __init__(self):
        self.estudiantes: list[Estudiante] = []  # Lista interna en memoria

    def insertar(self, est: Estudiante):
        # Inserción O(1): agrega el elemento al final del arreglo
        self.estudiantes.append(est)

    def buscar(self, student_id: int) -> Estudiante | None:
        # Búsqueda Lineal O(N): recorre secuencialmente cada elemento hasta hallar la coincidencia
        for est in self.estudiantes:
            if est.id == student_id:
                return est
        return None

    def buscar_por_rango(self, id_inicio: int, id_fin: int) -> list[Estudiante]:
        # Filtrado O(N) para recolectar elementos en el rango e invocación de ordenamiento O(N log N)
        resultado = [est for est in self.estudiantes if id_inicio <= est.id <= id_fin]
        return sorted(resultado, key=lambda x: x.id)

    def listar_ascendente(self) -> list[Estudiante]:
        # Ordenamiento TimSort O(N log N) para devolver los estudiantes ordenados por ID
        return sorted(self.estudiantes, key=lambda x: x.id)


# ==========================================
# 2. ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# ==========================================
class NodoABB:
    """Nodo individual de un Árbol Binario de Búsqueda."""

    def __init__(self, estudiante: Estudiante):
        self.estudiante = estudiante
        self.izq: NodoABB | None = None  # Puntero al subárbol izquierdo (IDs menores)
        self.der: NodoABB | None = None  # Puntero al subárbol derecho (IDs mayores)


class SistemaABB:
    """Árbol Binario de Búsqueda no balanceado con operaciones iterativas."""

    def __init__(self):
        self.raiz: NodoABB | None = None  # Referencia al nodo raíz del árbol

    def insertar(self, est: Estudiante):
        # Inserción Iterativa O(h): h=altura del árbol
        nuevo_nodo = NodoABB(est)
        if not self.raiz:
            self.raiz = nuevo_nodo
            return

        curr = self.raiz
        while True:
            # Desplazamiento a la izquierda si el nuevo ID es menor
            if est.id < curr.estudiante.id:
                if curr.izq is None:
                    curr.izq = nuevo_nodo
                    break
                curr = curr.izq
            # Desplazamiento a la derecha si el nuevo ID es mayor o igual
            else:
                if curr.der is None:
                    curr.der = nuevo_nodo
                    break
                curr = curr.der

    def buscar(self, student_id: int) -> Estudiante | None:
        # Búsqueda Iterativa O(h): desciende por el árbol descartando subárboles
        curr = self.raiz
        while curr:
            if curr.estudiante.id == student_id:
                return curr.estudiante  # Elemento encontrado
            elif student_id < curr.estudiante.id:
                curr = curr.izq  # Buscar en subárbol izquierdo
            else:
                curr = curr.der  # Buscar en subárbol derecho
        return None  # No se encontró el estudiante

    def buscar_por_rango(self, id_inicio: int, id_fin: int) -> list[Estudiante]:
        # Recorrido Inorden Acotado Iterativo utilizando una Pila auxiliar
        resultado = []
        stack = []
        curr = self.raiz

        while curr or stack:
            while curr:
                # Poda a la izquierda: si el nodo actual es menor que id_inicio, se descarta su lado izquierdo
                if curr.estudiante.id >= id_inicio:
                    stack.append(curr)
                    curr = curr.izq
                else:
                    curr = curr.der

            if not stack:
                break

            curr = stack.pop()

            # Evaluación de la clave actual dentro del rango [id_inicio, id_fin]
            if id_inicio <= curr.estudiante.id <= id_fin:
                resultado.append(curr.estudiante)
            elif curr.estudiante.id > id_fin:
                # Poda a la derecha: al superar id_fin en inorden, se detiene la búsqueda
                break

            curr = curr.der

        return resultado

    def listar_ascendente(self) -> list[Estudiante]:
        # Recorrido Inorden Iterativo completo usando Pila: devuelve los elementos en orden ascendente O(N)
        resultado = []
        stack = []
        curr = self.raiz
        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.izq  # Navegar hasta el nodo más a la izquierda
            curr = stack.pop()
            resultado.append(curr.estudiante)  # Procesar nodo
            curr = curr.der  # Navegar a la derecha
        return resultado


# ==========================================
# 3. ÁRBOL B+
# ==========================================
class NodoBPlus:
    """Nodo interno o hoja de un Árbol B+."""

    def __init__(self, es_hoja: bool = False):
        self.es_hoja = es_hoja
        self.claves: list[int] = []  # Lista de IDs ordenados
        self.valores: list[Estudiante] = []  # Registros guardados solo si es_hoja=True
        self.hijos: list[
            NodoBPlus
        ] = []  # Punteros a nodos hijos (solo si es_hoja=False)
        self.siguiente: NodoBPlus | None = (
            None  # Puntero al siguiente nodo hoja (Lista enlazada)
        )


class SistemaBPlus:
    """Árbol B+ multicamino auto-balanceado de orden M."""

    def __init__(self, orden: int = 16):
        self.raiz = NodoBPlus(es_hoja=True)  # La raíz inicia como hoja
        self.orden = orden  # Grado/Orden del árbol (máximo de hijos por nodo)

    def buscar(self, student_id: int) -> Estudiante | None:
        # 1. Navegación descendente O(log_B N) hasta llegar a la hoja correspondiente
        curr = self.raiz
        while not curr.es_hoja:
            i = 0
            while i < len(curr.claves) and student_id >= curr.claves[i]:
                i += 1
            curr = curr.hijos[i]

        # 2. Búsqueda directa dentro de los valores de la hoja
        for i, k in enumerate(curr.claves):
            if k == student_id:
                return curr.valores[i]
        return None

    def buscar_por_rango(self, id_inicio: int, id_fin: int) -> list[Estudiante]:
        # 1. Ubicar la hoja inicial en O(log_B N) navegando desde la raíz
        resultado = []
        curr = self.raiz

        while not curr.es_hoja:
            i = 0
            while i < len(curr.claves) and id_inicio >= curr.claves[i]:
                i += 1
            curr = curr.hijos[i]

        # 2. Recorrido secuencial O(K) usando el puntero 'siguiente' de las hojas
        alcanzado_fin = False
        while curr and not alcanzado_fin:
            for i, clave in enumerate(curr.claves):
                if id_inicio <= clave <= id_fin:
                    resultado.append(curr.valores[i])
                elif clave > id_fin:
                    alcanzado_fin = True  # Fin del rango detectado
                    break
            curr = (
                curr.siguiente
            )  # Avanzar directo al bloque de la siguiente hoja en memoria

        return resultado

    def insertar(self, est: Estudiante):
        # Inserción con división de nodos llena (Proactiva/Top-Down)
        if len(self.raiz.claves) == self.orden - 1:
            # Si la raíz está llena, se crea una nueva raíz y se divide la anterior
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.hijos.append(self.raiz)
            self._dividir_hijo(nueva_raiz, 0, self.raiz)
            self.raiz = nueva_raiz

        curr = self.raiz
        while not curr.es_hoja:
            idx = len(curr.claves) - 1
            while idx >= 0 and est.id < curr.claves[idx]:
                idx -= 1
            idx += 1

            # Dividir hijos llenos durante el descenso
            if len(curr.hijos[idx].claves) == self.orden - 1:
                self._dividir_hijo(curr, idx, curr.hijos[idx])
                if est.id >= curr.claves[idx]:
                    idx += 1
            curr = curr.hijos[idx]

        # Insertar la clave y el registro manteniendo el orden en la hoja objetivo
        idx = 0
        while idx < len(curr.claves) and curr.claves[idx] < est.id:
            idx += 1
        curr.claves.insert(idx, est.id)
        curr.valores.insert(idx, est)

    def _dividir_hijo(self, padre: NodoBPlus, i: int, hijo: NodoBPlus):
        # Método auxiliar para dividir un nodo sobrecargado en dos mitades
        mid = len(hijo.claves) // 2
        nuevo_nodo = NodoBPlus(es_hoja=hijo.es_hoja)

        if hijo.es_hoja:
            # División de nodo hoja: conserva copias de la clave en las hojas
            nuevo_nodo.claves = hijo.claves[mid:]
            nuevo_nodo.valores = hijo.valores[mid:]
            hijo.claves = hijo.claves[:mid]
            hijo.valores = hijo.valores[:mid]
            # Actualizar enlaces entre hojas
            nuevo_nodo.siguiente = hijo.siguiente
            hijo.siguiente = nuevo_nodo
            padre.claves.insert(i, nuevo_nodo.claves[0])
        else:
            # División de nodo interno: promueve la clave media al padre
            nuevo_nodo.claves = hijo.claves[mid + 1 :]
            nuevo_nodo.hijos = hijo.hijos[mid + 1 :]
            clave_promovida = hijo.claves[mid]
            hijo.claves = hijo.claves[:mid]
            hijo.hijos = hijo.hijos[: mid + 1]
            padre.claves.insert(i, clave_promovida)

        padre.hijos.insert(i + 1, nuevo_nodo)

    def listar_ascendente(self) -> list[Estudiante]:
        # Recorrido lineal O(N) desde la primera hoja navegando punto a punto por '.siguiente'
        resultado = []
        curr = self.raiz
        while not curr.es_hoja:
            curr = curr.hijos[0]  # Descender a la primera hoja (más a la izquierda)
        while curr:
            resultado.extend(curr.valores)
            curr = curr.siguiente  # Seguir la cadena secuencial
        return resultado
