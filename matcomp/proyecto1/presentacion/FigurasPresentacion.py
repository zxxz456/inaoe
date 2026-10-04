"""
FigurasPresentacion.py
========================


Descripcion:
------------
Genera las animaciones e imagenes de la presentacion Ksvd.qmd a partir
de los datos reales del experimento: la ventana de ECG, las vueltas de
OMP, la SVD del residual de un atomo, la curva de entrenamiento, la
comparacion entre diccionarios y la prueba con otros pacientes.

No escribe archivos aparte para las animaciones. Reescribe dentro de
Ksvd.qmd las regiones marcadas con los comentarios inicio:nombre y
fin:nombre, asi la presentacion queda en un solo archivo, igual que la
de Aprendizaje Computacional. Las imagenes fijas van a img/. Necesita
out/modelo.npz, asi que hay que correr src/Experimento.py antes.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       04/10/2026      Paso SVD en cuatro estados y diccionario mejorado
zxxz6       04/10/2026      Creation


"""

import os
import re
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, os.pardir, "src"))

from Analisis import (OTROS_PACIENTES, TOPES_COMPARACION,  # noqa: E402
                      comparar_diccionarios, diccionario_dct,
                      evaluar_paciente)
from Datos import cargar_ecg, construir_x  # noqa: E402
from Experimento import partir_entrenamiento  # noqa: E402
from Figuras import (SUPERFICIE, elegir_ventana,  # noqa: E402
                     figura_atomos, figura_reconstruccion)
from Ksvd import actualizar_atomo, diccionario_inicial  # noqa: E402
from Omp import omp, omp_matriz  # noqa: E402
from Utils import (REGISTRO, RUTA_SALIDA, TAM_VENTANA,  # noqa: E402
                   error_relativo)

ARCHIVO_QMD = os.path.join(AQUI, "Ksvd.qmd")
RUTA_IMG = os.path.join(AQUI, "img")
ARCHIVO_MODELO = os.path.join(AQUI, os.pardir, "src", RUTA_SALIDA,
                              "modelo.npz")
DPI = 160

# Margen interior de cada trazo, en pixeles de su caja
MARGEN = 8

# Cuantos pares de coordenadas por renglon, para no pasar de 80
# columnas dentro del .qmd
PARES_POR_RENGLON = 6

# La animacion de OMP muestra estas vueltas
VUELTAS_OMP = (1, 2, 3, 4)

# La de la ventana armada con pocas piezas usa este numero de atomos
PIEZAS = 3

# Segundos de senal en la tira y cuantas ventanas se resaltan
SEGUNDOS_TIRA = 3
VENTANAS_TIRA = 5

# Valores singulares que se dibujan en la barra de energia
BARRAS_SVD = 12

# Ventanas del subconjunto con el que se calcula el residual de un
# atomo, igual que en Notes.ipynb
VENTANAS_RESIDUAL = 600

# Recorte de alfa que se dibuja: cuantas ventanas, cuantos atomos y el
# lado de cada celda en pixeles
COLUMNAS_ALFA = 36
FILAS_ALFA = 16
CELDA_ALFA = 18

# Columnas de R que se enciman en el paso 3; todas saturan el dibujo
COLUMNAS_R = 40

# Atomos que se comparan antes y despues de entrenar, y la franja en
# pixeles que se deja arriba de cada uno para su etiqueta
ATOMOS_DIC = 8
FRANJA_ETQ = 26

# Muestras a cada lado del pico que se consideran parte del QRS, unos
# 42 ms
MARGEN_QRS = 15

# Rejilla de la diapositiva de compresion
COLUMNAS_REJILLA = 16
LADO_CUADRO = 30
HUECO_CUADRO = 8


# =====================================================================
#  Piezas de HTML y SVG
# =====================================================================

def puntos(y, ancho, alto, lo, hi, x0=0.0, x1=None):
    """
    Convierte una senal en coordenadas de polilinea dentro de una caja.
    El eje vertical se invierte porque en SVG la y crece hacia abajo.
    Los pares se parten en renglones para no rebasar 80 columnas

    Inputs:
    -------
    y: Arreglo con los valores de la senal
    ancho: Ancho de la caja en pixeles
    alto: Alto de la caja en pixeles
    lo: Valor que va al borde de abajo
    hi: Valor que va al borde de arriba
    x0: Posicion relativa, de 0 a 1, del primer punto
    x1: Posicion relativa del ultimo punto, None para 1

    Returns:
    -------
    str: Coordenadas "x,y" separadas por espacios y renglones

    """
    x1 = 1.0 if x1 is None else x1
    n = len(y)
    util = ancho - 2 * MARGEN
    xs = MARGEN + util * (x0 + (x1 - x0) * np.arange(n) / max(n - 1, 1))
    ys = MARGEN + (hi - np.asarray(y)) * (alto - 2 * MARGEN) / (hi - lo)

    pares = [f"{a:.1f},{b:.1f}" for a, b in zip(xs, ys)]
    return "\n".join(" ".join(pares[i:i + PARES_POR_RENGLON])
                     for i in range(0, len(pares), PARES_POR_RENGLON))


def polilinea(y, ancho, alto, lo, hi, clase, **kw):
    """
    Una polilinea con la clase de trazo del proyecto.
    pathLength=1 deja que la animacion de dibujado funcione igual para
    cualquier largo de linea

    Inputs:
    -------
    y, ancho, alto, lo, hi: Ver puntos
    clase: Clases CSS del trazo, por ejemplo "azul grueso dibuja"
    kw: x0 y x1 de puntos, si hacen falta

    Returns:
    -------
    str: Elemento polyline

    """
    return (f'<polyline class="t {clase}" pathLength="1" points="\n'
            f'{puntos(y, ancho, alto, lo, hi, **kw)}"/>')


def svg(ancho, alto, contenido):
    """
    Lienzo SVG en las coordenadas de su caja.

    Inputs:
    -------
    ancho: Ancho de la caja
    alto: Alto de la caja
    contenido: Elementos SVG

    Returns:
    -------
    str: Elemento svg

    """
    return (f'<svg viewBox="0 0 {ancho} {alto}" '
            f'preserveAspectRatio="none">\n{contenido}\n</svg>')


def caja(x, y, ancho, alto, contenido="", ident=None, clase="caja",
         estilo=""):
    """
    Un div posicionado en coordenadas absolutas de la diapositiva.
    Con ident lleva data-id, que es lo que usa auto-animate para
    emparejarlo con el de la diapositiva siguiente y moverlo

    Inputs:
    -------
    x, y: Esquina superior izquierda, en pixeles de la diapositiva
    ancho, alto: Tamano de la caja
    contenido: HTML interior
    ident: data-id, o None si no se empareja
    clase: Clases CSS
    estilo: CSS extra en linea

    Returns:
    -------
    str: Elemento div

    """
    did = f' data-id="{ident}"' if ident else ""
    salto = "\n" if contenido else ""
    extra = f"\n  {estilo}" if estilo else ""
    return (f'<div class="{clase}"{did}\n  style="left:{x:.0f}px;'
            f'top:{y:.0f}px;width:{ancho:.0f}px;height:{alto:.0f}px;'
            f'{extra}">{salto}{contenido}</div>')


def etiqueta(x, y, ancho, texto, ident=None, clase="etq c", estilo="",
             atributos=""):
    """
    Texto posicionado; el alto lo pone el propio texto.

    Inputs:
    -------
    x, y, ancho: Posicion y ancho en pixeles
    texto: HTML del texto
    ident: data-id para auto-animate, o None
    clase: Clases CSS
    estilo: CSS extra en linea
    atributos: Atributos HTML extra, por ejemplo el orden de un
               fragmento

    Returns:
    -------
    str: Elemento div

    """
    did = f' data-id="{ident}"' if ident else ""
    extra = f" {atributos}" if atributos else ""
    # El texto va en sus propios renglones; HTML junta los espacios, asi
    # que partirlo no cambia lo que se ve
    cuerpo = "\n".join(textwrap.wrap(texto, 76, break_long_words=False,
                                      break_on_hyphens=False))
    mas = f"\n  {estilo}" if estilo else ""
    return (f'<div class="{clase}"{did}{extra}\n  style="left:{x:.0f}px;'
            f'top:{y:.0f}px;width:{ancho:.0f}px;{mas}">\n'
            f'{cuerpo}\n</div>')


def bloque_html(*partes):
    """
    Envuelve HTML crudo para que Quarto no lo interprete.

    Inputs:
    -------
    partes: Fragmentos de HTML

    Returns:
    -------
    str: Bloque de codigo crudo de Quarto

    """
    return "```{=html}\n" + "\n".join(partes) + "\n```"


def rango(*senales, holgura=0.08):
    """
    Limites verticales comunes para varias senales.
    Usar el mismo rango en todos los trazos de una diapositiva es lo que
    permite comparar sus alturas a ojo

    Inputs:
    -------
    senales: Arreglos a abarcar
    holgura: Fraccion del rango que se agrega arriba y abajo

    Returns:
    -------
    tuple: (lo, hi)

    """
    todo = np.concatenate([np.ravel(s) for s in senales])
    lo, hi = float(todo.min()), float(todo.max())
    extra = (hi - lo) * holgura

    return lo - extra, hi + extra


def sub(nombre, indice):
    """
    Nombre con subindice en HTML, sin caracteres de subindice Unicode.

    Inputs:
    -------
    nombre: Letra base
    indice: Lo que va abajo

    Returns:
    -------
    str: HTML

    """
    return f"{nombre}<sub>{indice}</sub>"


# =====================================================================
#  Regiones de la presentacion
# =====================================================================

def region_representacion(d, x):
    """
    Tres estados: la ventana, sus piezas por separado y la suma.

    Inputs:
    -------
    d: Diccionario entrenado
    x: Ventana de prueba

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    alpha, elegidos = omp(d, x, error=0.0, max_atomos=PIEZAS)
    piezas = [alpha[j] * d[:, j] for j in elegidos]
    suma = d @ alpha
    err = error_relativo(x, suma)
    lo, hi = rango(x, *piezas, suma)

    gx, gy, gw, gh = 240, 140, 800, 260
    panel = caja(gx, gy, gw, gh, ident="rep-panel", clase="caja panel")

    def ventana(clase):
        return caja(gx, gy, gw, gh, svg(gw, gh, polilinea(
            x, gw, gh, lo, hi, clase)), ident="rep-x")

    texto_x = etiqueta(gx, gy + gh + 12, gw,
                       "una ventana del ECG: 128 números", ident="rep-tx")

    pw, ph, py = 340, 150, 470
    nombres = [f"{alpha[j]:.2f} {sub('d', j)}" for j in elegidos]

    def piezas_html(en_grande):
        partes = []
        for i, (pieza, nombre) in enumerate(zip(piezas, nombres)):
            px = 70 + i * 390
            if en_grande:
                partes.append(caja(px, py, pw, ph, ident=f"rep-pp{i}",
                                   clase="caja panel",
                                   estilo="opacity:0;"))
                partes.append(caja(gx, gy, gw, gh, svg(gw, gh, polilinea(
                    pieza, gw, gh, lo, hi, "naranja fino")),
                    ident=f"rep-p{i}", estilo="opacity:0.7;"))
                partes.append(etiqueta(px, py + ph + 8, pw, nombre,
                                       ident=f"rep-e{i}",
                                       estilo="opacity:0;"))
            else:
                partes.append(caja(px, py, pw, ph, ident=f"rep-pp{i}",
                                   clase="caja panel"))
                partes.append(caja(px, py, pw, ph, svg(pw, ph, polilinea(
                    pieza, pw, ph, lo, hi, "naranja")),
                    ident=f"rep-p{i}"))
                partes.append(etiqueta(px, py + ph + 8, pw, nombre,
                                       ident=f"rep-e{i}"))
        return partes

    uno = bloque_html(panel, ventana("tinta grueso dibuja"), texto_x)
    dos = bloque_html(panel, ventana("tinta grueso"), texto_x,
                      *piezas_html(False))

    terminos = []
    for i, j in enumerate(elegidos):
        signo = "" if i == 0 else (" + " if alpha[j] >= 0 else " - ")
        valor = abs(alpha[j]) if i else alpha[j]
        terminos.append(f"{signo}{valor:.2f}\\,d_{{{j}}}")
    formula = "".join(terminos)

    tres = (bloque_html(panel, ventana("tinta grueso"), *piezas_html(True),
                        caja(gx, gy, gw, gh, svg(gw, gh, polilinea(
                            suma, gw, gh, lo, hi, "azul grueso dibuja")),
                            ident="rep-suma"))
            + "\n\n::: {.etq .c .grande style=\"left:140px; top:425px; "
              "width:1000px;\"}\n"
            + f"$x \\approx {formula}$\n:::\n\n"
            + "::: {.etq .c style=\"left:140px; top:500px; "
              "width:1000px;\"}\n"
            + f"{PIEZAS} números en lugar de 128, con error relativo de "
            + f"**{err:.3f}**\n:::")

    return {"representacion_1": uno, "representacion_2": dos,
            "representacion_3": tres}


def region_omp(d, x):
    """
    Una diapositiva por vuelta de OMP sobre la misma ventana.
    La ventana, los paneles, las fichas de atomos y la barra de error
    llevan data-id para que auto-animate los mueva. La reconstruccion
    y el residual no, asi que se desvanecen de una vuelta a la otra

    Inputs:
    -------
    d: Diccionario entrenado
    x: Ventana de prueba

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    px, py, pw, ph = 60, 130, 780, 270
    rx, ry, rw, rh = 60, 420, 780, 190
    lo, hi = rango(x)
    escala = (ph - 2 * MARGEN) / (hi - lo)
    medio_r = (rh - 2 * MARGEN) / escala / 2

    # El peso de cada atomo en cada vuelta, para contar cuando cambia
    vueltas = []
    for tope in VUELTAS_OMP:
        alpha, elegidos = omp(d, x, error=0.0, max_atomos=tope)
        vueltas.append((alpha, elegidos))

    err_max = 0.30
    regiones = {}
    for k, (alpha, elegidos) in enumerate(vueltas, start=1):
        recon = d @ alpha
        resid = x - recon
        err = error_relativo(x, recon)

        partes = [
            caja(px, py, pw, ph, ident="omp-px", clase="caja panel"),
            caja(px, py, pw, ph, svg(pw, ph, polilinea(
                x, pw, ph, lo, hi, "tinta grueso")), ident="omp-x"),
            caja(px, py, pw, ph, svg(pw, ph, polilinea(
                recon, pw, ph, lo, hi, "azul grueso"))),
            etiqueta(px + 14, py + 8, 400, "original y reconstrucción",
                     ident="omp-t1", clase="etq chica"),
            caja(rx, ry, rw, rh, ident="omp-pr", clase="caja panel"),
            caja(rx, ry, rw, rh, svg(rw, rh, polilinea(
                resid, rw, rh, -medio_r, medio_r, "naranja"))),
            etiqueta(rx + 14, ry + 8, 400, "residual: lo que falta",
                     ident="omp-t2", clase="etq chica"),
            etiqueta(880, 92, 340, f"Vuelta {k}", ident="omp-vuelta",
                     clase="etq grande"),
        ]
        for i, j in enumerate(elegidos):
            clase = "chip nuevo" if i == len(elegidos) - 1 else "chip"
            partes.append(
                f'<div class="{clase}" data-id="omp-c{j}"\n'
                f'  style="left:880px;top:{140 + 56 * i}px;">'
                f'{sub("d", j)}, peso {alpha[j]:.2f}</div>')

        ancho = 340 * err / err_max
        partes += [
            etiqueta(880, 400, 340, "error relativo", ident="omp-te",
                     clase="etq"),
            caja(880, 432, ancho, 30, ident="omp-barra",
                 clase="barra h naranja-f"),
            etiqueta(880 + ancho + 10, 434, 120, f"{err:.3f}",
                     ident="omp-num", clase="etq"),
        ]

        if k == 2:
            j0 = vueltas[0][1][0]
            nota = (f"El peso de {sub('d', j0)} cambió de "
                    f"{vueltas[0][0][j0]:.2f} a {alpha[j0]:.2f}: en cada "
                    f"vuelta se reajustan <strong>todos</strong>")
        elif k == len(vueltas):
            nota = (f"Con {k} átomos el error ya es {err:.3f}. Un par de "
                    f"vueltas más y baja del umbral de 0.1")
        else:
            nota = "Cada vuelta, el residual se encoge"
        partes.append(etiqueta(60, 628, 1160, nota, ident="omp-nota"))

        regiones[f"omp_{k}"] = bloque_html(*partes)

    return regiones


def region_svd(entrena):
    """
    Cuatro estados del paso SVD sobre un atomo real.
    Repite el calculo de Notes.ipynb: diccionario inicial, dispersion de
    las primeras ventanas y el atomo que mas ventanas usan. El estado
    final sale de actualizar_atomo, la misma funcion del entrenamiento,
    asi que lo que se ve es exactamente lo que hace K-SVD

    Inputs:
    -------
    entrena: Ventanas de entrenamiento

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    d0 = diccionario_inicial(entrena)
    sub_x = entrena[:, :VENTANAS_RESIDUAL]
    alpha = omp_matriz(d0, sub_x)

    j = int(np.argmax(np.count_nonzero(alpha, axis=1)))
    w = np.flatnonzero(alpha[j, :])
    coef = alpha[:, w].copy()
    coef[j, :] = 0.0
    otros = d0 @ coef
    residual = sub_x[:, w] - otros

    u, sigma, _ = np.linalg.svd(residual, full_matrices=False)
    energia = sigma ** 2 / (sigma ** 2).sum()
    # El signo de un vector singular es arbitrario; se alinea con el
    # atomo viejo para que la comparacion se lea
    u1 = u[:, 0] * (np.sign(u[:, 0] @ d0[:, j]) or 1.0)

    d1, a1 = d0.copy(), alpha.copy()
    actualizar_atomo(d1, sub_x, a1, j)
    nuevo = d1[:, j] * (np.sign(d1[:, j] @ d0[:, j]) or 1.0)
    coseno = float(abs(nuevo @ d0[:, j]))
    antes = error_relativo(sub_x[:, w], d0 @ alpha[:, w])
    despues = error_relativo(sub_x[:, w], d1 @ a1[:, w])

    dj = sub("d", j)
    return {"svd_1": _svd_quien(alpha, j, w, d0[:, j], dj, sub_x.shape[1]),
            "svd_2": _svd_restar(sub_x, otros, residual, alpha, w, j, dj),
            "svd_3": _svd_juntar(residual, u1, energia, dj),
            "svd_4": _svd_actualizar(d0[:, j], nuevo, coseno, antes,
                                     despues, len(w), dj)}


def _svd_quien(alpha, j, w, atomo, dj, total):
    """
    Estado 1: un recorte real de alfa con la fila del atomo resaltada.

    Inputs:
    -------
    alpha: Pesos de las ventanas del ejemplo
    j: Atomo que se va a actualizar
    w: Ventanas que lo usan
    atomo: El atomo antes de actualizarlo
    dj: Nombre del atomo en HTML
    total: Cuantas ventanas tiene el ejemplo

    Returns:
    -------
    str: Contenido de la region

    """
    cols = np.arange(COLUMNAS_ALFA)
    sub = alpha[:, cols]
    usos = np.count_nonzero(sub, axis=1)
    usos[j] = -1
    filas = np.sort(np.append(np.argsort(-usos)[:FILAS_ALFA - 1], j))

    paso = CELDA_ALFA + 3
    gx, gy = 130, 150
    rects = []
    for r, atomo_r in enumerate(filas):
        for c in cols:
            activo = sub[atomo_r, c] != 0
            if atomo_r == j:
                clase = "cj" if activo else "cjz"
            else:
                clase = "cn" if activo else "cz"
            rects.append(f'<rect x="{c * paso}" y="{r * paso}" '
                         f'width="{CELDA_ALFA}" height="{CELDA_ALFA}" '
                         f'class="{clase}"/>')
    ancho, alto = len(cols) * paso - 3, len(filas) * paso - 3
    fila_j = int(np.flatnonzero(filas == j)[0])

    lo, hi = rango(atomo)
    aw, ah = 330, 200
    partes = [
        caja(gx, gy, ancho, alto, svg(ancho, alto, "\n".join(rects))),
        etiqueta(gx - 70, gy + fila_j * paso - 4, 60, dj,
                 clase="etq chica", estilo="text-align:right;"),
        etiqueta(gx, gy + alto + 10, ancho,
                 f"recorte de &alpha;: {len(filas)} de 256 átomos "
                 f"(filas) por {len(cols)} de {total} ventanas (columnas)",
                 clase="etq c chica"),
        caja(900, 170, aw, ah, ident="svd-pa", clase="caja panel"),
        caja(900, 170, aw, ah, svg(aw, ah, polilinea(
            atomo, aw, ah, lo, hi, "tinta grueso")), ident="svd-atomo"),
        etiqueta(900, 380, aw, f"{dj}, el átomo que se va a actualizar",
                 clase="etq c"),
        etiqueta(60, 590, 1160,
                 f"De {total} ventanas, <strong>{len(w)}</strong> usan el "
                 f"átomo: son las celdas naranjas de su fila. Solo esas se "
                 f"miran", clase="etq c"),
    ]
    return bloque_html(*partes)


def _svd_restar(sub_x, otros, residual, alpha, w, j, dj):
    """
    Estado 2: a tres ventanas se les quita lo que explican los demas.

    Inputs:
    -------
    sub_x: Ventanas del ejemplo
    otros: Lo que aportan los demas atomos en cada ventana de w
    residual: R, columna por ventana de w
    alpha: Pesos de las ventanas del ejemplo
    w: Ventanas que usan el atomo
    j: Atomo que se va a actualizar
    dj: Nombre del atomo en HTML

    Returns:
    -------
    str: Contenido de la region

    """
    muestra = np.argsort(-np.abs(alpha[j, w]))[:3]
    bw, bh = 320, 130
    partes = []
    for i, t in enumerate(muestra):
        ventana = w[t]
        x, o, r = sub_x[:, ventana], otros[:, t], residual[:, t]
        lo, hi = rango(x, o, r)
        y = 115 + i * 152
        n_otros = int(np.count_nonzero(alpha[:, ventana])) - 1
        for k, (bx, serie, clase, texto) in enumerate((
                (60, x, "tinta", f"ventana {ventana}"),
                (434, o, "naranja", f"lo que explican los otros "
                                    f"{n_otros}"),
                (808, r, "azul", "lo que sobra"))):
            partes += [
                caja(bx, y, bw, bh, clase="caja panel"),
                caja(bx, y, bw, bh, svg(bw, bh, polilinea(
                    serie, bw, bh, lo, hi, f"{clase} grueso"))),
                etiqueta(bx + 10, y + 4, bw - 20, texto,
                         clase="etq chica"),
            ]
        partes += [
            etiqueta(386, y + 40, 40, "&minus;", clase="etq c grande"),
            etiqueta(760, y + 40, 40, "=", clase="etq c grande"),
        ]
    texto = ("\n\n::: {.etq .c style=\"left:60px; top:580px; "
             "width:1160px;\"}\n"
             f"Cada sobra es una columna de $R$: lo que le tocaría\n"
             f"explicar a $d_{{{j}}}$ en esa ventana\n:::")
    return bloque_html(*partes) + texto


def _svd_juntar(residual, u1, energia, dj):
    """
    Estado 3: varias columnas de R encimadas, con u_1 encima.
    Las columnas se normalizan y se alinean en signo con u_1 para que se
    vea la forma que comparten, que es lo que la SVD encuentra

    Inputs:
    -------
    residual: R
    u1: Primer vector singular izquierdo, alineado con el atomo viejo
    energia: Fraccion de energia de cada valor singular
    dj: Nombre del atomo en HTML

    Returns:
    -------
    str: Contenido de la region

    """
    cols = np.linspace(0, residual.shape[1] - 1,
                       min(COLUMNAS_R, residual.shape[1])).astype(int)
    trazos = []
    for c in cols:
        col = residual[:, c] / (np.linalg.norm(residual[:, c]) or 1.0)
        trazos.append(col * (np.sign(col @ u1) or 1.0))
    lo, hi = rango(u1, *trazos)

    pw, ph = 720, 400
    capas = "\n".join(polilinea(t[::2], pw, ph, lo, hi, "gris fino")
                      for t in trazos)
    partes = [
        caja(60, 130, pw, ph, ident="svd-panel", clase="caja panel"),
        caja(60, 130, pw, ph, svg(pw, ph, capas),
             estilo="opacity:0.55;"),
        caja(60, 130, pw, ph, svg(pw, ph, polilinea(
            u1, pw, ph, lo, hi, "azul grueso dibuja"))),
        etiqueta(74, 138, 600,
                 f"{len(cols)} de las {residual.shape[1]} columnas de R, "
                 f"normalizadas. En azul, {sub('u', 1)}",
                 clase="etq chica"),
    ]

    bx, by, bw, bh = 820, 150, 400, 300
    tope = max(energia[0], 1e-9)
    paso = (bw - 40) / BARRAS_SVD
    partes.append(caja(bx, by, bw, bh, clase="caja panel"))
    for i in range(BARRAS_SVD):
        alto = (bh - 50) * energia[i] / tope
        color = "azul-f" if i == 0 else "gris-f"
        partes.append(caja(
            bx + 20 + i * paso, by + bh - 30 - alto, paso * 0.7, alto,
            clase=f"barra crece {color}",
            estilo=f"animation-delay:{0.06 * i:.2f}s;"))
    partes += [
        etiqueta(bx + 20 + paso * 0.7 + 8, by + 18, 140,
                 f"{energia[0]:.1%}", clase="etq grande",
                 estilo="color:#2a78d6;"),
        etiqueta(bx, by + bh - 26, bw,
                 f"los primeros {BARRAS_SVD} valores singulares",
                 clase="etq c chica"),
        etiqueta(bx, by + bh + 8, bw, "fracción de la energía de R",
                 clase="etq c"),
    ]
    texto = ("\n\n::: {.etq .c style=\"left:60px; top:560px; "
             "width:1160px;\"}\n"
             f"$R$ es de ${residual.shape[0]} \\times {residual.shape[1]}$"
             ": casi todas sus columnas apuntan en la misma\n"
             "dirección, y esa dirección es $u_1$\n:::")
    return bloque_html(*partes) + texto


def _svd_actualizar(viejo, nuevo, coseno, antes, despues, n, dj):
    """
    Estado 4: el atomo antes y despues, y cuanto cambio.

    Inputs:
    -------
    viejo: El atomo antes
    nuevo: El atomo despues, alineado en signo con el viejo
    coseno: Coseno entre los dos
    antes: Error de las ventanas que lo usan, antes
    despues: El mismo error, despues
    n: Cuantas ventanas lo usan
    dj: Nombre del atomo en HTML

    Returns:
    -------
    str: Contenido de la region

    """
    pw, ph = 720, 400
    lo, hi = rango(viejo, nuevo)
    partes = [
        caja(60, 130, pw, ph, ident="svd-panel", clase="caja panel"),
        caja(60, 130, pw, ph, svg(pw, ph,
                                  polilinea(nuevo, pw, ph, lo, hi,
                                            "azul grueso dibuja") + "\n"
                                  + polilinea(viejo, pw, ph, lo, hi,
                                              "tinta punteado")),
             ident="svd-atomo"),
        etiqueta(74, 138, 640,
                 f"punteado: {dj} antes. Azul: {sub('u', 1)}, el átomo "
                 f"nuevo", clase="etq chica"),
        etiqueta(820, 150, 400,
                 f"{dj} pasa a ser {sub('u', 1)}, y sus pesos pasan a "
                 f"ser &sigma;<sub>1</sub> {sub('v', 1)}",
                 clase="etq"),
        etiqueta(820, 260, 400,
                 f"Coseno entre el viejo y el nuevo: "
                 f"<strong>{coseno:.3f}</strong>", clase="etq"),
        etiqueta(820, 340, 400,
                 f"Error de esas {n} ventanas: de <strong>{antes:.3f}"
                 f"</strong> a <strong>{despues:.3f}</strong>",
                 clase="etq"),
        etiqueta(820, 430, 400,
                 "Un solo paso cambia poco. Lo que mueve al diccionario "
                 "es repetirlo: 256 átomos, 20 iteraciones",
                 clase="etq fragment"),
    ]
    return bloque_html(*partes)


def region_diccionario(d0, d, alpha, dispersion):
    """
    Los atomos mas usados antes y despues de entrenar.
    Muestra el efecto acumulado, que es donde se ve el aprendizaje: en
    un solo paso un atomo casi no cambia, en 20 iteraciones la linea
    base pierde buena parte de su ruido

    Inputs:
    -------
    d0: Diccionario inicial
    d: Diccionario entrenado, que arranca de d0
    alpha: Pesos de las ventanas de prueba, para escoger los atomos
    dispersion: Atomos por ventana en cada iteracion

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    d = d * np.sign(np.sum(d0 * d, axis=0))
    orden = np.argsort(-np.count_nonzero(alpha, axis=1))[:ATOMOS_DIC]
    baja = ruido_fuera_del_qrs(d0, d)

    bw, bh = 280, 180
    def estado(entrenado):
        partes = []
        for i, j in enumerate(orden):
            x = 60 + (i % 4) * 300
            y = 140 + (i // 4) * 215
            lo, hi = rango(d0[:, j], d[:, j])
            th = bh - FRANJA_ETQ
            if entrenado:
                trazo = (polilinea(d0[:, j], bw, th, lo, hi,
                                   "gris punteado") + "\n"
                         + polilinea(d[:, j], bw, th, lo, hi,
                                     "azul grueso"))
            else:
                trazo = polilinea(d0[:, j], bw, th, lo, hi, "tinta")
            # El trazo deja libre una franja arriba para la etiqueta;
            # sin ella el pico de los atomos con el QRS a la izquierda
            # quedaba debajo del texto
            partes += [
                caja(x, y, bw, bh, ident=f"dic-p{i}", clase="caja panel"),
                caja(x, y + FRANJA_ETQ, bw, bh - FRANJA_ETQ,
                     svg(bw, bh - FRANJA_ETQ, trazo)),
                etiqueta(x + 10, y + 2, bw - 20, f"átomo {j}",
                         ident=f"dic-e{i}", clase="etq chica"),
            ]
        return partes

    uno = estado(False) + [
        etiqueta(60, 92, 1160, "D<sub>0</sub>: ventanas reales tomadas al "
                 "azar. Los 8 átomos que más se usan al final, en su forma "
                 "inicial", ident="dic-t", clase="etq"),
        etiqueta(60, 580, 1160, "Fíjense en las ondulaciones de la línea "
                 "base", clase="etq c"),
    ]
    dos = estado(True) + [
        etiqueta(60, 92, 1160, "Después de 20 iteraciones, en azul sobre "
                 "el original punteado", ident="dic-t", clase="etq"),
        etiqueta(60, 572, 1160,
                 f"Fuera del complejo QRS el ruido de la línea base baja "
                 f"<strong>{baja:.0%}</strong>, y el pico se conserva",
                 clase="etq c"),
        etiqueta(60, 618, 1160,
                 f"Para el mismo error, cada ventana pasa de "
                 f"<strong>{dispersion[0]:.2f}</strong> a "
                 f"<strong>{dispersion[-1]:.2f}</strong> átomos",
                 clase="etq c fragment"),
    ]
    return {"dic_1": bloque_html(*uno), "dic_2": bloque_html(*dos)}


def ruido_fuera_del_qrs(d0, d):
    """
    Cuanto baja el ruido de la linea base al entrenar.
    Mide la energia de la primera diferencia lejos del pico principal de
    cada atomo. Medirla en todo el atomo no sirve: el pico domina la
    cuenta, y como al entrenar se afila, tapa lo que pasa en el resto

    Inputs:
    -------
    d0: Diccionario inicial
    d: Diccionario entrenado

    Returns:
    -------
    float: Fraccion en que baja la mediana, de 0 a 1

    """
    def rugosidad(m):
        valores = []
        for c in m.T:
            pico = int(np.argmax(np.abs(c)))
            lejos = np.ones(len(c) - 1, dtype=bool)
            lejos[max(pico - MARGEN_QRS, 0):pico + MARGEN_QRS] = False
            valores.append(np.sum(np.diff(c)[lejos] ** 2))
        return np.median(valores)

    return 1.0 - rugosidad(d) / rugosidad(d0)


def region_datos(senal, x, fs):
    """
    La tira de senal con las primeras ventanas resaltadas, y esas mismas
    ventanas ya centradas y normalizadas como columnas de X.

    Inputs:
    -------
    senal: Senal completa del registro
    x: Matriz de ventanas ya preprocesadas
    fs: Frecuencia de muestreo

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    n = int(SEGUNDOS_TIRA * fs)
    tira = senal[:n]
    lo, hi = rango(tira)

    tx, ty, tw, th = 60, 200, 1160, 200
    reducida = tira[::2]

    def tira_html(estilo=""):
        return [caja(tx, ty, tw, th, ident="dat-pt", clase="caja panel",
                     estilo=estilo),
                caja(tx, ty, tw, th, svg(tw, th, polilinea(
                    reducida, tw, th, lo, hi, "tinta")),
                    ident="dat-t", estilo=estilo)]

    util = tw - 2 * MARGEN
    ancho_v = util * TAM_VENTANA / (n - 1)

    marcas = [etiqueta(tx + MARGEN + util * s / SEGUNDOS_TIRA - 30,
                       ty + th + 6, 60, f"{s} s", ident=f"dat-s{s}",
                       clase="etq c chica")
              for s in range(SEGUNDOS_TIRA + 1)]

    uno = tira_html() + marcas
    for i in range(VENTANAS_TIRA):
        inicio = i * TAM_VENTANA
        trozo = tira[inicio:inicio + TAM_VENTANA]
        vx = tx + MARGEN + util * inicio / (n - 1)
        uno.append(caja(vx, ty, ancho_v, th, svg(ancho_v, th, polilinea(
            trozo, ancho_v, th, lo, hi, "azul fino", x0=0.0, x1=1.0)),
            ident=f"dat-v{i}", clase="caja ventana"))
    uno.append(etiqueta(tx, ty + th + 34, tw,
                        f"en azul, las primeras {VENTANAS_TIRA} ventanas "
                        f"de {TAM_VENTANA} muestras", ident="dat-nota"))

    columnas = x[:, :VENTANAS_TIRA]
    lo_c, hi_c = rango(columnas)
    cw, ch, cy = 190, 130, 490
    dos = tira_html("opacity:0.3;") + marcas
    for i in range(VENTANAS_TIRA):
        cx = 60 + i * 230
        dos.append(caja(cx, cy, cw, ch, svg(cw, ch, polilinea(
            columnas[:, i], cw, ch, lo_c, hi_c, "azul")),
            ident=f"dat-v{i}", clase="caja ventana"))
        dos.append(etiqueta(cx, cy + ch + 6, cw, f"columna {i + 1}",
                            clase="etq c chica"))
    dos.append(etiqueta(1210 - 30, cy + 40, 90, "...",
                        clase="etq c grande"))
    dos.append(etiqueta(tx, ty + th + 34, tw,
                        "cada ventana se centra y se normaliza, y pasa a "
                        "ser una columna de X", ident="dat-nota"))

    texto = ("\n\n::: {.etq .c style=\"left:60px; top:662px; "
             "width:1160px;\"}\n"
             f"$X$ es de ${x.shape[0]} \\times {x.shape[1]}$: la primera "
             "mitad entrena y la segunda prueba\n:::")

    return {"datos_tira": bloque_html(*uno),
            "datos_columnas": bloque_html(*dos) + texto}


def region_entrenamiento(dispersion):
    """
    La dispersion por iteracion, dibujandose sola.

    Inputs:
    -------
    dispersion: Atomos por ventana en cada iteracion de K-SVD

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    gx, gy, gw, gh = 130, 140, 680, 420
    lo, hi = 8.0, 11.0
    util_h = gh - 2 * MARGEN

    def y_de(v):
        return gy + MARGEN + (hi - v) * util_h / (hi - lo)

    partes = [caja(gx, gy, gw, gh, clase="caja panel"),
              caja(gx, gy, gw, gh, svg(gw, gh, polilinea(
                  dispersion, gw, gh, lo, hi, "azul grueso dibuja")))]
    for v in (8, 9, 10, 11):
        partes.append(etiqueta(gx - 50, y_de(v) - 12, 40, f"{v}",
                               clase="etq chica",
                               estilo="text-align:right;"))
    n = len(dispersion)
    for it in (1, 5, 10, 15, 20):
        xp = gx + MARGEN + (gw - 2 * MARGEN) * (it - 1) / (n - 1)
        partes.append(etiqueta(xp - 20, gy + gh + 6, 40, f"{it}",
                               clase="etq c chica"))
    partes += [
        etiqueta(gx, gy + gh + 30, gw, "iteración de K-SVD",
                 clase="etq c"),
        etiqueta(gx, gy - 34, gw, "átomos por ventana para llegar al "
                 "error de 0.1", clase="etq"),
        etiqueta(gx + 16, y_de(dispersion[0]) - 34, 120,
                 f"{dispersion[0]:.2f}", clase="etq grande",
                 estilo="color:#2a78d6;"),
        etiqueta(gx + gw - 110, y_de(dispersion[-1]) + 10, 100,
                 f"{dispersion[-1]:.2f}", clase="etq grande",
                 estilo="color:#2a78d6;"),
        etiqueta(860, 170, 380,
                 "El <strong>error</strong> de entrenamiento se queda en "
                 "<strong>0.10</strong> desde la primera iteración: es el "
                 "umbral de paro de OMP.", clase="etq"),
        etiqueta(860, 330, 380,
                 "Lo que baja es cuántos átomos hacen falta para "
                 f"alcanzarlo: de <strong>{dispersion[0]:.2f}</strong> a "
                 f"<strong>{dispersion[-1]:.2f}</strong>.",
                 clase="etq fragment"),
    ]

    return {"entrenamiento": bloque_html(*partes)}


def region_comparacion(curvas):
    """
    Las tres curvas de error, una por fragmento, dibujandose solas.

    Inputs:
    -------
    curvas: Lo que devuelve comparar_diccionarios, en el orden
            aprendido, D_0, DCT

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    gx, gy, gw, gh = 120, 130, 700, 440
    lo, hi = 0.0, 0.85
    topes = np.array(TOPES_COMPARACION, dtype=float)
    posicion = np.log2(topes) / np.log2(topes[-1])
    util_w, util_h = gw - 2 * MARGEN, gh - 2 * MARGEN

    def xy(p, v):
        return (MARGEN + util_w * p, MARGEN + (hi - v) * util_h / (hi - lo))

    estilos = (("azul", "#2a78d6", "aprendido con K-SVD"),
               ("naranja", "#eb6834", "D<sub>0</sub>: ventanas sin "
                                      "entrenar"),
               ("aqua", "#1baf7a", "DCT: diccionario fijo"))

    capas = []
    for f, ((clase, color, _), errores) in enumerate(
            zip(estilos, curvas.values()), start=1):
        coords = [xy(p, v) for p, v in zip(posicion, errores)]
        pares = "\n".join(" ".join(f"{a:.1f},{b:.1f}"
                                    for a, b in coords[i:i + 3])
                           for i in range(0, len(coords), 3))
        circulos = "\n".join(
            f'<circle class="punto {clase}" cx="{a:.1f}" cy="{b:.1f}" '
            f'r="6"/>' for a, b in coords)
        capas.append(
            f'<g class="fragment" data-fragment-index="{f}">\n'
            f'<polyline class="t {clase} grueso dibuja" pathLength="1"\n'
            f'  points="{pares}"/>\n{circulos}\n</g>')

    ultimo = xy(posicion[-1], list(curvas.values())[2][-1])
    capas.append(
        f'<g class="fragment" data-fragment-index="4">\n'
        f'<circle class="pulso aro" cx="{ultimo[0]:.1f}"\n'
        f'  cy="{ultimo[1]:.1f}" r="22"/>\n</g>')

    partes = [caja(gx, gy, gw, gh, clase="caja panel"),
              caja(gx, gy, gw, gh, svg(gw, gh, "\n".join(capas)))]
    for p, t in zip(posicion, TOPES_COMPARACION):
        partes.append(etiqueta(gx + MARGEN + util_w * p - 20,
                               gy + gh + 6, 40, f"{t}",
                               clase="etq c chica"))
    for v in (0.0, 0.2, 0.4, 0.6, 0.8):
        partes.append(etiqueta(gx - 54, gy + xy(0, v)[1] - 12, 44,
                               f"{v:.1f}", clase="etq chica",
                               estilo="text-align:right;"))
    partes += [
        etiqueta(gx, gy + gh + 30, gw, "átomos permitidos por ventana",
                 clase="etq c"),
        etiqueta(gx, gy - 34, gw, "error relativo sobre las ventanas "
                 "de prueba", clase="etq"),
    ]

    errores = list(curvas.values())
    i8 = TOPES_COMPARACION.index(8)
    for f, (clase, color, nombre) in enumerate(estilos, start=1):
        partes.append(etiqueta(
            860, 150 + 52 * (f - 1), 380,
            f'<span class="muestra {clase}-f"></span>{nombre}',
            clase="etq fragment",
            atributos=f'data-fragment-index="{f}"'))
    partes += [
        etiqueta(860, 330, 380,
                 f"Con 8 átomos: <strong>{errores[0][i8]:.3f}</strong> "
                 f"contra {errores[1][i8]:.3f} y {errores[2][i8]:.3f}. "
                 "Donde importa, con pocos átomos, gana el aprendido.",
                 clase="etq fragment",
                 atributos='data-fragment-index="3"'),
        etiqueta(860, 470, 380,
                 f"Con 32 átomos la DCT lo alcanza: "
                 f"{errores[2][-1]:.3f} contra {errores[0][-1]:.3f}.",
                 clase="etq fragment",
                 atributos='data-fragment-index="4"'),
    ]

    return {"comparacion": bloque_html(*partes)}


def region_pacientes(resultados):
    """
    Barras de error por paciente que crecen al entrar a la diapositiva.

    Inputs:
    -------
    resultados: Dict de registro a lo que devuelve evaluar_paciente

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    base, alto_max, tope = 540, 340, 0.25
    partes = []
    for i, (registro, r) in enumerate(resultados.items()):
        bx = 110 + i * 150
        alto = alto_max * r["error_tope"] / tope
        color = "azul-f" if registro == REGISTRO else "naranja-f"
        partes += [
            caja(bx, base - alto, 90, alto,
                 clase=f"barra crece {color}",
                 estilo=f"animation-delay:{0.12 * i:.2f}s;"),
            etiqueta(bx - 20, base - alto - 32, 130,
                     f"{r['error_tope']:.3f}", clase="etq c"),
            etiqueta(bx - 20, base + 8, 130,
                     f"<strong>{registro}</strong><br>serie "
                     f"{registro[0]}00", clase="etq c chica"),
        ]

    marca = '<span class="muestra {}"></span>'
    a = resultados[REGISTRO]["atomos_objetivo"]
    partes += [
        etiqueta(90, 120, 760, "error con 8 átomos, diccionario entrenado "
                 f"solo con el registro {REGISTRO}", clase="etq"),
        etiqueta(860, 150, 380, marca.format("azul-f")
                 + f"registro {REGISTRO}, mitad no usada al entrenar",
                 clase="etq chica"),
        etiqueta(860, 190, 380, marca.format("naranja-f")
                 + "otros pacientes", clase="etq chica"),
        etiqueta(860, 260, 380,
                 "En 103 y 208 funciona igual que en el propio 100.",
                 clase="etq fragment"),
        etiqueta(860, 360, 380,
                 "En 101 y 200 el error sube: hacen falta "
                 f"{resultados['101']['atomos_objetivo']:.1f} y "
                 f"{resultados['200']['atomos_objetivo']:.1f} átomos en "
                 f"lugar de {a:.1f}.", clase="etq fragment"),
        etiqueta(860, 515, 380,
                 "La serie no lo predice: el 208 es de arritmias y sale "
                 "igual de bien.", clase="etq fragment"),
    ]

    return {"pacientes": bloque_html(*partes)}


def region_compresion(atomos_media):
    """
    128 cuadros que se reducen a los pesos y los indices de los atomos.
    Los cuadros que desaparecen siguen en la segunda diapositiva con
    opacidad cero, para que auto-animate los desvanezca en vez de
    quitarlos de golpe

    Inputs:
    -------
    atomos_media: Atomos por ventana en promedio, sobre prueba

    Returns:
    -------
    dict: Nombre de region -> contenido

    """
    lado, hueco = LADO_CUADRO, HUECO_CUADRO
    paso = lado + hueco
    filas = TAM_VENTANA // COLUMNAS_REJILLA
    ancho = COLUMNAS_REJILLA * paso - hueco
    x0, y0 = (1280 - ancho) / 2, 150

    k = int(round(atomos_media))
    rng = np.random.default_rng(7)
    quedan = rng.choice(TAM_VENTANA, 2 * k, replace=False)
    pesos, indices = list(quedan[:k]), list(quedan[k:])

    uno, dos = [], []
    for c in range(TAM_VENTANA):
        cx = x0 + (c % COLUMNAS_REJILLA) * paso
        cy = y0 + (c // COLUMNAS_REJILLA) * paso
        uno.append(caja(cx, cy, lado, lado, ident=f"cmp{c}",
                        clase="cuadro gris-f"))
        if c in pesos:
            i = pesos.index(c)
            dos.append(caja((1280 - k * paso) / 2 + i * paso + 60, 250,
                            lado, lado, ident=f"cmp{c}",
                            clase="cuadro azul-f"))
        elif c in indices:
            i = indices.index(c)
            dos.append(caja((1280 - k * paso) / 2 + i * paso + 60, 320,
                            lado, lado, ident=f"cmp{c}",
                            clase="cuadro aqua-f"))
        else:
            dos.append(caja(cx, cy, lado, lado, ident=f"cmp{c}",
                            clase="cuadro gris-f", estilo="opacity:0;"))

    uno.append(etiqueta(0, y0 + filas * paso + 20, 1280,
                        f"una ventana: {TAM_VENTANA} números",
                        ident="cmp-t", clase="etq c grande"))

    izq = (1280 - k * paso) / 2 + 60 - 280
    dos += [
        etiqueta(izq, 252, 260, f"{k} pesos", clase="etq",
                 estilo="text-align:right;"),
        etiqueta(izq, 322, 260, f"{k} índices de átomo", clase="etq",
                 estilo="text-align:right;"),
        etiqueta(0, 430, 1280,
                 f"<strong>{2 * k} números</strong> en lugar de "
                 f"{TAM_VENTANA}, con error cercano al 10 %",
                 ident="cmp-t", clase="etq c grande"),
        etiqueta(0, 500, 1280,
                 "El diccionario se guarda una sola vez y lo comparten "
                 "quien comprime y quien reconstruye", clase="etq c"),
    ]

    return {"compresion_1": bloque_html(*uno),
            "compresion_2": bloque_html(*dos)}


# =====================================================================
#  Escritura
# =====================================================================

def reescribir_regiones(regiones, ruta=ARCHIVO_QMD):
    """
    Sustituye el contenido de cada region marcada del .qmd.
    Solo toca lo que hay entre los dos comentarios; el resto del archivo
    queda intacto, asi que se puede correr tantas veces como haga falta

    Inputs:
    -------
    regiones: Dict de nombre de region a su contenido
    ruta: Archivo .qmd

    Returns:
    -------
    None: Reescribe el archivo

    """
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    for nombre, contenido in regiones.items():
        patron = re.compile(rf"(<!-- inicio:{nombre} -->\n).*?"
                            rf"(<!-- fin:{nombre} -->)", re.S)
        if not patron.search(texto):
            raise SystemExit(f"no encontre la region {nombre}")
        texto = patron.sub(lambda m: m.group(1) + contenido + "\n"
                           + m.group(2), texto)

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


def guardar_imagen(figura, nombre):
    """
    Guarda una figura en img/ con el fondo del proyecto.

    Inputs:
    -------
    figura: Figure de matplotlib
    nombre: Nombre del archivo

    Returns:
    -------
    None: Escribe el archivo

    """
    os.makedirs(RUTA_IMG, exist_ok=True)
    figura.savefig(os.path.join(RUTA_IMG, nombre), dpi=DPI,
                   facecolor=SUPERFICIE, bbox_inches="tight")


def main():
    """
    Calcula todo, reescribe las regiones y guarda las imagenes.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Modifica Ksvd.qmd y escribe en img/

    """
    if not os.path.exists(ARCHIVO_MODELO):
        raise SystemExit("falta out/modelo.npz, corre src/Experimento.py")

    datos = np.load(ARCHIVO_MODELO)
    d = datos["diccionario"]
    prueba = datos["prueba"]
    alpha_prueba = datos["alpha_prueba"]

    senal, fs = cargar_ecg(REGISTRO)
    x = construir_x(senal)
    entrena, _ = partir_entrenamiento(x)
    ventana = prueba[:, elegir_ventana(prueba)]

    curvas = comparar_diccionarios({
        "aprendido": d,
        "inicial": diccionario_inicial(entrena),
        "dct": diccionario_dct(),
    }, prueba)

    resultados = {REGISTRO: evaluar_paciente(d, prueba)}
    for registro in OTROS_PACIENTES:
        otra, _ = cargar_ecg(registro)
        resultados[registro] = evaluar_paciente(d, construir_x(otra))

    regiones = {}
    regiones.update(region_representacion(d, ventana))
    regiones.update(region_omp(d, ventana))
    regiones.update(region_svd(entrena))
    regiones.update(region_diccionario(diccionario_inicial(entrena), d,
                                       alpha_prueba,
                                       datos["historia_dispersion"]))
    regiones.update(region_datos(senal, x, fs))
    regiones.update(region_entrenamiento(datos["historia_dispersion"]))
    regiones.update(region_comparacion(curvas))
    regiones.update(region_pacientes(resultados))
    regiones.update(region_compresion(
        resultados[REGISTRO]["atomos_objetivo"]))
    reescribir_regiones(regiones)
    print(f"{len(regiones)} regiones reescritas en {ARCHIVO_QMD}")

    guardar_imagen(figura_atomos(d, alpha_prueba), "atomos.png")
    guardar_imagen(figura_reconstruccion(d, prueba), "reconstruccion.png")
    print(f"imagenes en {RUTA_IMG}")


if __name__ == "__main__":
    main()


######################## END OF FIGURASPRESENTACION.PY #########################
################################################################################
