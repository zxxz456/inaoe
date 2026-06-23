/*
Cinta.h
========================


Descripcion:
------------
Clase para representar la cabeza y la cinta de la MT. 
La cinta es potencialmente infinita: se expande con blancos de forma automatica 
hacia ambos lados conforme la cabeza lo necesita (peeero no es infinita 
realmente, la memoria es limiada)


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       19/06/2026      Creation


*/

#ifndef CINTA_H
#define CINTA_H

#include <string>
#include <deque>

#include "Utils.h"

class Cinta 
{

    public:

        // Constructor
        Cinta(const std::string& entrada, char blanco);

        // Simbolo bajo la cabeza
        char leer() const;

        // Escribe un simbolo en la celda actual
        void escribir(char c);

        // Mueve la cabeza una posicion, expandiendo con blancos si hace falta
        void mover(Mov dir);

        // Indice de la celda bajo la cabeza
        int posicion() const;

        // ID (Instant Description)
        std::string contenido() const;

    private:

        std::deque<char> celdas;            // celdas de la cinta
        char             blanco;            // simbolo blanco
        int              cabeza;           // indice de la celda bajo la cabeza

};

#endif // CINTA_H
