/*
CuentaDeAhorro.cpp
========================


Descripcion:
------------
Cuenta de ahorro, con un interes y un limite de retiros mensuales.
Es hija de Cuenta.



Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#include "if/CuentaDeAhorro.h"

// Override del metodo retirar para aplicar el interes
bool CuentaDeAhorro::retirar(double dinero)
{
    /*
    Retirar()
    ----------------
    Metodo override que permite retirar dinero de la cuenta de ahorro con las 
    constraints de que no se pueden hacer mas de 6 retiros al mes
    
    Parametros:
    ----------------
    - dinero (double): cantidad de dinero a retirar

    Return:
    ----------------
    - bool: true si el retiro fue exitoso, false si no hay suficiente 
            saldo o se ha excedido el limite de retiros
    */

    // Checamos el limite de retiros del mes
    if (this->retirosRealizados >= MAX_RETIROS_MES) return false;

    // Sanity check: no se retiran cantidades negativas (silent)
    dinero = (dinero > 0) ? dinero : 0;

    // La cuenta de ahorro debe conservar SIEMPRE al menos el saldo minimo
    if (this->saldo - dinero < SALDO_MINIMO_AHORRO) return false;

    // Hacemos op
    this->saldo -= dinero;
    this->retirosRealizados++;

    // Printeamos
    printf("Retirando %.2f, nuevo saldo: %.2f\n"
           " Retiros realizados: %d\n"
           " Retiros restantes: %d\n",
        dinero,
        this->saldo,
        this->retirosRealizados,
        MAX_RETIROS_MES - this->retirosRealizados
    );

    return true;
}

void CuentaDeAhorro::aplicarInteres()
{
    /*
    AplicarInteres()
    ----------------
    Metodo que permite aplicar el interes al saldo de la cuenta de ahorro
    
    Parametros:
    ----------------

    Return:
    ----------------
    */

    // Aplicamos el interes al saldo
    float interesAplicado = this->saldo * (this->interes / 100.0);
    this->saldo += interesAplicado;

    // Printeamos
    printf("Aplicando interes del %.2f%%, interes aplicado: %.2f \n"
           "    nuevo saldo: %.2f\n",
        this->interes,
        interesAplicado,
        this->saldo
    );
}

void CuentaDeAhorro::info() const
{
    /*
    Info()
    ----------------
    Imprimir info de la cuenta de ahorro
    
    Parametros:
    ----------------

    Return:
    ----------------
    */

    printf("Cuenta ID: %s\n"
           "Tipo de cuenta: Ahorro\n"
           "Saldo: %.2f\n"
           "Interes: %.2f%%\n"
           "Retiros realizados este mes: %d\n"
           "Retiros restantes este mes: %d\n",
        this->getId().c_str(),
        this->saldo,
        this->interes,
        this->retirosRealizados,
        MAX_RETIROS_MES - this->retirosRealizados
    );
}

// ########################### FIN DE CUENTADEAHORRO.CPP #######################
// #############################################################################
