/*
MaquinaTuring.cpp
========================


Descripcion:
------------
Implementacion del motor generico de la Maquina de Turing: registro de
transiciones, impresion de la tabla y simulacion paso a paso.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       22/06/2026      Fixed bug: No se imprimia correctamente ID, no se
                            construia la MT de manera correcta, no se podia
                            leer la cinta, no se enumeraban los pasos bien
zxxz6       21/06/2026      Creation


*/

#include "if/MaquinaTuring.h"

#include <cstdio>
#include <algorithm>


MaquinaTuring::MaquinaTuring(std::string inicial, 
                             char blanco): 
                             inicial(std::move(inicial)),
                             blanco(blanco)
{
    /*
    MaquinaTuring()
    ----------------
    Constructor: inicializa la MT vacia

    Parametros:
    ----------------
    - inicial (std::string): estado inicial
    - blanco  (char): simbolo blanco de la cinta

    Return:
    ----------------
    */

    registrarEstado(this->inicial);            
}


void MaquinaTuring::agregarAceptacion(const std::string& estado)
{
    /*
    agregarAceptacion()
    ----------------
    Marca un estado como estado de aceptacion (pueden ser varios)

    Parametros:
    ----------------
    - estado (const std::string&): estado a marcar como aceptacion

    Return:
    ----------------

    */

    aceptacion.insert(estado);
    registrarEstado(estado);
}


bool MaquinaTuring::esAceptacion(const std::string& estado) const
{
    /*
    esAceptacion()
    ----------------

    Parametros:
    ----------------
    - estado (const std::string&): estado a consultar

    Return:
    ----------------
    - bool: true si el estado dado es de aceptacion
    
    */

    return aceptacion.count(estado) > 0;
}


bool MaquinaTuring::esInicial(const std::string& estado) const
{
    /*
    esInicial()
    ----------------

    Parametros:
    ----------------
    - estado (const std::string&): estado a consultar

    Return:
    ----------------
    - bool: true si el estado dado es el estado inicial

    */

    return estado == inicial;
}


void MaquinaTuring::agregarTransicion(const std::string& estado, 
                                      char lee,
                                      const std::string& destino, 
                                      char escribe, 
                                      Mov mueve)
{
    /*
    agregarTransicion()
    ----------------
    Registra una regla delta(estado, lee) = (destino, escribe, mueve) y lleva
    cuenta de los estados y simbolos vistos para poder imprimir la tabla

    Parametros:
    ----------------
    - estado  (const std::string&): estado de origen
    - lee     (char): simbolo leido bajo la cabeza
    - destino (const std::string&): estado al que se transita
    - escribe (char): simbolo que se escribe
    - mueve   (Mov):  direccion del movimiento

    Return:
    ----------------

    */

    delta[{estado, lee}] = {destino, escribe, mueve};

    registrarEstado(estado);
    registrarEstado(destino);
    registrarSimbolo(lee);
    registrarSimbolo(escribe);
}


void MaquinaTuring::agregarEstado(const std::string& estado)
{
    /*
    agregarEstado()
    ----------------
    Declara un estado de Q para que salga en la tabla aunque no tenga
    transiciones salientes

    Parametros:
    ----------------
    - estado (const std::string&): estado a declarar

    Return:
    ----------------

    */

    registrarEstado(estado);
}


void MaquinaTuring::agregarSimbolo(char simbolo)
{
    /*
    agregarSimbolo()
    ----------------
    Declara un simbolo del alfabeto de cinta para que salga como columna en la
    tabla aunque no aparezca en ninguna transicion

    Parametros:
    ----------------
    - simbolo (char): simbolo a declarar

    Return:
    ----------------
    
    */

    registrarSimbolo(simbolo);
}


void MaquinaTuring::agregarEntrada(char simbolo)
{
    /*
    agregarEntrada()
    ----------------
    Declara un simbolo del alfabeto de entrada (Sigma)

    Parametros:
    ----------------
    - simbolo (char): simbolo a declarar

    Return:
    ----------------

    */

    sigma.insert(simbolo);
    registrarSimbolo(simbolo);
}


char MaquinaTuring::visible(char c) const
{
    /*
    visible()
    ----------------
    Muestra el simbolo blanco como 'B' para que sea legible en pantalla

    Parametros:
    ----------------
    - c (char): simbolo a mostrar

    Return:
    ----------------
    - char: simbolo visible
    */

    return c == blanco ? 'B' : c;
}


void MaquinaTuring::registrarEstado(const std::string& e)
{
    /*
    registrarEstado()
    ----------------
    Agrega el estado a la lista de estados vistos si aun no estaba

    Parametros:
    ----------------
    - e (const std::string&): estado a registrar

    Return:
    ----------------

    */

    for (const std::string& x : estados)
        if (x == e) return;
    estados.push_back(e);
}


void MaquinaTuring::registrarSimbolo(char s)
{
    /*
    registrarSimbolo()
    ----------------
    Agrega el simbolo a la lista de simbolos vistos si aun no estaba

    Parametros:
    ----------------
    - s (char): simbolo a registrar

    Return:
    ----------------

    */

    for (char x : simbolos)
        if (x == s) return;
    simbolos.push_back(s);
}


std::vector<char> MaquinaTuring::columnasOrdenadas() const
{
    /*
    columnasOrdenadas()
    ----------------
    Devuelve los simbolos del alfabeto de cinta (Gamma) en orden ASCII pero con
    el simbolo blanco al final, de modo que la tabla quede como 0,1,X,Y,B

    Parametros:
    ----------------

    Return:
    ----------------
    - std::vector<char>: simbolos en orden ASCII 
    
    */

    std::vector<char> cols;
    for (char s : simbolos)
        if (s != blanco) cols.push_back(s);
    std::sort(cols.begin(), cols.end());
    cols.push_back(blanco);
    return cols;
}


void MaquinaTuring::imprimirTabla() const
{
    /*
    imprimirTabla()
    ----------------
    Imprime la definicion de la MT como 7-tupla T = (Q, Sigma, Gamma, delta,
    q_ini, B, F) con sus valores, y luego la tabla de la funcion de transicion

    Parametros:
    ----------------

    Return:
    ----------------

    */

    // Estados (Q) y simbolos de cinta (Gamma) ordenados.
    std::vector<std::string> filas = estados;
    std::sort(filas.begin(), filas.end());
    std::vector<char> cols = columnasOrdenadas();    
    std::vector<char> sig(sigma.begin(), sigma.end());
    std::sort(sig.begin(), sig.end());

    // Helpers para imprimir un conjunto: { a, b, c }
    auto unirStr = [](const std::vector<std::string>& v) {
        std::string s = "{";
        for (std::size_t i = 0; i < v.size(); i++) s += (i ? ", " : " ") + v[i];
        s += v.empty() ? "}" : " }";
        return s;
    };
    auto unirChar = [this](const std::vector<char>& v) {
        std::string s = "{";
        for (std::size_t i = 0; i < v.size(); i++)
            s += (i ? std::string(", ") : std::string(" ")) +
                  std::string(1, visible(v[i]));
        s += v.empty() ? "}" : " }";
        return s;
    };

    std::vector<std::string> Fv(aceptacion.begin(), aceptacion.end());

    // Def formal
    printf("T = (Q, Sigma, Gamma, delta, q_ini, B, F)\n");
    printf("  Q      = %s\n", unirStr(filas).c_str());
    printf("  Sigma  = %s\n", unirChar(sig).c_str());
    printf("  Gamma  = %s\n", unirChar(cols).c_str());
    printf("  q_ini  = %s\n", inicial.c_str());
    printf("  B      = %c\n", visible(blanco));
    printf("  F      = %s\n\n", unirStr(Fv).c_str());

    // delta
    printf("Tabla de transiciones:\n");
    printf("%s\n", std::string(71, '-').c_str());

    // hdr
    printf("  delta |");
    for (char s : cols)
        printf("   %c        ", visible(s));
    printf("\n");
    printf("--------+%s\n", std::string(62, '-').c_str());

    // filas
    for (const std::string& e : filas) {
        std::string etiqueta = (esAceptacion(e) ? "*" : 
                                esInicial(e) ? "->" : "") + e;
        printf("  %-5s |", etiqueta.c_str());
        for (char s : cols) {
            auto it = delta.find({e, s});
            if (it == delta.end())
                printf("    -       ");
            else {
                const Transicion& t = it->second;
                printf(" (%s,%c,%c)  ", t.destino.c_str(), visible(t.escribe),
                       (t.mueve == Mov::R ? 'R' : 'L'));
            }
        }
        printf("\n");
    }
    printf("%s\n", std::string(71, '-').c_str());

}


void MaquinaTuring::imprimirPaso(int paso, 
                                 const std::string& estado,
                                 const Cinta& cinta) const
{
    /*
    imprimirPaso()
    ----------------
    Imprime la descripcion instantanea (ID) de la configuracion actual como se
    define en el hmu: e estado se escribe en la cinta, justo a la izquierda
    del simbolo bajo la cabeza (alfa q beta)...
    Se usan orchetes para delimitar el estado ara no confundir con los simbolos
    de la cinta 
    
    Parametros:
    ----------------
    - paso   (int): numero de paso actual
    - estado (const std::string&): estado actual de la MT
    - cinta  (const Cinta&): cinta actual de la MT

    Return:
    ----------------

    */

    std::string cintaTxt = cinta.contenido();
    int h = cinta.posicion();

    // ID = parte a la izquierda de la cabeza + [estado] + parte desde la cabeza
    std::string id = cintaTxt.substr(0, h) + "[" + estado + "]" + 
                     cintaTxt.substr(h);

    printf("Paso %s |- %s\n", pad(std::to_string(paso), 3).c_str(), id.c_str());
}


bool MaquinaTuring::run(const std::string& entrada) const
{
    /*
    run()
    ----------------
    Ejecuta la MT sobre la entrada, imprimiendo cada configuracion y esperando
    un Enter antes de aplicar cada transicion, hasta que acepta, se queda sin
    transicion o se excede el tope de pasos

    Parametros:
    ----------------
    - entrada (const std::string&): cadena de entrada

    Return:
    ----------------
    - bool: true si la cadena es ACEPTADA, false si es RECHAZADA
    */

    Cinta cinta(entrada, blanco);
    std::string estado = inicial;
    int paso = 0;

    printf("%s\n", std::string(71, '=').c_str());
    printf("Simulando entrada: \"%s\"\n",
           entrada.empty() ? "(cadena vacia)" : entrada.c_str());
    printf("%s\n", std::string(71, '=').c_str());

    while (paso < kMaxPasos) {
        imprimirPaso(paso, estado, cinta);

        if (esAceptacion(estado)) {
            printf("--> Se alcanzo un estado de aceptacion (%s)\n",
                   estado.c_str());
            printf("RESULTADO: ACEPTADA\n\n");
            return true;
        }

        char leido = cinta.leer();
        auto it = delta.find({estado, leido});
        if (it == delta.end()) {
            printf("--> No hay transicion para (%s, %c) FIN\n",
                   estado.c_str(), visible(leido));
            printf("RESULTADO: RECHAZADA\n\n");
            return false;
        }

        pausa();

        const Transicion& t = it->second;
        printf("           delta(%s, %c) = (%s, %c, %c)\n",
               estado.c_str(), visible(leido), t.destino.c_str(),
               visible(t.escribe), (t.mueve == Mov::R ? 'R' : 'L'));

        cinta.escribir(t.escribe);
        cinta.mover(t.mueve);
        estado = t.destino;
        paso++;
    }

    printf("--> Se excedio el numero maximo de pasos (%d)\n"
           "END\n\n", kMaxPasos);
    return false;
}
