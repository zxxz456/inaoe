# Simulador de Árbol Binario genérico

Construye un árbol binario **sin orden** (no es un BST) insertando los
valores por nivel (BFS-fill, el primer hueco disponible) y muestra una
**animación interactiva en el navegador**. Una vez construido, la página
permite ejecutar **Insertar, Buscar, Eliminar (subárbol)** y los cuatro
recorridos clásicos: **Preorden, Inorden, Postorden y Por niveles**.

## Archivos
- `arbol_binario.py` - estructura base en Python: clases `NodoBinario` y
  `ArbolBinario`.
- `simulador_arbol_binario.py` - CLI que carga la plantilla, inyecta la
  secuencia inicial y genera/abre la animación HTML.
- `plantilla.html` - plantilla con todo el HTML/CSS/JS del simulador.
- `arbol_binario_animacion.html` - archivo generado (no editar a mano).

## Uso
```bash
# Árbol completo de 3 niveles
python3 simulador_arbol_binario.py 1 2 3 4 5 6 7
```
Los valores se insertan por nivel: el primero es la raíz, el segundo va a
la izquierda, el tercero a la derecha, y así sucesivamente.

### Opciones
- `--no-open` - solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` - ruta del HTML de salida.

## Operaciones interactivas (en la página)
- **Insertar** - coloca el valor en el primer hueco libre (BFS-fill).
- **Buscar** - recorre en profundidad (preorden) comparando con el valor.
- **Eliminar subárbol** - busca el nodo y, si lo encuentra, lo borra junto
  con todos sus descendientes.
- **Preorden / Inorden / Postorden / Por niveles** - recorridos animados,
  resaltando cada nodo en el momento que se visita.
- **Reiniciar** - reconstruye el árbol con la secuencia inicial.

## Controles de reproducción
Idénticos a los demás simuladores (controles de paso a paso, play/pausa,
velocidad regulable, flechas y barra espaciadora).

## Colores
- Azul: nodo normal · Amarillo: visitando · Verde: nuevo o resultado · Cian:
  encontrado · Rojo: nodo o subárbol que se va a eliminar.
