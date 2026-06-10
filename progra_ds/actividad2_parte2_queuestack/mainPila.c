/*
mainPila.c
========================


Descripcion:
------------
Pila interactiva de la clase sobre pilas y colas. Es la actividad que dejo
el dr en las diapositivas marcada como Ejercicio 3.


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
#include "Utils.h"   // limpiarPantalla() reutilizada de actividad1 (-I .../if)
#include <stdio.h>

int main()
{
    Pila pila;
    pilaInit(&pila);

    int opcion;
    int valor;
    char mensaje[64];
    snprintf(mensaje, sizeof(mensaje), "N/A");

    do {
        // refrescar la pantalla y mostrar el estado actual
        limpiarPantalla();
        printf("=== Pila/Stack (LIFO) ===\n\n");
        pilaMostrar(&pila);
        printf("[ %s ]\n", mensaje);   // resultado de la operacion anterior

        printf("\nMenu:\n");
        printf("  0 -> apilar (push)\n");
        printf("  1 -> desapilar (pop)\n");
        printf("  otra opcion -> salir\n");
        printf("Opcion: ");

        // si no se lee un entero valido (p. ej. una letra), salimos
        if (scanf("%d", &opcion) != 1) {
            printf("\nEntrada no valida. Saliendo...\n");
            break;
        }

        if (opcion == 0) {
            // ----- apilar -----
            printf("Numero a apilar: ");
            if (scanf("%d", &valor) != 1) {
                printf("Numero no valido. Saliendo...\n");
                break;
            }
            if (apilar(&pila, valor))
                snprintf(mensaje, 
                         sizeof(mensaje), 
                         "Apilado %d (entra arriba).", valor);
            else
                snprintf(mensaje, 
                         sizeof(mensaje), 
                         "No se pudo apilar (OOM).");

        } else if (opcion == 1) {
            // ----- desapilar -----
            int sacado;
            if (desapilar(&pila, &sacado))
                snprintf(mensaje, 
                         sizeof(mensaje), 
                         "Desapilado %d (salio de arriba).", sacado);
            else
                snprintf(mensaje, 
                         sizeof(mensaje), 
                         "La pila estaba vacia, nada que sacar.");

        } else {
            // ----- salir -----
            printf("Saliendo...\n");
            break;
        }
    } while (1);

    // liberar toda la memoria antes de terminar
    pilaLiberar(&pila);
    return 0;
}

// ########################### FIN DE MAINPILA.C ###############################
// #############################################################################
