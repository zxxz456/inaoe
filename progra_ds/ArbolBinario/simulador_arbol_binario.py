"""
simulador_arbol_binario.py
========================


Description:
------------
Simulador interactivo de un Arbol Binario generico (no BST). Recibe una
secuencia de valores por linea de comandos y los inserta por nivel
(BFS-fill) construyendo el arbol paso a paso. Dentro de la pagina hay
botones para INSERTAR, BUSCAR, ELIMINAR (subarbol) y los cuatro recorridos
(preorden, inorden, postorden y por niveles), cada uno con su animacion.

La estructura del arbol esta en `arbol_binario.py` (clases NodoBinario y
ArbolBinario). Como las operaciones interactivas se ejecutan en el
navegador, la misma logica esta reflejada en JavaScript dentro de la
pagina.


Usage:
------
    python3 simulador_arbol_binario.py 1 2 3 4 5 6 7
    python3 simulador_arbol_binario.py A B C D E --no-open -o arbol.html


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

    Inputs:
    ------
    keys: Lista de valores iniciales (int o str) a precargar en el arbol.

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

    Inputs:
    ------
    argv: Lista de argumentos a procesar; si es None usa los de sys.argv.

    Returns:
    -------
    str: Ruta absoluta del archivo HTML generado.
    """
    parser = argparse.ArgumentParser(
        description="Simulador interactivo de un Arbol Binario generico.")
    parser.add_argument("valores", nargs="*",
                        help="valores iniciales a insertar por nivel (BFS-fill)")
    parser.add_argument("--no-open", action="store_true",
                        help="solo genera el HTML, sin abrir el navegador")
    parser.add_argument("-o", "--output", default=None,
                        help="ruta del HTML de salida "
                             "(por defecto: arbol_binario_animacion.html en el directorio actual)")
    args = parser.parse_args(argv)

    keys = [parse_value(v) for v in args.valores]

    tipos = {type(k) for k in keys}
    if len(tipos) > 1:
        parser.error("no mezcles numeros y texto en la misma secuencia.")

    html = generate_html(keys)

    out = args.output if args.output else "arbol_binario_animacion.html"
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
