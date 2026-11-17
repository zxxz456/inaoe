<!--
README.md
========================


Descripcion:
------------
Presentacion por equipos de Matematicas para la Computacion sobre el
capitulo 9 de Calling Bullshit (Bergstrom y West, 2020), "The
Susceptibility of Science", con ejemplos propios en lugar de los del
libro


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.2.0


History:
------------
Author      Date            Description
zxxz6       16/11/2026      Solo contenido del capitulo 9
zxxz6       16/11/2026      La falacia del fiscal en una sola diapositiva
zxxz6       16/11/2026      Creation


-->

# Capítulo 9: la susceptibilidad de la ciencia

Presentación del capítulo 9 de *Calling Bullshit: The Art of Skepticism in a Data-Driven World* (Carl T. Bergstrom y Jevin D. West, 2020), el libro de la segunda parte del curso. La única fuente es el libro: todos los conceptos, datos y citas salen del capítulo 9. Los ejemplos que los ilustran son propios, hipotéticos, para no repetir los del libro.

## Contenido

Son 23 diapositivas de contenido en seis secciones, más la referencia al libro:

1. **La ciencia.** Una institución humana que se autocorrige; científicos epistémicamente puros y contaminados (Kitcher); el ciclo de reputación; la replicación.
2. **El valor p.** Qué mide, con un modelo que gana 15 de 20 comparaciones; voltear la condicional; la falacia del fiscal; por qué importa la probabilidad previa.
3. **p-hacking y sesgo de publicación.** Por qué no se publican los negativos, las comparaciones múltiples y Bonferroni, parar en cuanto sale significativo, cómo evitarlo y la ley de Goodhart.
4. **El argumento de Ioannidis.** Un estudio como una prueba médica, la tasa base de hipótesis verdaderas con un control deslizante, y la crítica a sus supuestos.
5. **Del laboratorio al titular.** El teléfono descompuesto de un estudio inventado, por qué las correcciones no viajan, un estudio como argumento y no como hecho, el mercado de las revistas y las depredadoras, y cómo juzgar si un artículo es legítimo.
6. **Por qué la ciencia sí funciona.** Cuatro razones y seis preguntas para leer un hallazgo.

Las notas del presentador son un guion corto en español; se abren con la tecla `s`.

## Archivos

```
presentacion_cap9/
├── README.md
├── SusceptibilidadCiencia.qmd     presentacion en Quarto
├── SusceptibilidadCiencia.html    presentacion compilada, autocontenida
└── FigurasSusceptibilidad.py      simula y escribe las graficas en el qmd
```

## Cómo verla y regenerarla

```bash
cd matcomp/presentacion_cap9
xdg-open SusceptibilidadCiencia.html     # la version compilada
python3 FigurasSusceptibilidad.py        # regenera las graficas en el qmd
quarto render SusceptibilidadCiencia.qmd
```

El script solo necesita numpy. Escribe cuatro figuras SVG entre los comentarios `inicio:nombre` y `fin:nombre` del `.qmd`, que no se editan a mano: la distribución del ejemplo del valor p, la probabilidad de algún falso positivo con varias pruebas, las trayectorias del valor p al juntar datos hasta que salga significativo y el árbol de Ioannidis. La simulación usa semilla fija, así que la cifra de la diapositiva no cambia al regenerar: 29 % de falsos positivos al parar en cuanto p < 0.05.

El control deslizante de la sección 4 es HTML con un script al final del encabezado YAML; funciona sin conexión en el HTML compilado.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
