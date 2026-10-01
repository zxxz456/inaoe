"""
Ksvd.py
========================


Descripcion:
------------
Dictionary Learning con K-SVD: dada una matriz de senales X, aprende
el diccionario D que las representa de la forma mas dispersa posible.

Alterna dos pasos. Con D fijo calcula las dispersiones con OMP; con
las dispersiones fijas actualiza D atomo por atomo. La actualizacion
de cada atomo es una aproximacion de rango 1 del residual, y por eso
se resuelve con una SVD.


Considerations:
------------
- El atomo j y sus coeficientes salen del primer par de vectores
  singulares del residual, porque d_j alpha_j' es columna por renglon,
  o sea rango 1, y la mejor aproximacion de rango 1 la da
  Eckart-Young. Ahi es donde el algoritmo gana su nombre
- La actualizacion se restringe a las senales que ya usaban el atomo.
  Si usara todas, el atomo entraria en senales que no lo tenian y se
  destruiria la dispersion que OMP acababa de construir
- Un atomo que nadie usa deja el residual vacio y la SVD truena. En
  vez de saltarlo se reinicializa con la senal peor reconstruida, que
  es donde mas falta hace un atomo nuevo
- El error de entrenamiento baja monotonamente solo si OMP encuentra
  la solucion optima, que siendo voraz no garantiza. En la practica
  sube de vez en cuando y no es sintoma de un error de programacion


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

from Omp import omp_matriz
from Utils import (ERROR_OMP, ITERACIONES_KSVD, MAX_ATOMOS_OMP,
                   N_ATOMOS, SEMILLA, TOLERANCIA, dispersion_media,
                   error_relativo, normalizar_columnas)


def diccionario_inicial(x, m=N_ATOMOS, semilla=SEMILLA):
    """
    D_0 tomado de las propias senales.
    Arrancar con columnas de X y no con ruido le da a K-SVD un punto
    de partida que ya vive en la zona correcta del espacio, y suele
    converger en menos iteraciones

    Inputs:
    -------
    x: Matriz de senales, k por n
    m: Cuantos atomos tendra el diccionario
    semilla: Para que la corrida sea reproducible

    Returns:
    -------
    ndarray: Diccionario de k por m, columnas de norma 1

    """
    rng = np.random.default_rng(semilla)
    elegidas = rng.choice(x.shape[1], m, replace=x.shape[1] < m)

    return normalizar_columnas(x[:, elegidas].copy())


def _reiniciar_atomo(d, x, alpha, j):
    """
    Repone un atomo que ninguna senal esta usando.
    Lo reemplaza por la senal peor reconstruida, que es el lugar donde
    al diccionario mas le falta cobertura. Dejarlo como estaba lo
    convierte en una columna muerta que nunca se vuelve a elegir

    Inputs:
    -------
    d: Diccionario, se modifica en el lugar
    x: Matriz de senales
    alpha: Matriz de coeficientes actual
    j: Indice del atomo a reponer

    Returns:
    -------
    None: Modifica d en el lugar

    """
    errores = np.linalg.norm(x - d @ alpha, axis=0)
    peor = int(np.argmax(errores))

    columna = x[:, peor]
    norma = np.linalg.norm(columna)
    if norma > TOLERANCIA:
        d[:, j] = columna / norma


def actualizar_atomo(d, x, alpha, j):
    """
    Actualiza un atomo y sus coeficientes con una SVD.
    Toma solo las senales que usan el atomo j, les quita la
    contribucion de ese atomo para ver que queda sin explicar, y pide
    la mejor aproximacion de rango 1 de ese residual. El primer vector
    singular izquierdo es el atomo nuevo y el derecho, escalado por el
    primer valor singular, son sus coeficientes

    Inputs:
    -------
    d: Diccionario, se modifica en el lugar
    x: Matriz de senales
    alpha: Matriz de coeficientes, se modifica en el lugar
    j: Indice del atomo a actualizar

    Returns:
    -------
    bool: True si el atomo se actualizo, False si nadie lo usaba y
          hubo que reiniciarlo

    """
    w = np.flatnonzero(alpha[j, :])
    if w.size == 0:
        _reiniciar_atomo(d, x, alpha, j)
        return False

    # La fila j se pone a cero para que el residual sea justo lo que
    # el atomo j tendria que explicar
    coeficientes = alpha[:, w].copy()
    coeficientes[j, :] = 0.0
    residual = x[:, w] - d @ coeficientes

    u, sigma, vt = np.linalg.svd(residual, full_matrices=False)

    d[:, j] = u[:, 0]
    alpha[j, w] = sigma[0] * vt[0, :]

    return True


def ksvd(x, m=N_ATOMOS, iteraciones=ITERACIONES_KSVD,
         error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP,
         semilla=SEMILLA, verboso=True):
    """
    Entrena el diccionario sobre X.

    Inputs:
    -------
    x: Matriz de senales, k por n, columnas normalizadas
    m: Numero de atomos
    iteraciones: Cuantas pasadas completas se hacen
    error: Error relativo objetivo de OMP
    max_atomos: Tope de atomos por senal en OMP
    semilla: Para que la corrida sea reproducible
    verboso: Si imprime el avance de cada iteracion

    Returns:
    -------
    tuple: (diccionario entrenado, alpha final, lista con un dict por
            iteracion que trae error y dispersion)

    """
    d = diccionario_inicial(x, m, semilla)
    historia = []

    for paso in range(iteraciones):
        alpha = omp_matriz(d, x, error, max_atomos)

        reiniciados = 0
        for j in range(m):
            if not actualizar_atomo(d, x, alpha, j):
                reiniciados += 1

        # El error se queda donde lo deja el criterio de paro de
        # OMP, asi que lo que de verdad mejora con las iteraciones es
        # la dispersion: cuantos atomos hacen falta para ese error
        paso_actual = {
            "error": error_relativo(x, d @ alpha),
            "dispersion": dispersion_media(alpha),
            "reiniciados": reiniciados,
        }
        historia.append(paso_actual)

        if verboso:
            print(f"  iteracion {paso + 1:>3}/{iteraciones}   "
                  f"error {paso_actual['error']:.4f}   "
                  f"atomos por senal {paso_actual['dispersion']:5.2f}   "
                  f"reiniciados {reiniciados}")

    alpha = omp_matriz(d, x, error, max_atomos)

    return d, alpha, historia


def main():
    """
    Prueba sobre datos sinteticos con diccionario conocido.
    Si K-SVD sirve, los atomos aprendidos deben parecerse a los
    originales. La medida es el coseno entre cada atomo verdadero y el
    aprendido mas parecido: cerca de 1 significa que lo recupero, y el
    signo no importa porque un atomo invertido representa igual

    Inputs:
    -------
    None

    Returns:
    -------
    None: Solo imprime

    """
    rng = np.random.default_rng(SEMILLA)
    k, m, n, usados = 20, 50, 1500, 3

    verdadero = normalizar_columnas(rng.standard_normal((k, m)))
    senales = np.column_stack([
        verdadero[:, rng.choice(m, usados, replace=False)]
        @ rng.standard_normal(usados)
        for _ in range(n)])
    senales = normalizar_columnas(senales)

    print(f"diccionario verdadero {k} x {m}, {n} senales de "
          f"{usados} atomos\n")
    d, alpha, historia = ksvd(senales, m=m, iteraciones=15,
                              error=1e-6, max_atomos=usados)

    # Para cada atomo verdadero, que tanto se le parece el aprendido
    # mas cercano. El valor absoluto porque el signo es arbitrario
    parecido = np.abs(verdadero.T @ d).max(axis=1)

    print(f"\nerror {historia[0]['error']:.4f} -> "
          f"{historia[-1]['error']:.4f}")
    print(f"atomos recuperados con coseno > 0.99: "
          f"{(parecido > 0.99).sum()}/{m}")
    print(f"parecido promedio: {parecido.mean():.4f}")


if __name__ == "__main__":
    main()


################################ END OF KSVD.PY ################################
################################################################################
