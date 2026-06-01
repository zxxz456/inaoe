"""
arbol.py
========================


Description:
------------
Estructura de un Arbol n-ario (general). Cada nodo guarda un valor y una
lista de hijos de longitud arbitraria. La clase `ArbolNario` ofrece
insercion como hijo de un padre dado, busqueda en profundidad, eliminacion
del nodo (con todo su subarbol) y los recorridos preorden, postorden y por
niveles.


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


class NodoNario:
    """Nodo de un arbol n-ario.

    Guarda un valor, una referencia al padre y una lista de hijos en el
    orden en que se agregaron.
    """

    def __init__(self, valor, padre=None):
        """Inicializa el nodo con su valor y lista de hijos vacia.

        Inputs:
        ------
        valor: Valor almacenado en el nodo.
        padre: Nodo padre o None si es la raiz.

        Returns:
        -------
        None
        """
        self.valor = valor
        self.hijos = []
        self.padre = padre


class ArbolNario:
    """Arbol n-ario (general): los nodos pueden tener cualquier numero de hijos.

    La estructura crece indicando para cada nuevo nodo cual sera su padre.
    La eliminacion borra el nodo y todo su subarbol.
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

    def put(self, valor, padre_valor=None):
        """Inserta un valor como hijo del nodo cuyo valor es `padre_valor`.

        Si el arbol esta vacio y no se indica padre, el valor se convierte
        en la raiz.

        Inputs:
        ------
        valor: Valor a insertar.
        padre_valor: Valor del padre del nuevo nodo (None solo para la raiz).

        Returns:
        -------
        NodoNario | None: El nodo creado o None si el padre no existe.
        """
        if self.root is None:
            if padre_valor is not None:
                return None
            self.root = NodoNario(valor)
            return self.root
        padre = self.search(padre_valor)
        if padre is None:
            return None
        nuevo = NodoNario(valor, padre=padre)
        padre.hijos.append(nuevo)
        return nuevo

    def search(self, valor):
        """Busca un nodo con el valor dado mediante un DFS preorden.

        Inputs:
        ------
        valor: Valor a buscar.

        Returns:
        -------
        NodoNario | None: El primer nodo encontrado o None.
        """
        def dfs(n):
            if n is None:
                return None
            if n.valor == valor:
                return n
            for c in n.hijos:
                r = dfs(c)
                if r is not None:
                    return r
            return None
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
        else:
            n.padre.hijos.remove(n)
        return True

    def preorden(self):
        """Recorrido en preorden (raiz primero, luego cada subarbol hijo).

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
            for c in n.hijos: walk(c)
        walk(self.root)
        return out

    def postorden(self):
        """Recorrido en postorden (los subarboles hijos antes que la raiz).

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
            for c in n.hijos: walk(c)
            out.append(n.valor)
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
            for c in n.hijos:
                q.append(c)
        return out
