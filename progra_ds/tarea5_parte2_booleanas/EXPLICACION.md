# Explicación

**Lineas 57-65** — Decidi usar macros pq es mas legible y entendible el codigo, NOT_VAR es para decir si un nodo es una variable o un operador

**Linea 72-77** — Decidi usar esa estructura pq, a falta de poder usar objetos como en c++, lo cual facilitaria mnucho las cosas, use un struct. En ese struct necesitamos almacenar dos tipos de """"objetos"""", la variable y el operador, en lugar de hacer dos tipos de nodos, lo cual haria las cosas mas enredosas, use uno generico para ambos

**Linea 81-106** — Nada del otro mundo, funcion estandar para la creacaion de nodos

**Linea 109-181** — ES la funcion de construir. El prototipo se tomo tal cual la definicion dada en la tarea. Recibe los tokens q son un arreglo de "a", "b", "or" y asi, variables y operadores y el tamano... Ahora lo interesante es el como se agregan.

Tenemos una pila/stack, aqui se iran guardando mientras procesamos cada token, por que decidi usar pila? Lo decia el enunciado y ademas es muy parecido al ejercicio de calculadora postfija.

Se consume token del array de tokens, se procesa, si es una variable se apila, si es un operador se desapila y se guarda en el hijo derecho y luego el izquierdo, esto es importante pq respeta el orden de las operaciones, y el nodo creado es el que tiene tipo operador y los hijos son simples vars... Este proceso se repite y se repite hasta haber consumido todo el array de tokens y al final en la pila queda el root del arbol con todos los subarboles que se fueron construyendo en el camino

**Lineas 184-215** — Se corresponde a la funcion de evaluar, nada complejo, solo se evalua recursivamente el arbol y se van combinando los resultados. Por que use recursividad? Pues pq es un arbol, son re buenos para recursividad por la misma estructura.

**Linea 219-241** — FUncion auxiliar para imprimir nodo, nada que exlicar a detalle

**Linea 243-309** — FUnciones de recorridos, nada profundo que explicar, solo se llaman recursivamente en diferentes ordenes

**Linea 313-334** — Funcion auxiliar paea liberar

**Linea 341-378** — Dummy main para probar
