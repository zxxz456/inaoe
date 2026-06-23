/*
Utils.h
========================


Descripcion:
------------
Misc, tipos y funciones para el proyecto


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/06/2026      Add fnc leerLinea y MAX_BUFF_SIZE
zxxz6       20/06/2026      Add funcion para pausar y MAX_STEPS
zxxz6       19/06/2026      Creation


*/

#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <cstddef>
#include <cstdio>

#define MAX_STEPS 10000
#define MAX_BUFF_SIZE 256

// Direccion del movimiento de la cabeza sobre la cinta
enum class Mov { L, R };

// Una transicion de la MT: a que estado ir, que escribir y hacia donde mover
struct Transicion {
    std::string destino;                     // estado destino
    char        escribe;                     // simbolo a escribir
    Mov         mueve;                       // L (izquierda) o R (derecha)
};

// Una regla ya parseada por el lector: la transicion completa (estado y simbolo
// leidos incluidos) junto con el numero de linea, para los mensajes de error
struct Regla {
    std::string estado;                      // estado de origen
    char        lee;                         // simbolo leido
    std::string destino;                     // estado destino
    char        escribe;                     // simbolo a escribir
    Mov         mueve;                       // L o R
    std::size_t linea;                       // numero de linea en la definicion
};


inline std::string pad(std::string s, std::size_t ancho)
{
    /*
    pad()
    ----------------
    Rellena una cadena con espacios a la izquierda hasta alcanzar el ancho dado

    Parametros:
    ----------------
    - s     (std::string): cadena a rellenar
    - ancho (std::size_t): ancho minimo deseado

    Return:
    ----------------
    - std::string: la cadena rellenada
    */

    while (s.size() < ancho) s = " " + s;
    return s;
}


inline void pausa()
{
    /*
    pausa()
    ----------------
    Detiene la ejecucion hasta que el usuario presione Enter, consumiendo la
    linea completa para no dejar residuos en la entrada

    Parametros:
    ----------------

    Return:
    ----------------
    */

    printf("\tEnter para continuar...");
    fflush(stdout);

    int c;
    while ((c = getchar()) != '\n' && c != EOF){}
}


inline bool leerLinea(const char* prompt, std::string& destino)
{
    /*
    leerLinea()
    ----------------
    Imprime el prompt y lee una linea completa de stdin, guardandola en
    'destino' sin el salto de linea

    Parametros:
    ----------------
    - prompt  (const char*):  texto a mostrar antes de leer
    - destino (std::string&): donde se guarda la linea leida

    Return:
    ----------------
    - bool: false si se llego a fin de archivo (Ctrl-D); true en otro caso
    */

    printf("%s", prompt);
    fflush(stdout);

    char buffer[MAX_BUFF_SIZE];
    if (!fgets(buffer, sizeof(buffer), stdin))
        return false;                           

    destino = buffer;
    while (!destino.empty() && (destino.back() == '\n' || 
            destino.back() == '\r'))
        destino.pop_back();                  
    return true;
}


#endif // UTILS_H
