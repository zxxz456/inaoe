"""
pila.py
========================


Description:
------------
Estructura de una Pila (Stack, LIFO: Last In, First Out). Provee la clase
`Pila` con las operaciones tipicas: `push`, `pop`, `peek`, busqueda,
recorrido y consulta de tamano. Se usa como base por el simulador
interactivo. Internamente los elementos se guardan en una lista; el final
de la lista representa el TOPE de la pila.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""


class Pila:
    """Pila (LIFO): los elementos se insertan y retiran por el TOPE.

    El TOPE es el ultimo elemento insertado y el primero en salir. La base
    de la pila contiene el primer elemento que se inserto y sera el ultimo
    en ser retirado.
    """

    def __init__(self):
        """Crea una pila vacia.

        Inputs:
        ------
        None

        Returns:
        -------
        None
        """
        self.items = []

    def push(self, item):
        """Coloca un elemento en el tope de la pila.

        Inputs:
        ------
        item: Valor a apilar.

        Returns:
        -------
        None
        """
        self.items.append(item)

    def pop(self):
        """Retira y devuelve el elemento del tope.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: El elemento retirado o None si la pila esta vacia.
        """
        if not self.items:
            return None
        return self.items.pop()

    def peek(self):
        """Devuelve el elemento del tope sin retirarlo.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: El elemento del tope o None si la pila esta vacia.
        """
        if not self.items:
            return None
        return self.items[-1]

    def search(self, item):
        """Busca un valor recorriendo desde el TOPE hacia la BASE.

        Inputs:
        ------
        item: Valor a buscar.

        Returns:
        -------
        int: Distancia desde el tope (0 si esta en el tope) o -1 si no esta.
        """
        for i in range(len(self.items) - 1, -1, -1):
            if self.items[i] == item:
                return len(self.items) - 1 - i
        return -1

    def is_empty(self):
        """Indica si la pila esta vacia.

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si no hay elementos.
        """
        return len(self.items) == 0

    def size(self):
        """Devuelve el numero de elementos en la pila.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)

    def __len__(self):
        """Permite usar len(pila) para conocer el numero de elementos.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)
