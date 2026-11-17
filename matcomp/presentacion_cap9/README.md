<!--
README.md
========================


Descripcion:
------------
Presentacion por equipos de Matematicas para la Computacion sobre el
capitulo 9 de Calling Bullshit (Bergstrom y West, 2020), "The
Susceptibility of Science", en el orden del capitulo y con sus
ejemplos


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.5.0


History:
------------
Author      Date            Description
zxxz6       17/11/2026      Carpeta img con las imagenes de las
                            secciones 01 y 02
zxxz6       17/11/2026      Sin el modelo, el Higgs, Scott Kelly ni
                            Dumas-Mallet; 23 diapositivas, dos figuras
zxxz6       17/11/2026      Sin la diapositiva del argumento de
                            Ioannidis; 27 diapositivas
zxxz6       17/11/2026      Sin el control deslizante de Ioannidis
zxxz6       17/11/2026      Del p-hacking en adelante con los ejemplos
                            del libro; tres figuras, 28 diapositivas y
                            el script ya sin numpy
zxxz6       17/11/2026      Seccion del valor p con los ejemplos del
                            libro; cinco figuras y 27 diapositivas
zxxz6       16/11/2026      Solo contenido del capitulo 9
zxxz6       16/11/2026      La falacia del fiscal en una sola diapositiva
zxxz6       16/11/2026      Creation


-->

# Capítulo 9: la susceptibilidad de la ciencia

Presentación del capítulo 9 de *Calling Bullshit: The Art of Skepticism in a Data-Driven World* (Carl T. Bergstrom y Jevin D. West, 2020), el libro de la segunda parte del curso. La única fuente es el libro: todos los conceptos, datos, ejemplos y citas salen del capítulo 9, en su mismo orden y con poco texto por diapositiva.

## Contenido

Son 23 diapositivas de contenido en seis secciones, más la referencia al libro:

1. **La ciencia.** Una institución humana que se autocorrige; científicos epistémicamente puros y contaminados (Kitcher); el ciclo de reputación; la replicación.
2. **El valor p.** En el orden del libro: qué es dicho a la ligera; el robo de arte y la tabla de la huella, que lleva a la falacia del fiscal; las cartas de Carl, con su valor p de 0.043; lo que el valor p da contra lo que queremos saber; y por qué importa la probabilidad previa (H1a y H1b).
3. **p-hacking y sesgo de publicación.** Por qué no se publican los negativos; las decisiones del estudio de elecciones y analgésicos; las tentaciones que llevan al p-hacking; los mil investigadores honestos y el efecto cajón; la ley de Goodhart.
4. **El argumento de Ioannidis.** La falacia de la tasa base con Lyme y *Helicobacter*, y los antidepresivos de Turner: lo registrado ante la FDA contra lo publicado.
5. **Del laboratorio al titular.** Un estudio como argumento y la carta de los opioides, el mercado de las revistas con la uromicitisis de McCool, Pauling y el poliagua, y cómo juzgar si un artículo es legítimo.
6. **Por qué la ciencia sí funciona.** Cuatro razones y seis preguntas para leer un hallazgo.

Las notas del presentador son un guion corto en español; se abren con la tecla `s`.

## Archivos

```
presentacion_cap9/
├── README.md
├── SusceptibilidadCiencia.qmd     presentacion en Quarto
├── SusceptibilidadCiencia.html    presentacion compilada, autocontenida
├── FigurasSusceptibilidad.py      escribe las graficas en el qmd
└── img/                           imagenes de las secciones 01 y 02
```

## Cómo verla y regenerarla

```bash
cd matcomp/presentacion_cap9
xdg-open SusceptibilidadCiencia.html     # la version compilada
python3 FigurasSusceptibilidad.py        # regenera las graficas en el qmd
quarto render SusceptibilidadCiencia.qmd
```

El script solo usa la biblioteca estándar de Python. Escribe dos figuras SVG entre los comentarios `inicio:nombre` y `fin:nombre` del `.qmd`, que no se editan a mano: la binomial de las cartas de Carl, calculada exacta, y las barras de los 74 ensayos de Turner, con las cifras del libro.
<!--
############################### END OF README.MD ###############################
################################################################################
-->
