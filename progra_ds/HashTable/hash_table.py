"""
hash_table.py
========================


Description:
------------
Estructura de una Tabla Hash con encadenamiento (separate chaining) para
resolver colisiones. Cada cubeta es una lista en la que se almacenan los
pares (clave, valor) cuyo hash apunta a esa posicion. La funcion hash es la
suma de codigos de los caracteres de la clave (o el propio valor si es
entero) modulo el numero de cubetas.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""


class HashTable:
    """Tabla hash con resolucion de colisiones por encadenamiento.

    Cada cubeta es una lista de pares (clave, valor). El indice de cubeta se
    obtiene aplicando la funcion hash a la clave y tomando modulo el numero
    de cubetas.
    """

    def __init__(self, cubetas=7):
        """Crea una tabla hash con `cubetas` cubetas vacias.

        Inputs:
        ------
        cubetas: Numero de cubetas (mejor primo, para mejor distribucion).

        Returns:
        -------
        None
        """
        self.cubetas = cubetas
        self.buckets = [[] for _ in range(cubetas)]
        self.size = 0

    def _hash(self, clave):
        """Funcion hash: suma de codigos modulo el numero de cubetas.

        Para enteros usa el propio valor; para cadenas suma los codigos
        Unicode de los caracteres.

        Inputs:
        ------
        clave: Clave a hashear (int o str).

        Returns:
        -------
        int: Indice de cubeta en [0, cubetas).
        """
        if isinstance(clave, int):
            return abs(clave) % self.cubetas
        return sum(ord(c) for c in str(clave)) % self.cubetas

    def put(self, clave, valor=None):
        """Inserta o actualiza un par (clave, valor) en la tabla.

        Inputs:
        ------
        clave: Clave a insertar.
        valor: Valor asociado (si es None, usa la propia clave).

        Returns:
        -------
        None
        """
        if valor is None:
            valor = clave
        i = self._hash(clave)
        cubeta = self.buckets[i]
        for k, par in enumerate(cubeta):
            if par[0] == clave:
                cubeta[k] = (clave, valor)
                return
        cubeta.append((clave, valor))
        self.size += 1

    def get(self, clave):
        """Devuelve el valor asociado a `clave` o None si no esta.

        Inputs:
        ------
        clave: Clave a buscar.

        Returns:
        -------
        any | None: El valor asociado o None.
        """
        i = self._hash(clave)
        for k, v in self.buckets[i]:
            if k == clave:
                return v
        return None

    def remove(self, clave):
        """Elimina la clave de la tabla.

        Inputs:
        ------
        clave: Clave a eliminar.

        Returns:
        -------
        bool: True si se elimino, False si no estaba.
        """
        i = self._hash(clave)
        cubeta = self.buckets[i]
        for k, par in enumerate(cubeta):
            if par[0] == clave:
                cubeta.pop(k)
                self.size -= 1
                return True
        return False

    def __len__(self):
        """Permite usar len(tabla) para conocer el numero de pares.

        Inputs:
        ------
        None

        Returns:
        -------
        int: Cantidad de pares almacenados.
        """
        return self.size
