"""
arbol_binario.py
========================


Description:
------------
Estructura de un Arbol Binario generico (no ordenado como un BST). Cada
nodo tiene un valor y a lo sumo dos hijos: izquierdo y derecho. La clase
`ArbolBinario` ofrece insercion por nivel (BFS-fill, llena el primer hueco
disponible), busqueda en profundidad, eliminacion del nodo (con todo su
subarbol) y los cuatro recorridos clasicos: preorden, inorden, postorden y
por niveles.


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


class NodoBinario:
    """Nodo de un arbol binario generico.

    Guarda un valor y sus enlaces al hijo izquierdo, al derecho y al padre.
    A diferencia del BST, no se mantiene un orden basado en el valor.
    """

    def __init__(self, valor, padre=None):
        """Inicializa el nodo con su valor y los enlaces vacios.

        Inputs:
        ------
        valor: Valor almacenado en el nodo.
        padre: Nodo padre o None si es la raiz.

        Returns:
        -------
        None
        """
        self.valor = valor
        self.izq = None
        self.der = None
        self.padre = padre


class ArbolBinario:
    """Arbol binario generico construido por relleno por niveles (BFS).

    La insercion coloca cada valor en el primer hueco disponible recorriendo
    el arbol por niveles. La eliminacion borra el nodo y todo su subarbol.
    """

    def __init__(self):
        """Crea un arbol vacio.

        Inputs:
        ------
        None

        Returns:
        -------
        None
        """
        self.root = None

    def put(self, valor):
        """Inserta un valor en el primer hueco libre (BFS).

        Recorre por niveles desde la raiz y coloca el nuevo nodo en el
        primer hijo (izquierdo, luego derecho) que este vacio.

        Inputs:
        ------
        valor: Valor a insertar.

        Returns:
        -------
        None
        """
        if self.root is None:
            self.root = NodoBinario(valor)
            return
        q = deque([self.root])
        while q:
            n = q.popleft()
            if n.izq is None:
                n.izq = NodoBinario(valor, padre=n)
                return
            q.append(n.izq)
            if n.der is None:
                n.der = NodoBinario(valor, padre=n)
                return
            q.append(n.der)

    def search(self, valor):
        """Busca un valor con un recorrido en profundidad (preorden).

        Inputs:
        ------
        valor: Valor a buscar.

        Returns:
        -------
        NodoBinario | None: El primer nodo encontrado o None.
        """
        def dfs(n):
            if n is None:
                return None
            if n.valor == valor:
                return n
            return dfs(n.izq) or dfs(n.der)
        return dfs(self.root)

    def remove(self, valor):
        """Elimina el nodo y todo su subarbol.

        Inputs:
        ------
        valor: Valor del nodo a eliminar.

        Returns:
        -------
        bool: True si se elimino, False si no se encontro.
        """
        n = self.search(valor)
        if n is None:
            return False
        if n.padre is None:
            self.root = None
        elif n.padre.izq is n:
            n.padre.izq = None
        else:
            n.padre.der = None
        return True

    def preorden(self):
        """Recorrido en preorden (raiz, izquierda, derecha).

        Inputs:
        ------
        None

        Returns:
        -------
        list: Valores en el orden de visita.
        """
        out = []
        def walk(n):
            if n is None: return
            out.append(n.valor)
            walk(n.izq); walk(n.der)
        walk(self.root)
        return out

    def inorden(self):
        """Recorrido en inorden (izquierda, raiz, derecha).

        Inputs:
        ------
        None

        Returns:
        -------
        list: Valores en el orden de visita.
        """
        out = []
        def walk(n):
            if n is None: return
            walk(n.izq); out.append(n.valor); walk(n.der)
        walk(self.root)
        return out

    def postorden(self):
        """Recorrido en postorden (izquierda, derecha, raiz).

        Inputs:
        ------
        None

        Returns:
        -------
        list: Valores en el orden de visita.
        """
        out = []
        def walk(n):
            if n is None: return
            walk(n.izq); walk(n.der); out.append(n.valor)
        walk(self.root)
        return out

    def por_niveles(self):
        """Recorrido por niveles (BFS).

        Inputs:
        ------
        None

        Returns:
        -------
        list: Valores en el orden BFS.
        """
        out = []
        if self.root is None:
            return out
        q = deque([self.root])
        while q:
            n = q.popleft()
            out.append(n.valor)
            if n.izq: q.append(n.izq)
            if n.der: q.append(n.der)
        return out
