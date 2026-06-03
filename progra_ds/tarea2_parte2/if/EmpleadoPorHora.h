/*
EmpleadoPorHora.h
========================


Descripcion:
------------
Clase derivada que representa a un empleado por hora.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#ifndef EMPLEADOPORHORA_H
#define EMPLEADOPORHORA_H

#include "Empleado.h"

class EmpleadoPorHora : public Empleado {
    public:
        // Constructor
        EmpleadoPorHora(double tarifa, int horasTrabajadas) : 
        horasTrabajadas(horasTrabajadas),
        tarifaPorHora(tarifa),
        Empleado(0) {}

        // getters y setters
        // NO DECLARADOS EN EL DIAGRAMA PERO IGUAL NO HACE MAL TENERLOS
        void setHorasTrabajadas(int horasTrabajadas)
        { 
            this->horasTrabajadas = horasTrabajadas; 
        }

        void setTarifaPorHora(double tarifaPorHora)
        {
            this->tarifaPorHora = tarifaPorHora;
        }

        int getHorasTrabajadas() const{ return horasTrabajadas; }
        double getTarifaPorHora() const{ return tarifaPorHora; }

        // Override de ganancias e imprimir
        double ganancias() override;
        void imprimir() override;

    private:
        int horasTrabajadas;                      // variable hours del diagrama
        double tarifaPorHora;                     // variable wage del diagrama


};

#endif // EMPLEADOPORHORA_H