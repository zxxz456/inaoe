/*
Cola.c
========================


Descripcion:
------------
Implementacion de la cola (Queue) FIFO con lista ligada: inicializar, encolar
(enqueue, al final), desencolar (dequeue, del frente), consultar el frente,
mostrar, vaciar y liberar. La memoria de los nodos se reserva con malloc y se
libera con free.

Clave del FIFO: se mete por 'fin' y se saca por 'frente'. Manteniendo el puntero
'fin' las dos operaciones son O(1) (no hay que recorrer la cola).


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#include "if/Cola.h"
#include <stdio.h>
#include <stdlib.h>


void colaInit(Cola* cola)
{
    /*
    colaInit()
    ----------------
    Deja la cola vacia: sin nodos y con tam en 0. Hay que llamarla antes de usar
    la cola, porque una Cola recien declarada tiene basura.

    Parametros:
    - cola (Cola*): cola a inicializar

    Return:

    */
    cola->frente = NULL;
    cola->fin = NULL;
    cola->tam = 0;
}


int colaVacia(const Cola* cola)
{
    /*
    colaVacia()
    ----------------
    Indica si la cola no tiene elementos (isEmpty).

    Parametros:
    - cola (const Cola*): cola a consultar

    Return:
    - int: 1 si esta vacia, 0 si tiene al menos un nodo
    */
    return (cola->frente == NULL);
}


int colaTam(const Cola* cola)
{
    /*
    colaTam()
    ----------------
    Devuelve cuantos elementos hay en la cola.

    Parametros:
    - cola (const Cola*): cola a consultar

    Return:
    - int: numero de nodos
    */
    return cola->tam;
}


int encolar(Cola* cola, int dato)
{
    /*
    encolar()  (enqueue)
    ----------------
    Crea un nodo nuevo y lo engancha al FINAL de la cola (en 'fin'). Si la cola
    esta vacia, el nodo nuevo es a la vez frente y fin.

    Parametros:
    - cola (Cola*): cola donde se mete
    - dato (int): valor a guardar

    Return:
    - int: 1 si lo encolo, 0 si fallo malloc
    */

    Nodo* nuevo = (Nodo*) malloc(sizeof(Nodo));
    if (nuevo == NULL) return 0;   // no hubo memoria
    nuevo->dato = dato;
    nuevo->siguiente = NULL;       // el nuevo siempre queda al final

    if (cola->fin == NULL) {
        // cola vacia: el nuevo nodo es frente y fin
        cola->frente = nuevo;
        cola->fin = nuevo;
    } else {
        // enganchar despues del ultimo y mover 'fin'
        cola->fin->siguiente = nuevo;
        cola->fin = nuevo;
    }

    cola->tam++;
    return 1;
}


int desencolar(Cola* cola, int* salida)
{
    /*
    desencolar()  (dequeue)
    ----------------
    Saca el nodo del FRENTE (el que lleva mas tiempo, FIFO), escribe su dato en
    *salida y libera ese nodo. Si la cola queda vacia, tambien pone 'fin' en NULL.

    Parametros:
    - cola (Cola*): cola de donde se saca
    - salida (int*): donde se escribe el dato sacado (si habia)

    Return:
    - int: 1 si saco un elemento, 0 si la cola estaba vacia
    */

    if (cola->frente == NULL) return 0;   // cola vacia

    Nodo* tmp = cola->frente;
    if (salida != NULL) *salida = tmp->dato;

    cola->frente = tmp->siguiente;        // avanzar el frente
    if (cola->frente == NULL)
        cola->fin = NULL;                 // la cola quedo vacia

    free(tmp);
    cola->tam--;
    return 1;
}


int colaFrente(const Cola* cola, int* salida)
{
    /*
    colaFrente()  (peek)
    ----------------
    Consulta el dato del frente SIN sacarlo.

    Parametros:
    - cola (const Cola*): cola a consultar
    - salida (int*): donde se escribe el dato del frente (si habia)

    Return:
    - int: 1 si habia elemento, 0 si la cola estaba vacia
    */

    if (cola->frente == NULL) return 0;
    if (salida != NULL) *salida = cola->frente->dato;
    return 1;
}


void colaMostrar(const Cola* cola)
{
    /*
    colaMostrar()  (showQueue)
    ----------------
    Imprime la cola del frente al fin. Si esta vacia lo dice.

    Parametros:
    - cola (const Cola*): cola a imprimir

    Return:

    */

    if (cola->frente == NULL) {
        printf("Cola: VACIA\n");
        return;
    }

    printf("Cola (%d): frente > ", cola->tam);
    Nodo* aux = cola->frente;
    while (aux != NULL) {
        printf("%d > ", aux->dato);
        aux = aux->siguiente;
    }
    printf("fin\n");
}


void colaLiberar(Cola* cola)
{
    /*
    colaLiberar()
    ----------------
    Recorre la cola liberando cada nodo con free y la deja vacia. En C hay que
    hacerlo a mano: si no, se queda la memoria reservada (memory leak).

    Parametros:
    - cola (Cola*): cola a liberar

    Return:

    */

    Nodo* aux = cola->frente;
    while (aux != NULL) {
        Nodo* siguiente = aux->siguiente;   // guardar antes de liberar
        free(aux);
        aux = siguiente;
    }
    cola->frente = NULL;
    cola->fin = NULL;
    cola->tam = 0;
}

// ########################### FIN DE COLA.C ###################################
// #############################################################################
