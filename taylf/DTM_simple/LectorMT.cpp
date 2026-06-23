/*
LectorMT.cpp
========================


Descripcion:
------------
Implementacion del lector/constructor de Maquinas de Turing: parsea la
definicion en texto (como 7-tupla: Q, Sigma, Gamma, transiciones, q_ini, B, F),
valida que sea determinista y coherente, y arma el objeto MT


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       22/06/2026      Fixed bug: no se detectaba correctamente los delta
zxxz6       21/06/2026      Vibe coded funcs auxiliares (trim, sinComentario,
                            tokenizar, aMinusculas, parseLista, claveDirectiva)
zxxz6       20/06/2026      Creation


*/

#include "if/LectorMT.h"
#include "if/Utils.h"

#include <fstream>
#include <sstream>
#include <set>
#include <cctype>


namespace {

    // Quita espacios al inicio y al final
    std::string trim(const std::string& s)
    {
        std::size_t a = s.find_first_not_of(" \t\r\n");
        if (a == std::string::npos) return "";
        std::size_t b = s.find_last_not_of(" \t\r\n");
        return s.substr(a, b - a + 1);
    }

    // Elimina el comentario que empieza en '#'
    std::string sinComentario(const std::string& s)
    {
        std::size_t p = s.find('#');
        return (p == std::string::npos) ? s : s.substr(0, p);
    }

    // Parte la cadena en palabras separadas por espacios
    std::vector<std::string> tokenizar(const std::string& s)
    {
        std::vector<std::string> tok;
        std::istringstream iss(s);
        std::string w;
        while (iss >> w) tok.push_back(w);
        return tok;
    }

    // Pasa una cadena a minusculas
    std::string aMinusculas(const std::string& s)
    {
        std::string r = s;
        for (char& c : r) c = static_cast<char>(
            std::tolower(static_cast<unsigned char>(c))
        );
        return r;
    }

    // Separa una lista por comas y/o espacios: "q1,q2 q3" -> [q1, q2, q3]
    std::vector<std::string> parseLista(const std::string& valor)
    {
        std::string s = valor;
        for (char& c : s) if (c == ',') c = ' ';
        return tokenizar(s);
    }

    // Devuelve la directiva canonica de la palabra a la izquierda del '=',
    // o "" si no es una directiva conocida
    std::string claveDirectiva(const std::string& izq)
    {
        std::string k = aMinusculas(izq);
        if (k == "q") return "Q";
        if (k == "sigma") return "Sigma";
        if (k == "gamma") return "Gamma";
        if (k == "q_ini" || k == "qini" || k == "inicial")
            return "inicial";
        if (k == "f" || k == "aceptacion" || k == "aceptar" || k == "final")
            return "F";
        if (k == "blanco" || k == "vacio") return "blanco";
        return "";
    }

}


MaquinaTuring* LectorMT::construir(const std::vector<std::string>& lineas,
                                   std::string& error)
{
    /*
    construir()
    ----------------
    Recorre las lineas de la definicion (formato de 7-tupla) separando los
    attrs Q/Sigma/Gamma/q_ini/F/blanco de las transiciones, valida que sea
    determinista y coherente con los conjuntos declarados, y construye la MT

    Formato de directiva:  <clave>=<valores separados por coma/espacio>
    Formato de transicion: <estado> <lee> -> <destino> <escribe> <L|R>

    Parametros:
    ----------------
    - lineas (const std::vector<std::string>&): lineas de la definicion
    - error  (std::string&): mensaje de error si la construccion falla

    Return:
    ----------------
    - MaquinaTuring*: la MT creada con new, o nullptr si hubo error
    */

    std::string inicial;
    bool tieneInicial = false;
    char blanco = 'B';

    std::set<std::string> Q;                        // estados
    bool tieneQ = false;
    std::set<char>        sigma;                    // alfabeto de entrada
    std::set<char>        gamma;                    // alfabeto de cinta extra
    bool                  tieneAlfabeto = false;    // se declaro Sigma o Gamma
    std::vector<std::string> F;                     // aceptacion


    std::vector<Regla> reglas;                      // transiciones
    std::set<std::pair<std::string, char>> vistos;  // para detectar NTM

    for (std::size_t i = 0; i < lineas.size(); i++)
    {
        std::string linea = trim(sinComentario(lineas[i]));
        if (linea.empty()) continue;

        const std::string ubic = "linea " + std::to_string(i + 1) + ": ";

        // Es directiva si trae '=' antes de la flecha '->' (las transiciones
        // usan '->', no '=').
        std::size_t eq     = linea.find('=');
        std::size_t flecha = linea.find("->");
        bool esDirectiva = (eq != std::string::npos) &&
                           (flecha == std::string::npos || eq < flecha);

        if (esDirectiva)
        {
            std::string izq = trim(linea.substr(0, eq));
            std::string der = trim(linea.substr(eq + 1));
            std::string k = claveDirectiva(izq);

            if (k == "Q")
            {
                for (const std::string& q : parseLista(der)) Q.insert(q);
                tieneQ = true;
            }
            else if (k == "Sigma" || k == "Gamma")
            {
                std::set<char>& destino = (k == "Sigma") ? sigma : gamma;
                for (const std::string& s : parseLista(der))
                {
                    if (s.size() != 1)
                    {
                        error = ubic + k + ": '" + s + 
                                "' debe ser un simbolo de un caracter";
                        return nullptr;
                    }
                    destino.insert(s[0]);
                }
                tieneAlfabeto = true;
            }
            else if (k == "inicial")
            {
                std::vector<std::string> v = parseLista(der);
                if (v.empty())
                {
                    error = ubic + "falta el estado inicial";
                    return nullptr;
                }
                inicial = v[0];
                tieneInicial = true;
            }
            else if (k == "F")
            {
                for (const std::string& f : parseLista(der)) F.push_back(f);
            }
            else if (k == "blanco")
            {
                if (der.size() != 1)
                {
                    error = ubic + 
                            "el blanco debe ser un simbolo de un caracter";
                    return nullptr;
                }
                blanco = der[0];
            }
            else
            {
                error = ubic + "directiva desconocida '" + izq +
                        "' (se esperaba Q, Sigma, Gamma, q_ini, F o blanco)";
                return nullptr;
            }
        }
        else
        {
            // Transicion: estado lee [->] destino escribe mueve
            std::vector<std::string> p;
            for (const std::string& t : tokenizar(linea))
                if (t != "->") p.push_back(t);        

            if (p.size() != 5)
            {
                error = ubic + "una transicion necesita 5 campos "
                               "(estado lee -> destino escribe mueve)";
                return nullptr;
            }
            if (p[1].size() != 1 || p[3].size() != 1)
            {
                error = ubic + "'lee' y 'escribe' deben ser un solo simbolo";
                return nullptr;
            }

            Mov mueve = Mov::R;
            if (p[4] == "R" || p[4] == "r")      mueve = Mov::R;
            else if (p[4] == "L" || p[4] == "l") mueve = Mov::L;
            else
            {
                error = ubic + "el movimiento debe ser L o R";
                return nullptr;
            }

            std::pair<std::string, char> clavet(p[0], p[1][0]);
            if (vistos.count(clavet))
            {
                error = ubic + "transicion duplicada para (" + 
                        p[0] + ", " + p[1] +
                        "); la MT debe ser determinista";
                return nullptr;
            }
            vistos.insert(clavet);
            reglas.push_back({p[0], p[1][0], p[2], p[3][0], mueve, i + 1});
        }
    }

    if (!tieneInicial)
    {
        error = "falta declarar el estado inicial (q_ini=...)";
        return nullptr;
    }

    // Alfabeto de cinta completo = Sigma U Gamma U {blanco} (para validar)
    std::set<char> alfabeto;
    for (char c : sigma) alfabeto.insert(c);
    for (char c : gamma) alfabeto.insert(c);
    if (tieneAlfabeto) alfabeto.insert(blanco);

    // Sanity check
    if (tieneQ)
    {
        if (Q.count(inicial) == 0)
        {
            error = "el estado inicial '" + inicial + "' no esta en Q";
            return nullptr;
        }
        for (const std::string& f : F)
            if (Q.count(f) == 0)
            {
                error = "el estado de aceptacion '" + f + "' no esta en Q";
                return nullptr;
            }
        for (const Regla& r : reglas)
        {
            if (Q.count(r.estado) == 0)
            {
                error = "linea " + std::to_string(r.linea) +
                        ": el estado '" + r.estado + "' no esta en Q";
                return nullptr;
            }
            if (Q.count(r.destino) == 0)
            {
                error = "linea " + std::to_string(r.linea) +
                        ": el estado '" + r.destino + "' no esta en Q";
                return nullptr;
            }
        }
    }
    if (tieneAlfabeto)
    {
        for (const Regla& r : reglas)
        {
            if (alfabeto.count(r.lee) == 0)
            {
                error = "linea " + std::to_string(r.linea) + ": el simbolo '" +
                        std::string(1, r.lee) + "' no esta en Sigma/Gamma";
                return nullptr;
            }
            if (alfabeto.count(r.escribe) == 0)
            {
                error = "linea " + std::to_string(r.linea) + ": el simbolo '" +
                        std::string(1, r.escribe) + "' no esta en Sigma/Gamma";
                return nullptr;
            }
        }
    }

    // Todo buen. construye TM
    MaquinaTuring* mt = new MaquinaTuring(inicial, blanco);
    for (const std::string& q : Q) mt->agregarEstado(q);     // Q
    for (char c : sigma)           mt->agregarEntrada(c);    // Sigma
    for (char c : gamma)           mt->agregarSimbolo(c);    // Gamma
    mt->agregarSimbolo(blanco);                              // B in Gamma
    for (const std::string& f : F) mt->agregarAceptacion(f); // F
    for (const Regla& r : reglas)                            // delta
        mt->agregarTransicion(r.estado, r.lee, r.destino, r.escribe, r.mueve);

    return mt;
}


MaquinaTuring* LectorMT::cargarArchivo(const std::string& ruta, std::string& error)
{
    /*
    cargarArchivo()
    ----------------
    Lee todas las lineas del archivo y invoca construir()

    Parametros:
    ----------------

    - ruta  (const std::string&): ruta del archivo de definicion
    - error (std::string&): mensaje de error si falla

    Return:
    ----------------

    - MaquinaTuring*: la MT creada con new, o nullptr si hubo error

    */

    std::ifstream f(ruta.c_str());
    if (!f)
    {
        error = "no se pudo abrir el archivo '" + ruta + "'";
        return nullptr;
    }

    std::vector<std::string> lineas;
    std::string l;
    while (std::getline(f, l))
        lineas.push_back(l);

    return construir(lineas, error);
}
