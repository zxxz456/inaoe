"""
Analisis.py
========================


Descripcion:
------------
Analisis de resultados del proyecto 1: pone el diccionario entrenado
contra dos referencias y contra pacientes que no vio.

Las referencias son un diccionario fijo, la DCT sobrecompleta, y el
diccionario inicial D_0, que son ventanas tomadas tal cual sin
entrenar. Sin ellas el error de 0.10 del entrenamiento no tiene contra
que medirse. La prueba entre pacientes reconstruye registros de
MIT-BIH distintos del 100 con el mismo diccionario, para ver si lo que
aprendio es la forma del ECG o la de un paciente.

Lee out/modelo.npz, asi que hay que correr Experimento.py antes.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.0.0


History:
------------
Author      Date            Description
zxxz6       04/10/2026      Creation


"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from Datos import cargar_ecg, construir_x
from Experimento import curva_error, partir_entrenamiento
from Figuras import (SERIE_AQUA, SERIE_AZUL, SERIE_NARANJA, SUPERFICIE,
                     TINTA, estilo)
from Ksvd import diccionario_inicial
from Omp import omp_matriz
from Utils import (ERROR_OMP, N_ATOMOS, REGISTRO, RUTA_SALIDA,
                   TAM_VENTANA, dispersion_media, error_relativo,
                   normalizar_columnas)

ARCHIVO_MODELO = f"{RUTA_SALIDA}/modelo.npz"

# Topes de atomos de la comparacion entre diccionarios
TOPES_COMPARACION = (1, 2, 4, 8, 16, 32)

# Tope fijo con el que se comparan los pacientes
TOPE_PACIENTES = 8

# Otros pacientes de MIT-BIH. Dos de la serie 100, que son pacientes
# ambulatorios al azar como el 100, y dos de la serie 200, escogida por
# tener arritmias raras. Se evitan 102 y 104, cuyo canal 0 es V5 y no
# MLII como en los demas
OTROS_PACIENTES = ("101", "103", "200", "208")


def diccionario_dct(k=TAM_VENTANA, m=N_ATOMOS):
    """
    Diccionario fijo: cosenos de la DCT, sobrecompleto.
    Es el ejemplo clasico de diccionario predefinido: no mira los datos,
    solo supone que la senal se describe bien con oscilaciones. Tiene el
    mismo tamano que el aprendido para que la comparacion sea justa

    Inputs:
    -------
    k: Longitud de cada atomo
    m: Numero de atomos; con m > k las frecuencias se parten mas fino
       que en la DCT ortogonal

    Returns:
    -------
    ndarray: Diccionario de k por m, columnas de norma 1

    """
    n = np.arange(k)[:, None]
    frecuencia = np.arange(m)[None, :]

    return normalizar_columnas(np.cos(np.pi * (n + 0.5) * frecuencia / m))


def comparar_diccionarios(diccionarios, x, topes=TOPES_COMPARACION):
    """
    Curva de error de cada diccionario sobre las mismas senales.

    Inputs:
    -------
    diccionarios: Dict de nombre a diccionario
    x: Senales de prueba
    topes: Topes de atomos a probar

    Returns:
    -------
    dict: Nombre -> arreglo con el error en cada tope

    """
    return {nombre: np.array([f["error"]
                              for f in curva_error(d, x, topes)])
            for nombre, d in diccionarios.items()}


def evaluar_paciente(d, x, tope=TOPE_PACIENTES):
    """
    Que tan bien representa el diccionario las senales de un paciente.
    Se miden dos cosas que dicen lo mismo desde lados opuestos: el error
    con un tope fijo de atomos, y cuantos atomos hacen falta para llegar
    al error objetivo

    Inputs:
    -------
    d: Diccionario entrenado
    x: Ventanas del paciente
    tope: Atomos permitidos en la primera medida

    Returns:
    -------
    dict: Ventanas, error con el tope y atomos necesarios para
          ERROR_OMP

    """
    fijo = omp_matriz(d, x, error=0.0, max_atomos=tope)
    objetivo = omp_matriz(d, x)

    return {
        "ventanas": x.shape[1],
        "error_tope": error_relativo(x, d @ fijo),
        "atomos_objetivo": dispersion_media(objetivo),
    }


def figura_diccionarios(curvas, topes=TOPES_COMPARACION):
    """
    Error contra atomos para los tres diccionarios.

    Inputs:
    -------
    curvas: Lo que devuelve comparar_diccionarios
    topes: Topes de atomos de cada punto

    Returns:
    -------
    Figure: La figura armada

    """
    colores = (SERIE_AZUL, SERIE_NARANJA, SERIE_AQUA)
    fig, eje = plt.subplots(figsize=(7, 3.6))

    for (nombre, errores), color in zip(curvas.items(), colores):
        # Sin etiqueta en el ultimo punto: en 32 atomos las tres
        # curvas casi se tocan y los numeros se enciman. Los valores
        # exactos van en la tabla del reporte
        eje.plot(topes, errores, color=color, linewidth=2, marker="o",
                 markersize=6, markeredgecolor=SUPERFICIE,
                 markeredgewidth=1.5, label=nombre)

    eje.set_xscale("log", base=2)
    eje.set_xticks(topes)
    eje.set_xticklabels([str(t) for t in topes])
    estilo(eje, "Error de reconstruccion segun el diccionario")
    eje.set_xlabel("atomos permitidos por senal", fontsize=9,
                   color=TINTA)
    eje.set_ylabel("error relativo", fontsize=9, color=TINTA)
    eje.set_ylim(0, None)
    eje.legend(fontsize=8, frameon=False)
    fig.tight_layout()

    return fig


def figura_pacientes(resultados, tope=TOPE_PACIENTES):
    """
    Error de reconstruccion por paciente, con el tope fijo.
    Solo se distinguen dos grupos, el paciente de entrenamiento y los
    demas. Colorear por serie sugeriria que la serie decide que tan bien
    generaliza el diccionario, y los datos no lo sostienen: el 208, de
    la serie de arritmias, sale igual que el propio 100

    Inputs:
    -------
    resultados: Dict de registro a lo que devuelve evaluar_paciente
    tope: Atomos permitidos, para el titulo

    Returns:
    -------
    Figure: La figura armada

    """
    registros = list(resultados)
    errores = [resultados[r]["error_tope"] for r in registros]
    colores = [SERIE_AZUL if r == REGISTRO else SERIE_NARANJA
               for r in registros]
    etiquetas = [f"{r}\nserie {r[0]}00" for r in registros]

    fig, eje = plt.subplots(figsize=(7, 3.2))
    barras = eje.bar(etiquetas, errores, color=colores, width=0.6)
    eje.bar_label(barras, fmt="%.3f", fontsize=8, color=TINTA,
                  padding=2)

    marcas = [Patch(color=SERIE_AZUL,
                    label=f"registro {REGISTRO}, mitad que no se uso "
                          f"al entrenar"),
              Patch(color=SERIE_NARANJA, label="otros pacientes")]

    estilo(eje, f"Error con {tope} atomos, diccionario entrenado "
                f"solo con el registro {REGISTRO}")
    eje.set_ylabel("error relativo", fontsize=9, color=TINTA)
    eje.set_ylim(0, max(errores) * 1.3)
    eje.tick_params(axis="x", labelsize=8)
    eje.legend(handles=marcas, fontsize=8, frameon=False,
               loc="upper left")
    fig.tight_layout()

    return fig


def main():
    """
    Corre las dos comparaciones, imprime las tablas y guarda las figuras.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Escribe dos PDF en RUTA_SALIDA

    """
    if not os.path.exists(ARCHIVO_MODELO):
        raise SystemExit(f"falta {ARCHIVO_MODELO}, "
                         f"corre Experimento.py primero")

    datos = np.load(ARCHIVO_MODELO)
    d = datos["diccionario"]

    senal, _ = cargar_ecg(REGISTRO)
    entrena, prueba = partir_entrenamiento(construir_x(senal))

    diccionarios = {
        "aprendido con K-SVD": d,
        "D_0, ventanas sin entrenar": diccionario_inicial(entrena),
        "DCT, fijo": diccionario_dct(),
    }
    curvas = comparar_diccionarios(diccionarios, prueba)

    print(f"error sobre la mitad de prueba del registro {REGISTRO}, "
          f"{prueba.shape[1]} ventanas\n")
    print(f"  {'atomos':>6}" + "".join(f"{n[:22]:>24}" for n in curvas))
    for i, tope in enumerate(TOPES_COMPARACION):
        print(f"  {tope:>6}" + "".join(f"{e[i]:>24.4f}"
                                       for e in curvas.values()))

    resultados = {REGISTRO: evaluar_paciente(d, prueba)}
    for registro in OTROS_PACIENTES:
        senal_otro, _ = cargar_ecg(registro)
        resultados[registro] = evaluar_paciente(d,
                                                construir_x(senal_otro))

    print(f"\npor paciente, con el diccionario del registro {REGISTRO}")
    print(f"  {'registro':>8} {'ventanas':>9} "
          f"{'error, ' + str(TOPE_PACIENTES) + ' atomos':>18} "
          f"{'atomos para ' + str(ERROR_OMP):>18}")
    for registro, r in resultados.items():
        print(f"  {registro:>8} {r['ventanas']:>9} "
              f"{r['error_tope']:>18.4f} {r['atomos_objetivo']:>18.2f}")

    figuras = {
        "comparacion_diccionarios.pdf": figura_diccionarios(curvas),
        "pacientes.pdf": figura_pacientes(resultados),
    }
    for nombre, figura in figuras.items():
        ruta = f"{RUTA_SALIDA}/{nombre}"
        figura.savefig(ruta, bbox_inches="tight", facecolor=SUPERFICIE)
        print(f"\n{ruta}")


if __name__ == "__main__":
    main()


############################## END OF ANALISIS.PY ##############################
################################################################################
