/*
Empleado.cpp
========================


Descripcion:
------------
Clase base que representa la abstraccion de un empleado.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/Empleado.h"
#include <cstdio>

Empleado::~Empleado() {}

double Empleado::ganancias() 
{
    /*
    ganancias()
    ----------------
    Metodo vertual que permite calcular las ganancias del empleado...
    (Por ahora solo regresa el salario como si fuera un geter)
    
    Parametros:
    ----------------

    Return:
    ----------------
    - double: las ganancias del empleado
    
    */
    return salario;
}

void Empleado::imprimir() 
{
    /*
    imprimir()
    ----------------
    Metodo virtual que permite imprimir la informacion del empleado
    
    Parametros:
    ----------------

    Return:
    ----------------
    - void
    
    */
    printf("Salario: %.2f\n", salario);
}