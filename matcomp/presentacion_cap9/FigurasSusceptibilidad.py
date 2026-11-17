"""
FigurasSusceptibilidad.py
========================


Descripcion:
------------
Simula y dibuja las graficas de datos de la presentacion del capitulo 9
de Calling Bullshit, y las escribe en SusceptibilidadCiencia.qmd entre
los comentarios inicio:nombre y fin:nombre. Cada figura es un SVG
autocontenido; las regiones del qmd no se editan a mano.

Todas las simulaciones usan una semilla fija, asi que las cifras que
aparecen en las diapositivas son reproducibles.


Considerations:
------------
- Solo necesita numpy; las colas de la normal salen de math.erfc
- Paleta validada con el validador de la guia de visualizacion: azul
  para lo verdadero y naranja para los falsos positivos. El gris es
  contexto, no serie
- Los simbolos matematicos van como entidades HTML para que el fuente
  quede en ASCII


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.2.0


History:
------------
Author      Date            Description
zxxz6       16/11/2026      Solo las figuras de lo que trata el
                            capitulo; arbol de Ioannidis sin potencia
zxxz6       16/11/2026      Sin la cuadricula del detector; la falacia
                            del fiscal va con una tabla en el qmd
zxxz6       16/11/2026      Creation


"""

import math
import re
from pathlib import Path

import numpy as np

PRESENTACION = Path(__file__).resolve().parent / "SusceptibilidadCiencia.qmd"

AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#b9b7af"
GRIS_CLARO = "#dcd9d0"
TINTA = "#1b2a41"
TINTA_2 = "#52514e"
TENUE = "#8a8984"
REJILLA = "#e3e1da"
FONDO = "#fbfaf7"
FUENTE = "Inter, Segoe UI, Helvetica Neue, Arial, sans-serif"

ALFA = 0.05
Z_CRITICO = 1.959964
MAYOR_IGUAL = "&#8805;"


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


def cola_normal(z):
    """
    Valor p de dos colas para un estadistico z.

    Inputs:
    -------
    z: Estadistico, escalar o arreglo

    Returns:
    -------
    float o ndarray: P(|Z| >= |z|) bajo la normal estandar

    """
    return np.vectorize(lambda v: math.erfc(abs(v) / math.sqrt(2)))(z)


def porcentaje(valor, decimales=0):
    """
    Formatea una proporcion como porcentaje con espacio fino.

    Inputs:
    -------
    valor: Proporcion entre 0 y 1
    decimales: Decimales a mostrar

    Returns:
    -------
    str: Por ejemplo "64 %"

    """
    return f"{valor * 100:.{decimales}f}&#8201;%"


def figura_binomial():
    """
    Distribucion del numero de victorias en 20 conjuntos de datos si los
    dos modelos son igual de buenos, con la cola de 15 o mas resaltada.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    n, observado = 20, 15
    probs = [math.comb(n, k) / 2 ** n for k in range(n + 1)]
    valor_p = sum(probs[observado:])
    ancho, alto = 1180, 290
    izq, der, arriba, abajo = 80, 1140, 40, 230
    maximo = 0.18
    paso = (der - izq) / (n + 1)
    out = [abrir(ancho, alto)]
    for frac in (0.05, 0.10, 0.15):
        y = abajo - frac / maximo * (abajo - arriba)
        out.append(linea(izq, y, der, y))
        out.append(texto(izq - 10, y + 5, f"{frac:.2f}", tam=17,
                         ancla="end"))
    out.append(linea(izq, abajo, der, abajo, color=TENUE))
    for k, p in enumerate(probs):
        x = izq + k * paso + (paso - 24) / 2
        y = abajo - p / maximo * (abajo - arriba)
        en_cola = k >= observado
        color = NARANJA if en_cola else GRIS
        clase = ' class="fragment" data-fragment-index="1"' if en_cola \
            else ""
        if en_cola:
            out.append(barra_vertical(x, abajo, y, 24, GRIS,
                                      f"{k} victorias: {p:.4f}"))
        out.append(barra_vertical(x, abajo, y, 24, color,
                                  f"{k} victorias: {p:.4f}", extra=clase))
        out.append(texto(x + 12, abajo + 22, str(k), tam=17,
                         ancla="middle"))
    out.append(texto((izq + der) / 2, abajo + 50,
                     "victorias de mi modelo en 20 conjuntos de datos, "
                     "si H<tspan baseline-shift='sub' font-size='11'>0"
                     "</tspan> es cierta", tam=18, ancla="middle"))
    out.append(texto(izq - 60, arriba - 14, "probabilidad", tam=17))
    x_obs = izq + observado * paso
    out.append(f'<g class="fragment" data-fragment-index="1">')
    out.append(linea(x_obs, arriba + 10, der - 6, arriba + 10,
                     color=TINTA, grosor=1.5))
    out.append(linea(x_obs, arriba + 4, x_obs, arriba + 16, color=TINTA,
                     grosor=1.5))
    out.append(texto((x_obs + der) / 2, arriba + 2,
                     f"P(X {MAYOR_IGUAL} 15 | H<tspan baseline-shift='sub' "
                     f"font-size='12'>0</tspan>) = {valor_p:.3f}", tam=19,
                     color=TINTA, ancla="middle",
                     extra=' font-weight="700"'))
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def figura_comparaciones():
    """
    Probabilidad de al menos un falso positivo al hacer k pruebas
    independientes con todas las hipotesis nulas ciertas, sin correccion
    y con la correccion de Bonferroni.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    ks = np.arange(1, 31)
    sin = 1 - (1 - ALFA) ** ks
    con = 1 - (1 - ALFA / ks) ** ks
    ancho, alto = 1180, 340
    izq, der, arriba, abajo = 90, 960, 50, 280

    def px(k):
        """
        Coordenada horizontal del numero de pruebas k.

        Inputs:
        -------
        k: Numero de pruebas

        Returns:
        -------
        float: Coordenada en pixeles

        """
        return izq + (k - 1) / 29 * (der - izq)

    def py(v):
        """
        Coordenada vertical de una probabilidad.

        Inputs:
        -------
        v: Probabilidad entre 0 y 1

        Returns:
        -------
        float: Coordenada en pixeles

        """
        return abajo - v * (abajo - arriba)

    out = [abrir(ancho, alto)]
    for v in (0.25, 0.5, 0.75, 1.0):
        out.append(linea(izq, py(v), der, py(v)))
        out.append(texto(izq - 10, py(v) + 5, porcentaje(v), tam=17,
                         ancla="end"))
    out.append(linea(izq, abajo, der, abajo, color=TENUE))
    out.append(texto(izq - 10, abajo + 5, "0", tam=17, ancla="end"))
    for k in (1, 5, 10, 15, 20, 25, 30):
        out.append(texto(px(k), abajo + 24, str(k), tam=17, ancla="middle"))
    out.append(texto((izq + der) / 2, abajo + 52,
                     "número de hipótesis probadas con los mismos datos",
                     tam=18, ancla="middle"))
    out += leyenda(izq, 24, [(NARANJA, "sin corrección"),
                             (AZUL, "con Bonferroni (α / k en cada prueba)")])
    for serie, color, clase in [(con, AZUL, ""), (sin, NARANJA, "dibuja")]:
        puntos = " ".join(f"{px(k):.1f},{py(v):.1f}"
                          for k, v in zip(ks, serie))
        out.append(f'<polyline points="{puntos}" fill="none" '
                   f'stroke="{color}" stroke-width="2.5" '
                   f'stroke-linejoin="round" stroke-linecap="round" '
                   f'class="{clase}" pathLength="1"/>')
    for k in (1, 5, 10, 20):
        v = sin[k - 1]
        out.append(f'<circle cx="{px(k):.1f}" cy="{py(v):.1f}" r="5" '
                   f'fill="{NARANJA}" stroke="{FONDO}" stroke-width="2">'
                   f'<title>{k} pruebas: {porcentaje(v, 1)}</title>'
                   f'</circle>')
        out.append(texto(px(k) - 8, py(v) - 12, porcentaje(v), tam=19,
                         color=TINTA, ancla="end",
                         extra=' font-weight="700"'))
    out.append(texto(der + 12, py(sin[-1]) + 5,
                     porcentaje(sin[-1]) + " sin corregir", tam=18))
    out.append(texto(der + 12, py(con[-1]) + 5,
                     porcentaje(con[-1], 1) + " con Bonferroni", tam=18))
    out.append("</svg>")
    return "\n".join(out)


def figura_parar():
    """
    Parar en cuanto el valor p baja de 0.05: trayectorias del valor p
    con datos de pura ruido, revisando cada 10 observaciones.

    Inputs:
    -------
    None

    Returns:
    -------
    tuple: (SVG completo, tasa de falsos positivos con la regla)

    """
    revisiones = np.arange(10, 301, 10)
    generador = np.random.default_rng(2026)

    def trayectoria(datos):
        """
        Valor p en cada revision para una serie de observaciones.

        Inputs:
        -------
        datos: Arreglo de observaciones N(0, 1)

        Returns:
        -------
        ndarray: Valor p de dos colas en cada revision

        """
        sumas = np.cumsum(datos)[revisiones - 1]
        return cola_normal(sumas / np.sqrt(revisiones))

    simulaciones = generador.standard_normal((10000, revisiones[-1]))
    sumas = np.cumsum(simulaciones, axis=1)[:, revisiones - 1]
    zetas = np.abs(sumas / np.sqrt(revisiones))
    tasa = float(np.mean((zetas > Z_CRITICO).any(axis=1)))

    ejemplos = generador.standard_normal((18, revisiones[-1]))
    ancho, alto = 1180, 360
    izq, der, arriba, abajo = 90, 1000, 30, 300
    decadas = 3

    def px(n):
        """
        Coordenada horizontal del tamano de muestra n.

        Inputs:
        -------
        n: Numero de observaciones

        Returns:
        -------
        float: Coordenada en pixeles

        """
        return izq + (n - 10) / 290 * (der - izq)

    def py(p):
        """
        Coordenada vertical de un valor p en escala logaritmica.

        Inputs:
        -------
        p: Valor p

        Returns:
        -------
        float: Coordenada en pixeles

        """
        p = max(p, 10 ** -decadas)
        return arriba + (-math.log10(p)) / decadas * (abajo - arriba)

    out = [abrir(ancho, alto)]
    out.append(f'<rect x="{izq}" y="{py(ALFA):.1f}" width="{der - izq}" '
               f'height="{abajo - py(ALFA):.1f}" fill="{NARANJA}" '
               f'opacity="0.08"/>')
    for p in (1, 0.1, 0.01, 0.001):
        out.append(linea(izq, py(p), der, py(p)))
        out.append(texto(izq - 10, py(p) + 5, f"{p:g}", tam=17, ancla="end"))
    out.append(linea(izq, py(ALFA), der, py(ALFA), color=NARANJA,
                     grosor=1.5))
    out.append(texto(der + 12, py(ALFA) + 5, "p = 0.05", tam=18,
                     color=TINTA, extra=' font-weight="700"'))
    out.append(texto(der + 12, py(0.005), "zona", tam=17))
    out.append(texto(der + 12, py(0.005) + 18, "significativa", tam=17))
    for n in (10, 50, 100, 150, 200, 250, 300):
        out.append(texto(px(n), abajo + 24, str(n), tam=17, ancla="middle"))
    out.append(texto((izq + der) / 2, abajo + 52,
                     "observaciones juntadas hasta el momento",
                     tam=18, ancla="middle"))
    out.append(texto(izq - 70, arriba - 12, "valor p", tam=17))
    grises, naranjas = [], []
    for datos in ejemplos:
        ps = trayectoria(datos)
        cruce = np.flatnonzero(ps < ALFA)
        fin = cruce[0] + 1 if len(cruce) else len(ps)
        puntos = " ".join(f"{px(n):.1f},{py(p):.1f}"
                          for n, p in zip(revisiones[:fin], ps[:fin]))
        if len(cruce):
            n_par, p_par = revisiones[cruce[0]], ps[cruce[0]]
            naranjas.append(
                f'<polyline points="{puntos}" fill="none" '
                f'stroke="{NARANJA}" stroke-width="2.5" '
                f'stroke-linejoin="round"/>'
                f'<circle cx="{px(n_par):.1f}" cy="{py(p_par):.1f}" r="6" '
                f'fill="{NARANJA}" stroke="{FONDO}" stroke-width="2">'
                f'<title>se detiene con n = {n_par}, p = {p_par:.3f}'
                f'</title></circle>')
        else:
            grises.append(f'<polyline points="{puntos}" fill="none" '
                          f'stroke="{GRIS}" stroke-width="2" '
                          f'stroke-linejoin="round"/>')
    out += grises
    out.append('<g class="fragment" data-fragment-index="1">')
    out += naranjas
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out), tasa


def caja(x, y, ancho, alto, borde, lineas, relleno="#ffffff", tam=17,
         extra=""):
    """
    Caja redondeada con borde izquierdo de color y una o varias lineas
    de texto centradas verticalmente.

    Inputs:
    -------
    x, y: Esquina superior izquierda
    ancho, alto: Dimensiones
    borde: Color de la franja izquierda
    lineas: Lista de pares (texto, negrita)
    relleno: Color de fondo
    tam: Tamano de letra
    extra: Atributos del grupo

    Returns:
    -------
    str: Grupo SVG

    """
    out = [f'<g{extra}>',
           f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" rx="6" '
           f'fill="{relleno}" stroke="{REJILLA}"/>',
           f'<rect x="{x}" y="{y}" width="8" height="{alto}" rx="3" '
           f'fill="{borde}"/>']
    alto_linea = tam * 1.3
    y0 = y + alto / 2 - alto_linea * (len(lineas) - 1) / 2 + tam * 0.35
    for i, (contenido, negrita) in enumerate(lineas):
        peso = ' font-weight="700"' if negrita else ""
        out.append(texto(x + 22, y0 + i * alto_linea, contenido, tam=tam,
                         color=TINTA if negrita else TINTA_2, extra=peso))
    out.append("</g>")
    return "".join(out)


def curva(x1, y1, x2, y2, color=GRIS, grosor=1.5, extra=""):
    """
    Conector en S entre dos puntos, horizontal en ambos extremos.

    Inputs:
    -------
    x1, y1: Punto de salida
    x2, y2: Punto de llegada
    color: Color del trazo
    grosor: Ancho del trazo
    extra: Atributos adicionales

    Returns:
    -------
    str: Elemento path

    """
    medio = (x1 + x2) / 2
    return (f'<path d="M{x1:.1f},{y1:.1f} C{medio:.1f},{y1:.1f} '
            f'{medio:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{grosor}"{extra}/>')


def figura_arbol():
    """
    Arbol de frecuencias naturales del argumento de Ioannidis, como lo
    plantea el libro: 1000 hipotesis, 10 % verdaderas que salen
    positivas, y alfa de 5 % para las falsas.

    Inputs:
    -------
    None

    Returns:
    -------
    str: SVG completo

    """
    ancho, alto = 1180, 380
    out = [abrir(ancho, alto)]
    a, h = 230, 76
    out.append(caja(20, 152, a, h, TINTA, [("1000", True),
                                          ("hipótesis probadas", False)]))
    f1 = ' class="fragment" data-fragment-index="1"'
    f2 = ' class="fragment" data-fragment-index="2"'
    f3 = ' class="fragment" data-fragment-index="3"'
    out.append(f"<g{f1}>")
    out.append(curva(250, 190, 330, 95))
    out.append(curva(250, 190, 330, 285))
    out.append(texto(262, 120, "10&#8201;%", tam=17))
    out.append(texto(262, 270, "90&#8201;%", tam=17))
    out.append("</g>")
    out.append(caja(330, 57, a, h, AZUL, [("100", True),
                                         ("verdaderas", False)], extra=f1))
    out.append(caja(330, 247, a, h, GRIS, [("900", True),
                                          ("falsas", False)], extra=f1))
    out.append(f"<g{f2}>")
    out.append(curva(560, 95, 640, 95))
    out.append(curva(560, 285, 640, 240))
    out.append(curva(560, 285, 640, 330))
    out.append(texto(630, 205, "α = 5&#8201;%", tam=17, ancla="end"))
    out.append("</g>")
    out.append(caja(640, 65, a, 60, AZUL, [("100 significativas", True)],
                    extra=f2))
    out.append(caja(640, 210, a, 60, NARANJA,
                    [("45 significativas", True)], extra=f2))
    out.append(caja(640, 300, a, 60, GRIS_CLARO, [("855 no", False)],
                    extra=f2))
    out.append(f"<g{f3}>")
    out.append(curva(870, 95, 940, 150, color=AZUL, grosor=2.5))
    out.append(curva(870, 240, 940, 200, color=NARANJA, grosor=2.5))
    out.append(caja(940, 120, 220, 112, TINTA,
                    [("145 hallazgos", True), ("100 verdaderos,", False),
                     ("45 falsos", False)], tam=17))
    out.append(texto(1050, 268, "verdaderos: 100 / 145", tam=17,
                     color=TINTA, ancla="middle"))
    out.append(texto(1050, 300, "= 69&#8201;%", tam=26, color=TINTA,
                     ancla="middle", extra=' font-weight="800"'))
    out.append("</g>")
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
    Corre la simulacion, arma las figuras y las escribe en la
    presentacion. Imprime la cifra que cita la diapositiva.

    Inputs:
    -------
    None

    Returns:
    -------
    None

    """
    parar, tasa = figura_parar()
    escribir({
        "binomial": figura_binomial(),
        "comparaciones": figura_comparaciones(),
        "parar": parar,
        "arbol": figura_arbol(),
    })
    print(f"parar en cuanto p < 0.05: falsos positivos {tasa:.3f}")


if __name__ == "__main__":
    main()

######################## END OF FIGURASSUSCEPTIBILIDAD.PY ######################
################################################################################
