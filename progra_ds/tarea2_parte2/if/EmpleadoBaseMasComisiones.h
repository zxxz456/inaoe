/*
EmpleadoBaseMasComisiones.h
========================


Descripcion:
------------
Clase derivada que representa a un empleado con salario base más comisiones.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#ifndef EMPLEADOBASMASCOMISIONES_H
#define EMPLEADOBASMASCOMISIONES_H

#include "EmpleadoPorComisiones.h"

class EmpleadoBaseMasComisiones : public EmpleadoPorComisiones {
    public:
        // Constructor
        EmpleadoBaseMasComisiones(double salarioBase, 
                                  double comision, 
                                  int ventasTotales) : 
        salarioBase(salarioBase),
        EmpleadoPorComisiones(comision, ventasTotales) {}

        // getters y setters
        // NO DECLARADOS EN EL DIAGRAMA PERO IGUAL NO HACE MAL TENERLOS
        void setSalarioBase(double salarioBase)
        { 
            this->salarioBase = salarioBase; 
        }

        double getSalarioBase() const{ return salarioBase; }

        // Override de ganancias e imprimir
        double ganancias() override;
        void imprimir() override;

    private:
        double salarioBase;                 // variable baseSalary del diagrama          

};

#endif // EMPLEADOBASMASCOMISIONES_H