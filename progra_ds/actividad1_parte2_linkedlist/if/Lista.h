/*
Lista.h
========================


Descripcion:
------------
Lista ligada simple de enteros. Guarda un puntero al primer nodo (cabeza) y el
numero de elementos (tam) para no tener que recorrer toda la lista si se
pide el size


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#ifndef LISTA_H
#define LISTA_H

#include "Nodo.h"

typedef struct {
    Nodo* cabeza;   // primer nodo de la lista 
    int tam;        // numero de nodos en la lista
} Lista;

// Inicializa una lista vacia (cabeza = NULL, tam = 0)
void listaInit(Lista* lista);

// Dice si lista es vacio
int listaVacia(const Lista* lista);

// Devuelve el numero de elementos de la lista.
int listaTam(const Lista* lista);

// Agrega un dato al FINAL de la lista
int listaAgregar(Lista* lista, int dato);

// Agrega un dato al INICIO de la lista
int listaAgregarInicio(Lista* lista, int dato);

// Busca la primera ocurrencia de un dato
Nodo* listaBuscar(const Lista* lista, int dato);

// Elimina la primera ocurrencia de un dato
int listaEliminar(Lista* lista, int dato);

// Imprime la lista en pantalla
void listaMostrar(const Lista* lista);

// Libera toda la memoria de la lista y la deja vacia
void listaLiberar(Lista* lista);

#endif // LISTA_H

// ########################### FIN DE LISTA.H ##################################
// #############################################################################
