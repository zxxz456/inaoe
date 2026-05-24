"""
bst.py
========================


Description:
------------
Estructura de un Arbol Binario de Busqueda (BST). Contiene las clases
TreeNode y BinarySearchTree usadas como base por el simulador. El metodo
`put` inserta una clave conservando la propiedad de orden del BST: claves
menores a la izquierda, mayores o iguales a la derecha.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""


class TreeNode:
    """Nodo de un arbol binario de busqueda.

    Guarda una clave (`key`) con su valor asociado (`payload`) y los enlaces
    a su hijo izquierdo, su hijo derecho y su padre. Los metodos de consulta
    permiten conocer la posicion del nodo dentro del arbol.
    """

    def __init__(self, key, val, left=None, right=None, parent=None):
        """Inicializa el nodo con su clave, valor y enlaces.

        Inputs:
        ------
        key: Clave que ordena el nodo dentro del arbol.
        val: Valor (payload) asociado a la clave.
        left: Hijo izquierdo (TreeNode) o None.
        right: Hijo derecho (TreeNode) o None.
        parent: Nodo padre (TreeNode) o None si es la raiz.

        Returns:
        -------
        None
        """
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def has_left_child(self):
        """Indica si el nodo tiene hijo izquierdo.

        Inputs:
        ------
        None

        Returns:
        -------
        TreeNode | None: El hijo izquierdo (valor verdadero) o None.
        """
        return self.left_child

    def has_right_child(self):
        """Indica si el nodo tiene hijo derecho.

        Inputs:
        ------
        None

        Returns:
        -------
        TreeNode | None: El hijo derecho (valor verdadero) o None.
        """
        return self.right_child

    def is_left_child(self):
        """Indica si el nodo es el hijo izquierdo de su padre.

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si tiene padre y es su hijo izquierdo.
        """
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        """Indica si el nodo es el hijo derecho de su padre.

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si tiene padre y es su hijo derecho.
        """
        return self.parent and self.parent.right_child == self

    def is_root(self):
        """Indica si el nodo es la raiz del arbol.

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si el nodo no tiene padre.
        """
        return not self.parent

    def is_leaf(self):
        """Indica si el nodo es una hoja (sin hijos).

        Inputs:
        ------
        None

        Returns:
        -------
        bool: True si no tiene hijo izquierdo ni derecho.
        """
        return not (self.right_child or self.left_child)

    def has_any_children(self):
        """Indica si el nodo tiene al menos un hijo.

        Inputs:
        ------
        None

        Returns:
        -------
        TreeNode | None: Un hijo (valor verdadero) o None si es hoja.
        """
        return self.right_child or self.left_child

    def has_both_children(self):
        """Indica si el nodo tiene ambos hijos.

        Inputs:
        ------
        None

        Returns:
        -------
        TreeNode | None: El hijo derecho si existen ambos; None si falta uno.
        """
        return self.right_child and self.left_child

    def replace_node_data(self, key, value, lc, rc):
        """Reemplaza los datos y enlaces del nodo, reajustando los padres.

        Inputs:
        ------
        key: Nueva clave del nodo.
        value: Nuevo valor (payload) del nodo.
        lc: Nuevo hijo izquierdo (TreeNode) o None.
        rc: Nuevo hijo derecho (TreeNode) o None.

        Returns:
        -------
        None
        """
        self.key = key
        self.payload = value
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self


class BinarySearchTree:
    """Arbol binario de busqueda construido sobre nodos TreeNode.

    Mantiene una referencia a la raiz y el numero de nodos. Las inserciones
    conservan la propiedad de orden del BST: las claves menores quedan en el
    subarbol izquierdo y las mayores o iguales en el derecho.
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
        self.size = 0

    def length(self):
        """Devuelve el numero de nodos del arbol.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de nodos almacenados.
        """
        return self.size

    def __len__(self):
        """Permite usar len(arbol) para obtener el numero de nodos.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de nodos almacenados.
        """
        return self.size

    def __iter__(self):
        """Devuelve un iterador sobre el arbol delegando en la raiz.

        Inputs:
        ------
        None

        Returns:
        -------
        iterator: Iterador proporcionado por la raiz del arbol.
        """
        return self.root.__iter__()

    def _put(self, key, val, current_node):
        """Inserta de forma recursiva una clave a partir de un nodo dado.

        Recorre el arbol comparando la clave con cada nodo: baja a la
        izquierda si es menor y a la derecha en caso contrario, hasta
        encontrar el hueco donde crear el nuevo nodo.

        Inputs:
        ------
        key: Clave a insertar.
        val: Valor (payload) asociado a la clave.
        current_node: Nodo desde el que continua la busqueda del lugar.

        Returns:
        -------
        None
        """
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, val, current_node.left_child)
            else:
                current_node.left_child = TreeNode(
                    key, val, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, val, current_node.right_child)
            else:
                current_node.right_child = TreeNode(
                    key, val, parent=current_node)

    def put(self, key, val):
        """Inserta una clave/valor en el arbol e incrementa su tamano.

        Si el arbol esta vacio, la clave se convierte en la raiz; en otro
        caso delega la insercion en `_put`.

        Inputs:
        ------
        key: Clave a insertar.
        val: Valor (payload) asociado a la clave.

        Returns:
        -------
        None
        """
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1
