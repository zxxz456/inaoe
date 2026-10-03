"""
Utils.py
========================


Descripcion:
------------
Constantes y funciones auxiliares compartidas por el proyecto 1 de
Matematicas para la Computacion.

Aqui viven los parametros del experimento, los que el enunciado deja
abiertos (registro de ECG, longitud de ventana, numero de atomos,
dispersion objetivo), y los helpers que usan dos o mas modulos. Si un
numero aparece en el codigo, su lugar es este archivo.


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       02/10/2026      Constantes del modo paso a paso
zxxz6       01/10/2026      Registros de MIT-BIH y ruta de su cache local
zxxz6       30/09/2026      Creation


"""

import os

import numpy as np

# Coleccion de PhysioNet. mitdb es MIT-BIH Arrhythmia: 48 registros de
# media hora, 360 Hz, dos canales
BASE_PHYSIONET = "mitdb"
REGISTRO = "100"

# Los 48 registros de mitdb, la lista que da wfdb.get_record_list. Son
# 47 personas: 201 y 202 son del mismo paciente. La serie 100 es una
# muestra al azar de pacientes ambulatorios; la 200 se escogio por
# tener arritmias raras, asi que sus latidos son menos tipicos
REGISTROS_MITDB = (
    "100", "101", "102", "103", "104", "105", "106", "107", "108",
    "109", "111", "112", "113", "114", "115", "116", "117", "118",
    "119", "121", "122", "123", "124", "200", "201", "202", "203",
    "205", "207", "208", "209", "210", "212", "213", "214", "215",
    "217", "219", "220", "221", "222", "223", "228", "230", "231",
    "232", "233", "234",
)
CANAL = 0
FRECUENCIA_HZ = 360

# Geometria del problema. D queda de TAM_VENTANA x N_ATOMOS
TAM_VENTANA = 128
N_ATOMOS = 256
PASO_VENTANA = TAM_VENTANA

# Dispersion y entrenamiento
ERROR_OMP = 0.1
MAX_ATOMOS_OMP = 16
ITERACIONES_KSVD = 20

# Reproducibilidad
SEMILLA = 7

# Rutas de salida, relativas a src/
RUTA_SALIDA = "../out"

# Copia local de los registros de PhysioNet, en proyecto1/datos. Se
# arma desde este archivo y no desde el directorio de trabajo, porque
# el notebook y la terminal no siempre corren desde src/
RUTA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          os.pardir, "datos")

# Modo paso a paso. Cuantos valores de un vector se imprimen, cuantas
# filas y columnas de una matriz, y cuantos atomos candidatos de OMP o
# valores singulares se listan en cada pausa
DEPURACION_VALORES = 8
DEPURACION_FILAS = 5
DEPURACION_COLUMNAS = 6
DEPURACION_TOP = 5
DEPURACION_ANCHO = 72

# Debajo de esto una norma se considera cero, para no dividir entre
# un residual que ya se agoto
TOLERANCIA = 1e-10


def normalizar_columnas(mat):
    """
    Lleva cada columna a norma 1.
    Las columnas de norma cero se dejan intactas en vez de dividirlas,
    porque una ventana plana o un atomo muerto no tienen direccion que
    conservar y dividir entre cero solo propaga nan al resto

    Inputs:
    -------
    mat: Arreglo de 2 dimensiones, una senal o un atomo por columna

    Returns:
    -------
    ndarray: Copia con las columnas normalizadas

    """
    normas = np.linalg.norm(mat, axis=0)
    seguras = np.where(normas < TOLERANCIA, 1.0, normas)

    return mat / seguras


def error_relativo(original, reconstruida):
    """
    Error de reconstruccion como fraccion de la energia original.
    Es el mismo criterio de paro que usa OMP, asi que se define una
    sola vez y se usa en las dos partes

    Inputs:
    -------
    original: Senal o matriz de senales de referencia
    reconstruida: Lo que devolvio el modelo, de la misma forma

    Returns:
    -------
    float: Norma de Frobenius del residual entre la de la original

    """
    norma = np.linalg.norm(original)
    if norma < TOLERANCIA:
        return 0.0

    return float(np.linalg.norm(original - reconstruida) / norma)


def dispersion_media(alpha):
    """
    Promedio de atomos usados por senal.
    Es la cifra que dice si la representacion de verdad es dispersa:
    sirve de poco un error bajo si cada senal gasta medio diccionario

    Inputs:
    -------
    alpha: Matriz de coeficientes, N_ATOMOS por numero de senales

    Returns:
    -------
    float: Cuantos coeficientes distintos de cero tiene en promedio
           cada columna

    """
    return float(np.count_nonzero(alpha, axis=0).mean())


############################### END OF UTILS.PY ################################
################################################################################
