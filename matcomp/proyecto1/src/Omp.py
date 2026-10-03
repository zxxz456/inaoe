"""
Omp.py
========================


Descripcion:
------------
Orthogonal Matching Pursuit: dado un diccionario D y una senal x,
busca el vector de coeficientes alpha mas disperso tal que
x sea aproximadamente D alpha.

Es un algoritmo voraz. En cada vuelta escoge el atomo mas
correlacionado con lo que falta por explicar, resuelve minimos
cuadrados sobre todos los atomos escogidos hasta el momento, y
actualiza el residual. Para cuando el error relativo baja del umbral
o cuando ya gasto el presupuesto de atomos.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       02/10/2026      Pausas del modo paso a paso en cada vuelta
zxxz6       30/09/2026      Creation


"""

import numpy as np

import Depuracion
from Utils import (DEPURACION_TOP, ERROR_OMP, MAX_ATOMOS_OMP,
                   TOLERANCIA, error_relativo, normalizar_columnas)


def _mostrar_vuelta(depurador, etiqueta, correlacion, nuevo, elegidos,
                    coeficientes, residual, norma_x, error):
    """
    Pausa del modo paso a paso despues de una vuelta de OMP.
    Muestra los candidatos, el atomo que gano, los coeficientes que
    salieron de minimos cuadrados y lo que queda por explicar

    Inputs:
    -------
    depurador: Depurador activo
    etiqueta: Que senal es, por ejemplo "ventana 0 de 2539"
    correlacion: |D' r| de esta vuelta, con los ya elegidos en -1
    nuevo: Indice del atomo que se escogio
    elegidos: Todos los atomos escogidos hasta ahora, en orden
    coeficientes: Pesos de los elegidos, en el mismo orden
    residual: Lo que falta por explicar despues de esta vuelta
    norma_x: Norma de la senal original
    error: Error relativo objetivo

    Returns:
    -------
    None

    """
    top = np.argsort(-correlacion)[:DEPURACION_TOP]
    candidatos = "  ".join(f"{i}:{correlacion[i]:.3f}" for i in top)
    relativo = np.linalg.norm(residual) / norma_x
    sigue = "sigue" if relativo > error else "ya alcanza"

    depurador.mostrar("omp", f"OMP {etiqueta}, vuelta {len(elegidos)}", [
        "1. correlacion |d_i . residual| de cada atomo, los mas altos:",
        f"     {candidatos}",
        f"2. gana el atomo {nuevo}",
        f"3. minimos cuadrados sobre los elegidos {elegidos}:",
        f"     pesos {Depuracion.vector(coeficientes)}",
        "4. residual = x - D_elegidos @ pesos",
        f"     {Depuracion.vector(residual)}",
        f"     error relativo {relativo:.4f} contra objetivo {error} "
        f"-> {sigue}",
    ])


def omp(d, x, error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP,
        depurador=None, etiqueta="senal"):
    """
    Dispersion de una senal sobre un diccionario.
    Devuelve el vector completo de coeficientes, con ceros en los
    atomos que no se usaron, para que se pueda multiplicar por D
    directamente sin reacomodar indices

    Inputs:
    -------
    d: Diccionario de k por m, columnas de norma 1
    x: Senal de longitud k
    error: Error relativo al que se deja de iterar
    max_atomos: Tope de atomos, por si el error nunca baja
    depurador: Depurador del modo paso a paso, o None
    etiqueta: Nombre de la senal en las pausas del depurador

    Returns:
    -------
    tuple: (alpha de longitud m, lista de indices elegidos en orden)

    """
    alpha = np.zeros(d.shape[1])
    elegidos = []
    mira = depurador is not None and depurador.quiere("omp")

    norma_x = np.linalg.norm(x)
    if norma_x < TOLERANCIA:
        return alpha, elegidos

    if mira:
        depurador.mostrar("omp", f"OMP {etiqueta}, inicio", [
            f"senal x: {Depuracion.vector(x)}",
            f"norma de x: {norma_x:.4f}",
            f"diccionario D: {d.shape}",
            f"para cuando el error relativo baje de {error} o use "
            f"{max_atomos} atomos",
            "al inicio el residual es la senal completa",
        ])

    residual = x.astype("float64").copy()
    motivo = f"llego al tope de {max_atomos} atomos"

    while len(elegidos) < max_atomos:
        if np.linalg.norm(residual) / norma_x <= error:
            motivo = f"el error bajo de {error}"
            break

        # A mayor producto interno, mayor correlacion. El valor
        # absoluto porque un atomo invertido explica igual de bien
        correlacion = np.abs(d.T @ residual)
        correlacion[elegidos] = -1.0
        nuevo = int(np.argmax(correlacion))

        if correlacion[nuevo] < TOLERANCIA:
            motivo = "ningun atomo se parece a lo que falta"
            break

        elegidos.append(nuevo)

        # Minimos cuadrados sobre todos los elegidos, no solo el
        # nuevo: eso es lo que hace al metodo ortogonal
        coeficientes, *_ = np.linalg.lstsq(d[:, elegidos], x,
                                           rcond=None)
        residual = x - d[:, elegidos] @ coeficientes

        if mira:
            _mostrar_vuelta(depurador, etiqueta, correlacion, nuevo,
                            elegidos, coeficientes, residual, norma_x,
                            error)

    if elegidos:
        alpha[elegidos] = coeficientes

    if mira:
        depurador.mostrar("omp", f"OMP {etiqueta}, fin", [
            f"se detuvo porque {motivo}",
            f"uso {len(elegidos)} atomos: {elegidos}",
            f"alpha tiene {alpha.size} entradas, "
            f"{np.count_nonzero(alpha)} distintas de cero",
            f"error final {error_relativo(x, d @ alpha):.4f}",
        ])

    return alpha, elegidos


def omp_matriz(d, x, error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP,
               depurador=None):
    """
    Dispersion de todas las senales de una matriz.
    Va columna por columna. Es el paso caro de K-SVD, porque se repite
    en cada iteracion del entrenamiento

    Inputs:
    -------
    d: Diccionario de k por m
    x: Matriz de k por n, una senal por columna
    error: Error relativo al que se deja de iterar cada senal
    max_atomos: Tope de atomos por senal
    depurador: Depurador del modo paso a paso, o None

    Returns:
    -------
    ndarray: Matriz alpha de m por n

    """
    alpha = np.zeros((d.shape[1], x.shape[1]))
    n = x.shape[1]

    for j in range(n):
        alpha[:, j], _ = omp(d, x[:, j], error, max_atomos, depurador,
                             f"ventana {j} de {n}")

    if depurador is not None and depurador.quiere("alpha"):
        usados = np.count_nonzero(alpha, axis=0)
        filas = np.flatnonzero(alpha[:, 0])
        pesos = "  ".join(f"{i}:{alpha[i, 0]:.3f}" for i in filas)
        depurador.mostrar("alpha", "OMP terminado sobre todas las "
                          "ventanas", [
            f"alpha: {alpha.shape}, una columna de pesos por ventana",
            f"atomos por ventana: promedio {usados.mean():.2f}, "
            f"min {usados.min()}, max {usados.max()}",
            f"de {alpha.size} entradas, {np.count_nonzero(alpha)} son "
            f"distintas de cero ({np.count_nonzero(alpha) / alpha.size:.1%})",
            f"ventana 0 usa los atomos (indice:peso): {pesos}",
            f"error de todas las ventanas: "
            f"{error_relativo(x, d @ alpha):.4f}",
        ])

    return alpha


def main():
    """
    Prueba sobre datos sinteticos, donde si se sabe la respuesta.
    Se arma un diccionario al azar, se generan senales usando un
    numero conocido de atomos y se revisa si OMP recupera justo esos.
    Si esto falla, cualquier problema de K-SVD es consecuencia y no
    causa

    Inputs:
    -------
    None

    Returns:
    -------
    None: Solo imprime

    """
    rng = np.random.default_rng(7)
    k, m, n, usados = 40, 100, 300, 5

    d = normalizar_columnas(rng.standard_normal((k, m)))

    aciertos, exactos = 0, 0
    for _ in range(n):
        verdaderos = rng.choice(m, usados, replace=False)
        pesos = rng.standard_normal(usados)
        senal = d[:, verdaderos] @ pesos

        _, elegidos = omp(d, senal, error=1e-6, max_atomos=usados)

        comunes = len(set(elegidos) & set(verdaderos))
        aciertos += comunes
        exactos += comunes == usados

    print(f"diccionario {k} x {m}, {n} senales de {usados} atomos")
    print(f"  atomos recuperados: {aciertos / (n * usados):.2%}")
    print(f"  senales con soporte exacto: {exactos / n:.2%}")

    # Ahora el caso realista: senales dispersas con ruido encima, y
    # el umbral de error que de verdad usa K-SVD. Aqui ya no se busca
    # el soporte exacto sino cuantos atomos pide para llegar al error
    limpias = np.column_stack([
        d[:, rng.choice(m, usados, replace=False)]
        @ rng.standard_normal(usados)
        for _ in range(100)])
    ruidosas = limpias + 0.05 * rng.standard_normal(limpias.shape)

    alpha = omp_matriz(d, ruidosas)
    reconstruida = d @ alpha
    print(f"\nsenales de {usados} atomos mas ruido, "
          f"ERROR_OMP={ERROR_OMP}:")
    print(f"  atomos por senal: "
          f"{np.count_nonzero(alpha, axis=0).mean():.1f}")
    print(f"  error de reconstruccion: "
          f"{error_relativo(ruidosas, reconstruida):.4f}")


if __name__ == "__main__":
    main()


################################ END OF OMP.PY #################################
################################################################################
