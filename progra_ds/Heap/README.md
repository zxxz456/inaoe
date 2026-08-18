# Simulador de Heap Binario

Construye un montículo binario (min-heap o max-heap) insertando una
secuencia de valores y muestra una **animación interactiva en el navegador**
con `bubble-up` al insertar y `bubble-down` al extraer la raíz. Una vez
construido, la misma página permite ejecutar **Insertar, Extraer, Peek,
Buscar y Recorrer (por niveles)**.

## Archivos
- `heap.py` - estructura base en Python: clase `Heap` con flag `es_min`.
- `simulador_heap.py` - CLI que carga la plantilla e inyecta valores y modo.
- `plantilla.html` - HTML/CSS/JS del simulador (lógica reflejada en JS).
- `heap_animacion.html` - archivo generado por el script (no editar a mano).

## Uso
```bash
# min-heap (la raíz queda en el menor)
python3 simulador_heap.py 5 3 8 1 9 4 7

# max-heap
python3 simulador_heap.py 5 3 8 1 9 4 7 --max
```

### Opciones
- `--max` - usa max-heap (por defecto: min-heap).
- `--no-open` - solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` - ruta del HTML de salida.

## Operaciones interactivas (en la página)
- **Insertar** - agrega al final del arreglo y reordena con bubble-up.
- **Extraer** - saca la raíz, mueve el último a la raíz y reordena con
  bubble-down.
- **Peek** - resalta la raíz sin modificar.
- **Buscar** - recorre linealmente el arreglo comparando con el valor.
- **Recorrer (por niveles)** - visita los nodos en el orden del arreglo
  (equivale a un recorrido por anchura).
- **Reiniciar** - reconstruye el heap con la secuencia inicial.

Debajo de la animación se muestra el **arreglo subyacente**, resaltado al
mismo ritmo que el árbol.

## Controles de reproducción
- **⏮ / ◀ / ▶ / ⏭** - inicio, anterior, siguiente, fin.
- **▶ Reproducir / Pausa** - animación automática.
- **Barra de velocidad** - regula el ritmo.
- **Teclado** - flechas ← → para avanzar/retroceder, espacio para
  reproducir/pausar, Enter en la casilla para insertar.

## Colores
- Azul: nodo normal · Amarillo: comparando · Verde: nuevo o intercambio
  hecho · Cian: encontrado / raíz · Rojo: nodo que se intercambia o se va a
  eliminar.
