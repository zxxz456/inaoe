<!--
README.md
========================


Descripcion:
------------
Tarea de correlacion y regresion de Matematicas para la Computacion: un
modelo lineal para el precio de los anuncios de Airbnb en la Ciudad de
Mexico, con notebook y reporte en formato Springer


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       13/11/2026      Version de Arturo en arturo/, con otras
                            variables y tono formal
zxxz6       12/11/2026      Creation


-->

# Tarea: correlación y regresión

## Qué se pide

Con los datos propios (aquí, los de Airbnb del proyecto 2):

1. Calcular la correlación entre las variables independientes.
2. Seleccionar tres variables no correlacionadas o poco correlacionadas entre ellas.
3. Observar la gráfica de dispersión de cada una.
4. Escribir un modelo lineal posible.
5. Calcular los residuos y ajustar el modelo.

Antes hay que decidir si el objetivo es explicar o predecir. El entregable es la ecuación, los β estimados, el R² y el error, el diagnóstico, una gráfica y los límites de la interpretación.

## Resultado

El objetivo es explicar. De once candidatas, la búsqueda sobre todas las ternas con correlación de Spearman menor a 0.3 entre cada par escoge capacidad, distancia al Ángel y calificación, con una correlación máxima de 0.04 entre ellas. El modelo pasa por tres versiones, guiadas por los residuos: el precio en pesos, el logaritmo del precio y, al final, un modelo log-log:

```
log(precio) = 5.959 + 0.717 log(capacidad) - 0.182 log(distancia) + 0.164 calificacion
```

R² de 0.425 con 24,763 anuncios, igual en una partición de prueba del 20 %. Los errores estándar están agrupados por anfitrión, porque los anuncios de un mismo anfitrión no son independientes.

## Archivos

```
tarea_regresion/
├── README.md
├── Regresion.ipynb    analisis completo, paso por paso, con salidas guardadas
├── Reporte.tex        reporte en LNCS de Springer, en tono relajado
├── Reporte.pdf        reporte compilado
├── figuras/           las tres figuras del reporte, las escribe el notebook
└── arturo/            version de Arturo Zabdi Reyes Perez, misma estructura
```

## Versión de Arturo

[`arturo/`](arturo/) repite la actividad con otras variables candidatas y en tono formal. La selección elige baños, longitud (expresada como kilómetros al este del meridiano del Ángel) y alojamiento entero, con una correlación máxima de 0.19 entre ellas. El modelo final es

```
log(precio) = 6.252 + 0.752 log(1 + banos) - 0.031 este + 0.684 entero
```

con R² de 0.347 sobre 28,289 anuncios. El diagnóstico muestra que el número de baños mezcla baños privados y compartidos, con pendientes opuestas. El notebook lee `../../proyecto2/data/2026-09-23/listings.csv.gz` y usa el mismo kernel.

## Cómo correrlo

El notebook lee `../proyecto2/data/2026-09-23/listings.csv.gz`, así que necesita el clon de [zxxz456/proyecto_mate](https://github.com/zxxz456/proyecto_mate) en `matcomp/proyecto2/`. Usa numpy, pandas, scipy y matplotlib; corre con el kernel `matcomp-proyecto1`, el entorno de `matcomp/proyecto1/.venv`. Al ejecutarlo reescribe las figuras de `figuras/`.

El reporte se compila desde esta carpeta:

```bash
latexmk -pdf Reporte.tex
```

<!--
############################### END OF README.MD ###############################
################################################################################
-->
