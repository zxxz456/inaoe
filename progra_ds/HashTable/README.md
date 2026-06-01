# Simulador de Tabla Hash (con encadenamiento)

Construye una tabla hash insertando una secuencia de claves y muestra una
**animación interactiva en el navegador**. Las colisiones se resuelven con
**encadenamiento (separate chaining)**: cada cubeta es una cadena de pares
que comparten el mismo hash. Una vez construida, la misma página permite
ejecutar **Insertar, Buscar, Eliminar y Recorrer**.

## Función hash
- Si la clave es **entera**: `|clave| mod M`.
- Si es **texto**: suma de códigos Unicode de los caracteres `mod M`.

`M` = número de cubetas (configurable con `-m`, por defecto 7).

## Archivos
- `hash_table.py` — estructura base en Python: clase `HashTable`.
- `simulador_hash.py` — CLI que carga la plantilla e inyecta claves y `M`.
- `plantilla.html` — HTML/CSS/JS del simulador (lógica reflejada en JS).
- `hash_animacion.html` — archivo generado por el script (no editar a mano).

## Uso
```bash
# numéricas, 7 cubetas (default)
python3 simulador_hash.py 10 22 31 4 15 7 19

# texto, 5 cubetas
python3 simulador_hash.py manzana pera uva kiwi -m 5
```

### Opciones
- `-m N` / `--cubetas N` — número de cubetas (por defecto 7).
- `--no-open` — solo genera el HTML, sin abrir el navegador.
- `-o RUTA` / `--output RUTA` — ruta del HTML de salida.

## Operaciones interactivas (en la página)
- **Insertar** — calcula el hash, viaja a la cubeta y agrega al final de la
  cadena (o actualiza si la clave ya existía).
- **Buscar** — calcula el hash y recorre la cadena de esa cubeta comparando.
- **Eliminar** — busca y, si está, lo retira de la cadena.
- **Recorrer** — visita cubeta por cubeta, mostrando todas sus claves.
- **Reiniciar** — reconstruye la tabla con la secuencia inicial.

## Controles de reproducción
Idénticos a los demás simuladores (⏮ / ◀ / ▶ / ⏭ + barra de velocidad +
flechas y barra espaciadora).

## Colores
- Azul: par normal · Amarillo: cubeta o par que se está visitando · Verde:
  nuevo o resultado · Cian: encontrado · Rojo: par que se va a eliminar.
