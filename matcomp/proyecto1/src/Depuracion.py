"""
Depuracion.py
========================


Descripcion:
------------
Modo paso a paso del entrenamiento. Imprime los datos con los que se
esta trabajando en cada paso importante (la senal, X, cada vuelta de
OMP, cada actualizacion de atomo) y espera a que se presione Enter
para seguir.

Se activa con la bandera --paso-a-paso de Experimento.py. Los modulos
del algoritmo reciben un Depurador opcional; si no se les pasa, o si
esta inactivo, corren igual que siempre y no imprimen nada extra.


Considerations:
------------
- Cada pausa pertenece a una categoria: datos, inicio, iteracion,
  omp, alpha, atomo o resumen. Escribir s en la pausa salta el resto
  de esa categoria hasta la siguiente iteracion de K-SVD. Sin eso,
  revisar OMP seria presionar Enter miles de veces por iteracion
- c corre sin pausas hasta el final y q sale del programa
- Si la entrada estandar no es una terminal (por ejemplo, con la
  salida redirigida), input() falla con EOFError. En ese caso se pasa
  a modo continuo en vez de tronar
- Los resumenes de cada paso se arman solo si se van a mostrar.
  quiere() se consulta antes de calcular algo caro, como los cosenos
  entre el diccionario viejo y el nuevo


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       02/10/2026      Creation


"""

import numpy as np

from Utils import (DEPURACION_ANCHO, DEPURACION_COLUMNAS,
                   DEPURACION_FILAS, DEPURACION_VALORES)

INSTRUCCIONES = ("[Enter] siguiente   [s] saltar esto   "
                 "[c] sin pausas   [q] salir")


def vector(v, n=DEPURACION_VALORES):
    """
    Resume un vector en una linea: su forma y sus primeros valores.

    Inputs:
    -------
    v: Arreglo de 1 dimension
    n: Cuantos valores mostrar antes de cortar con ...

    Returns:
    -------
    str: Algo como "(128,) [-0.145 -0.145 ... ]"

    """
    v = np.asarray(v)
    valores = " ".join(f"{a:7.3f}" for a in v[:n])
    resto = " ..." if v.size > n else ""

    return f"{v.shape} [{valores}{resto} ]"


def matriz(m, filas=DEPURACION_FILAS, columnas=DEPURACION_COLUMNAS):
    """
    Resume una matriz: su forma y su esquina superior izquierda.

    Inputs:
    -------
    m: Arreglo de 2 dimensiones
    filas: Cuantas filas de la esquina mostrar
    columnas: Cuantas columnas de la esquina mostrar

    Returns:
    -------
    str: Varias lineas, la forma y luego la esquina

    """
    m = np.asarray(m)
    lineas = [f"forma {m.shape}, esquina de {min(filas, m.shape[0])} x "
              f"{min(columnas, m.shape[1])}:"]
    for fila in m[:filas, :columnas]:
        valores = " ".join(f"{a:7.3f}" for a in fila)
        resto = " ..." if m.shape[1] > columnas else ""
        lineas.append(f"    [{valores}{resto} ]")
    if m.shape[0] > filas:
        lineas.append("     ...")

    return "\n".join(lineas)


class Depurador:
    """
    Controla las pausas del modo paso a paso.
    Lleva la cuenta de los pasos mostrados, de las categorias que el
    usuario pidio saltar en la iteracion actual y de si ya pidio correr
    sin pausas

    """

    def __init__(self, activo=True):
        """
        Arma el depurador.

        Inputs:
        -------
        activo: False para que no muestre nada; asi los modulos pueden
                recibir siempre un Depurador sin preguntar por la bandera

        Returns:
        -------
        None

        """
        self.activo = activo
        self.continuo = False
        self.saltadas = set()
        self.contador = 0

    def quiere(self, categoria):
        """
        Dice si la siguiente pausa de esta categoria se va a mostrar.
        Sirve para no calcular un resumen que nadie va a ver

        Inputs:
        -------
        categoria: Nombre de la categoria, por ejemplo "omp"

        Returns:
        -------
        bool: True si se mostraria

        """
        return (self.activo and not self.continuo
                and categoria not in self.saltadas)

    def nueva_iteracion(self):
        """
        Olvida las categorias saltadas.
        Se llama al empezar cada iteracion de K-SVD, para que s salte
        solo lo que queda de la iteracion actual

        Inputs:
        -------
        None

        Returns:
        -------
        None

        """
        self.saltadas.clear()

    def mostrar(self, categoria, titulo, lineas):
        """
        Imprime un paso y espera la tecla del usuario.

        Inputs:
        -------
        categoria: A que tipo de paso pertenece, para poder saltarlo
        titulo: Encabezado corto del paso
        lineas: Lista de cadenas con los datos del paso

        Returns:
        -------
        None

        """
        if not self.quiere(categoria):
            return

        self.contador += 1
        print("\n" + "=" * DEPURACION_ANCHO)
        print(f"paso {self.contador}  [{categoria}]  {titulo}")
        print("-" * DEPURACION_ANCHO)
        for linea in lineas:
            print(linea)
        print("-" * DEPURACION_ANCHO)
        self._esperar(categoria)

    def _esperar(self, categoria):
        """
        Lee la decision del usuario despues de una pausa.

        Inputs:
        -------
        categoria: La del paso que se acaba de mostrar

        Returns:
        -------
        None: Cambia el estado del depurador, o sale con q

        """
        try:
            respuesta = input(INSTRUCCIONES + "\n> ").strip().lower()
        except EOFError:
            self.continuo = True
            return

        if respuesta == "s":
            self.saltadas.add(categoria)
            print(f"(saltando [{categoria}] hasta la siguiente "
                  f"iteracion)")
        elif respuesta == "c":
            self.continuo = True
            print("(corriendo sin pausas)")
        elif respuesta == "q":
            raise SystemExit("detenido desde el modo paso a paso")


############################# END OF DEPURACION.PY #############################
################################################################################
