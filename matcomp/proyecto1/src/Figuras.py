"""
Figuras.py
========================


Descripcion:
------------
Figuras del reporte del proyecto 1, generadas a partir de lo que dejo
Experimento.py en out/modelo.npz.

Son cuatro: los atomos aprendidos, la comparacion entre la senal
original y su reconstruccion, la curva de error contra numero de
atomos, y el avance de la dispersion durante el entrenamiento.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       04/10/2026      El aqua pasa a la paleta compartida
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       30/09/2026      Creation


"""

import os

import matplotlib.pyplot as plt
import numpy as np

from Omp import omp
from Utils import FRECUENCIA_HZ, RUTA_SALIDA, TAM_VENTANA

ARCHIVO_MODELO = f"{RUTA_SALIDA}/modelo.npz"

# Paleta validada: superficie, tinta, rejilla y los tres primeros
# slots categoricos, que son los que separan bien en todos los pares
SUPERFICIE = "#fcfcfb"
TINTA = "#52514e"
REJILLA = "#e8e7e2"
SERIE_AZUL = "#2a78d6"
SERIE_NARANJA = "#eb6834"
SERIE_AQUA = "#1baf7a"

ATOMOS_MUESTRA = (2, 4, 8, 16)
N_ATOMOS_DIBUJADOS = 24


def estilo(eje, titulo=None):
    """
    Deja un eje con la rejilla y los bordes recesivos del proyecto.

    Inputs:
    -------
    eje: Axes a estilizar
    titulo: Titulo del panel, o None

    Returns:
    -------
    None: Modifica eje en el lugar

    """
    eje.grid(color=REJILLA, linewidth=1)
    eje.set_axisbelow(True)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eje.spines[lado].set_color(REJILLA)
    eje.tick_params(labelsize=8, colors=TINTA)

    if titulo:
        eje.set_title(titulo, fontsize=10, color=TINTA)


def figura_atomos(d, alpha, n=N_ATOMOS_DIBUJADOS, cols=6):
    """
    Los primeros atomos del diccionario, como formas de onda.
    Es lo que el diccionario aprendio a reconocer: si el entrenamiento
    sirvio, aqui se ven complejos QRS y ondas T, no ruido

    Inputs:
    -------
    d: Diccionario entrenado
    alpha: Coeficientes, para saber que tanto se usa cada atomo
    n: Cuantos atomos dibujar
    cols: Paneles por renglon

    Returns:
    -------
    Figure: La figura armada

    """
    renglones = -(-n // cols)
    fig, ejes = plt.subplots(renglones, cols,
                             figsize=(1.7 * cols, 1.2 * renglones),
                             squeeze=False)

    # Ordenados por uso, o sea en cuantas senales participa cada
    # atomo. Ordenarlos por norma L1 devuelve las rampas suaves, que
    # son todas parecidas entre si y no dicen que aprendio el
    # diccionario
    usos = np.count_nonzero(alpha, axis=1)
    orden = np.argsort(-usos)[:n]

    for eje, j in zip(ejes.ravel(), orden):
        eje.plot(d[:, j], color=SERIE_AZUL, linewidth=1.4)
        eje.set_title(f"{usos[j]} senales", fontsize=6, color=TINTA,
                      pad=2)
        eje.set_xticks([])
        eje.set_yticks([])
        for lado in eje.spines.values():
            lado.set_color(REJILLA)

    for eje in ejes.ravel()[len(orden):]:
        eje.set_visible(False)

    fig.suptitle(f"Los {n} atomos mas usados del diccionario",
                 fontsize=11, color=TINTA)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    return fig


def elegir_ventana(x):
    """
    Escoge una ventana con un latido completo y centrado.
    Pedir la de mayor amplitud devuelve un artefacto: un pico en el
    borde y el resto plano. Por eso primero se filtra a las de
    amplitud alta pero no extrema, y de esas se toma la que tiene su
    pico mas cerca del centro, que es la que muestra el complejo QRS
    entero en vez de cortado

    Inputs:
    -------
    x: Matriz de senales, k por n

    Returns:
    -------
    int: Indice de la columna elegida

    """
    rango = x.max(axis=0) - x.min(axis=0)
    bajo, alto = np.percentile(rango, [75, 95])
    candidatas = np.flatnonzero((rango >= bajo) & (rango <= alto))

    centro = x.shape[0] / 2
    picos = np.abs(x[:, candidatas]).argmax(axis=0)

    return int(candidatas[np.argmin(np.abs(picos - centro))])


def figura_reconstruccion(d, x, columna=None, topes=ATOMOS_MUESTRA):
    """
    La senal original contra sus reconstrucciones.
    Reproduce la figura del enunciado en tres paneles: la senal, su
    descomposicion en atomos y las reconstrucciones con un numero
    creciente de formas de onda. Los trazos van desplazados en
    vertical porque encimados se tapan entre si y no se alcanza a ver
    donde mejora cada uno

    Inputs:
    -------
    d: Diccionario entrenado
    x: Matriz de senales de prueba
    columna: Cual senal dibujar, None para la de mayor amplitud
    topes: Numeros de atomos a probar

    Returns:
    -------
    Figure: La figura armada

    """
    if columna is None:
        columna = elegir_ventana(x)

    senal = x[:, columna]
    tiempo = np.arange(len(senal)) / FRECUENCIA_HZ * 1000
    paso = (senal.max() - senal.min()) * 0.9

    fig, (izq, der) = plt.subplots(
        1, 2, figsize=(11, 5.4),
        gridspec_kw={"width_ratios": [1, 1.1], "wspace": 0.22})

    # Panel izquierdo: la senal y los atomos que la componen,
    # apilados para que se distingan
    alpha, elegidos = omp(d, senal, error=0.0, max_atomos=max(topes))

    izq.plot(tiempo, senal, color=TINTA, linewidth=2)
    izq.annotate("original", (tiempo[-1], senal[-1]),
                 textcoords="offset points", xytext=(6, 0),
                 fontsize=8, color=TINTA, va="center")

    for i, j in enumerate(elegidos[:6], start=1):
        izq.plot(tiempo, alpha[j] * d[:, j] - i * paso,
                 color=SERIE_NARANJA, linewidth=1.2, alpha=0.85)
        izq.annotate(f"atomo {i}", (tiempo[-1], -i * paso),
                     textcoords="offset points", xytext=(6, 0),
                     fontsize=7, color=TINTA, va="center")

    estilo(izq, "Descomposicion en atomos")
    izq.set_xlabel("ms", fontsize=8, color=TINTA)
    izq.set_yticks([])
    izq.set_xlim(tiempo[0], tiempo[-1] * 1.22)

    # Panel derecho: rampa de un solo tono, porque el numero de
    # atomos es una magnitud y no una identidad
    rampa = plt.cm.Blues(np.linspace(0.45, 0.95, len(topes)))

    der.plot(tiempo, senal, color=TINTA, linewidth=2)
    der.annotate("original", (tiempo[-1], senal[-1]),
                 textcoords="offset points", xytext=(6, 0),
                 fontsize=8, color=TINTA, va="center")

    for i, (color, tope) in enumerate(zip(rampa, topes), start=1):
        coef, _ = omp(d, senal, error=0.0, max_atomos=tope)
        recon = d @ coef
        err = np.linalg.norm(senal - recon) / np.linalg.norm(senal)

        der.plot(tiempo, recon - i * paso, color=color, linewidth=1.8)
        der.annotate(f"{tope} atomos\nerror {err:.3f}",
                     (tiempo[-1], recon[-1] - i * paso),
                     textcoords="offset points", xytext=(6, 0),
                     fontsize=7, color=TINTA, va="center")

    estilo(der, "Reconstruccion con mas atomos")
    der.set_xlabel("ms", fontsize=8, color=TINTA)
    der.set_yticks([])
    der.set_xlim(tiempo[0], tiempo[-1] * 1.28)

    return fig


def figura_curva(permitidos, errores):
    """
    Error de reconstruccion contra numero de atomos permitidos.

    Inputs:
    -------
    permitidos: Topes de atomos probados
    errores: Error relativo alcanzado en cada tope

    Returns:
    -------
    Figure: La figura armada

    """
    fig, eje = plt.subplots(figsize=(7, 3.6))

    eje.plot(permitidos, errores, color=SERIE_AZUL, linewidth=2,
             marker="o", markersize=6,
             markeredgecolor=SUPERFICIE, markeredgewidth=1.5)

    # Dos etiquetas directas, no una por punto
    for i in (0, len(permitidos) - 1):
        eje.annotate(f"{errores[i]:.3f}",
                     (permitidos[i], errores[i]),
                     textcoords="offset points", xytext=(8, 8),
                     fontsize=8, color=TINTA)

    estilo(eje, "Error de reconstruccion segun el tope de atomos")
    eje.set_xlabel("atomos permitidos por senal", fontsize=9,
                   color=TINTA)
    eje.set_ylabel("error relativo", fontsize=9, color=TINTA)
    eje.set_ylim(0, max(errores) * 1.15)
    fig.tight_layout()

    return fig


def figura_entrenamiento(dispersion):
    """
    Dispersion media a lo largo del entrenamiento.
    Se grafica la dispersion y no el error porque el error lo fija el
    criterio de paro de OMP y se queda plano. Lo que K-SVD mejora es
    cuantos atomos hacen falta para alcanzarlo

    Inputs:
    -------
    dispersion: Atomos por senal en cada iteracion

    Returns:
    -------
    Figure: La figura armada

    """
    fig, eje = plt.subplots(figsize=(7, 3.4))
    iteraciones = np.arange(1, len(dispersion) + 1)

    eje.plot(iteraciones, dispersion, color=SERIE_AZUL, linewidth=2)
    eje.annotate(f"{dispersion[0]:.2f}", (1, dispersion[0]),
                 textcoords="offset points", xytext=(8, 4),
                 fontsize=8, color=TINTA)
    eje.annotate(f"{dispersion[-1]:.2f}",
                 (len(dispersion), dispersion[-1]),
                 textcoords="offset points", xytext=(-28, -14),
                 fontsize=8, color=TINTA)

    estilo(eje, "Atomos por senal a lo largo del entrenamiento")
    eje.set_xlabel("iteracion de K-SVD", fontsize=9, color=TINTA)
    eje.set_ylabel("atomos por senal", fontsize=9, color=TINTA)
    fig.tight_layout()

    return fig


def main():
    """
    Genera las cuatro figuras y las guarda en out/.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Escribe los PDF en RUTA_SALIDA

    """
    if not os.path.exists(ARCHIVO_MODELO):
        raise SystemExit(f"falta {ARCHIVO_MODELO}, "
                         f"corre Experimento.py primero")

    datos = np.load(ARCHIVO_MODELO)
    d = datos["diccionario"]
    prueba = datos["prueba"]

    figuras = {
        "atomos.pdf": figura_atomos(d, datos["alpha_prueba"]),
        "reconstruccion.pdf": figura_reconstruccion(d, prueba),
        "curva_error.pdf": figura_curva(datos["permitidos"],
                                        datos["errores"]),
        "entrenamiento.pdf": figura_entrenamiento(
            datos["historia_dispersion"]),
    }

    for nombre, figura in figuras.items():
        ruta = f"{RUTA_SALIDA}/{nombre}"
        figura.savefig(ruta, bbox_inches="tight",
                       facecolor=SUPERFICIE)
        print(f"{ruta:32} {os.path.getsize(ruta) / 1024:7.1f} KB")


if __name__ == "__main__":
    main()


############################## END OF FIGURAS.PY ###############################
################################################################################
