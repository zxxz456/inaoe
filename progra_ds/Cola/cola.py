"""
cola.py
========================


Description:
------------
Estructura de una Cola (Queue, FIFO: First In, First Out). Provee la clase
`Cola` con las operaciones tipicas: `enqueue`, `dequeue`, `peek`, busqueda,
recorrido y consulta de tamano. Se usa como base por el simulador
interactivo. Internamente los elementos se guardan en una lista; el inicio
de la lista representa el FRENTE de la cola y el final, el FONDO.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""

from collections import deque


class Cola:
    """Cola (FIFO): los elementos entran por el FONDO y salen por el FRENTE.

    El primero en entrar es el primero en salir. Se apoya en `collections.deque`
    para que las operaciones de retiro por el frente sean eficientes.
    """

    def __init__(self):
        """Crea una cola vacia.

        Inputs:
        ------
        None

        Returns:
        -------
        None
        """
        self.items = deque()

    def enqueue(self, item):
        """Encola un elemento al final (fondo) de la cola.

        Inputs:
        ------
        item: Valor a encolar.

        Returns:
        -------
        None
        """
        self.items.append(item)

    def dequeue(self):
        """Retira y devuelve el elemento del frente de la cola.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: El elemento retirado o None si la cola esta vacia.
        """
        if not self.items:
            return None
        return self.items.popleft()

    def peek(self):
        """Devuelve el elemento del frente sin retirarlo.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: El elemento del frente o None si la cola esta vacia.
        """
        if not self.items:
            return None
        return self.items[0]

    def search(self, item):
        """Busca un valor recorriendo desde el FRENTE hacia el FONDO.

        Inputs:
        ------
        item: Valor a buscar.

        Returns:
        -------
        int: Posicion desde el frente (0 si esta en el frente) o -1 si no esta.
        """
        for i, v in enumerate(self.items):
            if v == item:
                return i
        return -1

    def is_empty(self):
        """Indica si la cola esta vacia.

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si no hay elementos.
        """
        return len(self.items) == 0

    def size(self):
        """Devuelve el numero de elementos en la cola.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)

    def __len__(self):
        """Permite usar len(cola) para conocer el numero de elementos.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)
