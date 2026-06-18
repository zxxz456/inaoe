/*
solucion_Bryan_Violante_Arriaga.c
===========================


Descripcion:
------------
Solucion de tarea 3 del curso propedeutico para ingreso a maestria en ciencias 
de la computacion. La tarea consiste en implementar dos funciones pa arboles
binarios


Metadata:
----------
* Author: zxxz6
* Version: 1.0.01


History:
------------
Author      Date            Description
zxxz6       17/06/2026      Creation


*/

#include <stdlib.h>


// ########################### INICIO DE SOLUCION ##############################

// Structs
// Este etruct se saco tal cual de las instrucciones del classroom
typedef struct nodo {
   int valor;                                     // valor almacenado en el nodo
   struct nodo *izq;                              // puntero al hijo izquierdo
   struct nodo *der;                              // puntero al hijo derecho
   int lvl;                                       // profundidad del nodo
}Nodo;


// Operaciones del arbol

static int contar_nodos(Nodo* r)
{
    /*
    contar_nodos()
    ----------------
    Cuenta los nodos tiene el subarbol con raiz en r (recursivo)

    Parametros:
    - r (Nodo*): raiz del subarbol a contar_nodos

    Return:
    - int: numero de nodos del subarbol
    */

    return (r == NULL) ? 0 : 1 + contar_nodos(r->izq) + contar_nodos(r->der);
}

Nodo *insertar(Nodo* groot, int val)
{
    /*
    insertar()
    ----------------
    Funcion para insertar un nuevo nodo. La insersion se hace por niveles, o sea
    primero se llena un nivel antes de insertar en el siguiente y, siempre
    se llena el mas izquierdo primerpo y despues el mas derecho (como el 
    ejemplo de la clase)

    Parametros:
    ----------------
    - groot (Nodo*): apuntador a la raiz del arbol
    - val (int): valor a insertar

    Return:
    ----------------
    - Nodo*: apuntador a la raiz del arbol (despues de insertar)
    */

    // Se crea nodo nuevo
    Nodo *nuevo = malloc(sizeof *nuevo);
    nuevo->valor = val;
    nuevo->izq = NULL;
    nuevo->der = NULL;
    nuevo->lvl = 0;

    // Arbol vacio
    if (groot == NULL) return nuevo;

    // Numerdo de nodos en el arbol
    int n = contar_nodos(groot);

    // Arreglo de apuntadores a nodo, tiene tamano n+1 para poder meter todos 
    // los nodos del arbol, es basicamente una cola
    Nodo **Q = malloc((size_t)(n + 1) * sizeof(*Q));
    int frente = 0, fin = 0;

    Q[fin++] = groot;                            // metemos a la cola el root

    while (frente < fin)
    {
        Nodo *act = Q[frente++];                // desencolar el nodo actual
        
        // Checamos si se puede meter x la izquierda
        if (act->izq == NULL)                   // Encontrramos hueco, mete
        {
            nuevo->lvl = act->lvl + 1;
            act->izq = nuevo;
            break;
        }
        Q[fin++] = act->izq;                    // si no, encolar el izquierdo

        // Checamos si se puede meter x la derecha
        if (act->der == NULL)                   // Encontramos hueco, mete nodo
        {
            nuevo->lvl = act->lvl + 1;
            act->der = nuevo;
            break;
        }
        Q[fin++] = act->der;                    // si no, encolar el derecho
    }

    free(Q);
    return groot;
}

Nodo *construir(const int* pre, const int* in, int n)
{
    /*
    construir()
    ----------------
    Reconstruye un arbol a partir de sus recorridos pre/in orden, los arrays
    son de tamano n 

    Parametros:
    - pre (const int*): recorrido en preorden (arrays de int)
    - in (const int*): recorrido en inorden (array de int)
    - n (int): numero de nodos (longitud de pre/in)

    Return:
    - Nodo*: raiz del arbol reconstruido
    */

    // caso base
    if (n <= 0) return NULL;

    // la raiz es el primer elemento del preorden
    Nodo* groot = malloc(sizeof(*groot));

    // En el recorrido preorden, el primer elemento siempre es la raiz del arbol
    // por lo que no hay pierde, solo lo tomamos y ya conocmos la raiz
    groot->valor = pre[0];

    // Ahora, ya conocemos la raiz... El recorrido in orden nos dice como se
    // estructura el arbil, ya que la raiz aparecera a la mitad del recorrido y,
    // lo que este a la izquierda es lo que hay en el subarbol izquierdo y lo q
    // este ala derecha es lo que hay en el subarbol derecho.
    // Entonses ahora lo que se hace es buscar el index de la raiz en el inorden
    // para splitear los arrays
    int idx = 0;
    while ((idx < n) && (in[idx] != pre[0])) // Mientras haya elementos q checar
        idx++;                               // y no hayamos encontrado la raiz

    // Construimos los subarboles
    groot->izq = construir(pre + 1, in, idx);
    groot->der = construir(pre + 1 + idx, in + idx + 1, n - idx - 1);

    return groot;
}

// ########################### FIN DE SOLUCION #################################
// #############################################################################
