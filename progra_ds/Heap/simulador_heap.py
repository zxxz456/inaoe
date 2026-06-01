"""
simulador_heap.py
========================


Description:
------------
Simulador interactivo de un Monticulo Binario (Heap). Recibe una secuencia
de valores por linea de comandos y un flag opcional `--max` para usar
max-heap (por defecto min-heap). Genera una pagina HTML que muestra la
construccion paso a paso con animacion de bubble-up al insertar. Dentro de
la pagina hay botones para INSERTAR, EXTRAER, PEEK, BUSCAR y RECORRER, con
sus animaciones (bubble-up / bubble-down y comparaciones).

La estructura del heap esta en `heap.py` (clase Heap). Como las operaciones
interactivas se ejecutan en el navegador, la misma logica esta reflejada en
JavaScript dentro de la pagina.


Usage:
------
    python3 simulador_heap.py 5 3 8 1 9 4 7        # min-heap
    python3 simulador_heap.py 5 3 8 1 9 4 7 --max  # max-heap
    python3 simulador_heap.py 5 3 8 1 --no-open -o heap.html


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       21/05/2026      Creation


"""

import argparse
import json
import os
import webbrowser


TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "plantilla.html")


def generate_html(keys, es_min):
    """Carga `plantilla.html` e inserta las claves iniciales y el modo.

    Inputs:
    ------
    keys: Lista de valores iniciales (int o str) a precargar en el heap.
    es_min: True para min-heap; False para max-heap.

    Returns:
    -------
    str: El HTML completo con la secuencia y el modo incrustados.
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()
    return (template
            .replace("__KEYS__", json.dumps(keys))
            .replace("__ES_MIN__", "true" if es_min else "false"))


def parse_value(token):
    """Convierte un argumento a int si se puede; si no, lo deja como texto.

    Inputs:
    ------
    token: Cadena recibida desde la linea de comandos.

    Returns:
    -------
    int | str: El entero correspondiente o la cadena original.
    """
    try:
        return int(token)
    except ValueError:
        return token


def main(argv=None):
    """Punto de entrada: procesa los argumentos, genera el HTML y lo abre.

    Inputs:
    ------
    argv: Lista de argumentos a procesar; si es None usa los de sys.argv.

    Returns:
    -------
    str: Ruta absoluta del archivo HTML generado.
    """
    parser = argparse.ArgumentParser(
        description="Simulador interactivo de un Heap Binario (min o max).")
    parser.add_argument("valores", nargs="*",
                        help="valores iniciales a insertar, en orden")
    parser.add_argument("--max", action="store_true",
                        help="usa max-heap (por defecto: min-heap)")
    parser.add_argument("--no-open", action="store_true",
                        help="solo genera el HTML, sin abrir el navegador")
    parser.add_argument("-o", "--output", default=None,
                        help="ruta del HTML de salida "
                             "(por defecto: heap_animacion.html en el directorio actual)")
    args = parser.parse_args(argv)

    keys = [parse_value(v) for v in args.valores]

    tipos = {type(k) for k in keys}
    if len(tipos) > 1:
        parser.error("no mezcles numeros y texto en la misma secuencia.")

    html = generate_html(keys, es_min=(not args.max))

    out = args.output if args.output else "heap_animacion.html"
    path = os.path.abspath(out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Modo:", "max-heap" if args.max else "min-heap")
    print("Valores iniciales:", " ".join(str(k) for k in keys) or "(ninguno)")
    print("Animacion generada en:", path)

    if not args.no_open:
        webbrowser.open("file://" + path)
        print("Abriendo en el navegador...")

    return path


if __name__ == "__main__":
    main()
