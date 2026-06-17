/*
AVLtree.c
========================


Descripcion:
------------
Arbol binario interactivo de enteros con control de altura (estilo AVL). El
script inicial fue creado por el Dr. Miguel Morales Sandoval.
Se agregaron algunas cosas como la opcion de precargar arbol, mostrar el arbol
interactivamente con ramas y mostrar la altura de cada nodo con el arg -v.
Igualmente se agrego lo requerido para la actividad 
(recorridos pre/in/postorden)

Parametros:
    -tree v1,v2,... : precarga el arbol con los valores dados
    -v: verbose, muestra la altura de cada nodo entre parentesis

Metadata:
----------
* Author: Dr. Miguel Morales Sandoval
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       16/06/2026      Fixed bug en salir y en calculo de altura
zxxz6       16/06/2026      Implementacion de recorridos y args
zxxz6       16/06/2026      Implementacion de dosctrings y correccion de
                            visualizacion interactiva (showTree())
DR.MI       XX/XX/2026      Creation


*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MENU_STR "\n=== AVL TREE ===\n \
1. Insertar nodo\n2. Recorrido preorden\n3. \
Recorrido inorden\n4. Recorrido postorden\n\
Cualquier otra tecla para salir\nIngrese su opcion: "


// ########################### INICIO DE AVLTREE.C ############################

// Structs
typedef struct tree_node{
   int item;                   // valor almacenado en el nodo
   struct tree_node* left;     // puntero al hijo izquierdo
   struct tree_node* right;    // puntero al hijo derecho
   int height;                 // altura del subarbol con raiz en este nodo
}TreeNode;

// Lienzo de texto para dibujar el arbol vertical (lo arma buildDisplay)
typedef struct {
   char** lines;               // arreglo de lineas (cada una de 'width' chars)
   int height;                 // numero de lineas
   int width;                  // ancho en caracteres de cada linea
   int middle;                 // columna donde se centra la etiqueta de la raiz
}Display;


// Prototipos
TreeNode *newNode(int data);
void insert(TreeNode *node, TreeNode *new);
TreeNode *buildFromCSV(const char *csv);
int readFromKeyBoard();
int getHeight(TreeNode *parent);
void preorden(TreeNode *node);
void inorden(TreeNode *node);
void postorden(TreeNode *node);
void showTree(TreeNode *root, int verbose);
Display buildDisplay(TreeNode *node, int verbose);
char *makeLine(int width);
void limpiarPantalla(void);
void pausa(void);


// main
int main(int argc, char *argv[])
{
    /*
    main()
    ----------------
    Funcion principal: en cada vuelta limpia la consola, dibuja el arbol y
    muestra el menu. Segun la opcion inserta un nodo (1) o imprime un recorrido
    preorden/inorden/postorden (2/3/4). Cualquier otra tecla termina el programa

    Parametros:
    ----------------
    - argc (int): numero de argumentos de linea de comandos
    - argv (char*[]): vector de argumentos

    Return:
    ----------------
    - int: 0 al terminar
    */

    TreeNode *root = NULL;
    TreeNode *new = NULL;
    int ans;
    int verbose = 0;   // si se activa con -v

    // -tree v1,v2,... : precargar el arbol
    // -v: verbose, mostrar altura de cada nodo
    for (int i = 1; i < argc; i++)
    {
        const char *csv = NULL;
        if (strcmp(argv[i], "-tree") == 0 && i + 1 < argc)
            csv = argv[++i];               // forma:  -tree 1,2,3
        else if (strncmp(argv[i], "-tree=", 6) == 0)
            csv = argv[i] + 6;             // forma:  -tree=1,2,3
        else if (strcmp(argv[i], "-v") == 0)
            verbose = 1;                   // forma:  -v

        if (csv != NULL)
            root = buildFromCSV(csv);
    }

    do
    {
        // limpiar la consola y redibujar el estado actual del arbol
        limpiarPantalla();
        showTree(root, verbose);

        printf(MENU_STR);

        // bug fix de letras
        // scanf("%d", &ans);
        if (scanf("%d", &ans) != 1)
            break;

        switch (ans)
        {
            case 1:   // insertar un nodo nuevo
            {
                new = newNode(readFromKeyBoard());
                if (root == NULL)
                {
                    root = new;   // el primer nodo es la raiz
                    /*
                    Antes aqui se hacia "root->height += 1", pero no es correcto:
                    si solo existe la raiz, marcaria altura 1 cuando deberia ser
                    0 (la altura se mide en aristas)
                    */
                }
                else
                    insert(root, new);
                break;
            }

            case 2:   // recorrido preorden: raiz - izq - der
            {
                printf("\nRecorrido PREORDEN (raiz, izq, der):\n  ");
                if (root == NULL) printf("(arbol vacio)");
                else              preorden(root);
                printf("\n");
                pausa();
                break;
            }

            case 3:   // recorrido inorden: izq - raiz - der
            {
                printf("\nRecorrido INORDEN (izq, raiz, der):\n  ");
                if (root == NULL) printf("(arbol vacio)");
                else              inorden(root);
                printf("\n");
                pausa();
                break;
            }

            case 4:   // recorrido postorden: izq - der - raiz
            {
                printf("\nRecorrido POSTORDEN (izq, der, raiz):\n  ");
                if (root == NULL) printf("(arbol vacio)");
                else              postorden(root);
                printf("\n");
                pausa();
                break;
            }

            default:  // cualquier otra opcion: salir del bucle
                break;
        }
    }
    while (ans >= 1 && ans <= 4);

    limpiarPantalla();
    printf("Saliendo...\n");
    return 0;
}


// Operaciones del arbol AVL

TreeNode *newNode(int data)
{
    /*
    newNode()
    ----------------
    Reserva un nodo nuevo con malloc, guarda el dato y deja los dos hijos en
    NULL y la altura en 0 (una hoja no tiene aristas debajo; la altura se mide
    en numero de aristas)

    Parametros:
    - data (int): valor a guardar en el nodo

    Return:
    - TreeNode*: puntero al nodo nuevo, o NULL si fallo malloc
    */

    TreeNode *new = (TreeNode *)malloc(sizeof(TreeNode));

    if (new == NULL)
       return NULL;
    else
    {
        new -> item = data;
        new -> left = NULL;
        new -> right = NULL;
        new -> height = 0;
        return new;
    }

}

void insert(TreeNode *parent, TreeNode *new)
{
    /*
    insert()
    ----------------
    Inserta el nodo new bajo parent. Si un lado esta libre (altura 0) cuelga ahi
    el nodo; si ambos estan ocupados, baja recursivamente por el subarbol de
    MENOR altura para mantener el arbol balanceado. Al regresar de la recursion,
    recalcula la altura (en aristas) de cada nodo del camino: getHeight() cuenta
    nodos (NULL=0, hoja=1), por eso la altura en aristas es getHeight(nodo) - 1

    Parametros:
    - parent (TreeNode*): nodo desde donde se busca el hueco
    - new (TreeNode*): nodo a insertar

    Return:

    */
    int lh = getHeight(parent->left);
    int rh = getHeight(parent->right);

    if(lh == 0)
    {
        parent->left = new;
        printf("\n ...%d inserted at left of %d.\n",new->item,parent->item);
    }
    else if(rh == 0){
        parent->right = new;
         printf("\n ...%d inserted at right of %d.\n",new->item,parent->item);
    }
    else if (rh < lh)
      insert(parent->right, new);
    else
      insert(parent->left, new);

    parent->height = getHeight(parent) - 1;
    /*
    Se hacia esto pero eso solo funciona como un contador de nodos insertados
    que si, getHeight() devuelve la altura correcta pero igual podria causar
    bugs si no se nota. El nombre de la variable es claro por lo que deberia
    almacenar la altura del nodo, no un contador de inserciones :P

    parent->height += 1;
    */

}

TreeNode *buildFromCSV(const char *csv)
{
    /*
    buildFromCSV()
    ----------------
    Construye un arbol a partir de una cadena de enteros separados por comas
    (p. ej. "50,30,70,20"). El PRIMER valor se vuelve la raiz y los demas se
    insertan en orden con insert(). Los separadores no numericos (comas,
    espacios) se ignoran; acepta numeros negativos

    Parametros:
    - csv (const char*): valores separados por comas

    Return:
    - TreeNode*: raiz del arbol construido, o NULL si no habia ningun valor
    */
    TreeNode *root = NULL;
    const char *p = csv;

    while (*p != '\0')
    {
        char *end;
        long value = strtol(p, &end, 10);   // lee un entero y avanza 'end'

        if (end == p)   // aqui no habia numero (coma, espacio, etc.)
        {
            p++;        // avanzar un caracter para no quedarse atascado
            continue;
        }
        p = end;

        TreeNode *node = newNode((int) value);
        if (root == NULL)
            root = node;          // el primero es la raiz
        else
            insert(root, node);   // los demas se acomodan con insert()
    }

    return root;
}

int getHeight(TreeNode *parent)
{
    /*
    getHeight()
    ----------------
    Calcula la altura del subarbol con raiz en parent de forma recursiva: 0 si
    el nodo es NULL, o 1 mas la altura del subarbol hijo mas alto

    Parametros:
    - parent (TreeNode*): raiz del subarbol a medir

    Return:
    - int: altura del subarbol (numero de niveles)
    */
    if (parent == NULL)
        return 0;

    int lbh = getHeight(parent->left);
    int rbh = getHeight(parent->right);

    if (lbh > rbh)
        return 1 + lbh;
    else
        return 1 + rbh;
}

void preorden(TreeNode *node)
{
    /*
    preorden()
    ----------------
    Recorrido en PREORDEN: visita primero la raiz, luego el subarbol izquierdo y
    al final el derecho (raiz - izq - der). Imprime cada item separado por
    espacios

    Parametros:
    - node (TreeNode*): raiz del subarbol a recorrer

    Return:

    */
    if (node == NULL)
        return;

    printf("%d ", node->item);
    preorden(node->left);
    preorden(node->right);
}

void inorden(TreeNode *node)
{
    /*
    inorden()
    ----------------
    Recorrido en INORDEN: visita primero el subarbol izquierdo, luego la raiz y
    al final el derecho (izq - raiz - der). Imprime cada item separado por
    espacios

    Parametros:
    - node (TreeNode*): raiz del subarbol a recorrer

    Return:

    */
    if (node == NULL)
        return;

    inorden(node->left);
    printf("%d ", node->item);
    inorden(node->right);
}

void postorden(TreeNode *node)
{
    /*
    postorden()
    ----------------
    Recorrido en POSTORDEN: visita primero el subarbol izquierdo, luego el
    derecho y al final la raiz (izq - der - raiz). Imprime cada item separado
    por espacios

    Parametros:
    - node (TreeNode*): raiz del subarbol a recorrer

    Return:

    */
    if (node == NULL)
        return;

    postorden(node->left);
    postorden(node->right);
    printf("%d ", node->item);
}

void showTree(TreeNode *root, int verbose)
{
    /*
    showTree()
    ----------------
    Dibuja el arbol en consola. Se apoya en buildDisplay() para armar el
    "lienzo" de texto; aqui solo se imprime linea por linea y se libera la
    memoria. Si el arbol esta vacio lo indica

    Parametros:
    - root (TreeNode*): raiz del arbol a mostrar

    Return:

    */
    if (root == NULL){
        printf("\n(arbol vacio)\n");
        return;
    }

    Display d = buildDisplay(root, verbose);
    printf("\n");
    for (int i = 0; i < d.height; i++){
        printf("%s\n", d.lines[i]);
        free(d.lines[i]);          // liberar cada linea ya impresa
    }
    free(d.lines);
}


// Utilidades

int readFromKeyBoard()
{
    /*
    readFromKeyBoard()
    ----------------
    Pide un entero por teclado y lo devuelve

    Parametros:
    ----------------

    Return:
    ----------------
    - int: el entero leido
    */

    printf("\n Enter int: ");
    int data;
    scanf("%d", &data);
    return data;
}

void limpiarPantalla(void)
{
    /*
    limpiarPantalla()
    ----------------
    Limpia la pantalla de la terminal con codigos de escape ANSI: borra todo el
    contenido y manda el cursor al inicio. Misma utilidad usada en las otras
    actividades (Utils.h)

    Parametros:

    Return:

    */
    printf("\033[2J\033[H");
}

void pausa(void)
{
    /*
    pausa()
    ----------------
    Detiene la ejecucion hasta que el usuario presione ENTER, para que alcance a
    leer la salida (p. ej. un recorrido) antes de que el bucle limpie la
    pantalla. Primero descarta lo que quede en el buffer de entrada (el '\n' que
    deja scanf) y luego espera una nueva linea

    Parametros:

    Return:

    */
    int c;
    while ((c = getchar()) != '\n' && c != EOF)
        ;   // descartar el resto de la linea actual (incluye el '\n' de scanf)

    printf("\nPresione ENTER para continuar...");
    getchar();   // esperar el ENTER del usuario
}

Display buildDisplay(TreeNode *node, int verbose)
{
    /*
    buildDisplay()
    ----------------
    Construye recursivamente el "lienzo" (conjunto de lineas de texto) que
    representa el subarbol de nodo dibujado vertical y con aristas. Devuelve,
    ademas de las lineas, su ancho, su alto y la columna donde queda centrada la
    etiqueta de la raiz; ese centro lo usa el nivel de arriba para encajar los
    subarboles izquierdo y derecho y trazar las ramas '/' y '\'

    Es una adaptacion del algoritmo clasico de "pretty print" de arboles: cada
    subarbol se arma como un bloque y el padre los pega lado a lado, dejando la
    etiqueta en medio

    Parametros:
    - node (TreeNode*): raiz del subarbol a dibujar (no debe ser NULL)

    Return:
    - Display: lienzo con lines, height, width y middle
    */

    Display d;
    char label[32];
    snprintf(label, 
             sizeof(label), 
             verbose ? "%d (h=%d)" : "%d", 
             node->item, 
             node->height); //(h=%d)
    int u = (int) strlen(label);

    // Caso 1: hoja (sin hijos) -> el bloque es solo la etiqueta
    if (node->left == NULL && node->right == NULL)
    {
        d.lines = (char**) malloc(sizeof(char*) * 1);
        d.lines[0] = makeLine(u);
        memcpy(d.lines[0], label, u);
        d.height = 1;
        d.width  = u;
        d.middle = u / 2;
        return d;
    }

    // Caso 2: solo hijo izquierdo
    if (node->right == NULL)
    {
        Display L = buildDisplay(node->left, verbose);
        int n = L.width, p = L.height, x = L.middle;
        int width = n + u;

        char *first = makeLine(width);
        for (int i = 0; i < n - x - 1; i++) first[x + 1 + i] = '_';
        memcpy(first + n, label, u);

        char *second = makeLine(width);
        second[x] = '/';

        d.height = p + 2;
        d.width  = width;
        d.middle = n + u / 2;
        d.lines  = (char**) malloc(sizeof(char*) * d.height);
        d.lines[0] = first;
        d.lines[1] = second;
        for (int i = 0; i < p; i++)
        {
            char *line = makeLine(width);
            memcpy(line, L.lines[i], n);       // subarbol izq pegado a la izq
            d.lines[2 + i] = line;
            free(L.lines[i]);
        }
        free(L.lines);
        return d;
    }

    // Caso 3: solo hijo derecho
    if (node->left == NULL)
    {
        Display R = buildDisplay(node->right, verbose);
        int m = R.width, q = R.height, y = R.middle;
        int width = u + m;

        char *first = makeLine(width);
        memcpy(first, label, u);
        for (int i = 0; i < y; i++) first[u + i] = '_';

        char *second = makeLine(width);
        second[u + y] = '\\';

        d.height = q + 2;
        d.width  = width;
        d.middle = u / 2;
        d.lines  = (char**) malloc(sizeof(char*) * d.height);
        d.lines[0] = first;
        d.lines[1] = second;
        for (int i = 0; i < q; i++)
        {
            char *line = makeLine(width);
            memcpy(line + u, R.lines[i], m);   // subarbol der pegado a la der
            d.lines[2 + i] = line;
            free(R.lines[i]);
        }
        free(R.lines);
        return d;
    }

    // Caso 4: dos hijos -> se pegan el bloque izq, la etiqueta y el bloque der
    Display L = buildDisplay(node->left, verbose);
    Display R = buildDisplay(node->right, verbose);
    int n = L.width, p = L.height, x = L.middle;
    int m = R.width, q = R.height, y = R.middle;
    int width = n + u + m;

    char *first = makeLine(width);
    for (int i = 0; i < n - x - 1; i++) first[x + 1 + i] = '_';// rama izq
    memcpy(first + n, label, u);                               // etiqueta al c
    for (int i = 0; i < y; i++) first[n + u + i] = '_';        // rama der

    char *second = makeLine(width);
    second[x] = '/';
    second[n + u + y] = '\\';

    int maxh = (p > q) ? p : q;
    d.height = maxh + 2;
    d.width  = width;
    d.middle = n + u / 2;
    d.lines  = (char**) malloc(sizeof(char*) * d.height);
    d.lines[0] = first;
    d.lines[1] = second;
    for (int i = 0; i < maxh; i++)
    {
        char *line = makeLine(width);
        if (i < p) memcpy(line, L.lines[i], n);          // izq a la izquierda
        if (i < q) memcpy(line + n + u, R.lines[i], m);  // der a la derecha
        d.lines[2 + i] = line;                           // el centro queda empt
    }
    for (int i = 0; i < p; i++) free(L.lines[i]);
    free(L.lines);
    for (int i = 0; i < q; i++) free(R.lines[i]);
    free(R.lines);
    return d;
}

char *makeLine(int width)
{
    /*
    makeLine()
    ----------------
    Reserva una linea de texto de 'width' caracteres rellena de espacios y
    terminada en '\0'. Sirve como lienzo en blanco sobre el que buildDisplay()
    coloca etiquetas y aristas

    Parametros:
    - width (int): numero de caracteres de la linea

    Return:
    - char*: cadena de width espacios (con su terminador)
    */
    char *line = (char*) malloc(width + 1);
    memset(line, ' ', width);
    line[width] = '\0';
    return line;
}

// ########################### FIN DE AVLTREE.C ################################
// #############################################################################
