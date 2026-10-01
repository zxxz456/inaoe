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


Considerations:
------------
- El "orthogonal" del nombre viene de resolver minimos cuadrados sobre
  TODO el conjunto elegido en cada vuelta, no solo de restar el atomo
  nuevo. Eso deja el residual ortogonal al espacio generado por los
  atomos elegidos, y por eso ninguno se repite
- Se usa lstsq y no la pseudoinversa explicita: las slides escriben
  (D_I)^-1, pero D_I es alta y rectangular y no tiene inversa. Lo que
  se resuelve ahi es un problema de minimos cuadrados
- alpha = D' x no sirve como atajo. Solo invierte x = D alpha cuando D
  es ortogonal, y aqui es sobrecompleto a proposito
- El paro por MAX_ATOMOS_OMP no es decorativo: sin el, una senal
  ruidosa sigue pidiendo atomos hasta volver densa la representacion,
  que es justo lo contrario de lo que se busca


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       30/09/2026      Creation


"""

import numpy as np

from Utils import (ERROR_OMP, MAX_ATOMOS_OMP, TOLERANCIA,
                   error_relativo,
                   normalizar_columnas)


def omp(d, x, error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP):
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

    Returns:
    -------
    tuple: (alpha de longitud m, lista de indices elegidos en orden)

    """
    alpha = np.zeros(d.shape[1])
    elegidos = []

    norma_x = np.linalg.norm(x)
    if norma_x < TOLERANCIA:
        return alpha, elegidos

    residual = x.astype("float64").copy()

    while len(elegidos) < max_atomos:
        if np.linalg.norm(residual) / norma_x <= error:
            break

        # A mayor producto interno, mayor correlacion. El valor
        # absoluto porque un atomo invertido explica igual de bien
        correlacion = np.abs(d.T @ residual)
        correlacion[elegidos] = -1.0
        nuevo = int(np.argmax(correlacion))

        if correlacion[nuevo] < TOLERANCIA:
            break

        elegidos.append(nuevo)

        # Minimos cuadrados sobre todos los elegidos, no solo el
        # nuevo: eso es lo que hace al metodo ortogonal
        coeficientes, *_ = np.linalg.lstsq(d[:, elegidos], x,
                                           rcond=None)
        residual = x - d[:, elegidos] @ coeficientes

    if elegidos:
        alpha[elegidos] = coeficientes

    return alpha, elegidos


def omp_matriz(d, x, error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP):
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

    Returns:
    -------
    ndarray: Matriz alpha de m por n

    """
    alpha = np.zeros((d.shape[1], x.shape[1]))

    for j in range(x.shape[1]):
        alpha[:, j], _ = omp(d, x[:, j], error, max_atomos)

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
