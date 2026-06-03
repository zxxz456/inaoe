/*
CuentaDeCheques.h
========================


Descripcion:
------------
Cuenta de cheques, es hija de cuenta pero no hace algo especial pq el ejercicio
no lo pide.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#ifndef CUENTADECHEQUES_H
#define CUENTADECHEQUES_H

#include "Cuenta.h"

class CuentaDeCheques : public Cuenta {

    public:
        CuentaDeCheques(Cliente* cliente, double saldo) :
        Cuenta(cliente, saldo, TIPO_CUENTA_CHEQUES)
        {   
        };
        ~CuentaDeCheques(){};
};

#endif // CUENTADECHEQUES_H

// ########################### FIN DE CUENTADECHEQUES.H ########################
// #############################################################################
