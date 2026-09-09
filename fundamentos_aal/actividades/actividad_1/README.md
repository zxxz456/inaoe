<!--
README.md
========================


Descripcion:
------------
Enunciado de la actividad 1 de Fundamentos para el Analisis Automatico
de Lenguaje, tal como lo dio el profesor. Preprocesar la coleccion Time
y extraer el vocabulario con su frecuencia de termino, tanto de los
documentos como de las consultas.


Considerations:
------------
- Las instrucciones se transcriben literales, no se reinterpretan. Si
  hay una duda de interpretacion se pregunta, no se decide aqui
- La coleccion Time no se versiona: son 423 documentos que se bajan de
  la liga de Glasgow que viene abajo
- Fecha de entrega: 11/09/2026


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0
* License: Copyright (c) 2026 Bryan Violante Arriaga.


History:
------------
Author      Date            Description
zxxz6       08/09/2026      Creation


-->

# Actividad 1

En este directorio se encuentra todo lo relacionado a la actividad 1, la
cual se entrega el 11/sept/2026

## Instrucciones
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

<!--
############################### END OF README.MD ###############################
################################################################################
-->
