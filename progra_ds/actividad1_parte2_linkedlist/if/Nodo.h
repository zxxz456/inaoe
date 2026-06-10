/*
Nodo.h
========================


Descripcion:
------------
Nodo de una lista ligada simple. Cada nodo guarda un entero (dato) y un puntero
al siguiente nodo de la lista.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#ifndef NODO_H
#define NODO_H

typedef struct nodo {
    int dato;                 // valor almacenado en el nodo
    struct nodo* siguiente;   // puntero al siguiente nodo
} Nodo;

#endif // NODO_H

// ########################### FIN DE NODO.H ###################################
// #############################################################################
