"""
FigurasDocs.py
========================


Descripcion:
------------
Genera las figuras de la documentacion de docs/, las que acompanan la
explicacion de los datos, la SVD, OMP y la actualizacion de atomos

Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       02/10/2026      Creation


"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, os.pardir, "src"))

from Datos import cargar_ecg, construir_x, partir_en_ventanas  # noqa
from Figuras import (SERIE_AZUL, SERIE_NARANJA, SUPERFICIE,  # noqa
                     TINTA, estilo)
from Ksvd import actualizar_atomo  # noqa
from Omp import omp  # noqa
from Utils import FRECUENCIA_HZ, TAM_VENTANA  # noqa

RUTA_IMG = os.path.join(AQUI, "img")
SERIE_AQUA = "#1baf7a"
DPI = 150

# El ejemplo de juguete de los documentos. Cada atomo es una columna
NOMBRES = ("A", "B", "C", "E")
D_JUGUETE = np.array([[1.0, 0.6, 0.0, 0.0],
                      [0.0, 0.8, 0.0, 1.0],
                      [0.0, 0.0, 1.0, 0.0]])
X_JUGUETE = np.array([[1.0, 0.9],
                      [1.0, 1.0],
                      [0.5, 0.0]])
ERROR_JUGUETE = 0.1

# Ventana del registro 100 donde cae un latido completo
VENTANA_LATIDO = 5


def guardar(figura, nombre):
    """
    Guarda una figura en docs/img con el fondo del proyecto.

    Inputs:
    -------
    figura: Figure de matplotlib
    nombre: Nombre del archivo, con extension

    Returns:
    -------
    None: Escribe el archivo y cierra la figura

    """
    os.makedirs(RUTA_IMG, exist_ok=True)
    ruta = os.path.join(RUTA_IMG, nombre)
    figura.savefig(ruta, dpi=DPI, facecolor=SUPERFICIE,
                   bbox_inches="tight")
    plt.close(figura)
    print(f"  {nombre}")


def barras_vector(eje, v, color, titulo, etiquetas=("1", "2", "3")):
    """
    Dibuja un vector chico como barras, una por posicion, con su valor.

    Inputs:
    -------
    eje: Axes donde dibujar
    v: Vector de pocas entradas
    color: Color de las barras
    titulo: Titulo del panel
    etiquetas: Nombre de cada posicion en el eje x

    Returns:
    -------
    None

    """
    estilo(eje, titulo)
    eje.set_facecolor(SUPERFICIE)
    # Lo que es cero salvo redondeo de punto flotante se dibuja como 0
    v = np.where(np.abs(v) < 1e-9, 0.0, v)
    pos = np.arange(len(v))
    eje.bar(pos, v, color=color, width=0.6)
    eje.axhline(0, color=TINTA, linewidth=0.8)
    for i, valor in zip(pos, v):
        desplaza = 0.04 if valor >= 0 else -0.04
        eje.text(i, valor + desplaza, f"{valor:.3g}", ha="center",
                 va="bottom" if valor >= 0 else "top", fontsize=8,
                 color=TINTA)
    eje.set_xticks(pos, [f"pos {e}" for e in etiquetas])
    eje.set_ylim(-0.4, 1.3)


def figura_ecg_ventanas(senal):
    """
    Dos segundos del ECG con los cortes de las ventanas marcados.

    Inputs:
    -------
    senal: ECG completo del registro 100

    Returns:
    -------
    None

    """
    n = 2 * FRECUENCIA_HZ
    t = np.arange(n) / FRECUENCIA_HZ

    figura, eje = plt.subplots(figsize=(10, 3.2), facecolor=SUPERFICIE)
    estilo(eje, "Registro 100, primeros 2 segundos, cortado en "
                f"ventanas de {TAM_VENTANA} muestras")
    eje.set_facecolor(SUPERFICIE)
    eje.plot(t, senal[:n], color=SERIE_AZUL, linewidth=1.5)

    for k in range(n // TAM_VENTANA + 1):
        inicio = k * TAM_VENTANA / FRECUENCIA_HZ
        eje.axvline(inicio, color=TINTA, linewidth=0.8, linestyle="--")
        if (k + 0.5) * TAM_VENTANA < n:
            eje.text(inicio + TAM_VENTANA / FRECUENCIA_HZ / 2,
                     senal[:n].max() * 1.05, f"ventana {k}",
                     ha="center", fontsize=8, color=TINTA)

    eje.set_xlabel("segundos", fontsize=9, color=TINTA)
    eje.set_ylabel("mV", fontsize=9, color=TINTA)
    guardar(figura, "ecg_ventanas.png")


def figura_normalizacion(senal):
    """
    Una ventana antes y despues de centrar y normalizar.

    Inputs:
    -------
    senal: ECG completo del registro 100

    Returns:
    -------
    None

    """
    cruda = partir_en_ventanas(senal)[:, VENTANA_LATIDO]
    lista = construir_x(senal)[:, VENTANA_LATIDO]
    muestras = np.arange(TAM_VENTANA)

    figura, ejes = plt.subplots(1, 2, figsize=(10, 3.2),
                                facecolor=SUPERFICIE)
    paneles = (
        (cruda, SERIE_AZUL, f"Ventana {VENTANA_LATIDO} cruda: promedio "
         f"{cruda.mean():.3f}, norma {np.linalg.norm(cruda):.2f}"),
        (lista, SERIE_NARANJA, "Centrada y normalizada: promedio 0, "
         "norma 1"),
    )
    for eje, (v, color, titulo) in zip(ejes, paneles):
        estilo(eje, titulo)
        eje.set_facecolor(SUPERFICIE)
        eje.plot(muestras, v, color=color, linewidth=2)
        eje.axhline(0, color=TINTA, linewidth=0.8)
        eje.set_xlabel("fila (muestra dentro de la ventana)",
                       fontsize=9, color=TINTA)
    ejes[0].set_ylabel("mV", fontsize=9, color=TINTA)
    guardar(figura, "ventana_normalizada.png")


def figura_matriz_x(senal):
    """
    Mapa de calor de las primeras columnas de X.

    Inputs:
    -------
    senal: ECG completo del registro 100

    Returns:
    -------
    None

    """
    x = construir_x(senal)[:, :60]
    tope = np.abs(x).max()

    figura, eje = plt.subplots(figsize=(10, 4), facecolor=SUPERFICIE)
    imagen = eje.imshow(x, aspect="auto", cmap="RdBu_r", vmin=-tope,
                        vmax=tope)
    eje.set_title("X: cada columna es una ventana (primeras 60 de "
                  "5078)", fontsize=10, color=TINTA)
    eje.set_xlabel("columna = ventana", fontsize=9, color=TINTA)
    eje.set_ylabel("fila = muestra", fontsize=9, color=TINTA)
    eje.tick_params(labelsize=8, colors=TINTA)
    barra = figura.colorbar(imagen, ax=eje)
    barra.ax.tick_params(labelsize=8, colors=TINTA)
    guardar(figura, "matriz_x.png")


def figura_svd_geometria():
    """
    La SVD como girar, estirar y girar, sobre el circulo unitario.
    Usa la matriz del ejemplo grafico de la exposicion de clase

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    a = np.array([[3.0, 1.0], [1.0, 2.0]])
    u, sigma, vt = np.linalg.svd(a)
    angulo = np.linspace(0, 2 * np.pi, 200)
    circulo = np.vstack([np.cos(angulo), np.sin(angulo)])
    flechas = np.eye(2)

    pasos = (
        ("Original", np.eye(2)),
        ("1. girar con V'", vt),
        ("2. estirar con Sigma", np.diag(sigma) @ vt),
        ("3. girar con U = A x", u @ np.diag(sigma) @ vt),
    )

    figura, ejes = plt.subplots(1, 4, figsize=(12, 3.4),
                                facecolor=SUPERFICIE)
    for eje, (titulo, m) in zip(ejes, pasos):
        estilo(eje, titulo)
        eje.set_facecolor(SUPERFICIE)
        puntos = m @ circulo
        eje.plot(puntos[0], puntos[1], color=SERIE_AZUL, linewidth=2)
        for f, color in zip((m @ flechas).T, (SERIE_NARANJA, SERIE_AQUA)):
            eje.annotate("", xy=f, xytext=(0, 0),
                         arrowprops=dict(arrowstyle="-|>", color=color,
                                         linewidth=2))
        eje.set_xlim(-4, 4)
        eje.set_ylim(-4, 4)
        eje.set_aspect("equal")
    ejes[0].text(1.05, 0.15, "(1, 0)", color=TINTA, fontsize=8)
    ejes[0].text(0.1, 1.15, "(0, 1)", color=TINTA, fontsize=8)
    figura.suptitle(f"A = [[3, 1], [1, 2]]:  sigma_1 = {sigma[0]:.2f}, "
                    f"sigma_2 = {sigma[1]:.2f}", fontsize=10,
                    color=TINTA)
    guardar(figura, "svd_geometria.png")


def figura_atomos_juguete():
    """
    Los cuatro atomos del ejemplo y las dos ventanas, como barras.

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    figura, ejes = plt.subplots(1, 6, figsize=(14, 2.8),
                                facecolor=SUPERFICIE, sharey=True)
    for j, nombre in enumerate(NOMBRES):
        barras_vector(ejes[j], D_JUGUETE[:, j], SERIE_AZUL,
                      f"atomo {nombre}")
    for k in range(2):
        barras_vector(ejes[4 + k], X_JUGUETE[:, k], SERIE_NARANJA,
                      f"ventana {k + 1}")
    guardar(figura, "atomos_juguete.png")


def figura_omp_vueltas():
    """
    OMP sobre la ventana 1, una fila por vuelta.
    En cada fila: lo que falta antes de la vuelta, la reconstruccion
    despues y el residual que queda

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    x = X_JUGUETE[:, 0]
    _, elegidos = omp(D_JUGUETE, x, error=ERROR_JUGUETE)

    figura, ejes = plt.subplots(len(elegidos), 3, figsize=(10, 7.5),
                                facecolor=SUPERFICIE, sharey=True)
    residual = x.copy()
    for vuelta in range(len(elegidos)):
        usados = elegidos[:vuelta + 1]
        pesos, *_ = np.linalg.lstsq(D_JUGUETE[:, usados], x, rcond=None)
        recon = D_JUGUETE[:, usados] @ pesos
        nombres = ", ".join(f"{NOMBRES[i]}={p:.3g}"
                            for i, p in zip(usados, pesos))

        barras_vector(ejes[vuelta, 0], residual, SERIE_NARANJA,
                      f"vuelta {vuelta + 1}: falta explicar")
        barras_vector(ejes[vuelta, 1], recon, SERIE_AZUL,
                      f"gana {NOMBRES[usados[-1]]} -> {nombres}")
        residual = x - recon
        error = np.linalg.norm(residual) / np.linalg.norm(x)
        barras_vector(ejes[vuelta, 2], residual, SERIE_AQUA,
                      f"residual, error {error:.3f}")
    figura.tight_layout(h_pad=2.5)
    guardar(figura, "omp_vueltas.png")


def figura_actualizar_b():
    """
    La actualizacion del atomo B, dibujada en el plano.
    Los residuales de las dos ventanas que usan B tienen tercera
    coordenada cero, asi que todo cabe en el plano (pos 1, pos 2)

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    d = D_JUGUETE.copy()
    alpha = np.column_stack([omp(d, X_JUGUETE[:, k],
                                 error=ERROR_JUGUETE)[0]
                             for k in range(2)])
    b = 1
    viejo = d[:, b].copy()

    coeficientes = alpha.copy()
    coeficientes[b, :] = 0.0
    residual = X_JUGUETE - d @ coeficientes

    actualizar_atomo(d, X_JUGUETE, alpha, 0)
    actualizar_atomo(d, X_JUGUETE, alpha, b)
    nuevo = d[:, b] * np.sign(d[0, b])

    figura, eje = plt.subplots(figsize=(6, 5.5), facecolor=SUPERFICIE)
    estilo(eje, "Actualizacion del atomo B con la SVD")
    eje.set_facecolor(SUPERFICIE)
    # Las etiquetas van a la izquierda o a la derecha de cada trazo
    # porque R1 cae justo sobre B viejo: R1 = 1.25 B viejo
    largo = 1.5
    trazos = (
        (viejo, SERIE_NARANJA, "B viejo", (-0.62, 0.02)),
        (nuevo, SERIE_AZUL, "B nuevo = u1", (0.04, -0.02)),
    )
    for vector, color, texto, (dx, dy) in trazos:
        punta = largo * vector[:2]
        eje.plot([0, punta[0]], [0, punta[1]], color=color,
                 linewidth=2.5)
        eje.text(punta[0] + dx, punta[1] + dy,
                 f"{texto}\n({vector[0]:.3f}, {vector[1]:.3f})",
                 fontsize=9, color=TINTA)

    marcas = ((-0.5, 0.02), (0.04, -0.06))
    for k, (dx, dy) in enumerate(marcas):
        punto = residual[:2, k]
        eje.annotate("", xy=punto, xytext=(0, 0),
                     arrowprops=dict(arrowstyle="-|>", color=TINTA,
                                     linewidth=1.5))
        eje.text(punto[0] + dx, punto[1] + dy,
                 f"R{k + 1} = ({punto[0]:.2f}, {punto[1]:.2f})",
                 fontsize=9, color=TINTA)

    eje.set_xlim(0, 1.5)
    eje.set_ylim(0, 1.35)
    eje.set_aspect("equal")
    eje.set_xlabel("posicion 1", fontsize=9, color=TINTA)
    eje.set_ylabel("posicion 2", fontsize=9, color=TINTA)
    guardar(figura, "actualizar_b.png")


def figura_diccionario_inicial(senal):
    """
    Algunos atomos del diccionario inicial real, D_0.

    Inputs:
    -------
    senal: ECG completo del registro 100

    Returns:
    -------
    None

    """
    from Ksvd import diccionario_inicial

    x = construir_x(senal)
    entrena = x[:, :x.shape[1] // 2]
    d0 = diccionario_inicial(entrena)

    figura, ejes = plt.subplots(2, 6, figsize=(12, 3.8),
                                facecolor=SUPERFICIE, sharey=True)
    for j, eje in enumerate(ejes.flat):
        estilo(eje, f"atomo {j}")
        eje.set_facecolor(SUPERFICIE)
        eje.plot(d0[:, j], color=SERIE_AZUL, linewidth=1.5)
        eje.set_xticks([])
    figura.suptitle("D_0: los primeros 12 de 256 atomos iniciales, "
                    "ventanas reales escogidas al azar", fontsize=10,
                    color=TINTA)
    guardar(figura, "diccionario_inicial.png")


def main():
    """
    Genera todas las figuras de docs/img.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Escribe los PNG

    """
    print(f"figuras en {RUTA_IMG}:")
    senal, _ = cargar_ecg()

    figura_ecg_ventanas(senal)
    figura_normalizacion(senal)
    figura_matriz_x(senal)
    figura_diccionario_inicial(senal)
    figura_svd_geometria()
    figura_atomos_juguete()
    figura_omp_vueltas()
    figura_actualizar_b()


if __name__ == "__main__":
    main()


############################ END OF FIGURASDOCS.PY #############################
################################################################################
