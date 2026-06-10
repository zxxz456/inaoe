/*
main.c
========================


Descripcion:
------------
Lista ligada simple interactiva...
1 para borrar
0 para agregar
otra tecla para salir


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.2.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#include "if/Lista.h"
#include "if/Utils.h"   // limpiarPantalla() compartida (lista, cola y pila)
#include <stdio.h>

int main()
{
    Lista lista;
    listaInit(&lista);

    int opcion;
    int valor;
    char mensaje[64];   
    snprintf(mensaje, sizeof(mensaje), "");

    do {
        // refrescar la pantalla y mostrar el estado actual
        limpiarPantalla();
        printf("=== Listas ligadass ===\n\n");
        listaMostrar(&lista);
        printf("[ %s ]\n", mensaje);   // resultado de la operacion anterior

        printf("\nMenu:\n");
        printf("  0 -> agregar un numero\n");
        printf("  1 -> eliminar un numero\n");
        printf("  otra opcion -> salir\n");
        printf("Opcion: ");

        // si no se lee un entero valido (p. ej. una letra), salimos
        if (scanf("%d", &opcion) != 1) {
            printf("\nEntrada no valida. Saliendo...\n");
            break;
        }

        if (opcion == 0) {
            // ----- agregar -----
            printf("Numero a agregar: ");
            if (scanf("%d", &valor) != 1) {
                printf("Numero no valido. Saliendo...\n");
                break;
            }
            if (listaAgregar(&lista, valor))
                snprintf(mensaje, sizeof(mensaje), "Agregado %d al final.", 
                         valor);
            else
                snprintf(mensaje, sizeof(mensaje), "No se pudo agregar (OOM).");

        } else if (opcion == 1) {
            // ----- eliminar -----
            printf("Numero a eliminar: ");
            if (scanf("%d", &valor) != 1) {
                printf("Numero no valido. Saliendo...\n");
                break;
            }
            if (listaEliminar(&lista, valor))
                snprintf(mensaje, sizeof(mensaje), "Eliminado %d.", valor);
            else
                snprintf(mensaje, sizeof(mensaje), "El %d no estaba en la \
                         lista.", valor);

        } else {
            // ----- salir -----
            printf("Saliendo...\n");
            break;
        }
    } while (1);

    // liberar toda la memoria antes de terminar
    listaLiberar(&lista);
    return 0;
}

// ########################### FIN DE MAIN.C ###################################
// #############################################################################
