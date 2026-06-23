/*
MaquinaTuring.h
========================


Descripcion:
------------
Cascaron generico de una MT. Se basa en la definicion del HMU... El cual define
una TM simple M como sigue

            M = (Q, Sigam, Gamma, d, q0, B, F)

donde:
            Q = {estados}
            Sigma = {Alfabeto de simbolos de entrada}
            Gamma = {Alfabeto de Cinta}
            d = funcion de transicion (se mapean como la tabla)
            q0 = estado inicial perteneciente a Q
            B = Simbolo blanco
            F = {estados de aceptacion} subset de Q


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       20/06/2026      Fixed bug - error en calculo d sig estado
zxxz6       20/06/2026      Fixed bug cuando se crea la MT desde archivo
zxxz6       19/06/2026      Creation


*/

#ifndef MAQUINATURING_H
#define MAQUINATURING_H

#include <string>
#include <vector>
#include <map>
#include <set>
#include <utility>

#include "Utils.h"
#include "Cinta.h"

class MaquinaTuring 
{

    public:

        // Constructor: estado inicial y simbolo blanco
        MaquinaTuring(std::string inicial, char blanco);

        // Marca un estado como estado de aceptacion
        void agregarAceptacion(const std::string& estado);

        // Indica si un estado es de aceptacion
        bool esAceptacion(const std::string& estado) const;

        // Indica si un estado es el estado inicial
        bool esInicial(const std::string& estado) const;

        // Declara un estado de Q 
        void agregarEstado(const std::string& estado);

        // Declara un simbolo del alfabeto de cinta
        void agregarSimbolo(char simbolo);

        // Declara un simbolo del alfabeto sigma
        void agregarEntrada(char simbolo);

        // Registra una entrada de la funcion de transicion
        void agregarTransicion(const std::string& estado, 
                               char lee,
                               const std::string& destino, 
                               char escribe, 
                               Mov mueve);

        // Corre la maquina sobre la entrada e imprime cada paso con el ID
        bool run(const std::string& entrada) const;

        // Imprime la tabla de transiciones en formato de definicion formal
        void imprimirTabla() const;

        

    private:
        
        static const int kMaxPasos = MAX_STEPS;     // tope anti bucle infinito
        
        // Propieades de la MT
        std::string inicial;                        // q0 pert a Q
        std::set<std::string> aceptacion;           // F = {}
        std::set<char> sigma;                       // SIGMA = {}
        char blanco;                                // B

        std::map<std::pair<std::string, char>, Transicion> delta;  // fnc. trans
        std::vector<std::string> estados;           // estados vistos
        std::vector<char>        simbolos;          // simbolos vistos

        // Funciones auxiliares internas
        char visible(char c) const;
        void registrarEstado(const std::string& e);
        void registrarSimbolo(char s);
        std::vector<char> columnasOrdenadas() const;
        void imprimirPaso(int paso,
                          const std::string& estado,
                          const Cinta& cinta) const;

};

#endif // MAQUINATURING_H
