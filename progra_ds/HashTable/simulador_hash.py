"""
simulador_hash.py
========================


Description:
------------
Simulador interactivo de una Tabla Hash con encadenamiento. Recibe una
secuencia de claves por linea de comandos y opcionalmente el numero de
cubetas (`-m`). Genera una pagina HTML que muestra la construccion paso a
paso. Dentro de la pagina hay botones para INSERTAR, BUSCAR, ELIMINAR y
RECORRER, cada una con su animacion.

La estructura de la tabla esta en `hash_table.py` (clase HashTable). Como
las operaciones interactivas se ejecutan en el navegador, la misma logica
esta reflejada en JavaScript dentro de la pagina.


Usage:
------
    python3 simulador_hash.py 10 22 31 4 15 7 19
    python3 simulador_hash.py manzana pera uva kiwi -m 5
    python3 simulador_hash.py 1 2 3 --no-open -o hash.html


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


def generate_html(keys, m):
    """Carga `plantilla.html` e inserta las claves iniciales y el numero
    de cubetas.

    Inputs:
    ------
    keys: Lista de valores iniciales (int o str) a insertar.
    m: Numero de cubetas de la tabla.

    Returns:
    -------
    str: El HTML completo con los datos incrustados.
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()
    return (template
            .replace("__KEYS__", json.dumps(keys))
            .replace("__M__", str(m)))


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
        description="Simulador interactivo de una Tabla Hash (con encadenamiento).")
    parser.add_argument("valores", nargs="*",
                        help="claves iniciales a insertar, en orden")
    parser.add_argument("-m", "--cubetas", type=int, default=7,
                        help="numero de cubetas de la tabla (default: 7)")
    parser.add_argument("--no-open", action="store_true",
                        help="solo genera el HTML, sin abrir el navegador")
    parser.add_argument("-o", "--output", default=None,
                        help="ruta del HTML de salida "
                             "(por defecto: hash_animacion.html en el directorio actual)")
    args = parser.parse_args(argv)

    if args.cubetas < 1:
        parser.error("--cubetas debe ser >= 1.")

    keys = [parse_value(v) for v in args.valores]

    tipos = {type(k) for k in keys}
    if len(tipos) > 1:
        parser.error("no mezcles numeros y texto en la misma secuencia.")

    html = generate_html(keys, args.cubetas)

    out = args.output if args.output else "hash_animacion.html"
    path = os.path.abspath(out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Cubetas: {args.cubetas}")
    print("Claves iniciales:", " ".join(str(k) for k in keys) or "(ninguna)")
    print("Animacion generada en:", path)

    if not args.no_open:
        webbrowser.open("file://" + path)
        print("Abriendo en el navegador...")

    return path


if __name__ == "__main__":
    main()
