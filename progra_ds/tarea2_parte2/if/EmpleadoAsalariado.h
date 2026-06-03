/*
EmpleadoAsalariado.h
========================


Descripcion:
------------
Clase derivada que representa a un empleado asalariado.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#ifndef EMPLEADOASALARIADO_H
#define EMPLEADOASALARIADO_H

#include "Empleado.h"

class EmpleadoAsalariado : public Empleado {
    public:
        // Constructor
        EmpleadoAsalariado(double salarioSemanal) : 
        salarioSemanal(salarioSemanal),
        Empleado(0) {}

        // getters y setters
        // NO DECLARADOS EN EL DIAGRAMA PERO IGUAL NO HACE MAL TENERLOS
        void setSalarioSemanal(double salarioSemanal)
        { 
            this->salarioSemanal = salarioSemanal; 
        }

        double getSalarioSemanal() const{ return salarioSemanal; }

        // Override de ganancias e imprimir
        double ganancias() override;
        void imprimir() override;

    private:
        double salarioSemanal;            // variable weeklySalary del diagrama

};

#endif // EMPLEADOASALARIADO_H

