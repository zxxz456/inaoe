/*
EmpleadoPorComisiones.cpp
========================


Descripcion:
------------
Clase derivada que representa a un empleado por comisiones.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/EmpleadoPorComisiones.h"
#include <cstdio>

double EmpleadoPorComisiones::ganancias() {
    /*
    ganancias()
    ----------------
    Sobreescritura del metodo virtual ganancias(). Se hace el calculo 
    dependiendo de las ventas totales y la comision por venta.
    
    Parametros:
    ----------------

    Return:
    ----------------
    - double: las ganancias del empleado por comisiones

    */
    return comisionPorVenta * ventasTotales;
}

void EmpleadoPorComisiones::imprimir()
{
    /*
    imprimir()
    ----------------
    Sobreescritura del metodo virtual imprimir(). Imprime la comision por
    venta y las ventas totales.

    Parametros:
    ----------------

    Return:
    ----------------
    - void

    */
    printf("Comision por venta: %.2f\n", comisionPorVenta);
    printf("Ventas totales: %d\n", ventasTotales);
}