/*
mainCola.c
========================


Descripcion:
------------
Cola interactiva de la clase sobre pilas y colas. Es la actividad que dejo
el dr en las diapositivas marcada como Ejercicio 3.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#include "if/Cola.h"
#include "Utils.h"   // limpiarPantalla() reutilizada de actividad1 (-I .../if)
#include <stdio.h>

int main()
{
    Cola cola;
    colaInit(&cola);

    int opcion;
    int valor;
    char mensaje[64];   
    snprintf(mensaje, sizeof(mensaje), "N/A");

    do {
        // refrescar la pantalla y mostrar el estado actual
        limpiarPantalla();
        printf("=== Cola (FIFO) interactiva ===\n\n");
        colaMostrar(&cola);
        printf("[ %s ]\n", mensaje);   // resultado de la operacion anterior

        printf("\nMenu:\n");
        printf("  0 -> encolar (enqueue)\n");
        printf("  1 -> desencolar (dequeue)\n");
        printf("  otra opcion -> salir\n");
        printf("Opcion: ");

        // si no se lee un entero valido (p. ej. una letra), salimos
        if (scanf("%d", &opcion) != 1) {
            printf("\nEntrada no valida. Saliendo...\n");
            break;
        }

        if (opcion == 0) {
            // ----- encolar -----
            printf("Numero a encolar: ");
            if (scanf("%d", &valor) != 1) {
                printf("Numero no valido. Saliendo...\n");
                break;
            }
            if (encolar(&cola, valor))
                snprintf(mensaje, 
                    sizeof(mensaje), 
                    "Metido en la cola xd %d (entra por el fin).", 
                    valor);
            else
                snprintf(mensaje, 
                        sizeof(mensaje), 
                        "No se pudo encolar (sin memoria).");

        } else if (opcion == 1) {
            // ----- desencolar -----
            int sacado;
            if (desencolar(&cola, &sacado))
                snprintf(mensaje, 
                        sizeof(mensaje), 
                        "Sacado de la cola %d (salio del frente).", 
                        sacado);
            else
                snprintf(mensaje, 
                        sizeof(mensaje), 
                        "La cola estaba vacia, nada que sacar.");

        } else {
            // ----- salir -----
            printf("Saliendo...\n");
            break;
        }
    } while (1);

    // liberar toda la memoria antes de terminar
    colaLiberar(&cola);
    return 0;
}

// ########################### FIN DE MAINCOLA.C ###############################
// #############################################################################
