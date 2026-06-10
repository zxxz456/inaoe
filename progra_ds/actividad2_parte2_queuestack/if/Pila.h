/*
Pila.h
========================


Descripcion:
------------
Pila (Stack) LIFO implementada con una lista ligada simple. Guarda un puntero al
nodo de arriba (cima), por donde se mete (push) y se saca (pop), mas el numero de
elementos. Aqui solo se DECLARAN las operaciones; la implementacion va en Pila.c.

REUTILIZACION:
Se reutiliza el struct Nodo de la actividad1_parte2_linkedlist (igual que la
cola). El header se incluye con #include "Nodo.h" y se le pasa la ruta al
compilador con:
    -I../actividad1_parte2_linkedlist/if


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#ifndef PILA_H
#define PILA_H

#include "Nodo.h"   // reutilizado de actividad1_parte2_linkedlist/if

typedef struct {
    Nodo* cima;   // nodo de arriba: por aqui se METE (push) y se SACA (pop)
    int tam;      // numero de elementos en la pila
} Pila;

// Inicializa una pila vacia (cima = NULL, tam = 0).
void pilaInit(Pila* pila);

// Devuelve 1 si la pila no tiene elementos, 0 en caso contrario (isEmpty).
int pilaVacia(const Pila* pila);

// Devuelve el numero de elementos de la pila.
int pilaTam(const Pila* pila);

// Mete un dato ARRIBA de la pila (push).
// Devuelve 1 si lo logro, 0 si fallo la reserva de memoria.
int apilar(Pila* pila, int dato);

// Saca el dato de ARRIBA de la pila (pop) y lo escribe en *salida.
// Devuelve 1 si saco un elemento, 0 si la pila estaba vacia.
int desapilar(Pila* pila, int* salida);

// Consulta el dato de arriba SIN sacarlo (peek/top) y lo escribe en *salida.
// Devuelve 1 si habia elemento, 0 si la pila estaba vacia.
int pilaCima(const Pila* pila, int* salida);

// Imprime la pila en pantalla, de la cima hacia el fondo.
void pilaMostrar(const Pila* pila);

// Libera toda la memoria de la pila y la deja vacia.
void pilaLiberar(Pila* pila);

#endif // PILA_H

// ########################### FIN DE PILA.H ###################################
// #############################################################################
