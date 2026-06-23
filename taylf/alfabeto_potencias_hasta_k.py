"""
alfabeto_potencias_hasta_k.py
========================


Description:
------------
Variante de ``alfabeto_potencia.py`` que, dado un alfabeto Sigma y un
exponente máximo k, genera todas las potencias del alfabeto desde
Sigma^0 hasta Sigma^k y muestra cada una junto con su cardinalidad.

Recordatorio teórico:
Para un alfabeto Sigma y un entero i >= 0:

    Sigma^i = { a_1 a_2 ... a_i | a_j pertenece a Sigma, 1 <= j <= i }

con la convención Sigma^0 = { epsilon } (la cadena vacía). La
cardinalidad de cada potencia es |Sigma^i| = |Sigma|^i.

Ejemplo de uso:
    >>> potencias = generar_potencias_hasta_k({'a', 'b'}, 2)
    >>> sorted(potencias.keys())
    [0, 1, 2]
    >>> potencias[0]
    {''}
    >>> sorted(potencias[2])
    ['aa', 'ab', 'ba', 'bb']


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       06/05/2026      Creation


"""

from typing import Dict, Iterable, Set

from alfabeto_potencia import (
    cardinalidad,
    generar_potencia_alfabeto,
)


def generar_potencias_hasta_k(
    alfabeto: Iterable[str], k: int
) -> Dict[int, Set[str]]:
    """
    Genera todas las potencias de un alfabeto desde Sigma^0 hasta Sigma^k.

    Construye un diccionario que asocia cada exponente i con el conjunto
    Sigma^i correspondiente, para i = 0, 1, ..., k.

    Parámetros
    ----------
    alfabeto : Iterable[str]
        Conjunto (o iterable) de símbolos del alfabeto.
    k : int
        Exponente máximo (entero no negativo). Se generarán todas las
        potencias desde 0 hasta k inclusive.

    Devuelve
    -------
    Dict[int, Set[str]]
        Diccionario { i : Sigma^i } para i en [0, k].

    Lanza
    -----
    ValueError
        Si k es negativo.
    TypeError
        Si k no es entero o si algún símbolo no es una cadena.

    """
    if not isinstance(k, int):
        raise TypeError(f"k debe ser un entero, se recibió {type(k).__name__}.")
    if k < 0:
        raise ValueError(f"k debe ser no negativo, se recibió k = {k}.")

    sigma = set(alfabeto)
    return {i: generar_potencia_alfabeto(sigma, i) for i in range(k + 1)}


def mostrar_potencias_hasta_k(alfabeto: Iterable[str], k: int) -> None:
    """
    Imprime todas las potencias Sigma^0 ... Sigma^k.

    Para cada i en [0, k] imprime el conjunto Sigma^i junto con su
    cardinalidad |Sigma^i| en una línea propia.

    Parámetros
    ----------
    alfabeto : Iterable[str]
        Conjunto de símbolos del alfabeto.
    k : int
        Exponente máximo, entero no negativo.

    Devuelve
    -------
    None
    """
    sigma = set(alfabeto)
    potencias = generar_potencias_hasta_k(sigma, k)

    print(f"Sigma = {sigma if sigma else '{}'}")
    print(f"k máximo = {k}")
    print("-" * 50)

    for i in range(k + 1):
        conjunto = potencias[i]
        card = cardinalidad(sigma, i)
        repr_conjunto = conjunto if conjunto else "{}"
        print(f"Sigma^{i} = {repr_conjunto}")
        print(f"|Sigma^{i}| = {card}")
        print()


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
    Lee el exponente máximo k desde stdin.

    Solicita un entero no negativo y repite la pregunta hasta obtener
    un valor válido.

    Devuelve
    -------
    int
        Entero no negativo introducido por el usuario.
    """
    while True:
        entrada = input("Introduce el valor máximo de k (entero >= 0): ").strip()
        try:
            k = int(entrada)
            if k < 0:
                print("k debe ser no negativo. Inténtalo de nuevo.")
                continue
            return k
        except ValueError:
            print("Entrada no válida. Debe ser un entero. Inténtalo de nuevo.")


def main() -> None:
    print("=== Generador de Sigma^0, Sigma^1, ..., Sigma^k ===")
    alfabeto = _leer_alfabeto_desde_usuario()
    k = _leer_k_desde_usuario()
    print()
    mostrar_potencias_hasta_k(alfabeto, k)


if __name__ == "__main__":
    main()
