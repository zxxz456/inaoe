/*
Cliente.h
========================


Descripcion:
------------
Clase que representa a un clinete de un bacno. Consta de noimbre y puede tener
vaarias cuentas aunque eso no se ve reflejado aqui sino en Banco.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#ifndef CLIENTE_H
#define CLIENTE_H

#include <string>

class Cliente {

    public:
        Cliente(std::string nombre) : nombre(nombre) 
        {
            
        };
        Cliente() : nombre("") {};
        ~Cliente(){};

        // Getters
        const std::string& getNombre() const { return nombre; }

        // Setters
        void setNombre(const std::string& nombre) { this->nombre = nombre; }

    private:
        std::string nombre;   // nombre del cliente
};

#endif // CLIENTE_H

// ########################### FIN DE CLIENTE.H ################################
// #############################################################################
