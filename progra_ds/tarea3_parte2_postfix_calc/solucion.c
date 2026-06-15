/*
solucion.c
========================


Descripcion:
------------
Calculadora de notacion posfija. IMplementa las funciones requeridas

    int aplicar_operador(int a, int b, char op)
    int evaluar_posfijo(const char *expresion)

La evaluacion se hace con una PILA (Stack, LIFO) de enteros sobre lista ligada,
la misma estructura vista en clase: cada numero leido se APILA; al leer un
operador se DESAPILAN sus dos operandos (primero b, luego a, porque el orden
importa), se aplica el operador y el resultado se vuelve a apilar. Al terminar,
en la cima queda el resultado de toda la expresion

NOTAS IMPORTANTES:
1) REUTILICE EL NODO Y PILA
2) NO SEGUI EL FORMATO QUE ACOSTUMBRO DEBIDO A QUE PUEDE SER MAS DIFICIL PARA 
   EJECUTAR EL TENER MAS DE UN ARCHIVO, ASIQ UE TRATE DE INCLUIR TODO EN 
   ESTE ARCHIVO


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       14/06/2026      Creation


*/

#include <stdio.h>
#include <stdlib.h>

// ########################### INICIO DE SOLUCION.C ############################

// Structs
typedef struct nodo {
    int dato;                 // valor almacenado en el nodo
    struct nodo* siguiente;   // puntero al siguiente nodo
} Nodo;

typedef struct {
    Nodo* cima;               // nodo de tope (push - pop)
    int tam;                  // numero de elementos en la pila
} Pila;


// Operaciones de la pila
static void pilaInit(Pila* pila)
{
    /*
    pilaInit()
    ----------------
    Deja la pila vacia: sin nodos y con tam en 0. Hay que llamarla antes de
    usar la pila, porque una Pila recien declarada tiene basura.

    Parametros:
    - pila (Pila*): pila a inicializar

    Return:

    */
    pila->cima = NULL;
    pila->tam = 0;
}


static int apilar(Pila* pila, int dato)
{
    /*
    apilar()  (push)
    ----------------
    Crea un nodo nuevo y lo pone ARRIBA de la pila (como nueva cima)

    Parametros:
    - pila (Pila*): pila donde se mete
    - dato (int): valor a guardar

    Return:
    - int: 1 si lo apilo, 0 si fallo malloc
    */

    Nodo* nuevo = (Nodo*) malloc(sizeof(Nodo));
    if (nuevo == NULL) return 0;   // no hay memoria
    nuevo->dato = dato;

    // el nuevo apunta a la antigua cima y pasa a ser la cima
    nuevo->siguiente = pila->cima;
    pila->cima = nuevo;

    pila->tam++;
    return 1;
}


static int desapilar(Pila* pila, int* salida)
{
    /*
    desapilar()  (pop)
    ----------------
    Saca el nodo de ARRIBA 

    Parametros:
    - pila (Pila*): pila de donde se saca
    - salida (int*): donde se escribe el dato sacado (si habia)

    Return:
    - int: 1 si saco un elemento, 0 si la pila estaba vacia
    */

    if (pila->cima == NULL) return 0;   // pila vacia

    Nodo* tmp = pila->cima;
    if (salida != NULL) *salida = tmp->dato;

    pila->cima = tmp->siguiente;        // bajar la cima al siguiente
    free(tmp);
    pila->tam--;
    return 1;
}


static void pilaLiberar(Pila* pila)
{
    /*
    pilaLiberar()
    ----------------
    Recorre la pila liberando cada nodo con free y la deja vacia

    Parametros:
    - pila (Pila*): pila a liberar

    Return:

    */

    Nodo* aux = pila->cima;
    while (aux != NULL) {
        Nodo* siguiente = aux->siguiente;   // guardar antes de liberar
        free(aux);
        aux = siguiente;
    }
    pila->cima = NULL;
    pila->tam = 0;
}


// Auxiliares para leer la expresion

static int esEspacio(char c)
{
    /*
    esEspacio()
    ----------------
    Indica si un caracter es un separador en blanco (espacio, tabulador o salto
    de linea)

    Parametros:
    - c (char): caracter a revisar

    Return:
    - int: 1 si es espacio en blanco, 0 si no
    */
    return (c == ' ' || c == '\t' || c == '\n' || c == '\r');
}


// Funciones de solucion (lo q se pide)

int aplicar_operador(int a, int b, char op)
{
    /*
    aplicar_operador()
    ----------------
    Aplica un operador binario sobre dos enteros. El orden importa: para resta y
    div se calcula a (op) b.

    Parametros:
    - a (int): operando izquierdo
    - b (int): operando derecho
    - op (char): uno de '+', '-', '*', '/'

    Return:
    - int: resultado de a op b (0 si el operador no se reconoce)
    */

    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
        default:  return 0;
    }
}


int evaluar_posfijo(const char *expresion)
{
    /*
    evaluar_posfijo()
    ----------------
    Evalua una expresion en notacion posfija. Los tokens (numeros y operadores)
    van separados por espacios. Recorre la cadena de izquierda a derecha:
      - numero  -> se apila
      - operador-> se desapila b, luego a, se aplica op y se apila el resultado
    Al final, la cima de la pila es el resultado de toda la expresion

    NO AGREGUE SANITY CHECKS PQ SE ASUME QUE LA EXPRESION ES CORRECTA

    Parametros:
    - expresion (const char*): expresion posfija, p. ej. "2 3 + 4 *"

    Return:
    - int: resultado entero de la expresion
    */
    Pila pila;
    int resultado = 0;
    const char *c = expresion;

    pilaInit(&pila);

    while (*c != '\0') {
        // saltamos espacios
        if (esEspacio(*c)) {
            c++;
            continue;
        }

        // numero: un digito, o un '-' seguido de digito (numero negativo)
        if ((*c >= '0' && *c <= '9') ||
            (*c == '-' && (*(c + 1) >= '0' && *(c + 1) <= '9'))) {

            int signo = 1;
            if (*c == '-') {
                signo = -1;
                c++;
            }

            int numero = 0;
            // construimos numero
            while (*c >= '0' && *c <= '9') {
                numero = numero * 10 + (*c - '0');
                c++;
            }
            apilar(&pila, signo * numero);

        } else {
            // operador: desapilar b, luego a (el orden importa)
            char op = *c;
            int b = 0, a = 0;
            desapilar(&pila, &b);
            desapilar(&pila, &a);
            apilar(&pila, aplicar_operador(a, b, op));
            c++;
        }
    }

    // la cima es el resultado; se saca y se libera lo que quede en la pila
    desapilar(&pila, &resultado);
    pilaLiberar(&pila);

    return resultado;
}

// main
#ifndef MODO_TEST
int main(void)
{
    const char *ejemplo = "2 3 + 4 *";            
    printf("%s = %d\n", ejemplo, evaluar_posfijo(ejemplo));
    ejemplo = "5 1 2 + 4 * + 3 -";                
    printf("%s = %d\n", ejemplo, evaluar_posfijo(ejemplo));
    ejemplo = "100 10 / 5 +";                    
    printf("%s = %d\n", ejemplo, evaluar_posfijo(ejemplo));
    ejemplo = "20 6 / 1 +";               
    printf("%s = %d\n", ejemplo, evaluar_posfijo(ejemplo));
    ejemplo = "3 5 - 4 *";                        
    printf("%s = %d\n", ejemplo, evaluar_posfijo(ejemplo));
    return 0;
}
#endif

// ########################### FIN DE SOLUCION.C ###############################
// #############################################################################
