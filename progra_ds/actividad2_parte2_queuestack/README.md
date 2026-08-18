# Cola y Pila con lista ligada (en C)

Implementacion de una cola (FIFO) y una pila (LIFO) hechas sobre una lista 
ligada, correspondientes al Ejercicio 3 de las diapositivas de ese tema.

Un detalle: la base usaba `int dequeue()` / `int pop()` que devuelven el dato,
pero si la estructura está vacía no hay un int válido que regresar. Por eso
`desencolar` y `desapilar` reciben un puntero de salida y devuelven 1 o 0 según
si sacaron algo.

## Archivos

- `if/Cola.h`, `Cola.c` - la cola: encolar, desencolar, frente, mostrar, liberar...
- `if/Pila.h`, `Pila.c` - la pila: apilar, desapilar, cima, mostrar, liberar...
- `mainCola.c`, `mainPila.c` - los menús interactivos (`0` mete, `1` saca, otra
  tecla sale).

## Compilar y correr

Se usan headers de actividad1_parte2_linkedlist x lo que se incluyen en el 
compilador con -I../actividad1_parte2_linkedlist/if

```bash
gcc -std=c11 -Wall -Wextra -I../actividad1_parte2_linkedlist/if mainCola.c Cola.c -o cola
gcc -std=c11 -Wall -Wextra -I../actividad1_parte2_linkedlist/if mainPila.c Pila.c -o pila
```
