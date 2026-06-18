# Tarea 4 — Árbol binario en C

Tarea 4 de la segunda parte del curso propedéutico de **Programación y
Estructuras de Datos** (Dr. Miguel Morales Sandoval).

## Instrucciones

En esta tarea trabajarás con **árboles binarios** en C. Implementarás dos
funciones: una que **inserta nodos por niveles** (construyendo el árbol
balanceado visto en clase) y otra que **reconstruye un árbol a partir de sus
recorridos**. Tu calificación se obtiene automáticamente al correr la suite de
tests incluida.

funciones a implementar:

```c
typedef struct nodo {
  int valor;
  struct nodo *izq;
  struct nodo *der;
} Nodo;


Nodo *insertar(Nodo *raiz, int valor);
Nodo *construir(const int *pre, const int *in, int n);
```

## Solucion

En la solucion `solucion_Bryan_Violante_Arriaga.c` se implemento lo requerido:

- **`insertar`** — inserción **por niveles**: llena un nivel completo antes de
  pasar al siguiente, de izquierda a derecha
- **`construir`** — reconstruye el árbol a partir de sus recorridos **preorden**
  e **inorden**

No tiene `main`, son solo las dos funciones, pensadas para compilarse junto con
la suite de tests.

**NOTA**: Al struct le puse un campo de nivel, que es la profundidad, lo hice
así porque al inicio mi solución la fui diseñando pensando en que lo ocuparía
pero al final ya no. Lo dejé porque no afecta en nada.

## Compilación y ejecución

Saltan muchos warnings pero no es nada relacionado con el código, supongo que
es debido a la ofuscación del test.c

```bash
$ gcc -DMODO_TEST tests.c solucion_Bryan_Violante_Arriaga.c -o tests && ./tests
tests.c: In function ‘_chk_arr’:
tests.c:1948:28: warning: format not a string literal and no format arguments [-Wformat-security]
 1948 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr11));
      |                            ^
tests.c:2105:28: warning: format not a string literal and no format arguments [-Wformat-security]
 2105 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr13));
      |                            ^
tests.c: In function ‘_check_insertar’:
tests.c:2328:21: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
 2328 |     raiz = (Nodo *)((void *)(! (_TIG_iO_iN0d_2_main_1_opaque_ptr_1 == _TIG_iO_iN0d_2_main_1_opaque_ptr_2)));
      |                     ^
tests.c: In function ‘_arbol_aleatorio’:
tests.c:11278:22: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
11278 |     return ((Nodo *)((void *)(! (_TIG_iO_iN0d_2_main_1_opaque_ptr_1 == _TIG_iO_iN0d_2_main_1_opaque_ptr_2))));
      |                      ^
tests.c: In function ‘main’:
tests.c:12222:28: warning: format not a string literal and no format arguments [-Wformat-security]
12222 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr16));
      |                            ^
tests.c:12224:28: warning: format not a string literal and no format arguments [-Wformat-security]
12224 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr17));
      |                            ^
tests.c:12226:28: warning: format not a string literal and no format arguments [-Wformat-security]
12226 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr18));
      |                            ^
tests.c:12228:28: warning: format not a string literal and no format arguments [-Wformat-security]
12228 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr19));
      |                            ^
tests.c:12366:58: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12366 |     _chk_int((unsigned long )tmp___2 == (unsigned long )((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )(((_TIG_iE_iN0d_1_entropy + 7) ^ ((long )(_TIG_iE_iN0d_1_entropy + 7) >> 63L)) - ((long )(_TIG_iE_iN0d_1_entropy + 7) >> 63L)) % 10) * 3 + 0] % _TIG_iO_iN0d_2_main_1__opaque_array[5]) + -3L))),
      |                                                          ^
tests.c:12381:28: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12381 |                   (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )(((_TIG_iE_iN0d_1_entropy ^ 2) ^ ((long )(_TIG_iE_iN0d_1_entropy ^ 2) >> 63L)) - ((long )(_TIG_iE_iN0d_1_entropy ^ 2) >> 63L)) % 10) * 3 + 0] % _TIG_iO_iN0d_2_main_1__opaque_array[5]) + -3L))),
      |                            ^
tests.c:12386:37: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12386 |                   tmp___5, (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )((_TIG_iE_iN0d_1_entropy + 4) - (((_TIG_iE_iN0d_1_entropy + 4) + (_TIG_iE_iN0d_1_entropy + 4)) & ((long )(_TIG_iE_iN0d_1_entropy + 4) >> 63L))) % 10) * 3 + 1] % _TIG_iO_iN0d_2_main_1__opaque_array[11]) + -5L))));
      |                                     ^
tests.c:12392:28: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12392 |                   (Nodo *)((void *)((_TIG_iO_iN0d_2_main_1_opaque_ptr_1 != _TIG_iO_iN0d_2_main_1_opaque_ptr_2) + (_TIG_iO_iN0d_2_main_1_opaque_ptr_1 != _TIG_iO_iN0d_2_main_1_opaque_ptr_2))),
      |                            ^
tests.c:12393:28: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12393 |                   (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )(((_TIG_iE_iN0d_1_entropy + 4) ^ ((long )(_TIG_iE_iN0d_1_entropy + 4) >> 63L)) - ((long )(_TIG_iE_iN0d_1_entropy + 4) >> 63L)) % 10) * 3 + 0] % _TIG_iO_iN0d_2_main_1__opaque_array[5]) + -3L))));
      |                            ^
tests.c:12395:28: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12395 |                   (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )((_TIG_iE_iN0d_1_entropy ^ 3) - (((_TIG_iE_iN0d_1_entropy ^ 3) + (_TIG_iE_iN0d_1_entropy ^ 3)) & ((long )(_TIG_iE_iN0d_1_entropy ^ 3) >> 63L))) % 10) * 3 + 1] % _TIG_iO_iN0d_2_main_1__opaque_array[11]) + -5L))),
      |                            ^
tests.c:12398:28: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12398 |                   (Nodo *)((void *)(_TIG_iO_iN0d_2_main_1_opaque_ptr_1 != _TIG_iO_iN0d_2_main_1_opaque_ptr_2)),
      |                            ^
tests.c:12405:29: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12405 |                    (Nodo *)((void *)(_TIG_iO_iN0d_2_main_1_opaque_ptr_1 != _TIG_iO_iN0d_2_main_1_opaque_ptr_2)),
      |                             ^
tests.c:12406:29: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12406 |                    (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )(((_TIG_iE_iN0d_1_entropy - 7) ^ ((long )(_TIG_iE_iN0d_1_entropy - 7) >> 63L)) - ((long )(_TIG_iE_iN0d_1_entropy - 7) >> 63L)) % 10) * 3 + 1] % _TIG_iO_iN0d_2_main_1__opaque_array[11]) + -5L))));
      |                             ^
tests.c:12410:29: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
12410 |                    (Nodo *)((void *)((int )((long )(_TIG_iO_iN0d_2_main_1__opaque_array[((unsigned int )((_TIG_iE_iN0d_1_entropy + 1) - (((_TIG_iE_iN0d_1_entropy + 1) << 1UL) & ((long )(_TIG_iE_iN0d_1_entropy + 1) >> 63L))) % 10) * 3 + 0] % _TIG_iO_iN0d_2_main_1__opaque_array[5]) + -3L))),
      |                             ^
tests.c:12472:28: warning: format not a string literal and no format arguments [-Wformat-security]
12472 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr45));
      |                            ^
tests.c:12474:28: warning: format not a string literal and no format arguments [-Wformat-security]
12474 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr46));
      |                            ^
tests.c:12533:28: warning: format not a string literal and no format arguments [-Wformat-security]
12533 |     printf((char const   *)(_TIG_EL_iN0d_3_encodeStrings_litStr51));
      |                            ^
╔══════════════════════════════════════════════════╗
║  Ejercicio — Arboles binarios                    ║
║  insertar por niveles y construir pre+in         ║
╚══════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════╗
║  Suite 1: insertar                               ║
╚══════════════════════════════════════════════════╝
  [PASS] insertar: pre-orden  - 1 nodo
  [PASS] insertar: in-orden   - 1 nodo
  [PASS] insertar: post-orden - 1 nodo
  [PASS] insertar: altura     - 1 nodo
  [PASS] insertar: pre-orden  - 3 nodos
  [PASS] insertar: in-orden   - 3 nodos
  [PASS] insertar: post-orden - 3 nodos
  [PASS] insertar: altura     - 3 nodos
  [PASS] insertar: pre-orden  - 7 nodos
  [PASS] insertar: in-orden   - 7 nodos
  [PASS] insertar: post-orden - 7 nodos
  [PASS] insertar: altura     - 7 nodos
  [PASS] insertar: pre-orden  - 15 nodos, arbol perfecto
  [PASS] insertar: in-orden   - 15 nodos, arbol perfecto
  [PASS] insertar: post-orden - 15 nodos, arbol perfecto
  [PASS] insertar: altura     - 15 nodos, arbol perfecto

╔══════════════════════════════════════════════════╗
║  Suite 2: insertar                               ║
╚══════════════════════════════════════════════════╝
  [PASS] insertar: pre-orden  - 5 nodos
  [PASS] insertar: in-orden   - 5 nodos
  [PASS] insertar: post-orden - 5 nodos
  [PASS] insertar: altura     - 5 nodos
  [PASS] insertar: pre-orden  - 6 nodos
  [PASS] insertar: in-orden   - 6 nodos
  [PASS] insertar: post-orden - 6 nodos
  [PASS] insertar: altura     - 6 nodos
  [PASS] insertar: pre-orden  - 10 nodos
  [PASS] insertar: in-orden   - 10 nodos
  [PASS] insertar: post-orden - 10 nodos
  [PASS] insertar: altura     - 10 nodos
  [PASS] insertar: pre-orden  - 12 nodos
  [PASS] insertar: in-orden   - 12 nodos
  [PASS] insertar: post-orden - 12 nodos
  [PASS] insertar: altura     - 12 nodos

╔══════════════════════════════════════════════════╗
║  Suite 3: insertar                               ║
╚══════════════════════════════════════════════════╝
  [PASS] insertar: pre-orden  - aleatorio #1, 26 nodos
  [PASS] insertar: in-orden   - aleatorio #1, 26 nodos
  [PASS] insertar: post-orden - aleatorio #1, 26 nodos
  [PASS] insertar: altura     - aleatorio #1, 26 nodos
  [PASS] insertar: pre-orden  - aleatorio #2, 27 nodos
  [PASS] insertar: in-orden   - aleatorio #2, 27 nodos
  [PASS] insertar: post-orden - aleatorio #2, 27 nodos
  [PASS] insertar: altura     - aleatorio #2, 27 nodos
  [PASS] insertar: pre-orden  - aleatorio #3, 12 nodos
  [PASS] insertar: in-orden   - aleatorio #3, 12 nodos
  [PASS] insertar: post-orden - aleatorio #3, 12 nodos
  [PASS] insertar: altura     - aleatorio #3, 12 nodos
  [PASS] insertar: pre-orden  - aleatorio #4, 8 nodos
  [PASS] insertar: in-orden   - aleatorio #4, 8 nodos
  [PASS] insertar: post-orden - aleatorio #4, 8 nodos
  [PASS] insertar: altura     - aleatorio #4, 8 nodos
  [PASS] insertar: pre-orden  - aleatorio #5, 14 nodos
  [PASS] insertar: in-orden   - aleatorio #5, 14 nodos
  [PASS] insertar: post-orden - aleatorio #5, 14 nodos
  [PASS] insertar: altura     - aleatorio #5, 14 nodos
  [PASS] insertar: pre-orden  - aleatorio #6, 41 nodos
  [PASS] insertar: in-orden   - aleatorio #6, 41 nodos
  [PASS] insertar: post-orden - aleatorio #6, 41 nodos
  [PASS] insertar: altura     - aleatorio #6, 41 nodos

╔══════════════════════════════════════════════════╗
║  Suite 4: construir                              ║
╚══════════════════════════════════════════════════╝
  [PASS] construir con n=0 regresa NULL
  [PASS] construir de un nodo
  [PASS] construir: pre-orden coincide - cadena a la izquierda
  [PASS] construir: in-orden coincide - cadena a la izquierda
  [PASS] construir: post-orden coincide - cadena a la izquierda
  [PASS] construir: altura coincide - cadena a la izquierda
  [PASS] construir: pre-orden coincide - cadena a la derecha
  [PASS] construir: in-orden coincide - cadena a la derecha
  [PASS] construir: post-orden coincide - cadena a la derecha
  [PASS] construir: altura coincide - cadena a la derecha
  [PASS] construir: pre-orden coincide - valores negativos
  [PASS] construir: in-orden coincide - valores negativos
  [PASS] construir: post-orden coincide - valores negativos
  [PASS] construir: altura coincide - valores negativos

╔══════════════════════════════════════════════════╗
║  Suite 5: construir                              ║
╚══════════════════════════════════════════════════╝
  [PASS] construir: pre-orden coincide - aleatorio #1, 27 nodos
  [PASS] construir: in-orden coincide - aleatorio #1, 27 nodos
  [PASS] construir: post-orden coincide - aleatorio #1, 27 nodos
  [PASS] construir: altura coincide - aleatorio #1, 27 nodos
  [PASS] construir: pre-orden coincide - aleatorio #2, 4 nodos
  [PASS] construir: in-orden coincide - aleatorio #2, 4 nodos
  [PASS] construir: post-orden coincide - aleatorio #2, 4 nodos
  [PASS] construir: altura coincide - aleatorio #2, 4 nodos
  [PASS] construir: pre-orden coincide - aleatorio #3, 53 nodos
  [PASS] construir: in-orden coincide - aleatorio #3, 53 nodos
  [PASS] construir: post-orden coincide - aleatorio #3, 53 nodos
  [PASS] construir: altura coincide - aleatorio #3, 53 nodos
  [PASS] construir: pre-orden coincide - aleatorio #4, 7 nodos
  [PASS] construir: in-orden coincide - aleatorio #4, 7 nodos
  [PASS] construir: post-orden coincide - aleatorio #4, 7 nodos
  [PASS] construir: altura coincide - aleatorio #4, 7 nodos
  [PASS] construir: pre-orden coincide - aleatorio #5, 37 nodos
  [PASS] construir: in-orden coincide - aleatorio #5, 37 nodos
  [PASS] construir: post-orden coincide - aleatorio #5, 37 nodos
  [PASS] construir: altura coincide - aleatorio #5, 37 nodos
  [PASS] construir: pre-orden coincide - aleatorio #6, 43 nodos
  [PASS] construir: in-orden coincide - aleatorio #6, 43 nodos
  [PASS] construir: post-orden coincide - aleatorio #6, 43 nodos
  [PASS] construir: altura coincide - aleatorio #6, 43 nodos
  [PASS] construir: pre-orden coincide - aleatorio #7, 47 nodos
  [PASS] construir: in-orden coincide - aleatorio #7, 47 nodos
  [PASS] construir: post-orden coincide - aleatorio #7, 47 nodos
  [PASS] construir: altura coincide - aleatorio #7, 47 nodos
  [PASS] construir: pre-orden coincide - aleatorio #8, 2 nodos
  [PASS] construir: in-orden coincide - aleatorio #8, 2 nodos
  [PASS] construir: post-orden coincide - aleatorio #8, 2 nodos
  [PASS] construir: altura coincide - aleatorio #8, 2 nodos

┌──────────────────────────────────────────────────┐
│  RESULTADOS FINALES                              │
│  Total        : 102                             │
│  Pass         : 102                             │
│  Fail         : 0                               │
│  Calificacion : 100 / 100                       │
└──────────────────────────────────────────────────┘

```
