/*
main.cpp
========================


Descripcion:
------------
Programa de prueba: crea un banco, da de alta un cliente, abre una cuenta de
cada tipo y ejercita las reglas del enunciado (IDs unicos, deposito/retiro,
interes, limite de 6 retiros y saldo minimo de $1000 en ahorro).
No es interactivo ni asi... Se puede hacer interactivo sin problema pero me 
apegue al enunciado de la tarea.


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

int main()
{
    Banco banco;

    // 1. Damos de alta un cliente
    Cliente* bryan = banco.agregarCliente("Bryan Violante");

    // 2. Abrimos una cuenta de cada tipo, asignadas al cliente
    CuentaDeAhorro*  ahorro  = banco.abrirCuentaAhorro(bryan, 5000.00, 3);  
    CuentaDeCheques* cheques = banco.abrirCuentaCheques(bryan, 1500.00);

    printf("\n>>> IDs generados (formato 2-mm-yy-id):\n");
    printf("Ahorro:  %s\n", ahorro->getId().c_str());
    printf("Cheques: %s\n", cheques->getId().c_str());

    // 3. Deposito y retiro en la cuenta de cheques
    printf("\n>>> Deposito y retiro en cuenta de cheques:\n");
    cheques->depositar(500.00);   // 1500 -> 2000
    cheques->retirar(300.00);     // 2000 -> 1700
    cheques->info();

    // 4. Interes de rendimiento
    printf("\n>>> Aplicando interes a la cuenta de ahorro:\n");
    ahorro->aplicarInteres();     // 5000 + 3% = 5150

    // 5. Testing saldo minimo
    printf("\n>>> Intentando retirar de mas (rompe el minimo de $1000):\n");
    bool ok = ahorro->retirar(5000.00);   // dejaria el saldo < 1000
    printf("Retiro de 5000: %s\n", ok ? "exitoso" : "RECHAZADO");

    // 6. Testing de limite de retiros
    printf("\n>>> Probando el limite de 6 retiros:\n");
    for (int i = 1; i <= 7; i++) {
        bool r = ahorro->retirar(10.00);
        printf("Retiro #%d de 10: %s\n", i, r ? "exitoso" : "RECHAZADO");
    }

    // 7. Testing de minimo al abrir
    printf("\n>>> Intentando abrir cuenta de ahorro con $500:\n");
    CuentaDeAhorro* invalida = banco.abrirCuentaAhorro(bryan, 500.00, 2);
    printf("Resultado: %s\n", invalida ? "abierta" : "NO se abrio");

    // 8. Buscar una cuenta por id
    printf("\n>>> Buscar cuenta por id:\n");
    Cuenta* encontrada = banco.buscarCuenta(ahorro->getId());
    printf("Buscando %s -> %s\n", ahorro->getId().c_str(),
           encontrada ? "encontrada" : "no existe");

    // 9. Estado final del banco
    printf("\n>>> Estado final del banco:\n");
    banco.info();

    return 0;
}

// ########################### FIN DE MAIN.CPP #################################
// #############################################################################
