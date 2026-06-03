/*
CuentaDeAhorro.h
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

#ifndef CUENTADEAHORRO_H
#define CUENTADEAHORRO_H
    
#include "Cuenta.h"

class CuentaDeAhorro : public Cuenta {

    public:
        //Constructor
        CuentaDeAhorro(Cliente* cliente, double saldo, int interes) :
        Cuenta(cliente, saldo, TIPO_CUENTA_AHORRO),
        interes(interes)
        {};
        //Destructor
        ~CuentaDeAhorro(){};

        // Getters
        float getInteres() const { return interes; }
        int getRetirosRealizados() const { return retirosRealizados; }

        // Setters
        void setInteres(float interes) { this->interes = interes; }
        void setRetirosRealizados(int retiros) { this->retirosRealizados = 
            retiros; }
        
        // MEtodo para resetear retiruos mensuales
        void resetearRetiros() { this->retirosRealizados = 0; }

        // Override de retirar 
        bool retirar(double dinero) override;

        // Metodo para aplicar el interes al saldo actual
        void aplicarInteres();

        // Override de info 
        void info() const override;


    private:
        float interes;
        int retirosRealizados = 0; // Contador de retiros realizados en el mes
};


#endif // CUENTADEAHORRO_H

// ########################### FIN DE CUENTADEAHORRO.H #########################
// #############################################################################
