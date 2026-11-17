"""
FigurasSusceptibilidad.py
========================


Descripcion:
------------
Dibuja las graficas de datos de la presentacion del capitulo 9 de
Calling Bullshit, y las escribe en SusceptibilidadCiencia.qmd entre los
comentarios inicio:nombre y fin:nombre. Cada figura es un SVG
autocontenido; las regiones del qmd no se editan a mano.

Son dos: la binomial de las cartas de Carl, calculada exacta, y los
ensayos de antidepresivos de Turner, con las cifras del libro.


Considerations:
------------
- Solo usa la biblioteca estandar
- Paleta validada con el validador de la guia de visualizacion: azul
  para lo positivo y naranja para lo negativo. El gris es contexto,
  no serie
- Los simbolos matematicos van como entidades HTML para que el fuente
  quede en ASCII


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.5.0


History:
------------
Author      Date            Description
zxxz6       17/11/2026      Sin la binomial del modelo; solo quedan las
                            cartas de Carl y Turner
zxxz6       17/11/2026      Fuera las figuras propias de comparaciones,
                            parar y el arbol; entra la de Turner del
                            libro, y ya no hace falta numpy
zxxz6       17/11/2026      La binomial toma sus parametros; agrega la
                            de las cartas de Carl del libro
zxxz6       16/11/2026      Solo las figuras de lo que trata el
                            capitulo; arbol de Ioannidis sin potencia
zxxz6       16/11/2026      Sin la cuadricula del detector; la falacia
                            del fiscal va con una tabla en el qmd
zxxz6       16/11/2026      Creation


"""

import math
import re
from pathlib import Path

PRESENTACION = Path(__file__).resolve().parent / "SusceptibilidadCiencia.qmd"

AZUL = "#2a78d6"
NARANJA = "#eb6834"
NARANJA_CLARO = "#f4b08f"
GRIS = "#b9b7af"
TINTA = "#1b2a41"
TINTA_2 = "#52514e"
TENUE = "#8a8984"
REJILLA = "#e3e1da"
FUENTE = "Inter, Segoe UI, Helvetica Neue, Arial, sans-serif"

MAYOR_IGUAL = "&#8805;"
ENSAYOS_FDA = 74


def abrir(ancho, alto, extra=""):
    """
    Etiqueta de apertura de un SVG con la fuente de la presentacion.

    Inputs:
    -------
    ancho: Ancho en pixeles
    alto: Alto en pixeles
    extra: Atributos adicionales para la etiqueta

    Returns:
    -------
    str: La etiqueta svg de apertura

    """
    return (f'<svg viewBox="0 0 {ancho} {alto}" width="{ancho}" '
            f'height="{alto}" style="display:block;margin:0 auto;" '
            f'font-family="{FUENTE}"{extra}>')


def texto(x, y, contenido, tam=19, color=TINTA_2, ancla="start", extra=""):
    """
    Un elemento text de SVG.

    Inputs:
    -------
    x, y: Posicion
    contenido: Texto, puede traer tspan
    tam: Tamano de letra
    color: Color de relleno
    ancla: start, middle o end
    extra: Atributos adicionales

    Returns:
    -------
    str: El elemento text

    """
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tam}" '
            f'fill="{color}" text-anchor="{ancla}"{extra}>{contenido}</text>')


def linea(x1, y1, x2, y2, color=REJILLA, grosor=1, extra=""):
    """
    Un segmento de recta.

    Inputs:
    -------
    x1, y1, x2, y2: Extremos
    color: Color del trazo
    grosor: Ancho del trazo
    extra: Atributos adicionales

    Returns:
    -------
    str: El elemento line

    """
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" stroke="{color}" stroke-width="{grosor}"'
            f'{extra}/>')


def barra_vertical(x, y_base, y_tope, ancho, color, titulo, extra=""):
    """
    Barra vertical con el extremo de datos redondeado a 4 px y la base
    recta.

    Inputs:
    -------
    x: Borde izquierdo
    y_base: Coordenada de la linea base
    y_tope: Coordenada del extremo de la barra
    ancho: Ancho de la barra
    color: Relleno
    titulo: Texto del tooltip
    extra: Atributos adicionales

    Returns:
    -------
    str: Elemento path, o cadena vacia si la barra no tiene altura

    """
    alto = y_base - y_tope
    if alto <= 0.5:
        return ""
    r = min(4, alto / 2, ancho / 2)
    d = (f"M{x:.1f},{y_base:.1f} V{y_tope + r:.1f} "
         f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},-{r:.1f} H{x + ancho - r:.1f} "
         f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} V{y_base:.1f} Z")
    return (f'<path d="{d}" fill="{color}"{extra}>'
            f'<title>{titulo}</title></path>')


def leyenda(x, y, series, tam=19):
    """
    Una fila de leyenda con cuadros de color y etiqueta.

    Inputs:
    -------
    x, y: Esquina izquierda de la fila
    series: Pares (color, etiqueta)
    tam: Tamano de letra

    Returns:
    -------
    list: Elementos SVG

    """
    out = []
    for color, etiqueta in series:
        out.append(f'<rect x="{x}" y="{y - 12}" width="14" height="14" '
                   f'rx="3" fill="{color}"/>')
        out.append(texto(x + 22, y, etiqueta, tam=tam))
        x += 22 + 0.55 * tam * len(etiqueta) + 36
    return out


def figura_binomial(n, prob, observado, k_max, maximo, rejilla, unidad,
                    eje):
    """
    Distribucion binomial del numero de exitos si H0 es cierta, con la
    cola de observado o mas resaltada y su valor p. La usan las cartas
    de Carl.

    Inputs:
    -------
    n: Numero de intentos
    prob: Probabilidad de exito en cada intento bajo H0
    observado: Exitos observados; la cola empieza aqui
    k_max: Ultimo numero de exitos que se dibuja; la cola que queda
           fuera entra al valor p aunque no se vea
    maximo: Probabilidad en el tope del eje vertical
    rejilla: Probabilidades donde van las lineas guia
    unidad: Palabra para el tooltip, como "victorias"
    eje: Leyenda del eje horizontal, sin el "si H0 es cierta"

    Returns:
    -------
    str: SVG completo

    """
    probs = [math.comb(n, k) * prob ** k * (1 - prob) ** (n - k)
             for k in range(n + 1)]
    valor_p = sum(probs[observado:])
    ancho, alto = 1180, 290
    izq, der, arriba, abajo = 80, 1140, 40, 230
    paso = (der - izq) / (k_max + 1)
    out = [abrir(ancho, alto)]
    for frac in rejilla:
        y = abajo - frac / maximo * (abajo - arriba)
        out.append(linea(izq, y, der, y))
        out.append(texto(izq - 10, y + 5, f"{frac:.2f}", tam=17,
                         ancla="end"))
    out.append(linea(izq, abajo, der, abajo, color=TENUE))
    for k, p in enumerate(probs[:k_max + 1]):
        x = izq + k * paso + (paso - 24) / 2
        y = abajo - p / maximo * (abajo - arriba)
        en_cola = k >= observado
        color = NARANJA if en_cola else GRIS
        clase = ' class="fragment" data-fragment-index="1"' if en_cola \
            else ""
        if en_cola:
            out.append(barra_vertical(x, abajo, y, 24, GRIS,
                                      f"{k} {unidad}: {p:.4f}"))
        out.append(barra_vertical(x, abajo, y, 24, color,
                                  f"{k} {unidad}: {p:.4f}", extra=clase))
        out.append(texto(x + 12, abajo + 22, str(k), tam=17,
                         ancla="middle"))
    out.append(texto((izq + der) / 2, abajo + 50,
                     f"{eje}, si H<tspan baseline-shift='sub' "
                     "font-size='11'>0</tspan> es cierta", tam=18,
                     ancla="middle"))
    out.append(texto(izq - 60, arriba - 14, "probabilidad", tam=17))
    x_obs = izq + observado * paso
    out.append(f'<g class="fragment" data-fragment-index="1">')
    out.append(linea(x_obs, arriba + 10, der - 6, arriba + 10,
                     color=TINTA, grosor=1.5))
    out.append(linea(x_obs, arriba + 4, x_obs, arriba + 16, color=TINTA,
                     grosor=1.5))
    out.append(texto((x_obs + der) / 2, arriba + 2,
                     f"P(X {MAYOR_IGUAL} {observado} | H<tspan "
                     f"baseline-shift='sub' font-size='12'>0</tspan>) = "
                     f"{valor_p:.3f}", tam=19, color=TINTA, ancla="middle",
                     extra=' font-weight="700"'))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def figura_turner():
    """
    Los 74 ensayos de antidepresivos registrados ante la FDA contra lo
    que llego a las revistas, segun Turner y colegas. Dos barras
    apiladas en las que cada ensayo ocupa el mismo ancho, asi que se ve
    cuanto se quedo sin publicar; la segunda aparece como fragmento.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    ancho, alto = 1180, 262
    izq, der, grueso = 260, 1150, 58
    unidad = (der - izq) / ENSAYOS_FDA
    fragmento = ' class="fragment" data-fragment-index="1"'
    filas = [
        ("Registrados ante la FDA", 24, "", [
            (38, AZUL, "38 positivos"),
            (12, GRIS, "12 dudosos"),
            (24, NARANJA, "24 negativos")]),
        ("Publicados en revistas", 116, fragmento, [
            (37, AZUL, "37 positivos"),
            (11, NARANJA_CLARO, "11"),
            (3, NARANJA, "3"),
            (23, None, "23 sin publicar")]),
    ]
    out = [abrir(ancho, alto)]
    for nombre, y, clase, tramos in filas:
        out.append(f"<g{clase}>")
        out.append(texto(izq - 16, y + grueso / 2 + 7, nombre, tam=19,
                         color=TINTA, ancla="end"))
        x = izq
        for n, color, etiqueta in tramos:
            w = n * unidad
            if color is None:
                relleno = (f'fill="none" stroke="{TENUE}" '
                           f'stroke-dasharray="6 4"')
                tinta = TINTA_2
            else:
                relleno = f'fill="{color}"'
                tinta = "#ffffff" if color in (AZUL, NARANJA) else TINTA
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w - 2:.1f}" '
                       f'height="{grueso}" rx="4" {relleno}>'
                       f'<title>{n} ensayos</title></rect>')
            out.append(texto(x + w / 2, y + grueso / 2 + 7, etiqueta,
                             tam=19, color=tinta, ancla="middle",
                             extra=' font-weight="700"'))
            x += w
        out.append("</g>")
    out.extend(leyenda(izq, 236, [
        (AZUL, "positivo"), (GRIS, "dudoso"), (NARANJA, "negativo"),
        (NARANJA_CLARO, "negativo o dudoso, publicado como positivo")],
        tam=17))
    out.append("</svg>")
    return "\n".join(out)


def escribir(figuras):
    """
    Reemplaza cada region inicio:nombre / fin:nombre del qmd por su
    figura dentro de un bloque HTML crudo.

    Inputs:
    -------
    figuras: Diccionario nombre -> contenido HTML de la region

    Returns:
    -------
    None: Reescribe SusceptibilidadCiencia.qmd

    """
    texto_qmd = PRESENTACION.read_text(encoding="utf-8")
    for nombre, contenido in figuras.items():
        patron = re.compile(rf"(<!-- inicio:{nombre} -->\n).*?"
                            rf"(<!-- fin:{nombre} -->)", re.S)
        if not patron.search(texto_qmd):
            raise SystemExit(f"falta la region inicio:{nombre}")
        bloque = "```{=html}\n" + contenido + "\n```\n"
        texto_qmd = patron.sub(lambda m: m.group(1) + bloque + m.group(2),
                               texto_qmd)
    PRESENTACION.write_text(texto_qmd, encoding="utf-8")


def main():
    """
    Arma las figuras y las escribe en la presentacion.

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    escribir({
        "cartas": figura_binomial(
            52, 0.25, 19, 30, 0.14, (0.04, 0.08, 0.12), "aciertos",
            "aciertos de Carl en 52 cartas"),
        "turner": figura_turner(),
    })


if __name__ == "__main__":
    main()

######################## END OF FIGURASSUSCEPTIBILIDAD.PY ######################
################################################################################
