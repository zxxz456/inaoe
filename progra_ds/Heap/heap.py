"""
heap.py
========================


Description:
------------
Estructura de un Monticulo Binario (Binary Heap). Provee la clase `Heap`
que puede comportarse como min-heap (raiz = menor) o max-heap (raiz = mayor)
segun el parametro `es_min` que recibe al construirse. Implementacion sobre
un arreglo: el hijo izquierdo de i esta en 2i+1, el derecho en 2i+2 y el
padre de i en (i-1)//2. Las operaciones de insercion y extraccion usan
`_bubble_up` y `_bubble_down` para restaurar la propiedad de monticulo.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""


class Heap:
    """Monticulo binario (min-heap o max-heap segun construccion).

    Se apoya en un arreglo: la raiz esta en el indice 0 y para cualquier
    nodo en el indice i, su hijo izquierdo es 2i+1, su hijo derecho es
    2i+2 y su padre es (i-1)//2.
    """

    def __init__(self, es_min=True):
        """Crea un monticulo vacio.

        Inputs:
        ------
        es_min: True para min-heap (raiz menor); False para max-heap.

        Returns:
        -------
        None
        """
        self.items = []
        self.es_min = es_min

    def _prioritario(self, a, b):
        """Decide si `a` debe estar por encima de `b` en el monticulo.

        Inputs:
        ------
        a: Valor candidato a estar mas arriba.
        b: Valor con el que se compara.

        Returns:
        -------
        bool: True si `a` tiene mayor prioridad que `b` segun el tipo de heap.
        """
        return a < b if self.es_min else a > b

    def push(self, value):
        """Inserta un valor y restaura la propiedad de monticulo subiendolo.

        Inputs:
        ------
        value: Valor a insertar.

        Returns:
        -------
        None
        """
        self.items.append(value)
        self._bubble_up(len(self.items) - 1)

    def pop(self):
        """Extrae la raiz (minimo o maximo) y reorganiza el monticulo.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: Valor extraido o None si el monticulo esta vacio.
        """
        if not self.items:
            return None
        root = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._bubble_down(0)
        return root

    def peek(self):
        """Devuelve la raiz sin retirarla.

        Inputs:
        ------
        None

        Returns:
        -------
        any | None: La raiz o None si esta vacio.
        """
        return self.items[0] if self.items else None

    def search(self, value):
        """Busca un valor mediante un recorrido lineal por niveles.

        Inputs:
        ------
        value: Valor a buscar.

        Returns:
        -------
        int: Indice donde se encuentra o -1 si no esta.
        """
        for i, v in enumerate(self.items):
            if v == value:
                return i
        return -1

    def _bubble_up(self, i):
        """Sube el elemento en `i` hasta restaurar la propiedad de monticulo.

        Inputs:
        ------
        i: Indice del elemento a subir.

        Returns:
        -------
        None
        """
        while i > 0:
            padre = (i - 1) // 2
            if self._prioritario(self.items[i], self.items[padre]):
                self.items[i], self.items[padre] = self.items[padre], self.items[i]
                i = padre
            else:
                return

    def _bubble_down(self, i):
        """Baja el elemento en `i` hasta restaurar la propiedad de monticulo.

        En cada paso elige el hijo de mayor prioridad y, si supera al padre,
        los intercambia.

        Inputs:
        ------
        i: Indice del elemento a bajar.

        Returns:
        -------
        None
        """
        n = len(self.items)
        while True:
            iz, de = 2 * i + 1, 2 * i + 2
            mejor = i
            if iz < n and self._prioritario(self.items[iz], self.items[mejor]):
                mejor = iz
            if de < n and self._prioritario(self.items[de], self.items[mejor]):
                mejor = de
            if mejor == i:
                return
            self.items[i], self.items[mejor] = self.items[mejor], self.items[i]
            i = mejor

    def size(self):
        """Devuelve el numero de elementos del monticulo.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)

    def __len__(self):
        """Permite usar len(heap) para conocer el numero de elementos.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de elementos almacenados.
        """
        return len(self.items)
