/*
Empleado.h
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

#ifndef EMPLEADO_H
#define EMPLEADO_H

class Empleado {

    public:

        // cONSTRUCTOR
        Empleado(double salario) : salario(salario) {}
        
        // Destructor virtual
        virtual ~Empleado();

        // Metodos virtuales para poly
        virtual double ganancias();
        virtual void imprimir();

        // Getters y Setters
        // OJOOO: EL DIAGRAMA NO DECLARA LOS GETTERS Y SETTERS PERO ES UNA BUENA
        // PRACTICA
        void setSalario(double salario){ this->salario = salario; }
        double getSalario() const{ return salario; }

    private:

        double salario;

};


#endif // EMPLEADO_H