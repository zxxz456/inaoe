# Tarea 3 - Calculadora de notación posfija (postfix) en C

Tarea 3 de la segunda parte del curso propedéutico de **Programación y
Estructuras de Datos** (Dr. Miguel Morales Sandoval)

## Instrucciones

IMplementar una calculadora de **notación posfija** (los operadores van después
de los operandos, p. ej. `2 3 + 4 *` = `20`) en un archivo `solucion.c` con dos
funciones:

```c
int aplicar_operador(int a, int b, char op);
int evaluar_posfijo(const char *expresion);
```

Solo enteros, operadores `+ - * /`, división entera, y usando únicamente pilas
y/o colas

## Solucion

`solucion.c` evalúa la expresión con una **pila de enteros sobre lista ligada**:
cada número se apila y cada operador desapila sus dos operandos, aplica la
operación y vuelve a apilar el resultado. Al final, la cima es el resultado

Está todo en un solo archivo para compilarlo fácil junto con los tests:

```bash
gcc solucion.c -o prueba && ./prueba
```

Se muestra ejemplo de la salida
```bash
$ ./prueba
2 3 + 4 * = 20
5 1 2 + 4 * + 3 - = 14
100 10 / 5 + = 15
20 6 / 1 + = 4
3 5 - 4 * = -8
```