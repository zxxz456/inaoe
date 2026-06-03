/*
Cuenta.h
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

#ifndef CUENTA_H
#define CUENTA_H

#include "Cliente.h"
#include "Utils.h"
#include "UUID.h"
#include <string>


class Cuenta {

    public:
        Cuenta(Cliente* cliente, double saldo, int tipoCuenta) :
        saldo(saldo),                          // orden de la lista = orden de declaracion
        cliente(cliente),
        id(UUID::getInstance().generar()),
        tipoCuenta(tipoCuenta)
        {
            
        };
        virtual ~Cuenta(){};   // virtual: permite borrar cuentas hijas via Cuenta*

        // Getters
        int getTipoCuenta() const { return tipoCuenta; }
        double getSaldo() const { return saldo; }
        const std::string& getId() const { return id; }
        Cliente* getCliente() const { return cliente; }

        // Setters
        void setCliente(Cliente* cliente) { this->cliente = cliente; }
        void setTipoCuenta(int tipoCuenta) { this->tipoCuenta = tipoCuenta; }
        void setSaldo(double saldo) { this->saldo = saldo; }
        void setId(const std::string& id) { this->id = id; }

        // Metodos virtuales
        virtual void depositar(double dinero);
        virtual bool retirar(double dinero);
        virtual void info() const;

    protected:
        double saldo;             // saldo actual de la cuenta

    private:
        Cliente* cliente;         // puntero al cliente propietario de la cuenta
        std::string id;           // identificador unico de la cuenta
        int tipoCuenta;           // 1 = ahorro, 2 = cheques
};

#endif // CUENTA_H

// ########################### FIN DE CUENTA.H #################################
// #############################################################################
