/*
Utils.h
========================


Descripcion:
------------
Utilidades varias


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       09/06/2026      Creation


*/

#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>

// Limpia la pantalla de la terminal
static inline void limpiarPantalla(void)
{
    printf("\033[2J\033[H");
}

#endif // UTILS_H

// ########################### FIN DE UTILS.H ##################################
// #############################################################################
