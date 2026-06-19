/*
solucion_Bryan_Violante_Arriaga.c
=================================


Descripcion:
------------
Solucion de la tarea 5 del curso propedeutico de progra y ds.
La tarea, segun lo poco que se alcanza a leer en el README.png en el repo 
https://github.com/diego-crag/CCC-prope-2026/tree/main/Arbol_expresion 
(que en lugar de mitigar el uso de IA solo hace mas dificil entender lo que
se pide), consiste en construir y evaluar un arbol de expresion booleana a
partir de una expresion dada en notacion postordem (postfija), usando un stack,
y mostrar el contenido del arbol en preorden, postorden e inorden.

Las instrucciones del README.png son las siguientes (copiadas literalmente):
- El programa recibe una expresion booleana en notacion postorden. Ejemplo:

      Entrada: a b and c d and or c not and
      // es la expresion  ((a and b) or (c and d)) and !c

- El programa construye el arbol correspondiente usando una PILA:
    * Si el simbolo leido NO es un operador booleano -> crea un nodo (hoja)
      para ese simbolo y lo apila (push).
    * Si SI es un operador:
        - Si el operador es BINARIO (and, or):
            1. Crea un nodo con el operador binario.
            2. Saca (pop) dos nodos de la pila y los hace los dos hijos del
               nodo creado en el paso 1.
            3. Apila (push) el nodo creado en el paso 1.
        - Si el operador es UNARIO (not):
            1. Crea un nodo con el operador unario.
            2. Saca (pop) un nodo de la pila y lo hace el unico hijo del
               nodo creado en el paso 1.
            3. Apila (push) el nodo creado en el paso 1.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       18/06/2026      Creation


*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Marcos de referencia para los tipos de nodo y el numero maximo de tokens
#define VAR 'V' 
#define AND 'A'
#define OR  'O'
#define NOT 'N'
#define AND_STR "and"
#define OR_STR  "or"
#define NOT_STR "not"
#define MAX_TOKENS 8
#define NOT_VAR 0


// ########################### INICIO DE SOLUCION ##############################

// Structs

typedef struct Nodo {
    char tipo;                 // tipo de nodo, puede ser alguno de los 
                               // declarados en los macros de arriba 
    char var;                  // letra de la variable (solo si tipo==VAR)
    struct Nodo *izq, *der;    // hijos; en NOT solo se usa izq
} Nodo;



static Nodo *nuevo(char tipo, char var, Nodo *izq, Nodo *der)
{
    /*
    nuevo()
    ----------------
    Crea un nodo nuevo con los datos dados 

    Parametros:
    ----------------
    - tipo (char): VAR variable, AND and, OR or, NOT not
    - var (char): letra de la variable (solo aplica si tipo==VAR)
    - izq (Nodo*): hijo izquierdo (o unico operando si es NOT)
    - der (Nodo*): hijo derecho (NULL en variables y en NOT)

    Return:
    ----------------
    - Nodo*: apuntador al nodo re100 creado
    */

    Nodo *n = malloc(sizeof(Nodo));
    n->tipo = tipo;
    n->var  = var;
    n->izq  = izq;
    n->der  = der;
    return n;
}

// Funciones core pedidas

void *construir(char (*tokens)[MAX_TOKENS], int n)
{
    /*
    construir()
    ----------------
    Construye el arbol a partir de los tokens en postfijo, usando un stack

    La idea principal de divide en 2 etapas...
    1) Recorremos los tokens de izquierda a derecha (pq estan en psotfix, como 
    el de la calculadora) y si...
        1.1) ES una variable, se crea una hoja y la pusheamos a la pila
        1.2) Es un operador, se sacan sus operandos de la pila, se crea el nodo
             operador con esos subarboles como hijos, y se pushea el nodo a la
             pila
    2) Al terminar, lo unico que queda en la pila es la raiz del arbol

    Parametros:
    - tokens (char (*)[MAX_TOKENS]): arreglo de tokens 
    - n (int): numero de tokens

    Return:
    - void*: apuntador a la raiz del arbol (NULL si no hubo tokens)
    */

    if (n <= 0) return NULL;   // sin tokens no hay arbol

    // Declaramos el stack como un arreglo dinamico de Nodos*
    Nodo** stack = malloc((size_t)n * sizeof(*stack));
    if (stack == NULL) return NULL;   // no hay memoria

    int top = 0;               // indice de la siguiente posicion libre

    for (int vc = 0; vc < n; vc++) 
    {
        // sacamos el token actual
        char *token = tokens[vc];

        // Q tipo de token es?
        if (strcmp(token, AND_STR) == 0)           // es un operador binario AND 
        {
            // binario: el primero que sale es el hijo DERECHO
            Nodo *der = stack[--top];
            Nodo *izq = stack[--top];
            stack[top++] = nuevo(AND, NOT_VAR, izq, der);

        } 
        else if (strcmp(token, OR_STR) == 0)        // es un operador binario OR
        {
            Nodo *der = stack[--top];
            Nodo *izq = stack[--top];
            stack[top++] = nuevo(OR, NOT_VAR, izq, der);

        } 
        else if (strcmp(token, NOT_STR) == 0)       // es un operador unario NOT
        {
            // unario: solo un operando
            Nodo *hijo = stack[--top];
            stack[top++] = nuevo(NOT, NOT_VAR, hijo, NULL);

        } 
        else                                        // Es una variable
        {
            // cualquier otra cosa es una variable de una letra
            stack[top++] = nuevo(VAR, token[0], NULL, NULL);
        }
    }

    // Al finbal lo que queda en la pila es la raiz del arbol con todos los
    // hijos como la representacion de la expresion dada x los tokens
    Nodo *raiz = (top > 0) ? stack[top - 1] : NULL;
    free(stack);
    return raiz;
}


int evaluar(const void *raiz, const int *valores)
{
    /*
    evaluar()
    ----------------
    Evalua el arbol recursivamente comos e ve en las imgs que adjunte
    Los valores supongo que los pasa en valores... en las instrucciones viene
    declarado el proto de la funcion pero no dice que es, ni su, tuve que 
    investigar y suponer por mi cuenta. 
    La idea es simple y usa recursividad, se evalua los nodos recursivamente
    y se combinan al final segun el type del nodo 

    Parametros:
    - raiz (const void*): raiz del (sub)arbol a evaluar
    - valores (const int*): tabla de valores indexada por ASCII de la variable

    Return:
    - int: 0 o 1 (resultado booleano de la expresion)
    */

    const Nodo *n = raiz;
    if (!n) return 0;

    // checamos tipo y llamamos recursivamente
    switch (n->tipo) {
        case VAR: return valores[(unsigned char)n->var] != 0;
        case NOT: return !evaluar(n->izq, valores);
        case AND: return evaluar(n->izq, valores) && evaluar(n->der, valores);
        case OR: return evaluar(n->izq, valores) || evaluar(n->der, valores);
    }
    return 0;
}

// Recorridos del arbol (preorden, inorden, postorden)

static void imprimir_nodo(const Nodo *n)
{
    /*
    imprimir_nodo()
    ----------------
    Funcion aux, imprime el "contenido" de un nodo, la letra si es variable, 
    o el nombre del operador (and / or / not)

    Parametros:
    ----------------
    - n (const Nodo*): nodo a imprimir

    Return:
    ----------------

    */

    switch (n->tipo) 
    {
        case VAR: printf("%c ", n->var);    break;
        case AND: printf("%s ", AND_STR);   break;
        case OR:  printf("%s ", OR_STR);    break;
        case NOT: printf("%s ", NOT_STR);   break;
    }
}

void preorden(const void *raiz)
{
    /*
    preorden()
    ----------------
    Recorrido preorden 

    Parametros:
    ----------------
    - raiz (const void*): raiz del (sub)arbol a recorrer

    Return:
    ----------------

    */

    const Nodo *n = raiz;
    if (!n) return;

    imprimir_nodo(n);          
    preorden(n->izq);        
    preorden(n->der);        
}

void inorden(const void *raiz)
{
    /*
    inorden()
    ----------------
    Recorrido inorden de toda la vida

    Parametros:
    ----------------
    - raiz (const void*): raiz del (sub)arbol a recorrer

    Return:
    ----------------

    */

    const Nodo *n = raiz;
    if (!n) return;

    inorden(n->izq);           
    imprimir_nodo(n);        
    inorden(n->der);        
}

void postorden(const void *raiz)
{
    /*
    postorden()
    ----------------
    Recorrido en postorden, nada nuevo que explicar

    Parametros:
    ----------------
    - raiz (const void*): raiz del (sub)arbol a recorrer

    Return:
    ----------------

    */

    const Nodo *n = raiz;
    if (!n) return;

    postorden(n->izq);         
    postorden(n->der);       
    imprimir_nodo(n);        
}

// Utils

void liberar(void *raiz)
{
    /*
    liberar()
    ----------------
    Libera la memoria

    Parametros:
    ----------------
    - raiz (void*): raiz del (sub)arbol a liberar

    Return:
    ----------------

    */

    Nodo *n = raiz;
    if (!n) return;

    liberar(n->izq);
    liberar(n->der);
    free(n);
}


// main de debuggin

#ifndef MODO_TEST

int main(void)
{

    char tokens[][MAX_TOKENS] = {
        "a", "b", "and", "c", "d", "and", "or", "c", "not", "and"
    };
    int ntok = (int)(sizeof(tokens) / sizeof(tokens[0]));

    void *arbol = construir(tokens, ntok);

    printf("--> a b and c d and or c not and\n");

    printf("\tPre : ");  preorden(arbol);   printf("\n");
    printf("\tIn  : ");  inorden(arbol);    printf("\n");
    printf("\tPost: ");  postorden(arbol);  printf("\n");

    liberar(arbol);


    char tokens2[][MAX_TOKENS] = {
        "a", "not", "not", "not", "not", "not"
    };
    int ntok2 = (int)(sizeof(tokens2) / sizeof(tokens2[0]));

    void *arbol2 = construir(tokens2, ntok2);

    printf("--> a not not not not not\n");

    printf("\tPre : ");  preorden(arbol2);   printf("\n");
    printf("\tIn  : ");  inorden(arbol2);    printf("\n");
    printf("\tPost: ");  postorden(arbol2);  printf("\n");

    liberar(arbol2);

    return 0;
}

#endif  // MODO_TEST

// ########################### FIN DE SOLUCION #################################
// #############################################################################
