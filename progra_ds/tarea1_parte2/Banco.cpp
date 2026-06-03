/*
Banco.cpp
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

#include "if/Banco.h"
#include <cstdio>

Banco::~Banco()
{
    /*
    ~Banco()
    ----------------
    Libera toda la memoria reservada con new (primero las cuentas, luego los
    clientes).

    Parametros:
    ----------------

    Return:
    ----------------
    */

    for (Cuenta* cuenta : this->cuentas)    delete cuenta;
    for (Cliente* cliente : this->clientes) delete cliente;
}

Cliente* Banco::agregarCliente(std::string nombre)
{
    /*
    agregarCliente()
    ----------------
    Crea un nuevo cliente, lo registra en el banco y devuelve su puntero

    Parametros:
    ----------------
    - nombre (std::string): nombre del cliente

    Return:
    ----------------
    - Cliente*: puntero al cliente creado
    */

    Cliente* cliente = new Cliente(nombre);
    this->clientes.push_back(cliente);
    return cliente;
}

CuentaDeAhorro* Banco::abrirCuentaAhorro(Cliente* cliente, 
                                         double saldoInicial, 
                                         int interes)
{
    /*
    abrirCuentaAhorro()
    ----------------
    Abre una cuenta de ahorro asignada a un cliente y la registra en el banco.

    Parametros:
    ----------------
    - cliente (Cliente*): dueno de la cuenta
    - saldoInicial (double): saldo con el que se abre la cuenta
    - interes (int): tasa de interes (de 1 a 5)

    Return:
    ----------------
    - CuentaDeAhorro*: puntero a la cuenta creada
    */

    // Regla del banco: una cuenta de ahorro no se abre por debajo del minimo
    if (saldoInicial < SALDO_MINIMO_AHORRO) {
        printf("No se puede abrir una cuenta de ahorro con menos de $%.2f "
               "(saldo dado: $%.2f)\n",
               SALDO_MINIMO_AHORRO, saldoInicial);
        return nullptr;
    }

    CuentaDeAhorro* cuenta = new CuentaDeAhorro(cliente, saldoInicial, interes);
    this->cuentas.push_back(cuenta);
    return cuenta;
}

CuentaDeCheques* Banco::abrirCuentaCheques(Cliente* cliente, 
                                           double saldoInicial)
{
    /*
    abrirCuentaCheques()
    ----------------
    Abre una cuenta de cheques asignada a un cliente y la registra en el banco

    Parametros:
    ----------------
    - cliente (Cliente*): dueno de la cuenta
    - saldoInicial (double): saldo con el que se abre la cuenta

    Return:
    ----------------
    - CuentaDeCheques*: puntero a la cuenta creada

    */

    CuentaDeCheques* cuenta = new CuentaDeCheques(cliente, saldoInicial);
    this->cuentas.push_back(cuenta);
    return cuenta;
}

Cuenta* Banco::buscarCuenta(const std::string& id) const
{
    /*
    buscarCuenta()
    ----------------
    Busca una cuenta por su identificador.

    Parametros:
    ----------------
    - id (std::string): identificador de la cuenta (formato 2-mm-yy-id)

    Return:
    ----------------
    - Cuenta*: puntero a la cuenta encontrada, o nullptr si no existe

    */

    for (Cuenta* cuenta : this->cuentas) {
        if (cuenta->getId() == id) return cuenta;
    }
    return nullptr;
}

void Banco::info() const
{
    /*
    info()
    ----------------
    Imprime la informacion de todas las cuentas registradas en el banco

    Parametros:
    ----------------

    Return:
    ----------------

    */

    printf("===== Cuentas del banco (%zu) =====\n", 
        this->cuentas.size());

    for (Cuenta* cuenta : this->cuentas) {
        cuenta->info();
        printf("------------------------------\n");
    }
}

// ########################### FIN DE BANCO.CPP ################################
// #############################################################################
