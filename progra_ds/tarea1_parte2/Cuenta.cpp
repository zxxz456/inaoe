/*
Cuenta.cpp
========================


Descripcion:
------------
Clase que representa una cuenta bancaria. Tiene un cliente propietario, un saldo
actual, un identificador unico y un tipo (ahorro o cheques). Permite depositar, 
retirar y mostrar info de la cuenta.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#include "if/Cuenta.h"

void Cuenta::depositar(double dinero)
{
    /*
    Depositar()
    ----------------
    Metodo vertual que permite depositar dinero en la cuenta 
    
    Parametros:
    - dinero (double): cantidad de dinero a depositar

    Return:
    
    */

    // Sanity check: no se pueden depositar cantidades negativas
    // lo hacemos silent si el user mete dinero negativo
    dinero = (dinero > 0) ? dinero : 0;
    this->saldo += dinero;
}

bool Cuenta::retirar(double dinero)
{
    /*
    Retirar()
    ----------------
    Metodo virtual que permite retirar dinero de la cuenta
    
    Parametros:
    - dinero (double): cantidad de dinero a retirar

    Return:
    - bool: true si el retiro fue exitoso, false si no hay suficiente 
    saldo
    */

    // Sanity check: no se pueden retirar cantidades negativas (silent)
    dinero = (dinero > 0) ? dinero : 0;

    if (dinero > this->saldo) return false; // No hay suficiente saldo para 
                                            // retirar

    this->saldo -= dinero;
    return true;
}

void Cuenta::info() const
{
    /*
    Info()
    ----------------
    Imprimir infoo
    
    Parametros:

    Return:

    */

    printf("Cuenta ID: %s\n"
           "Tipo de cuenta: %s\n"
           "Saldo: %.2f\n",
        this->id.c_str(),
        (this->tipoCuenta == TIPO_CUENTA_AHORRO) ? "Ahorro" : "Cheques",
        this->saldo);
}

// ########################### FIN DE CUENTA.CPP ###############################
// #############################################################################
