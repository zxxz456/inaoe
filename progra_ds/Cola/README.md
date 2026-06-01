# Simulador de Cola (Queue, FIFO)

Construye una cola encolando una secuencia de valores y muestra una
**animación interactiva en el navegador**. Una vez construida, la misma página
permite ejecutar **Enqueue, Dequeue, Peek, Buscar y Recorrer**, cada
operación con su propia animación paso a paso.

## Archivos
- `cola.py` — estructura base en Python: clase `Cola` (basada en `deque`).
- `simulador_cola.py` — CLI que carga la plantilla, inyecta la secuencia
  inicial y genera/abre la animación HTML.
- `plantilla.html` — plantilla con todo el HTML/CSS/JS del simulador. Aquí
  vive la lógica de las operaciones, reflejada en JavaScript porque la
  interacción ocurre en el navegador.
- `cola_animacion.html` — archivo generado por el script (no editar a mano).

## Uso
```bash
python3 simulador_cola.py 1 2 3 4 5
```
Los valores se encolan en el orden dado: el primero (1) queda en el FRENTE
y el último (5), en el FONDO.

### Opciones
- `--no-open` — solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` — guarda el HTML en una ruta concreta
  (por defecto: `cola_animacion.html` en el directorio actual).

## Operaciones interactivas (en la página)
- **Enqueue** — agrega el valor al final (fondo).
- **Dequeue** — retira el elemento del frente.
- **Peek** — resalta el frente sin modificar la cola.
- **Buscar** — recorre desde el frente hacia el fondo comparando con el
  valor; marca el primer hallazgo o avisa si no está.
- **Recorrer** — visita todos los elementos del frente al fondo.
- **Reiniciar** — reconstruye la cola con la secuencia inicial.

## Controles de reproducción
- **⏮ / ◀ / ▶ / ⏭** — inicio, anterior, siguiente, fin.
- **▶ Reproducir / Pausa** — animación automática.
- **Barra de velocidad** — regula el ritmo.
- **Teclado** — flechas ← → para avanzar/retroceder, barra espaciadora para
  reproducir/pausar, Enter en la casilla para hacer Enqueue.

## Colores
- Azul: elemento normal · Amarillo: comparando / visitando · Verde: nuevo o
  resultado · Cian: encontrado o frente · Rojo: elemento que se retirará.
