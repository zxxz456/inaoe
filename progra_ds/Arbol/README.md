# Simulador de Árbol n-ario (general)

Construye un árbol n-ario indicando para cada nodo cuál es su padre, y
muestra una **animación interactiva en el navegador**. Cada nodo puede
tener cualquier cantidad de hijos. La página permite ejecutar **Insertar
(con padre), Buscar, Eliminar (subárbol)** y los recorridos **Preorden,
Postorden y Por niveles**.

## Archivos
- `arbol.py` — estructura base en Python: clases `NodoNario` y `ArbolNario`.
- `simulador_arbol.py` — CLI que parsea las operaciones, carga la
  plantilla y genera/abre la animación HTML.
- `plantilla.html` — plantilla con todo el HTML/CSS/JS del simulador.
- `arbol_animacion.html` — archivo generado (no editar a mano).

## Uso
El primer argumento es la **raíz** y los siguientes son pares
`padre:hijo`:

```bash
python3 simulador_arbol.py A A:B A:C B:D B:E C:F
```

Produce:
```
        A
       / \
      B   C
     /\    \
    D  E    F
```

### Opciones
- `--no-open` — solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` — ruta del HTML de salida.

## Operaciones interactivas (en la página)
En el campo de texto:
- Si el árbol está vacío y escribes un valor (sin `:`), se vuelve la raíz.
- Si ya hay árbol, usa `padre:hijo` para colgar `hijo` del `padre`.

- **Insertar** — agrega un hijo a un padre existente (o crea la raíz).
- **Buscar** — recorre en profundidad (preorden) comparando con el valor.
- **Eliminar subárbol** — busca el nodo y borra todo su subárbol.
- **Preorden / Postorden / Por niveles** — recorridos animados.
- **Reiniciar** — reconstruye el árbol con la estructura inicial.

Para buscar o eliminar basta con escribir el valor (sin la parte `padre:`).

## Controles de reproducción
Idénticos a los demás simuladores (paso a paso, play/pausa, velocidad,
flechas y barra espaciadora).

## Colores
- Azul: nodo normal · Amarillo: visitando · Verde: nuevo o resultado · Cian:
  encontrado · Rojo: nodo o subárbol que se va a eliminar.
