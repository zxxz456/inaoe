/*
Cola.h
========================


Descripcion:
------------
Cola (Queue) FIFO implementada con una lista ligada simple. Guarda un puntero al
primer nodo (frente, de donde se saca con dequeue) y al ultimo (fin, donde se
mete con enqueue), mas el numero de elementos. Aqui solo se DECLARAN las
operaciones; la implementacion va en Cola.c.

REUTILIZACION:
Se reutiliza el struct Nodo de la actividad1_parte2_linkedlist (un nodo de cola
es igual a un nodo de lista: un dato y un puntero al siguiente). El header se
incluye con #include "Nodo.h" y se le pasa la ruta al compilador con:
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

#ifndef COLA_H
#define COLA_H

#include "Nodo.h" 

typedef struct {
    Nodo* frente;   // primer nodo
    Nodo* fin;      // ultimo nodo
    int tam;        // numero de elementos en la cola
} Cola;

// Inicializa una cola vacia 
void colaInit(Cola* cola);

int colaVacia(const Cola* cola);

// Devuelve el numero de elementos de la cola
int colaTam(const Cola* cola);

// Mete un dato al FINAL de la cola
int encolar(Cola* cola, int dato);

// Saca el dato del FRENTE de la cola y lo escribe en *salida
int desencolar(Cola* cola, int* salida);

// Consulta el dato del frente SIN sacarlo y lo escribe en *salida
int colaFrente(const Cola* cola, int* salida);

// Imprime la cola en pantalla, del frente al fin
void colaMostrar(const Cola* cola);

// Libera toda la memoria de la cola y la deja vacia
void colaLiberar(Cola* cola);

#endif // COLA_H

// ########################### FIN DE COLA.H ###################################
// #############################################################################
