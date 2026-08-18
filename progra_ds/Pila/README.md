# Simulador de Pila (Stack, LIFO)

Construye una pila apilando una secuencia de valores y muestra una
**animación interactiva en el navegador**. Una vez construida, la misma página
permite ejecutar **Push, Pop, Peek, Buscar y Recorrer**, cada operación con
su propia animación paso a paso.

## Archivos
- `pila.py` - estructura base en Python: clase `Pila`.
- `simulador_pila.py` - CLI que carga la plantilla, inyecta la secuencia
  inicial y genera/abre la animación HTML.
- `plantilla.html` - plantilla con todo el HTML/CSS/JS del simulador. Aquí
  vive la lógica de las operaciones, reflejada en JavaScript porque la
  interacción ocurre en el navegador.
- `pila_animacion.html` - archivo generado por el script (no editar a mano).

## Uso
```bash
python3 simulador_pila.py 1 2 3 4 5
```
Los valores se apilan en el orden dado: el último (5) queda en el TOPE.

### Opciones
- `--no-open` - solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` - guarda el HTML en una ruta concreta
  (por defecto: `pila_animacion.html` en el directorio actual).

## Operaciones interactivas (en la página)
- **Push** - apila el valor escrito en el tope.
- **Pop** - retira el elemento del tope.
- **Peek** - resalta el tope sin modificar la pila.
- **Buscar** - recorre desde el tope hacia la base comparando con el valor;
  marca el primer hallazgo o avisa si no está.
- **Recorrer** - visita todos los elementos desde el tope hacia la base.
- **Reiniciar** - reconstruye la pila con la secuencia inicial.

## Controles de reproducción
- **⏮ / ◀ / ▶ / ⏭** - inicio, anterior, siguiente, fin.
- **▶ Reproducir / Pausa** - animación automática.
- **Barra de velocidad** - regula el ritmo.
- **Teclado** - flechas ← → para avanzar/retroceder, barra espaciadora para
  reproducir/pausar, Enter en la casilla para hacer Push.

## Colores
- Azul: elemento normal · Amarillo: comparando / visitando · Verde: nuevo o
  resultado · Cian: encontrado o tope · Rojo: elemento que se retirará.
