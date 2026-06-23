/*
Cinta.cpp
========================


Descripcion:
------------
Implementacion de la clase Cinta (definicion en if/Cinta.h)


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       20/06/2026      Creation


*/

#include "if/Cinta.h"


Cinta::Cinta(const std::string& entrada, 
             char blanco): 
            blanco(blanco), 
            cabeza(0)
{
    /*
    Cinta()
    ----------------
    Construye la cinta a partir de la cadena de entrada. Si la entrada esta
    vacia, deja una sola celda en blanco

    Parametros:
    ----------------
    - entrada (const std::string&): cadena inicial sobre la cinta
    - blanco  (char): simbolo blanco de la cinta

    Return:
    ----------------
    */

    if (entrada.empty())
        celdas.push_back(blanco);               // al menos una celda
    else
        for (char c : entrada)
            celdas.push_back(c);
}


char Cinta::leer() const
{
    /*
    leer()
    ----------------
    Lee el simbolo bajo la cabeza de la cinta

    Parametros:
    ----------------


    ----------------
    Return:
    - char: simbolo bajo la cabeza
    
    */

    return celdas[cabeza];
}


void Cinta::escribir(char c)
{
    /*
    escribir()
    ----------------
    Escribe un simbolo en la celda bajo la cabeza

    Parametros:
    ----------------
    - c (char): simbolo a escribir
    
    Return:
    ----------------
    */

    celdas[cabeza] = c;
}


void Cinta::mover(Mov dir)
{
    /*
    mover()
    ----------------
    Mueve la cabeza una posicion en la direccion dada, si llega a un borde
    la expande con B

    Parametros:
    ----------------
    - dir (Mov): direccion del movimiento (L o R)

    Return:
    ----------------

    */

    if (dir == Mov::R) 
    {
        cabeza++;
        if (cabeza == static_cast<int>(celdas.size())) // borde der
            celdas.push_back(blanco);
    } 
    else 
    {
        if (cabeza == 0)
            celdas.push_front(blanco);                 // borde izq
        else
            cabeza--;
    }
}


int Cinta::posicion() const
{
    /*
    posicion()
    ----------------
    REgresa idx de la cabeza
    
    Parametros:
    ----------------

    Return:
    ----------------
    - int: indice de la celda bajo la cabeza
    */

    return cabeza;
}


std::string Cinta::contenido() const
{
    /*
    contenido()
    ----------------
    Da la representacion de la cinta el ID de la MT

    Parametros:
    ----------------

    Return:
    ----------------
    - std::string: contenido visible de la cinta

    */

    int fin = static_cast<int>(celdas.size()) - 1;
    while (fin > cabeza && fin > 0 && celdas[fin] == blanco)
        fin--;

    std::string s;
    for (int i = 0; i <= fin; i++)
        s += celdas[i];
    return s;
}
