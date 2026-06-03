/*
EmpleadoPorHora.cpp
========================


Descripcion:
------------
Clase derivada que representa a un empleado por hora.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/EmpleadoPorHora.h"
#include "if/Utils.h"
#include <cstdio>

double EmpleadoPorHora::ganancias() {
    /*
    ganancias()
    ----------------
    SObreescritura del metodo virtual ganancias(). Se hace el calculo 
    dependiendo de las horas trabajadas.
    
    Parametros:
    ----------------

    Return:
    ----------------
    - double: las ganancias del empleado por hora
    
    */
    return horasTrabajadas < UMBRAL_HORAS_EXTRA ? 
                            (tarifaPorHora * horasTrabajadas) : 
                            (tarifaPorHora * UMBRAL_HORAS_EXTRA + 
                                (horasTrabajadas - UMBRAL_HORAS_EXTRA) * 
                                PORCENTAJE_HORAS_EXTRA * tarifaPorHora);
}

void EmpleadoPorHora::imprimir()
{
    /*
    imprimir()
    ----------------
    Sobreescritura del metodo virtual imprimir(). Imprime las horas
    trabajadas y la tarifa por hora.

    Parametros:
    ----------------

    Return:
    ----------------
    - void

    */
    printf("Horas trabajadas: %d\n", horasTrabajadas);
    printf("Tarifa por hora: %.2f\n", tarifaPorHora);
}