/*
LectorMT.h
========================


Descripcion:
------------
Lector/constructor de MT a partir de una definicion en un file de texto plano

Este es el formato del archivo d texto para declarar una MT (se basa en la 
7-tupla del HMU)

    Q=q0,q1,q2,q3,q4           (estados)
    Sigma=0,1                  (alfabeto de entrada)
    Gamma=X,Y,B                (alfabeto de cinta)
    q_ini=q0                   (estado inicial)
    F=q4                       (estado(s) de aceptacion: "F=q4,q5")
    blanco=B                   (opcional; por defecto B)

    q0 0 -> q1 X R             (trans: estado lee -> destino escribe mueve)
    q0 Y -> q3 Y R


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       19/06/2026      Creation


*/

#ifndef LECTORMT_H
#define LECTORMT_H

#include <string>
#include <vector>

#include "MaquinaTuring.h"

namespace LectorMT 
{

    // Construye una MT a partir de la def formal
    MaquinaTuring* construir(const std::vector<std::string>& lineas, 
                             std::string& error);

    // Carga una MT desde un archivo de texto
    MaquinaTuring* cargarArchivo(const std::string& ruta, std::string& error);

}

#endif // LECTORMT_H
