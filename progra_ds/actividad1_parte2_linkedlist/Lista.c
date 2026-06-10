/*
Lista.c
========================


Descripcion:
------------
Implementacion de las operaciones de una lista ligada simple de enteros:
inicializar, agregar (al final y al inicio), buscar, eliminar, mostrar y liberar


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#include "if/Lista.h"
#include <stdio.h>
#include <stdlib.h>


void listaInit(Lista* lista)
{
    /*
    listaInit()
    ----------------
    Deja la lista en estado vacio: sin nodos y con tam en 0

    Parametros:
    - lista (Lista*): lista a inicializar

    Return:

    */
    lista->cabeza = NULL;
    lista->tam = 0;
}


int listaVacia(const Lista* lista)
{
    /*
    listaVacia()
    ----------------
    Indica si la lista no tiene elementos

    Parametros:
    - lista (const Lista*): lista a consultar

    Return:
    - int: 1 si esta vacia, 0 si tiene al menos un nodo
    */
    return (lista->cabeza == NULL);
}


int listaTam(const Lista* lista)
{
    /*
    listaTam()
    ----------------
    Devuelve cuantos elementos hay en la lista

    Parametros:
    - lista (const Lista*): lista a consultar

    Return:
    - int: numero de nodos
    */
    return lista->tam;
}


int listaAgregar(Lista* lista, int dato)
{
    /*
    listaAgregar()
    ----------------
    Crea un nodo nuevo y lo engancha al FINAL de la lista. Si la lista esta
    vacia, el nodo nuevo pasa a ser la cabeza

    Parametros:
    - lista (Lista*): lista donde se agrega
    - dato (int): valor a guardar

    Return:
    - int: 1 si lo agrego, 0 si fallo malloc
    */

    // 1. reservar e inicializar el nodo nuevo
    Nodo* nuevo = (Nodo*) malloc(sizeof(Nodo));
    if (nuevo == NULL) return 0;   // no hubo memoria
    nuevo->dato = dato;
    nuevo->siguiente = NULL;

    // 2. engancharlo en la lista
    if (lista->cabeza == NULL) {
        // 2.1 lista vacia: el nuevo nodo es la cabeza
        lista->cabeza = nuevo;
    } else {
        // 2.2 ubicar el ultimo nodo y enganchar ahi
        Nodo* aux = lista->cabeza;
        while (aux->siguiente != NULL)
            aux = aux->siguiente;
        aux->siguiente = nuevo;
    }

    lista->tam++;
    return 1;
}


int listaAgregarInicio(Lista* lista, int dato)
{
    /*
    listaAgregarInicio()
    ----------------
    Crea un nodo nuevo y lo engancha al INICIO de la lista, quedando como la
    nueva cabeza. Es O(1) porque no hay que recorrer nada

    Parametros:
    - lista (Lista*): lista donde se agrega
    - dato (int): valor a guardar

    Return:
    - int: 1 si lo agrego, 0 si fallo malloc
    */

    Nodo* nuevo = (Nodo*) malloc(sizeof(Nodo));
    if (nuevo == NULL) return 0;
    nuevo->dato = dato;

    // el nuevo nodo apunta a la antigua cabeza y pasa a ser la cabeza
    nuevo->siguiente = lista->cabeza;
    lista->cabeza = nuevo;

    lista->tam++;
    return 1;
}


Nodo* listaBuscar(const Lista* lista, int dato)
{
    /*
    listaBuscar()
    ----------------
    Recorre la lista de inicio a fin buscando la primera ocurrencia del dato

    Parametros:
    - lista (const Lista*): lista donde se busca
    - dato (int): valor a buscar

    Return:
    - Nodo*: puntero al nodo que contiene el dato, o NULL si no esta
    */

    Nodo* aux = lista->cabeza;
    while (aux != NULL) {
        if (aux->dato == dato) return aux;
        aux = aux->siguiente;
    }
    return NULL;
}


int listaEliminar(Lista* lista, int dato)
{
    /*
    listaEliminar()
    ----------------
    Elimina la primera ocurrencia del dato y libera ese nodo. Se lleva un
    puntero al nodo anterior para poder "saltar" el nodo borrado

    Parametros:
    - lista (Lista*): lista de donde se elimina
    - dato (int): valor a eliminar

    Return:
    - int: 1 si lo elimino, 0 si el dato no estaba
    */

    Nodo* actual = lista->cabeza;
    Nodo* anterior = NULL;

    while (actual != NULL) {
        if (actual->dato == dato) {
            // enlazar el anterior con el siguiente, saltando 'actual'
            if (anterior == NULL)
                lista->cabeza = actual->siguiente;  // era la cabeza
            else
                anterior->siguiente = actual->siguiente;

            free(actual);
            lista->tam--;
            return 1;
        }
        anterior = actual;
        actual = actual->siguiente;
    }
    return 0;   // no se encontro el dato
}


void listaMostrar(const Lista* lista)
{
    /*
    listaMostrar()
    ----------------
    Imprime la lista en pantalla. Si esta vacia lo dice; si no, recorre todos
    los nodos mostrando sus datos

    Parametros:
    - lista (const Lista*): lista a imprimir

    Return:

    */

    if (lista->cabeza == NULL) {
        printf("Lista: VACIA\n");
        return;
    }

    printf("Lista (%d): ", lista->tam);
    Nodo* aux = lista->cabeza;
    while (aux != NULL) {
        printf("%d -> ", aux->dato);
        aux = aux->siguiente;
    }
    printf("NULL\n");
}


void listaLiberar(Lista* lista)
{
    /*
    listaLiberar()
    ----------------
    Recorre la lista liberando cada nodo con free y deja la lista vacia 
    (memory leak handleado)

    Parametros:
    - lista (Lista*): lista a liberar

    Return:

    */

    Nodo* aux = lista->cabeza;
    while (aux != NULL) {
        Nodo* siguiente = aux->siguiente;   // guardar antes de liberar
        free(aux);
        aux = siguiente;
    }
    lista->cabeza = NULL;
    lista->tam = 0;
}

// ########################### FIN DE LISTA.C ##################################
// #############################################################################
