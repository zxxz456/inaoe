# Tarea 5 - Árbol de expresión booleana en C

Tarea 5 de la segunda parte del curso propedéutico de **Programación y
Estructuras de Datos** (Dr. Miguel Morales Sandoval).

## Instrucciones

Construir un **árbol de expresión booleana** desde una expresión en **notación
postfija** usando una pila, y mostrar el árbol en preorden, inorden y postorden.
Variables: una letra (`a`, `b`, …); operadores: `and`, `or` (binarios) y `not`
(unario).

```
a b and c d and or c not and   ==   ((a and b) or (c and d)) and !c
```

## Solucion

`solucion_Bryan_Violante_Arriaga.c` implementa lo requerido por el autograder:

```c
void *construir(char (*tokens)[8], int n);           // postfijo -> arbol (con pila)
int   evaluar(const void *raiz, const int *valores); // evalua el arbol a 0/1
```

Más los recorridos `preorden`/`inorden`/`postorden` y un `main` de prueba dentro
de `#ifndef MODO_TEST` (para no chocar con el `main` del `test.c`).

## Compilación y ejecución

Dummy test

```bash
$ gcc solucion_Bryan_Violante_Arriaga.c -o demo && ./demo
--> a b and c d and or c not and
	Pre : and or and a b and c d not c 
	In  : a and b or c and d and c not 
	Post: a b and c d and or c not and 
--> a not not not not not
	Pre : not not not not not a 
	In  : a not not not not not 
	Post: a not not not not not 
```

Autograder (`-DMODO_TEST` apaga el `main` propio; los warnings son del `test.c`):

```bash
$ gcc -w -DMODO_TEST test.c solucion_Bryan_Violante_Arriaga.c -o tests && ./tests

+--------------------------------------------------+
|  RESULTADOS FINALES                              |
|  Total        : 3873                            |
|  Pass         : 3873                            |
|  Fail         : 0                               |
|  Calificacion : 100 / 100                        |
+--------------------------------------------------+

```
