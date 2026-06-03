/*
EmpleadoPorComisiones.h
========================


Descripcion:
------------
Clase derivada que representa a un empleado por comisiones.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#ifndef EMPLEADOPORCOMISIONES_H
#define EMPLEADOPORCOMISIONES_H

#include "Empleado.h"

class EmpleadoPorComisiones : public Empleado {
    public:
        // Constructor
        EmpleadoPorComisiones(double comision, int ventasTotales) : 
        comisionPorVenta(comision),
        ventasTotales(ventasTotales),
        Empleado(0) {}

        // getters y setters
        // NO DECLARADOS EN EL DIAGRAMA PERO IGUAL NO HACE MAL TENERLOS
        void setComisionPorVenta(double comisionPorVenta)
        { 
            this->comisionPorVenta = comisionPorVenta; 
        }
        double getComisionPorVenta() const{ return comisionPorVenta; }

        void setVentasTotales(int ventasTotales)
        { 
            this->ventasTotales = ventasTotales; 
        }
        int getVentasTotales() const{ return ventasTotales; }

        // Override de ganancias e imprimir
        double ganancias() override;
        void imprimir() override;

    private:
        double comisionPorVenta;        // variable commissionRate del diagrama
        int ventasTotales;              // variable grossSales del diagrama

};

#endif // EMPLEADOPORCOMISIONES_H