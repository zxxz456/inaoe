/*
Banco.h
========================


Descripcion:
------------
Clase que representa el banco. Administra a los clientes y sus cuentas:
da de alta clientes, abre cuentas (de ahorro o de cheques) asignandolas a
un cliente y permite consultarlas.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#ifndef BANCO_H
#define BANCO_H

#include "Cliente.h"
#include "Cuenta.h"
#include "CuentaDeAhorro.h"
#include "CuentaDeCheques.h"
#include <vector>
#include <string>

class Banco {

    public:
        //Constructor y destructor
        Banco(){};
        ~Banco();   // libera las cuentas y clientes reservados con new

        
        // Metodo para crear un cliente
        Cliente* agregarCliente(std::string nombre);

        // Metodos para el maneji de cuentas
        CuentaDeAhorro*  abrirCuentaAhorro(Cliente* cliente, 
                                            double saldoInicial, 
                                            int interes);
        CuentaDeCheques* abrirCuentaCheques(Cliente* cliente, 
                                            double saldoInicial);
        Cuenta* buscarCuenta(const std::string& id) const;

        // Metodo para imprimir info del banco
        void info() const;                                  

    private:
        std::vector<Cliente*> clientes;   // VEctor de clientes
        std::vector<Cuenta*>  cuentas;    // Vector de cuentas de clientes
};

#endif // BANCO_H

// ########################### FIN DE BANCO.H ##################################
// #############################################################################
