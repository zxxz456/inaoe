/*
EmpleadoAsalariado.cpp
========================


Descripcion:
------------
Clase derivada que representa a un empleado asalariado.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/EmpleadoAsalariado.h"
#include <cstdio>

double EmpleadoAsalariado::ganancias() {
    /*
    ganancias()
    ----------------
    SObreescritura del metodo virtual ganancias(), por ahora solo regresa
    el salario semanal
    
    Parametros:
    ----------------

    Return:
    ----------------
    - double: las ganancias semanales del empleado

    */
    return salarioSemanal;
}

void EmpleadoAsalariado::imprimir()
{
    /*
    imprimir()
    ----------------
    Sobreescritura del metodo virtual imprimir(). Imprime el salario semanal.

    Parametros:
    ----------------

    Return:
    ----------------
    - void

    */
    printf("Salario semanal: %.2f\n", salarioSemanal);
}