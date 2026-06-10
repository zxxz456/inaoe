# Lista ligada simple (en C)

Una lista ligada de enteros, hecha en C puro (solo structs y funciones, nada de
clases). Está organizada parecido a la tarea1: los headers en `if/` y la
implementación en los `.c`.

La actividad que se dejó en clase era modificar el programa para agregar la
opción de eliminar con la tecla `1` (el original solo agregaba elementos).
Aproveché para cambiar la estructura del proyecto —separándolo en varios
archivos—, pero en esencia sigue siendo lo mismo: la misma lista ligada.

La lista vive en un struct `Lista` (guarda la cabeza y el tamaño) que se pasa por
puntero a cada función, en vez de la variable global `head` del código original.
Así se pueden tener varias listas a la vez. El nodo está aparte, en `Nodo.h`.

## Archivos

- `if/Nodo.h` — el nodo: un int y el puntero al siguiente.
- `if/Lista.h` — la lista y las firmas de las operaciones.
- `if/Utils.h` — `limpiarPantalla()` (también se reutiliza en la
  [actividad2](../actividad2_parte2_queuestack/)).
- `Lista.c` — agregar (al inicio o al final), eliminar, buscar, mostrar, liberar, etc.
- `main.c` — menú interactivo: `0` agrega, `1` elimina, cualquier otra tecla sale.

## Compilar y correr

```bash
gcc -std=c11 -Wall -Wextra *.c -o lista
./lista
```
