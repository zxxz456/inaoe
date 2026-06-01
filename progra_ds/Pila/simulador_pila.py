"""
simulador_pila.py
========================


Description:
------------
Simulador interactivo de una Pila (Stack, LIFO). Recibe una secuencia de
valores por linea de comandos, los pasa a una pagina HTML y genera una
animacion interactiva en el navegador que muestra, paso a paso, como se
construye la pila. Dentro de la misma pagina aparecen botones para PUSH,
POP, PEEK, BUSCAR y RECORRER, cada una con su animacion.

La estructura de la pila esta en `pila.py` (clase Pila). Como las
operaciones interactivas se ejecutan en el navegador, la misma logica esta
reflejada en JavaScript dentro de la pagina.


Usage:
------
    python3 simulador_pila.py 1 2 3 4 5
    python3 simulador_pila.py a b c d --no-open -o pila.html

    Cada valor se interpreta como entero si es posible; si no, como texto
    (no se pueden mezclar numeros y texto en la misma secuencia).


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


def generate_html(keys):
    """Carga `plantilla.html` e inserta las claves iniciales.

    Lee la plantilla HTML del archivo `plantilla.html` (junto a este script)
    y sustituye el marcador `__KEYS__` por la secuencia de valores.

    Inputs:
    ------
    keys: Lista de valores iniciales (int o str) a precargar en la pila.

    Returns:
    -------
    str: El HTML completo con la secuencia incrustada como JSON.
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()
    return template.replace("__KEYS__", json.dumps(keys))


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

    Lee los valores iniciales, valida que no se mezclen numeros y texto,
    escribe la animacion en un archivo del directorio actual y, salvo que se
    indique `--no-open`, la abre en el navegador.

    Inputs:
    ------
    argv: Lista de argumentos a procesar; si es None usa los de sys.argv.

    Returns:
    -------
    str: Ruta absoluta del archivo HTML generado.
    """
    parser = argparse.ArgumentParser(
        description="Simulador interactivo de una Pila (Stack, LIFO).")
    parser.add_argument("valores", nargs="*",
                        help="valores iniciales a apilar, en orden (el ultimo queda en el tope)")
    parser.add_argument("--no-open", action="store_true",
                        help="solo genera el HTML, sin abrir el navegador")
    parser.add_argument("-o", "--output", default=None,
                        help="ruta del HTML de salida "
                             "(por defecto: pila_animacion.html en el directorio actual)")
    args = parser.parse_args(argv)

    keys = [parse_value(v) for v in args.valores]

    tipos = {type(k) for k in keys}
    if len(tipos) > 1:
        parser.error("no mezcles numeros y texto en la misma secuencia.")

    html = generate_html(keys)

    out = args.output if args.output else "pila_animacion.html"
    path = os.path.abspath(out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Valores iniciales:", " ".join(str(k) for k in keys) or "(ninguno)")
    print("Animacion generada en:", path)

    if not args.no_open:
        webbrowser.open("file://" + path)
        print("Abriendo en el navegador...")

    return path


if __name__ == "__main__":
    main()
