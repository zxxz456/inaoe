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


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       02/10/2026      Pausas del modo paso a paso en cada atomo
zxxz6       30/09/2026      Creation


"""

import numpy as np

import Depuracion
from Omp import omp_matriz
from Utils import (DEPURACION_TOP, ERROR_OMP, ITERACIONES_KSVD,
                   MAX_ATOMOS_OMP, N_ATOMOS, SEMILLA, TOLERANCIA,
                   dispersion_media, error_relativo, normalizar_columnas)


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


def _reiniciar_atomo(d, x, alpha, j, depurador=None):
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
    depurador: Depurador del modo paso a paso, o None

    Returns:
    -------
    None: Modifica d en el lugar

    """
    errores = np.linalg.norm(x - d @ alpha, axis=0)
    peor = int(np.argmax(errores))
    viejo = d[:, j].copy()

    columna = x[:, peor]
    norma = np.linalg.norm(columna)
    if norma > TOLERANCIA:
        d[:, j] = columna / norma

    if depurador is not None:
        depurador.mostrar("atomo", f"atomo {j}: nadie lo usa", [
            "ninguna ventana escogio este atomo en OMP, asi que no hay",
            "residual al cual sacarle la SVD",
            f"se reemplaza por la ventana peor reconstruida, la {peor},",
            f"con error {errores[peor]:.4f}",
            f"atomo viejo: {Depuracion.vector(viejo)}",
            f"atomo nuevo: {Depuracion.vector(d[:, j])}",
        ])


def _mostrar_actualizacion(depurador, j, w, residual, sigma, viejo,
                           nuevo, pesos_viejos, pesos_nuevos):
    """
    Pausa del modo paso a paso despues de actualizar un atomo.
    Muestra con que ventanas se trabajo, el residual, los valores
    singulares y como cambiaron el atomo y sus pesos

    Inputs:
    -------
    depurador: Depurador activo
    j: Indice del atomo
    w: Ventanas que usan el atomo
    residual: Matriz de lo que el atomo tiene que explicar
    sigma: Valores singulares del residual
    viejo: El atomo antes de la SVD
    nuevo: El atomo despues, u_1
    pesos_viejos: Fila j de alpha en las ventanas w, antes
    pesos_nuevos: La misma fila despues, sigma_1 v_1

    Returns:
    -------
    None

    """
    energia = sigma[0] ** 2 / (sigma ** 2).sum()
    producto = float(viejo @ nuevo)
    valores = "  ".join(f"{s:.3f}" for s in sigma[:DEPURACION_TOP])
    lista = ", ".join(str(i) for i in w[:DEPURACION_TOP])
    mas = ", ..." if w.size > DEPURACION_TOP else ""

    lineas = [
        f"1. lo usan {w.size} ventanas: {lista}{mas}",
        "2. residual = lo que esas ventanas no explican sin el atomo",
        "   " + Depuracion.matriz(residual).replace("\n", "\n   "),
        "3. SVD del residual, primeros valores singulares:",
        f"     {valores}",
        f"     sigma_1 carga el {energia:.1%} de la energia del residual",
        "4. atomo nuevo = u_1 (primera columna de U)",
        f"     viejo: {Depuracion.vector(viejo)}",
        f"     nuevo: {Depuracion.vector(nuevo)}",
        f"     |coseno| viejo contra nuevo: {abs(producto):.4f}  "
        f"(1 = no cambio)",
    ]
    # La SVD no fija el signo de u_1. Si sale invertido, los pesos
    # tambien se invierten y el producto atomo por peso es el mismo
    if producto < 0:
        lineas.append("     salio con el signo invertido: los pesos "
                      "tambien se invierten")
    lineas += [
        "5. pesos nuevos = sigma_1 * v_1, uno por ventana que lo usa",
        f"     antes:   {Depuracion.vector(pesos_viejos)}",
        f"     despues: {Depuracion.vector(pesos_nuevos)}",
    ]

    depurador.mostrar("atomo", f"atomo {j}: actualizacion con SVD",
                      lineas)


def actualizar_atomo(d, x, alpha, j, depurador=None):
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
    depurador: Depurador del modo paso a paso, o None

    Returns:
    -------
    bool: True si el atomo se actualizo, False si nadie lo usaba y
          hubo que reiniciarlo

    """
    w = np.flatnonzero(alpha[j, :])
    if w.size == 0:
        _reiniciar_atomo(d, x, alpha, j, depurador)
        return False

    mira = depurador is not None and depurador.quiere("atomo")
    if mira:
        viejo = d[:, j].copy()
        pesos_viejos = alpha[j, w].copy()

    # La fila j se pone a cero para que el residual sea justo lo que
    # el atomo j tendria que explicar
    coeficientes = alpha[:, w].copy()
    coeficientes[j, :] = 0.0
    residual = x[:, w] - d @ coeficientes

    u, sigma, vt = np.linalg.svd(residual, full_matrices=False)

    d[:, j] = u[:, 0]
    alpha[j, w] = sigma[0] * vt[0, :]

    if mira:
        _mostrar_actualizacion(depurador, j, w, residual, sigma, viejo,
                               d[:, j], pesos_viejos, alpha[j, w])

    return True


def ksvd(x, m=N_ATOMOS, iteraciones=ITERACIONES_KSVD,
         error=ERROR_OMP, max_atomos=MAX_ATOMOS_OMP,
         semilla=SEMILLA, verboso=True, depurador=None):
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
    depurador: Depurador del modo paso a paso, o None

    Returns:
    -------
    tuple: (diccionario entrenado, alpha final, lista con un dict por
            iteracion que trae error y dispersion)

    """
    d = diccionario_inicial(x, m, semilla)
    historia = []

    if depurador is not None:
        depurador.mostrar("inicio", "diccionario inicial D_0", [
            f"X de entrenamiento: {x.shape}, una ventana por columna",
            f"D_0 = {m} ventanas de X escogidas al azar, normalizadas",
            "   " + Depuracion.matriz(d).replace("\n", "\n   "),
            f"atomo 0: {Depuracion.vector(d[:, 0])}",
            f"normas de los atomos: min "
            f"{np.linalg.norm(d, axis=0).min():.4f}, max "
            f"{np.linalg.norm(d, axis=0).max():.4f}",
            f"se haran {iteraciones} iteraciones de dos pasos: OMP con D "
            f"fijo, y SVD atomo por atomo",
        ])

    for paso in range(iteraciones):
        if depurador is not None:
            depurador.nueva_iteracion()
            depurador.mostrar("iteracion",
                              f"iteracion {paso + 1} de {iteraciones}", [
                f"paso 1: OMP sobre las {x.shape[1]} ventanas, con D "
                f"fijo -> alpha",
                f"paso 2: actualizar los {m} atomos uno por uno con "
                f"SVD -> D",
                "en cada pausa, s salta lo que queda de ese tipo de paso",
                "en esta iteracion",
            ])
            d_antes = d.copy()

        alpha = omp_matriz(d, x, error, max_atomos, depurador)

        reiniciados = 0
        for j in range(m):
            if not actualizar_atomo(d, x, alpha, j, depurador):
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

        if depurador is not None and depurador.quiere("resumen"):
            # |coseno| de cada atomo contra su version de antes de la
            # iteracion: 1 es que no se movio
            cambio = np.abs(np.sum(d_antes * d, axis=0))
            depurador.mostrar("resumen",
                              f"fin de la iteracion {paso + 1}", [
                f"error de reconstruccion: {paso_actual['error']:.4f}",
                f"atomos por ventana: {paso_actual['dispersion']:.2f}",
                f"atomos reiniciados: {reiniciados}",
                f"como cambio D: |coseno| promedio entre cada atomo y "
                f"su version anterior {cambio.mean():.4f}",
                f"   atomos que casi no cambiaron (> 0.99): "
                f"{(cambio > 0.99).sum()} de {m}",
                f"   atomo que mas cambio: {int(np.argmin(cambio))}, "
                f"|coseno| {cambio.min():.4f}",
            ])

        if verboso:
            print(f"  iteracion {paso + 1:>3}/{iteraciones}   "
                  f"error {paso_actual['error']:.4f}   "
                  f"atomos por senal {paso_actual['dispersion']:5.2f}   "
                  f"reiniciados {reiniciados}")

    if depurador is not None:
        depurador.nueva_iteracion()
        depurador.mostrar("iteracion", "OMP final", [
            "con el diccionario ya entrenado se corre OMP una ultima vez",
            "para obtener el alpha definitivo de cada ventana",
        ])

    alpha = omp_matriz(d, x, error, max_atomos, depurador)

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
