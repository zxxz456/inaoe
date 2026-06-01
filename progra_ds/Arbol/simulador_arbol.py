"""
simulador_arbol.py
========================


Description:
------------
Simulador interactivo de un Arbol n-ario (general). Recibe la estructura
inicial por linea de comandos: el primer argumento es la raiz (sin `:`) y
los siguientes son pares `padre:hijo` que indican como cuelga cada nodo.
Genera una pagina HTML que muestra la construccion paso a paso. Dentro de
la pagina hay botones para INSERTAR (`padre:hijo`), BUSCAR, ELIMINAR
(subarbol) y los recorridos PREORDEN, POSTORDEN y POR NIVELES.

La estructura del arbol esta en `arbol.py` (clases NodoNario y ArbolNario).
Como las operaciones interactivas se ejecutan en el navegador, la misma
logica esta reflejada en JavaScript dentro de la pagina.


Usage:
------
    python3 simulador_arbol.py A A:B A:C B:D B:E C:F
    python3 simulador_arbol.py raiz raiz:hoja1 raiz:hoja2 --no-open


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


def parse_value(token):
    """Convierte un token a int si se puede; si no, lo deja como texto.

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


def parse_ops(tokens):
    """Convierte la lista de argumentos en operaciones de construccion.

    El primer token (sin ':') se interpreta como la raiz. Cada token
    siguiente debe ser `padre:hijo` y agrega `hijo` como hijo de `padre`.

    Inputs:
    ------
    tokens: Lista de cadenas tal como se reciben en la linea de comandos.

    Returns:
    -------
    list: Lista de diccionarios {tipo:'root', v:...} o {tipo:'child', p:..., h:...}.
    """
    ops = []
    if not tokens:
        return ops
    if ':' in tokens[0]:
        raise ValueError(
            "el primer argumento es la raiz: no debe contener ':'.")
    ops.append({"tipo": "root", "v": parse_value(tokens[0])})
    for t in tokens[1:]:
        if ':' not in t:
            raise ValueError(f"'{t}' debe tener la forma padre:hijo.")
        p, h = t.split(':', 1)
        p, h = p.strip(), h.strip()
        if p == '' or h == '':
            raise ValueError(f"'{t}': padre y hijo no pueden estar vacios.")
        ops.append({"tipo": "child", "p": parse_value(p), "h": parse_value(h)})
    return ops


def generate_html(ops):
    """Carga `plantilla.html` e inserta las operaciones de construccion.

    Inputs:
    ------
    ops: Lista de operaciones devuelta por `parse_ops`.

    Returns:
    -------
    str: El HTML completo con las operaciones incrustadas como JSON.
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        template = f.read()
    return template.replace("__OPS__", json.dumps(ops))


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
        description="Simulador interactivo de un Arbol n-ario (general).")
    parser.add_argument("tokens", nargs="*",
                        help="primer token = raiz; despues pares padre:hijo")
    parser.add_argument("--no-open", action="store_true",
                        help="solo genera el HTML, sin abrir el navegador")
    parser.add_argument("-o", "--output", default=None,
                        help="ruta del HTML de salida "
                             "(por defecto: arbol_animacion.html en el directorio actual)")
    args = parser.parse_args(argv)

    try:
        ops = parse_ops(args.tokens)
    except ValueError as e:
        parser.error(str(e))

    html = generate_html(ops)

    out = args.output if args.output else "arbol_animacion.html"
    path = os.path.abspath(out)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("Operaciones iniciales:")
    for op in ops:
        if op["tipo"] == "root":
            print(f"  raiz: {op['v']}")
        else:
            print(f"  {op['p']} -> {op['h']}")
    print("Animacion generada en:", path)

    if not args.no_open:
        webbrowser.open("file://" + path)
        print("Abriendo en el navegador...")

    return path


if __name__ == "__main__":
    main()
