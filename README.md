<!--
README.md
========================


Descripción:
------------
Índice del repositorio: qué materia vive en cada carpeta y qué hace
cada proyecto. Es lo primero que se lee al abrir el repo, así que se
queda en el nivel de una línea por entrada; el detalle vive en el
README de cada carpeta.


Considerations:
------------
- Cada carpeta nueva se agrega aquí en el mismo commit que la crea, si
  no el índice se desincroniza y nadie lo nota hasta meses después
- El orden dentro de cada materia es cronológico, no alfabético: lo
  más reciente queda abajo


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.4.0
* License: Copyright (c) 2026 Bryan Violante Arriaga.


History:
------------
Author      Date            Description
zxxz6       19/08/2026      matcomp ya tiene libreta, no solo el crudo
zxxz6       19/08/2026      Agregue matcomp/ al indice
zxxz6       18/08/2026      Agregue fundamentos_aal/ al indice
zxxz6       18/08/2026      Agregue ada/ y templates/ al indice
zxxz6       09/08/2026      Creation


-->

# inaoe 


Repositorio personal 
para ejercicios, prácticas y experimentos de las materias del INAOE.


## Estructura 

- [ada/](ada/) - Análisis y Diseño de Algoritmos.
  - [apuntes/](ada/apuntes/) - Libreta de clase en LaTeX (`libreta.tex`),
    una sección por sesión, más la toma cruda en `.txt`.
- [fundamentos_aal/](fundamentos_aal/) - Fundamentos para el Análisis
  Automático de Lenguaje.
  - [apuntes/](fundamentos_aal/apuntes/) - Libreta de clase en LaTeX
    (`libreta.tex`), una sección por sesión, más la toma cruda en `.txt`.
- [matcomp/](matcomp/) - Matemáticas para Computación.
  - [apuntes/](matcomp/apuntes/) - Libreta de clase en LaTeX
    (`libreta.tex`), una sección por sesión, más la toma cruda en `.txt`.
- [taylf/](taylf/) - Teoría de Autómatas y Lenguajes Formales.
  - [DTM_simple/](taylf/DTM_simple/) - Simulador de una Máquina de Turing
    determinista de una sola cinta
  - [alfabeto_potencia.py](taylf/alfabeto_potencia.py) - genera la k-ésima
    potencia de un alfabeto 
  - [alfabeto_potencias_hasta_k.py](taylf/alfabeto_potencias_hasta_k.py) -
    variante que genera todas las potencias desde `Σ^0` hasta `Σ^k` y muestra cada
    una con su cardinalidad
- [progra_ds/](progra_ds/) - Programación y Estructuras de Datos.
  - [actividad_1/](progra_ds/actividad_1/) - Historia de las computadoras (documento LaTeX).
  - [actividad_3/](progra_ds/actividad_3/) - Tipos de algoritmos (documento LaTeX).
  - [BST/](progra_ds/BST/) - Simulador interactivo de un Árbol Binario de Búsqueda
    con animación en el navegador (insertar, buscar y eliminar).
  - [Pila/](progra_ds/Pila/) - Simulador interactivo de una Pila (Stack, LIFO):
    push, pop, peek, buscar y recorrer.
  - [Cola/](progra_ds/Cola/) - Simulador interactivo de una Cola (Queue, FIFO):
    enqueue, dequeue, peek, buscar y recorrer.
  - [Heap/](progra_ds/Heap/) - Simulador interactivo de un Heap binario
    (min o max): insertar, extraer, peek, buscar y recorrer; con bubble-up
    y bubble-down animados.
  - [HashTable/](progra_ds/HashTable/) - Simulador interactivo de una Tabla
    Hash con encadenamiento: insertar, buscar, eliminar y recorrer.
  - [ArbolBinario/](progra_ds/ArbolBinario/) - Simulador interactivo de un
    Árbol Binario genérico (no BST): inserción por nivel, búsqueda,
    eliminación de subárbol y recorridos pre/in/post/level.
  - [Arbol/](progra_ds/Arbol/) - Simulador interactivo de un Árbol n-ario
    (general): inserción como hijo de un padre, búsqueda, eliminación de
    subárbol y recorridos pre/post/level.
  - [tarea1_parte2/](progra_ds/tarea1_parte2/) - Tarea 1 (parte 2): modelado
    orientado a objetos de un sistema bancario en C++ (clientes y cuentas de
    ahorro/cheques), con herencia, polimorfismo y un singleton para los
    identificadores de cuenta.
  - [tarea2_parte2/](progra_ds/tarea2_parte2/) - Tarea 2 (parte 2): jerarquía de
    empleados (`Employee`) en C++ con el método `ganancias()`/`earnings()`
    polimórfico por subclase (asalariado, por hora, por comisiones y base más
    comisiones).
  - [actividad1_parte2_linkedlist/](progra_ds/actividad1_parte2_linkedlist/) -
    Lista ligada simple de enteros en C puro (structs, sin clases), con menú
    interactivo para agregar y eliminar.
  - [actividad2_parte2_queuestack/](progra_ds/actividad2_parte2_queuestack/) -
    Cola (FIFO) y pila (LIFO) sobre lista ligada en C, reutilizando el nodo de la
    actividad anterior. Ejercicio 3 de las diapositivas de listas y colas.
  - [tarea3_parte2_postfix_calc/](progra_ds/tarea3_parte2_postfix_calc/) - Tarea 3
    (parte 2): calculadora de notación posfija (postfix) en C, evaluada con una
    pila de enteros sobre lista ligada. Solo se versiona la solución (`solucion.c`).
  - [actividad3_parte2_avl/](progra_ds/actividad3_parte2_avl/) - Actividad 3
    (parte 2): árbol binario con control de altura (estilo AVL) en C. Sobre el
    código base se implementaron los tres recorridos (pre/in/postorden)
  - [tarea4_parte2_arbol/](progra_ds/tarea4_parte2_arbol/) - Tarea 4 (parte 2):
    dos funciones para árboles binarios en C: `insertar` (inserción por niveles
    con BFS) y `construir` (reconstrucción del árbol a partir de sus recorridos
    preorden e inorden). Solo se versiona la solución.
  - [tarea5_parte2_booleanas/](progra_ds/tarea5_parte2_booleanas/) - Tarea 5
    (parte 2): árbol de expresión booleana en C. `construir` arma el árbol desde
    una expresión en notación postfija usando una pila, `evaluar`, 
    y se agregan los tres recorridos (pre/in/postorden).

## Plantillas

- [templates/](templates/) - Lo que comparten los documentos de LaTeX.
  - [Preambulo.tex](templates/Preambulo.tex) - Preámbulo compartido de los
    apuntes: paquetes, estilo de página, entornos de teorema, cajas de
    color, listings y pseudocódigo en español. Cada documento lo carga
    con `\input` en vez de copiarlo, así que un arreglo ahí llega a
    todas las libretas de una vez.
  - [PlantillaApuntes.tex](templates/PlantillaApuntes.tex) - Punto de
    partida para una libreta nueva, y ejemplo de uso de cada entorno.
  - [ReferenciaLatex.md](templates/ReferenciaLatex.md) - Chuleta de los
    comandos y las fórmulas que salen a cada rato.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
