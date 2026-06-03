/*
main.cpp
========================


Descripcion:
------------
Aplicacion que crea un empleado de cada tipo y los procesa de forma
polimorfica: primero muestra las ganancias de cada uno y despues imprime
su informacion, asi como se muestra en las diapositivas


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       03/06/2026      Creation


*/

#include "if/EmpleadoAsalariado.h"
#include "if/EmpleadoPorHora.h"
#include "if/EmpleadoPorComisiones.h"
#include "if/EmpleadoBaseMasComisiones.h"
#include <vector>
#include <cstdio>

int main()
{
    // Vector de empleados...
    // La clase Empleado se usa como base y se agregan instancias
    // de cada tipo, esto es posible gracias a la herencia y el polimorfismo
    std::vector<Empleado*> empleados = {
        new EmpleadoAsalariado(1000.0),
        new EmpleadoPorHora(50.0, 45),
        new EmpleadoPorComisiones(0.10, 5000),
        new EmpleadoBaseMasComisiones(300.0, 0.10, 5000)
    };

    // Se muestran las ganancias como en la diapositiva de la clase
    printf("===== Ganancias =====\n");
    for (Empleado* empleado : empleados)
    {
        printf("Ganancias: %.2f\n", empleado->ganancias());
    }

    // Y tambien mostramos el metodo imprimir() de cada empleado,
    // el cual muestra su info especifica (polymorfismo de nuevo)
    printf("\n===== Imprimir =====\n");
    for (Empleado* empleado : empleados)
    {
        empleado->imprimir();
        printf("---------------------\n");
    }

    // Destructor virtual elimina correctamente cada tipo de emp
    for (Empleado* empleado : empleados)
    {
        delete empleado;
    }

    return 0;
}
