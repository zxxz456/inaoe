/*
Pila.c
========================


Descripcion:
------------
Implementacion de la pila (Stack) LIFO con lista ligada: inicializar, apilar
(push, arriba), desapilar (pop, de arriba), consultar la cima, mostrar, vaciar y
liberar. La memoria de los nodos se reserva con malloc y se libera con free.

Clave del LIFO: se mete y se saca SIEMPRE por el mismo extremo (la cima). Como
la cima es la cabeza de la lista, push y pop son O(1) (no se recorre nada).


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#include "if/Pila.h"
#include <stdio.h>
#include <stdlib.h>


void pilaInit(Pila* pila)
{
    /*
    pilaInit()
    ----------------
    Deja la pila vacia: sin nodos y con tam en 0. Hay que llamarla antes de usar
    la pila, porque una Pila recien declarada tiene basura.

    Parametros:
    - pila (Pila*): pila a inicializar

    Return:

    */
    pila->cima = NULL;
    pila->tam = 0;
}


int pilaVacia(const Pila* pila)
{
    /*
    pilaVacia()
    ----------------
    Indica si la pila no tiene elementos (isEmpty).

    Parametros:
    - pila (const Pila*): pila a consultar

    Return:
    - int: 1 si esta vacia, 0 si tiene al menos un nodo
    */
    return (pila->cima == NULL);
}


int pilaTam(const Pila* pila)
{
    /*
    pilaTam()
    ----------------
    Devuelve cuantos elementos hay en la pila.

    Parametros:
    - pila (const Pila*): pila a consultar

    Return:
    - int: numero de nodos
    */
    return pila->tam;
}


int apilar(Pila* pila, int dato)
{
    /*
    apilar()  (push)
    ----------------
    Crea un nodo nuevo y lo pone ARRIBA de la pila (como nueva cima). El nuevo
    nodo apunta a la antigua cima.

    Parametros:
    - pila (Pila*): pila donde se mete
    - dato (int): valor a guardar

    Return:
    - int: 1 si lo apilo, 0 si fallo malloc
    */

    Nodo* nuevo = (Nodo*) malloc(sizeof(Nodo));
    if (nuevo == NULL) return 0;   // no hubo memoria
    nuevo->dato = dato;

    // el nuevo apunta a la antigua cima y pasa a ser la cima
    nuevo->siguiente = pila->cima;
    pila->cima = nuevo;

    pila->tam++;
    return 1;
}


int desapilar(Pila* pila, int* salida)
{
    /*
    desapilar()  (pop)
    ----------------
    Saca el nodo de ARRIBA (el ultimo en entrar, LIFO), escribe su dato en
    *salida y libera ese nodo.

    Parametros:
    - pila (Pila*): pila de donde se saca
    - salida (int*): donde se escribe el dato sacado (si habia)

    Return:
    - int: 1 si saco un elemento, 0 si la pila estaba vacia
    */

    if (pila->cima == NULL) return 0;   // pila vacia

    Nodo* tmp = pila->cima;
    if (salida != NULL) *salida = tmp->dato;

    pila->cima = tmp->siguiente;        // bajar la cima al siguiente
    free(tmp);
    pila->tam--;
    return 1;
}


int pilaCima(const Pila* pila, int* salida)
{
    /*
    pilaCima()  (peek / top)
    ----------------
    Consulta el dato de arriba SIN sacarlo.

    Parametros:
    - pila (const Pila*): pila a consultar
    - salida (int*): donde se escribe el dato de la cima (si habia)

    Return:
    - int: 1 si habia elemento, 0 si la pila estaba vacia
    */

    if (pila->cima == NULL) return 0;
    if (salida != NULL) *salida = pila->cima->dato;
    return 1;
}


void pilaMostrar(const Pila* pila)
{
    /*
    pilaMostrar()  (showStack)
    ----------------
    Imprime la pila de la cima hacia el fondo. Si esta vacia lo dice.

    Parametros:
    - pila (const Pila*): pila a imprimir

    Return:

    */

    if (pila->cima == NULL) {
        printf("Pila: VACIA\n");
        return;
    }

    printf("Pila (%d): cima > ", pila->tam);
    Nodo* aux = pila->cima;
    while (aux != NULL) {
        printf("%d > ", aux->dato);
        aux = aux->siguiente;
    }
    printf("fondo\n");
}


void pilaLiberar(Pila* pila)
{
    /*
    pilaLiberar()
    ----------------
    Recorre la pila liberando cada nodo con free y la deja vacia. En C hay que
    hacerlo a mano: si no, se queda la memoria reservada (memory leak).

    Parametros:
    - pila (Pila*): pila a liberar

    Return:

    */

    Nodo* aux = pila->cima;
    while (aux != NULL) {
        Nodo* siguiente = aux->siguiente;   // guardar antes de liberar
        free(aux);
        aux = siguiente;
    }
    pila->cima = NULL;
    pila->tam = 0;
}

// ########################### FIN DE PILA.C ###################################
// #############################################################################
