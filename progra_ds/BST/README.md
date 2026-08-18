# Simulador de Árbol Binario de Búsqueda (BST)

Construye un BST insertando una secuencia de valores y muestra una
**animación interactiva en el navegador**. Una vez construido, la misma página
permite **insertar, buscar y eliminar** valores nuevos, cada operación con su
propia animación paso a paso.

## Archivos
- `bst.py` - estructura base en Python: clases `TreeNode` y
  `BinarySearchTree` (inserción).
- `simulador_bst.py` - recibe los valores por argumento, carga la plantilla,
  inserta la secuencia inicial y genera/abre la animación HTML.
- `plantilla.html` - plantilla con todo el HTML/CSS/JS del simulador. El
  marcador `__KEYS__` se sustituye por la secuencia inicial. Aquí vive la
  lógica de inserción, búsqueda y eliminación (los 3 casos: hoja, un hijo y
  dos hijos/sucesor), reflejada en JavaScript porque las operaciones
  interactivas se ejecutan en el navegador.
- `bst_animacion.html` - archivo generado por el script (no editar a mano).

## Uso
```bash
python3 simulador_bst.py 50 30 70 20 40 60 80 10 25
```
Los valores se insertan en el orden dado. Se interpretan como enteros si es
posible; si no, como texto (no se pueden mezclar números y texto).

### Opciones
- `--no-open` - solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` - guarda el HTML en una ruta concreta
  (por defecto: `bst_animacion.html` en el directorio actual).

```bash
python3 simulador_bst.py 8 3 10 1 6 14 4 7 13 -o arbol.html --no-open
```

## Operaciones interactivas (en la página)
Arriba del árbol hay una casilla de texto y cuatro botones:
- **Insertar** - agrega el valor escrito, animando el camino de inserción.
- **Buscar** - recorre el árbol mostrando las comparaciones; resalta el nodo
  si lo encuentra (cian) o avisa si no está.
- **Eliminar** - borra el valor: anima la búsqueda y luego el caso que
  corresponda (hoja, un hijo, o dos hijos buscando el sucesor).
- **Reiniciar** - reconstruye el árbol con la secuencia inicial.

(El valor puede ser número o texto; se interpreta como número si es válido.)

## Controles de reproducción
- **⏮ / ◀ / ▶ / ⏭** - inicio, anterior, siguiente, fin.
- **▶ Reproducir / Pausa** - animación automática.
- **Barra de velocidad** - regula el ritmo.
- **Teclado** - flechas ← → para avanzar/retroceder, barra espaciadora para
  reproducir/pausar, Enter en la casilla para buscar.

## Colores
- Azul: nodo normal · Amarillo: comparando / camino · Verde: nuevo o resultado
  final · Cian: encontrado en una búsqueda · Rojo: nodo que se va a eliminar.
