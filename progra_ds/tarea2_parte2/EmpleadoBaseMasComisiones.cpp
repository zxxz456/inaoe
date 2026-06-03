/*
EmpleadoBaseMasComisiones.cpp
========================


Descripcion:
------------
Clase derivada que representa a un empleado con salario base más comisiones.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/EmpleadoBaseMasComisiones.h"
#include <cstdio>

double EmpleadoBaseMasComisiones::ganancias() {
    /*
    ganancias()
    ----------------
    Sobreescritura del metodo virtual ganancias(). Se hace el calculo 
    dependiendo del salario base, las ventas totales y la comision por venta.
    
    Parametros:
    ----------------

    Return:
    ----------------
    - double: las ganancias del empleado con salario base más comisiones
    
    */
    // En el diagrama se usa una expresion como esta
    //      (comisionPorVenta * ventasTotales) + salarioBase
    // Pero como ya tenemos el metodo ganancias() de EmpleadoPorComisiones,
    // usamos el metodo de la supercalase
    return EmpleadoPorComisiones::ganancias() + salarioBase;
}

void EmpleadoBaseMasComisiones::imprimir()
{
    /*
    imprimir()
    ----------------
    Sobreescritura del metodo virtual imprimir(). Reutiliza el imprimir() de
    EmpleadoPorComisiones (comision y ventas) y agrega el salario base.

    Parametros:
    ----------------

    Return:
    ----------------
    - void

    */
    EmpleadoPorComisiones::imprimir();
    printf("Salario base: %.2f\n", salarioBase);
}