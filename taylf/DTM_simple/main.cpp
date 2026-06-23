/*
main.cpp
========================


Descripcion:
------------
Programa principal del simulador de Maquina de Turing


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       20/06/2026      Creation


*/

#include "if/MaquinaTuring.h"
#include "if/LectorMT.h"
#include "if/Utils.h"       

#include <cstdio>
#include <string>


static void simular(const MaquinaTuring& mt)
{
    /*
    simular()
    ----------------
    Muestra la tabla y, en bucle, pide cadenas y las simula paso a paso 

    Parametros:
    ----------------
    - mt (const MaquinaTuring&): la MT a simular

    Return:
    ----------------

    */

    mt.imprimirTabla();

    std::string entrada;
    while (leerLinea("w = ", entrada)) {
        if (entrada.empty())
            break;                              
        mt.run(entrada);
    }
}


int main(int argc, char* argv[])
{
    /*
    main()
    ----------------
    Carga la MT desde el archivo de definicion recibido como argumento y la
    corre en modo interactivo paso a paso. Requiere siempre un archivo.
    */

    // Se requiere la ruta de un archivo de definicion.
    if (argc < 2) {
        printf("Uso: %s <archivo.tm>\n", argv[0]);
        return 1;
    }

    // El argumento se trata como la ruta del archivo de definicion.
    std::string error;
    MaquinaTuring* mt = LectorMT::cargarArchivo(argv[1], error);

    if (!mt) {
        printf("Error al generar la MT: %s\n", error.c_str());
        return 1;
    }

    simular(*mt);
    delete mt;
    return 0;
}
