# Árbol con control de altura (estilo AVL, en C)

Actividad 3 de la segunda parte del curso propedéutico de **Programación y
Estructuras de Datos** (Dr. Miguel Morales Sandoval).

La actividad consiste en tomar el código base (un árbol binario interactivo que solo
insertaba) e implementar los tres recorridos: preorden, inorden y postorden.


## Cosas implementadas

- Los tres recorridos (pre/in/postorden) — lo pedido.
- El árbol se dibuja vertical y con aristas, y se actualiza en cada inserción.
- Arreglé dos bugs del original: el menú se colgaba al salir con una tecla no numérica, y la altura se calculaba como un contador en vez de la altura real. Esos estan fixed

## Parámetros

- `-tree v1,v2,...` — precarga el árbol (el primero es la raíz). También `-tree=v1,v2,...`.
- `-v` — muestra la altura de cada nodo, p. ej. `50 (h=2)`.

## Compilar y correr

```bash
gcc -std=c11 -Wall -Wextra AVLtree.c -o AVLtree
./AVLtree -tree 50,30,70,20,60


             ___50 (h=2)____________    
            /                       \   
     ___30 (h=1)             ___70 (h=1)
    /                       /           
20 (h=0)                60 (h=0)        

=== AVL TREE ===
 1. Insertar nodo
2. Recorrido preorden
3. Recorrido inorden
4. Recorrido postorden
Cualquier otra tecla para salir
Ingrese su opcion: 

```
