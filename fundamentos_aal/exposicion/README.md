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
* Version: 2.0.0


History:
------------
Author      Date            Description
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

La presentación explica el problema del diagnóstico diferencial de la psicosis, cómo se convierte una entrevista en un grafo de palabras, las catorce medidas del grafo, los resultados crudos y normalizados por número de palabras, la clasificación automática contra las escalas psiquiátricas, y la discusión con sus límites. Son 17 diapositivas de contenido en cuatro secciones. Las notas del presentador son un guion corto en viñetas.

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
