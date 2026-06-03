/*
UUID.h
========================


Descripcion:
------------
Generador de identificadores con formato 2-mm-yy-id
Ejemplo: 2-09-16-00001


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/06/2026      Creation


*/

#ifndef UUID_H
#define UUID_H

#include <string>
#include <ctime>
#include <cstdio>

class UUID {
    // Solo una instancia de UUID en todo el sistema (o sea singleton), es
    // accesible de manera golbal.

    public:
        // Devuelve siempre la misma instancia (singleton)
        static UUID& getInstance()
        {
            static UUID instancia;
            return instancia;
        }

        // Prohibimos copiar/asignar para que no se pueda duplicar la instancia
        UUID(const UUID&) = delete;
        UUID& operator=(const UUID&) = delete;

        // Generar un nuevo UUID con formato 2-mm-yy-id
        const char* generar(int prefijo = 2)
        {
            /*
            generar()
            ----------------
            Metodo que genera un nuevo UUID con formato 2-mm-yy-id

            Parametros:
            ----------------
            - prefijo (int): un numero entero que se coloca al inicio del UUID

            Return:
            ----------------
            - resultado (char*): Puntero a char que representa el UUID generado
            */

            // Se incrementa el contador (instancia global)
            contador++;
            char buffer[32];

            // Fecha actual del sistema
            std::time_t t = std::time(nullptr);
            std::tm* fecha = std::localtime(&t);

            // Obtener mes y año
            int mes  = fecha->tm_mon + 1;              
            int year = (fecha->tm_year + 1900) % 100;

            // Formatear el UUID en el buffer
            snprintf(buffer, 
                     sizeof(buffer), 
                     "%d-%02d-%02d-%05d",
                     prefijo, 
                     mes, 
                     year, 
                     contador);

            resultado = buffer;
            return resultado.c_str();
        }

    private:
        // Constructor privado: nadie mas puede crear instancias de UUID
        UUID() : contador(0) {}
        ~UUID(){};

        int contador;            // estado persistente del singleton
        std::string resultado;   // la uuid con formato 2-mm-yy-id 
};

#endif // UUID_H

// ########################### FIN DE UUID.H ###################################
// #############################################################################
