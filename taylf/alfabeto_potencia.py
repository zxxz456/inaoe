"""
alfabeto_potencia.py
====================

Script para generar la k-ésima potencia de un alfabeto (en el sentido
de teoría de autómatas y lenguajes formales) y calcular la cardinalidad
del conjunto resultante.

En teoría de autómatas, un alfabeto Sigma es un conjunto finito y no
vacío de símbolos. La k-ésima potencia, denotada Sigma^k, es el conjunto
de todas las cadenas de longitud exactamente k que se pueden formar
concatenando símbolos de Sigma:

    Sigma^k = { a_1 a_2 ... a_k | a_i pertenece a Sigma, 1 <= i <= k }

La cardinalidad de Sigma^k es:

    |Sigma^k| = |Sigma|^k

Casos especiales:
    - Si k = 0, Sigma^0 = { epsilon }, donde epsilon es la cadena vacía,
      por lo que |Sigma^0| = 1.
    - Si Sigma es vacío y k > 0, Sigma^k = vacío, con cardinalidad 0.

Ejemplo de uso:
    >>> alfabeto = {'a', 'b'}
    >>> potencia = generar_potencia_alfabeto(alfabeto, 2)
    >>> sorted(potencia)
    ['aa', 'ab', 'ba', 'bb']
    >>> cardinalidad(alfabeto, 2)
    4
"""

from itertools import product
from typing import Iterable, Set


CADENA_VACIA = ""  # epsilon


def generar_potencia_alfabeto(alfabeto: Iterable[str], k: int) -> Set[str]:
    """
    Genera la k-ésima potencia de un alfabeto.

    Construye el conjunto Sigma^k formado por todas las cadenas de
    longitud exactamente k que se pueden obtener concatenando símbolos
    del alfabeto dado.

    Parámetros
    ----------
    alfabeto : Iterable[str]
        Conjunto (o iterable) de símbolos del alfabeto.
    k : int
        Exponente entero no negativo que indica la longitud de las
        cadenas a generar.

    Devuelve
    -------
    Set[str]
        Conjunto con todas las cadenas de longitud k formadas con
        símbolos del alfabeto.

    Lanza
    -----
    ValueError
        Si k es negativo.
    TypeError
        Si algún elemento del alfabeto no es una cadena.

    """
    if not isinstance(k, int):
        raise TypeError(f"k debe ser un entero, se recibió {type(k).__name__}.")
    if k < 0:
        raise ValueError(f"k debe ser no negativo, se recibió k = {k}.")

    alfabeto_set: Set[str] = set()
    for simbolo in alfabeto:
        if not isinstance(simbolo, str):
            raise TypeError(
                f"Todos los símbolos deben ser cadenas; "
                f"se encontró {simbolo!r} de tipo {type(simbolo).__name__}."
            )
        alfabeto_set.add(simbolo)

    if k == 0:
        return {CADENA_VACIA}

    if not alfabeto_set:
        return set()

    return {"".join(tupla) for tupla in product(alfabeto_set, repeat=k)}


def cardinalidad(alfabeto: Iterable[str], k: int) -> int:
    """
    Calcula la cardinalidad de la k-ésima potencia de un alfabeto.

    Aplica la fórmula |Sigma^k| = |Sigma|^k sin construir el conjunto,
    útil para valores de k grandes.

    Parámetros
    ----------
    alfabeto : Iterable[str]
        Conjunto (o iterable) de símbolos del alfabeto.
    k : int
        Exponente entero no negativo.

    Devuelve
    -------
    int
        Número de cadenas distintas de longitud k.

    Lanza
    -----
    ValueError
        Si k es negativo.

    """
    if not isinstance(k, int):
        raise TypeError(f"k debe ser un entero, se recibió {type(k).__name__}.")
    if k < 0:
        raise ValueError(f"k debe ser no negativo, se recibió k = {k}.")

    n = len(set(alfabeto))

    if k == 0:
        return 1

    return n ** k


def mostrar_resultado(alfabeto: Iterable[str], k: int) -> None:
    """
    Imprime Sigma, Sigma^k y |Sigma^k|.

    Parámetros
    ----------
    alfabeto : Iterable[str]
        Conjunto de símbolos del alfabeto.
    k : int
        Exponente entero no negativo.

    Devuelve
    -------
    None
    """
    sigma = set(alfabeto)
    sigma_k = generar_potencia_alfabeto(sigma, k)
    card = cardinalidad(sigma, k)

    print(f"Sigma     = {sigma if sigma else '{}'}")
    print(f"k         = {k}")
    print(f"Sigma^k   = {sigma_k if sigma_k else '{}'}")
    print(f"|Sigma^k| = {card}")


def _leer_alfabeto_desde_usuario() -> Set[str]:
    """
    Lee un alfabeto desde stdin.

    Solicita una lista de símbolos separados por comas y los convierte
    en un conjunto, descartando espacios alrededor de cada símbolo.

    Devuelve
    -------
    Set[str]
        Conjunto de símbolos introducidos por el usuario.
    """
    entrada = input("Introduce los símbolos del alfabeto separados por comas "
                    "(ej. a,b,c): ")
    return {s.strip() for s in entrada.split(",") if s.strip()}


def _leer_k_desde_usuario() -> int:
    """
    Lee el exponente k desde stdin.

    Solicita un entero no negativo y repite la pregunta hasta obtener
    un valor válido.

    Devuelve
    -------
    int
        Entero no negativo introducido por el usuario.
    """
    while True:
        entrada = input("Introduce el valor de k (entero >= 0): ").strip()
        try:
            k = int(entrada)
            if k < 0:
                print("k debe ser no negativo. Inténtalo de nuevo.")
                continue
            return k
        except ValueError:
            print("Entrada no válida. Debe ser un entero. Inténtalo de nuevo.")


def main() -> None:
    print("=== Generador de Sigma^k ===")
    alfabeto = _leer_alfabeto_desde_usuario()
    k = _leer_k_desde_usuario()
    print()
    mostrar_resultado(alfabeto, k)


if __name__ == "__main__":
    main()
