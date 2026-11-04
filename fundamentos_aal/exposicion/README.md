<!--
README.md
========================


Descripcion:
------------
Exposicion de un paper para Fundamentos para el Analisis Automatico de
Lenguaje: "Speech Graphs Provide a Quantitative Measure of Thought
Disorder in Psychosis" (Mota et al., PLoS ONE 2012)


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 2.1.0


History:
------------
Author      Date            Description
zxxz6       03/11/2026      Presentacion reestructurada en el orden del
                            articulo, con plantilla propia
zxxz6       02/11/2026      Paper cambiado a Mota et al. 2012; presentacion
                            y figuras nuevas
zxxz6       01/11/2026      Paper elegido, presentacion y figuras
zxxz6       21/10/2026      Creation


-->

# Exposición de paper

**Speech Graphs Provide a Quantitative Measure of Thought Disorder in
Psychosis.** Mota, Vasconcelos, Lemos, Pieretti, Kinouchi, Cecchi, Copelli y
Ribeiro. PLoS ONE 7(4): e34928, 2012.
[doi:10.1371/journal.pone.0034928](https://doi.org/10.1371/journal.pone.0034928).

La presentación sigue el orden del artículo con una introducción previa: qué es la psicosis y cómo se diagnostica, qué es un grafo del habla con el ejemplo del paper, y después el paper en sí: participantes, entrevista, las catorce medidas, el análisis, los resultados crudos y normalizados, la clasificación automática contra las escalas psiquiátricas, y la discusión con sus límites. Son 23 diapositivas de contenido en cinco secciones numeradas. Las notas del presentador son un guion corto en viñetas.

La plantilla es propia, sobre el tema serif de reveal.js: fondo crema, títulos en serif con subrayado teal, secciones en claro con número grande y portada en teal oscuro. La paleta teal, magenta y ámbar pasó el validador de la guía de visualización.

## Estructura

```
exposicion/
├── README.md
├── Speech Graphs Provide a Quantitative Measure of Thought Disorder in Psychosis.pdf
├── GrafosDelHabla.qmd          presentacion en Quarto
├── GrafosDelHabla.html         presentacion compilada, autocontenida
├── FigurasGrafosDelHabla.py    escribe las dos graficas de datos en el qmd
└── Figura1Grafos.png           figura 1C del paper, recortada del PDF (CC BY)
```

## Cómo verla y regenerarla

```bash
cd fundamentos_aal/exposicion
quarto preview GrafosDelHabla.qmd      # en vivo
quarto render GrafosDelHabla.qmd       # vuelve a generar el html
python3 FigurasGrafosDelHabla.py       # regenera las graficas en el qmd
```

Las gráficas viven entre los comentarios `inicio:nombre` y `fin:nombre` del `.qmd` y se reescriben con el script; no se editan a mano. La gráfica de medidas globales usa valores leídos de los boxplots de la figura 7, porque el paper no publica esa tabla; la diapositiva lo advierte. Las notas para quien presenta se abren con la tecla `s`.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
