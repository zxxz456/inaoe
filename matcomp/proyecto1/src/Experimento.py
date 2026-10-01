"""
Experimento.py
========================


Descripcion:
------------
Corrida completa del proyecto: baja el ECG, arma X, entrena el
diccionario con K-SVD y guarda el resultado en out/.

Es el punto de entrada. Deja en disco el diccionario entrenado, los
coeficientes, el historial de error y la senal original, para que las
figuras del reporte se generen sin volver a entrenar.


Considerations:
------------
- El entrenamiento se hace sobre la primera mitad de las ventanas y
  la evaluacion sobre la segunda. Medir el error sobre las mismas
  senales con las que se entreno no dice si el diccionario generaliza,
  solo si memorizo
- La curva de error contra numero de atomos se calcula variando
  max_atomos en OMP con el diccionario ya entrenado, no reentrenando
- Todo se guarda en un solo .npz para que Figuras.py no dependa del
  orden en que se corran las cosas


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       30/09/2026      Creation


"""

import os
import time

import numpy as np

from Datos import cargar_ecg, construir_x
from Ksvd import ksvd
from Omp import omp_matriz
from Utils import (ERROR_OMP, ITERACIONES_KSVD, MAX_ATOMOS_OMP,
                   N_ATOMOS, REGISTRO, RUTA_SALIDA, TAM_VENTANA,
                   dispersion_media, error_relativo)

ARCHIVO_MODELO = f"{RUTA_SALIDA}/modelo.npz"
ATOMOS_CURVA = (1, 2, 4, 6, 8, 10, 12, 16, 24, 32)


def partir_entrenamiento(x, fraccion=0.5):
    """
    Separa X en entrenamiento y prueba por posicion.
    El corte es temporal y no aleatorio: las ventanas contiguas de un
    ECG se parecen mucho entre si, y repartirlas al azar dejaria en
    prueba vecinas directas de las de entrenamiento, lo que infla el
    resultado

    Inputs:
    -------
    x: Matriz de senales, k por n
    fraccion: Que parte se usa para entrenar

    Returns:
    -------
    tuple: (X de entrenamiento, X de prueba)

    """
    corte = int(x.shape[1] * fraccion)

    return x[:, :corte], x[:, corte:]


def curva_error(d, x, atomos=ATOMOS_CURVA):
    """
    Error de reconstruccion segun cuantos atomos se permiten.
    Es la version medible de la figura de las slides, donde la senal
    se reconstruye con 4, 6, 8, 10 y 13 formas de onda

    Inputs:
    -------
    d: Diccionario entrenado
    x: Matriz de senales a reconstruir
    atomos: Topes de atomos a probar

    Returns:
    -------
    list: Un dict por tope, con atomos permitidos, usados y error

    """
    filas = []
    for tope in atomos:
        alpha = omp_matriz(d, x, error=0.0, max_atomos=tope)
        filas.append({
            "permitidos": tope,
            "usados": dispersion_media(alpha),
            "error": error_relativo(x, d @ alpha),
        })

    return filas


def main():
    """
    Entrena y guarda. Imprime el avance y el resumen final.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Escribe out/modelo.npz

    """
    os.makedirs(RUTA_SALIDA, exist_ok=True)

    senal, fs = cargar_ecg()
    x = construir_x(senal)
    entrena, prueba = partir_entrenamiento(x)

    print(f"registro {REGISTRO}: {len(senal)} muestras a {fs} Hz")
    print(f"X de {x.shape[0]} x {x.shape[1]}, ventanas de "
          f"{TAM_VENTANA} muestras")
    print(f"  entrenamiento {entrena.shape[1]}, "
          f"prueba {prueba.shape[1]}\n")

    print(f"K-SVD con {N_ATOMOS} atomos, {ITERACIONES_KSVD} "
          f"iteraciones, error objetivo {ERROR_OMP}, "
          f"tope {MAX_ATOMOS_OMP} atomos")
    inicio = time.perf_counter()
    d, alpha, historia = ksvd(entrena)
    minutos = (time.perf_counter() - inicio) / 60

    alpha_prueba = omp_matriz(d, prueba)
    err_prueba = error_relativo(prueba, d @ alpha_prueba)

    print(f"\nentrenado en {minutos:.1f} min")
    print(f"  error en entrenamiento: {historia[-1]['error']:.4f}")
    print(f"  error en prueba:        {err_prueba:.4f}")
    print(f"  atomos por senal:       "
          f"{dispersion_media(alpha_prueba):.2f}")

    print("\ncurva de error contra numero de atomos, sobre prueba")
    curva = curva_error(d, prueba)
    print(f"  {'permitidos':>10} {'usados':>8} {'error':>8}")
    for fila in curva:
        print(f"  {fila['permitidos']:>10} {fila['usados']:>8.2f} "
              f"{fila['error']:>8.4f}")

    np.savez_compressed(
        ARCHIVO_MODELO,
        diccionario=d,
        alpha_prueba=alpha_prueba,
        historia_error=np.array([h["error"] for h in historia]),
        historia_dispersion=np.array(
            [h["dispersion"] for h in historia]),
        prueba=prueba,
        senal=senal,
        fs=fs,
        permitidos=np.array([f["permitidos"] for f in curva]),
        usados=np.array([f["usados"] for f in curva]),
        errores=np.array([f["error"] for f in curva]),
    )
    tam = os.path.getsize(ARCHIVO_MODELO) / 1e6
    print(f"\nguardado en {ARCHIVO_MODELO} ({tam:.1f} MB)")


if __name__ == "__main__":
    main()


############################ END OF EXPERIMENTO.PY #############################
################################################################################
