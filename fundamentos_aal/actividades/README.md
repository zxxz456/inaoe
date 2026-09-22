<!--
README.md
========================


Descripcion:
------------
Actividad 1


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.3.0
* License: Copyright (c) 2026 Bryan Violante Arriaga.


History:
------------
Author      Date            Description
zxxz6       21/09/2026      El README sube a la raiz de actividades/
zxxz6       14/09/2026      La carpeta actividad_1/ ahora se llama src/
zxxz6       08/09/2026      Creation


-->

# Actividades

En este directorio se encuentra todo lo relacionado a las actividades
de Fundamentos de AAL, codigo, entregables por actividad, etc.

## Actividad 1

### Instrucciones
Con la colección "Time", consistente de 423 documentos con 83 consultas asociadas con sus correspondientes juicios de relevancia, hacer lo siguiente:

- Preprocesar cada documento con: 
    - Eliminación de palabras vacías, usando la lista que viene asociada a la colección.
    - Truncamiento con el algoritmo de Porter.

- Extraer el vocabulario de cada documento junto con su frecuencia de término (tf).

- Repetir las tareas 1 y 2 con las consultas (queries) asociadas.

### NOTAS
Deberá entregarse el código y un archivo listando vocabularios de documentos:

- Doc1 termino1-1 frecuencia1-1 termino1-2 frecuencia1-2 ...
- Doci terminoi-1 frecuenciai-1 terminoi-2 frecuenciai-2 ...

Y de las consultas:
- Query1 termino1-1 frecuencia1-1 termino1-2 frecuencia1-2 ...
- Queryj terminoj-1 frecuenciaj-1 terminoj-2 frecuenciaj-2 ...

La colección se puede obtener de la siguiente liga: http://ir.dcs.gla.ac.uk/resources/test_collections/

Se puede obtener alguna implementación (e información adicional) del algoritmo de Porter en: https://tartarus.org/martin/PorterStemmer/

## Actividad 2

### Instrucciones

Partiendo de la tarea anterior para la colección Time, donde ya se cuenta con el
vocabulario de cada documento y de las consultas:

1) Conjuntar el vocabulario de la colección, calculando la frecuencia de documento
(número de documentos en que aparece) de cada término (aquí no intervienen las
consultas). A partir del vocabulario de la colección, construir los vectores de cada
documento con un pesado tf-idf y cada consulta con pesado binario.

2) Realizar la recuperación de información para las primeras 10 consultas, obteniendo
los documentos que tienen una medida de similitud coseno distinta de cero y
ordenándolos decrecientemente. Calcular los niveles de recuerdo y precisión alcanzados
según el orden obtenido en la recuperación en cada una de las consultas. Para esto se
usarán los juicios de relevancia de la colección.

Se deberá generar una salida de la siguiente forma:

```
Qi
D1 sim1 D2 sim2 ... Dj simj Pi Ri Fi
```

donde i = 1 a 10 indica el número de query, j índica la cantidad de documentos
relevantes para la query i, y Pi, Ri y Fi indican la precisión, recall y F1 obtenidos para la
query Qi.
Entregables: Código y listado de salida generada.

## Actividad 3

### Instrucciones

Partiendo de la tarea 2, para cada consulta recuperar los 100 documentos con mayor
similitud coseno. Considerar los 3 primeros documentos recuperados como relevantes,
y mediante la aplicación de la fórmula de Rocchio, construir una nueva consulta. 
Con esta nueva consulta recuperar nuevamente los 100 documentos con mayor similitud
coseno.
Calcular y comparar el "Average Precision" (AP) de los documentos recuperados para
cada consulta, antes y después de la expansión de la consulta.
Entregables: Código y lista de AP por consulta, antes y después de expansión.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
