"""
FigurasGrafosDelHabla.py
========================


Descripcion:
------------
Genera las dos graficas de datos de GrafosDelHabla.qmd como SVG en
linea y las escribe entre los comentarios inicio:nombre y fin:nombre
de la presentacion:

* clasificacion: AUC, kappa, sensibilidad y especificidad del
  clasificador naive Bayes con medidas de grafo contra escalas
  psicometricas, figura 8 del paper
* globales: rango y mediana de densidad, diametro y camino mas corto
  promedio normalizados por grupo, leidos de la figura 7

Los valores de la figura 8 estan impresos en el paper. Los de la
figura 7 se leyeron de los boxplots, asi que son aproximados y la
diapositiva lo dice; el paper no publica la tabla.

Van en linea y no como imagen para que usen las fuentes de la
presentacion y conserven los tooltips. Se corre con
"python3 FigurasGrafosDelHabla.py" desde esta carpeta.

Los colores son los de la plantilla, teal, magenta y ambar, y pasaron
el validador de la guia de visualizacion en sus combinaciones de dos
y de tres series. Toda barra lleva su valor como etiqueta directa.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       03/11/2026      Paleta y fuente de la plantilla nueva; nota de
                            que evalua cada metrica de clasificacion
zxxz6       02/11/2026      Creation


"""

import re
from pathlib import Path

PRESENTACION = Path(__file__).resolve().parent / "GrafosDelHabla.qmd"

TEAL = "#0b9aa6"
MAGENTA = "#a83487"
AMBAR = "#c97a05"
TINTA = "#0f4c5c"
TINTA_2 = "#52514e"
TENUE = "#8a8984"
REJILLA = "#d9d5c6"
FUENTE = "Palatino Linotype, Book Antiqua, Palatino, serif"

ANCHO = 1180
COMPARACIONES = ["S x M", "S x C", "M x C"]

# Figura 8: (metrica, maximo del eje, [(grafos, escalas)] por comparacion,
# que evalua)
FIGURA_8 = [
    ("AUC", 1.0, [(0.88, 0.57), (0.90, 0.84), (0.80, 0.98)],
     "qué tan lejos del azar queda; 0.5 es azar"),
    ("Kappa", 1.0, [(0.88, 0.25), (0.75, 0.75), (0.37, 0.75)],
     "acuerdo con el diagnóstico, sin el azar"),
    ("Sensibilidad %", 100, [(93.8, 62.5), (87.5, 87.5), (68.8, 87.5)],
     "de los del grupo, cuántos detectó"),
    ("Especificidad %", 100, [(93.7, 62.5), (87.5, 87.5), (68.7, 87.5)],
     "de los ajenos al grupo, cuántos rechazó"),
]

# Figura 7, leida del boxplot: (medida, maximo del eje,
# {grupo: (minimo, mediana, maximo)})
FIGURA_7 = [
    ("Densidad", 11, {
        "S": (2.2, 3.1, 4.0), "M": (5.9, 6.3, 9.0), "C": (2.3, 6.5, 10.3)}),
    ("Diámetro", 0.24, {
        "S": (0.10, 0.12, 0.16), "M": (0.02, 0.045, 0.11),
        "C": (0.02, 0.065, 0.22)}),
    ("Camino más corto promedio", 0.12, {
        "S": (0.045, 0.062, 0.09), "M": (0.012, 0.025, 0.05),
        "C": (0.01, 0.032, 0.105)}),
]
GRUPOS = [("S", "Esquizofrenia", TEAL), ("M", "Manía", MAGENTA),
          ("C", "Control", AMBAR)]


def abrir(ancho, alto):
    """
    Etiqueta de apertura de un SVG con las fuentes de la presentacion.

    Inputs:
    -------
    ancho: Ancho en pixeles
    alto: Alto en pixeles

    Returns:
    -------
    str: La etiqueta svg de apertura

    """
    return (f'<svg viewBox="0 0 {ancho} {alto}" width="{ancho}" '
            f'height="{alto}" style="display:block;margin:0 auto;" '
            f'font-family="{FUENTE}">')


def texto(x, y, contenido, tam=15, color=TINTA_2, ancla="start", extra=""):
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


def barra_vertical(x, y_base, y_tope, ancho, color, titulo):
    """
    Barra vertical con el extremo superior redondeado a 4 px.

    Inputs:
    -------
    x: Borde izquierdo
    y_base: Coordenada de la linea base
    y_tope: Coordenada del extremo de la barra
    ancho: Ancho de la barra
    color: Relleno
    titulo: Texto del tooltip

    Returns:
    -------
    str: Elemento path

    """
    r = min(4, (y_base - y_tope) / 2)
    d = (f"M{x:.1f},{y_base:.1f} V{y_tope + r:.1f} "
         f"a{r},{r} 0 0 1 {r},-{r} H{x + ancho - r:.1f} "
         f"a{r},{r} 0 0 1 {r},{r} V{y_base:.1f} Z")
    return f'<path d="{d}" fill="{color}"><title>{titulo}</title></path>'


def leyenda(y, series):
    """
    Una fila de leyenda con cuadros de color y etiqueta.

    Inputs:
    -------
    y: Coordenada vertical
    series: Pares (color, etiqueta)

    Returns:
    -------
    list: Elementos SVG

    """
    out = []
    x = 40
    for color, etiqueta in series:
        out.append(f'<rect x="{x}" y="{y - 11}" width="14" height="14" '
                   f'rx="3" fill="{color}"/>')
        out.append(texto(x + 22, y, etiqueta, tam=16))
        x += 22 + 9 * len(etiqueta) + 40
    return out


def figura_clasificacion():
    """
    Cuatro paneles de barras agrupadas: una metrica por panel, las
    tres comparaciones en el eje horizontal, dos barras por
    comparacion.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    alto = 400
    arriba, abajo = 70, 310
    margen, hueco = 60, 40
    ancho_panel = (ANCHO - 2 * margen - 3 * hueco) / 4
    ancho_barra, separacion = 30, 2
    out = [abrir(ANCHO, alto)]
    out += leyenda(26, [(TEAL, "Medidas de grafo"),
                        (AMBAR, "Escalas BPRS y PANSS")])
    for i, (nombre, maximo, valores, evalua) in enumerate(FIGURA_8):
        izq = margen + i * (ancho_panel + hueco)
        der = izq + ancho_panel
        out.append(texto((izq + der) / 2, arriba - 14, nombre, tam=18,
                         color=TINTA, ancla="middle",
                         extra=' font-weight="600"'))
        for frac in (0.25, 0.5, 0.75, 1.0):
            y = abajo - frac * (abajo - arriba)
            out.append(f'<line x1="{izq}" y1="{y:.1f}" x2="{der}" '
                       f'y2="{y:.1f}" stroke="{REJILLA}"/>')
        out.append(f'<line x1="{izq}" y1="{abajo}" x2="{der}" '
                   f'y2="{abajo}" stroke="{TENUE}"/>')
        paso = ancho_panel / 3
        for j, (grafo, escala) in enumerate(valores):
            centro = izq + paso * (j + 0.5)
            x0 = centro - ancho_barra - separacion / 2
            for k, (valor, color, serie) in enumerate([
                    (grafo, TEAL, "medidas de grafo"),
                    (escala, AMBAR, "escalas")]):
                x = x0 + k * (ancho_barra + separacion)
                y = abajo - valor / maximo * (abajo - arriba)
                fmt = f"{valor:.2f}" if maximo == 1.0 else f"{valor:.1f}"
                out.append(barra_vertical(
                    x, abajo, y, ancho_barra, color,
                    f"{nombre}, {COMPARACIONES[j]}, {serie}: {fmt}"))
                out.append(texto(x + ancho_barra / 2, y - 6, fmt, tam=13,
                                 ancla="middle"))
            out.append(texto(centro, abajo + 22, COMPARACIONES[j], tam=15,
                             ancla="middle"))
        out.append(texto((izq + der) / 2, abajo + 48, evalua, tam=13,
                         color=TENUE, ancla="middle",
                         extra=' font-style="italic"'))
    out.append(texto(ANCHO / 2, alto - 10,
                     "S: esquizofrenia, M: manía, C: control",
                     tam=14, color=TENUE, ancla="middle"))
    out.append("</svg>")
    return "\n".join(out)


def figura_globales():
    """
    Tres paneles de rangos horizontales: una medida por panel, un
    renglon por grupo, barra de minimo a maximo con la mediana
    marcada.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    alto = 300
    arriba, abajo = 60, 230
    margen, hueco, etiqueta = 40, 50, 110
    ancho_panel = (ANCHO - 2 * margen - 2 * hueco) / 3
    paso = (abajo - arriba) / 3
    out = [abrir(ANCHO, alto)]
    for i, (nombre, maximo, grupos) in enumerate(FIGURA_7):
        izq = margen + i * (ancho_panel + hueco) + etiqueta
        der = margen + (i + 1) * ancho_panel + i * hueco
        out.append(texto((izq + der) / 2, arriba - 24, nombre, tam=18,
                         color=TINTA, ancla="middle",
                         extra=' font-weight="600"'))
        for frac in (0.0, 0.5, 1.0):
            x = izq + frac * (der - izq)
            out.append(f'<line x1="{x:.1f}" y1="{arriba - 6}" '
                       f'x2="{x:.1f}" y2="{abajo}" stroke="{REJILLA}"/>')
            out.append(texto(x, abajo + 20, f"{frac * maximo:g}", tam=13,
                             ancla="middle"))
        for j, (clave, titulo, color) in enumerate(GRUPOS):
            minimo, mediana, max_ = grupos[clave]
            y = arriba + paso * (j + 0.5)
            x1 = izq + minimo / maximo * (der - izq)
            x2 = izq + max_ / maximo * (der - izq)
            xm = izq + mediana / maximo * (der - izq)
            out.append(texto(izq - 14, y + 5, titulo, tam=15, ancla="end"))
            out.append(f'<rect x="{x1:.1f}" y="{y - 9}" '
                       f'width="{x2 - x1:.1f}" height="18" rx="4" '
                       f'fill="{color}" fill-opacity=".35">'
                       f'<title>{nombre}, {titulo}: de {minimo:g} a '
                       f'{max_:g}, mediana {mediana:g}</title></rect>')
            out.append(f'<rect x="{xm - 2:.1f}" y="{y - 13}" width="4" '
                       f'height="26" rx="2" fill="{color}"/>')
    out.append(texto(ANCHO / 2, alto - 10,
                     "Barra: rango del grupo. Marca: mediana. "
                     "Valores por palabra, leídos de la figura 7.",
                     tam=14, color=TENUE, ancla="middle"))
    out.append("</svg>")
    return "\n".join(out)


def escribir(regiones):
    """
    Reemplaza cada region inicio:nombre ... fin:nombre de la
    presentacion por su figura.

    Inputs:
    -------
    regiones: Dict de nombre de region a SVG

    Returns:
    -------
    None: Reescribe GrafosDelHabla.qmd

    """
    texto_qmd = PRESENTACION.read_text(encoding="utf-8")
    for nombre, svg in regiones.items():
        patron = re.compile(rf"(<!-- inicio:{nombre} -->\n).*?"
                            rf"(<!-- fin:{nombre} -->)", re.S)
        if not patron.search(texto_qmd):
            raise SystemExit(f"falta la region inicio:{nombre}")
        bloque = "```{=html}\n" + svg + "\n```\n"
        texto_qmd = patron.sub(lambda m: m.group(1) + bloque + m.group(2),
                               texto_qmd)
    PRESENTACION.write_text(texto_qmd, encoding="utf-8")


def main():
    """
    Arma las dos figuras y las escribe en la presentacion.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Reescribe GrafosDelHabla.qmd

    """
    escribir({
        "clasificacion": figura_clasificacion(),
        "globales": figura_globales(),
    })
    print(f"figuras escritas en {PRESENTACION.name}")


if __name__ == "__main__":
    main()


######################## END OF FIGURASGRAFOSDELHABLA.PY #######################
################################################################################
