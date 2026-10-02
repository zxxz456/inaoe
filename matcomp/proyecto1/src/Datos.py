"""
Datos.py
========================


Descripcion:
------------
Carga de la senal de ECG desde PhysioNet y armado de la matriz X de
entrenamiento del proyecto 1.

Una senal de media hora no se le pasa entera a K-SVD. Se corta en
ventanas de TAM_VENTANA muestras, cada ventana se guarda como una
columna de X, y cada columna se normaliza. El resultado es la matriz
sobre la que se aprende el diccionario.


Considerations:
------------
- wfdb baja el registro del servidor de PhysioNet la primera vez; si
  no hay red, hay que tener el registro en local y pasar ruta en vez
  de pn_dir
- Las ventanas no se traslapan por omision. Traslaparlas da mas
  columnas de entrenamiento a cambio de que se parezcan mas entre si
- Se quita la media de cada ventana antes de normalizar: el ECG trae
  deriva de linea base y sin quitarla el primer atomo que aprende el
  diccionario es una constante, que no describe ninguna forma de onda
- Con varios registros, el canal 0 no es la misma derivacion en
  todos: en 102 y 104 es V5 y no MLII, porque a esos pacientes no se
  les pudo poner el electrodo de MLII. Sus latidos se ven distintos
- Los 48 registros dan unas 244 mil ventanas, 48 veces lo de uno solo.
  wfdb los baja cada vez que se cargan, sin cache


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       01/10/2026      Opcion de armar X con varios pacientes
zxxz6       30/09/2026      Creation


"""

import numpy as np
import wfdb

from Utils import (BASE_PHYSIONET, CANAL, PASO_VENTANA, REGISTRO,
                   TAM_VENTANA, normalizar_columnas)


def cargar_ecg(registro=REGISTRO, base=BASE_PHYSIONET, canal=CANAL):
    """
    Baja un registro de PhysioNet y devuelve un canal.

    Inputs:
    -------
    registro: Identificador del registro, por ejemplo "100"
    base: Coleccion de PhysioNet, por ejemplo "mitdb"
    canal: Cual de los dos canales del registro se usa

    Returns:
    -------
    tuple: (senal en milivolts como arreglo de 1 dimension,
            frecuencia de muestreo en Hz)

    """
    lectura = wfdb.rdrecord(registro, pn_dir=base)

    return lectura.p_signal[:, canal], lectura.fs


def partir_en_ventanas(senal, tam=TAM_VENTANA, paso=PASO_VENTANA):
    """
    Corta la senal en ventanas y las acomoda como columnas.
    La ultima ventana incompleta se descarta en vez de rellenarla con
    ceros, porque un relleno artificial seria una forma de onda que no
    existe en la senal y el diccionario acabaria aprendiendola

    Inputs:
    -------
    senal: Arreglo de 1 dimension con la senal completa
    tam: Cuantas muestras por ventana
    paso: Separacion entre inicios de ventana. Igual a tam para que no
          se traslapen

    Returns:
    -------
    ndarray: Matriz de tam por numero de ventanas

    """
    inicios = range(0, len(senal) - tam + 1, paso)
    ventanas = [senal[i:i + tam] for i in inicios]

    return np.array(ventanas, dtype="float64").T


def construir_x(senal, tam=TAM_VENTANA, paso=PASO_VENTANA):
    """
    Arma la matriz de entrenamiento X.
    A cada ventana se le quita su media y luego se normaliza, asi que
    las columnas de X viven en la esfera unitaria y lo unico que las
    distingue es la forma de onda, no su amplitud ni su nivel de
    continua

    Inputs:
    -------
    senal: Arreglo de 1 dimension con la senal completa
    tam: Cuantas muestras por ventana
    paso: Separacion entre inicios de ventana

    Returns:
    -------
    ndarray: Matriz tam por numero de ventanas, columnas de norma 1

    """
    ventanas = partir_en_ventanas(senal, tam, paso)
    centradas = ventanas - ventanas.mean(axis=0, keepdims=True)

    return normalizar_columnas(centradas)


def construir_x_registros(registros, base=BASE_PHYSIONET, canal=CANAL,
                          tam=TAM_VENTANA, paso=PASO_VENTANA):
    """
    Arma X con las ventanas de varios pacientes.
    Cada registro se carga y se ventanea por separado, y las matrices se
    pegan por columnas. Ventanear la concatenacion de las senales daria
    ventanas que empiezan en un paciente y terminan en otro, una forma
    de onda que no existe

    Inputs:
    -------
    registros: Identificadores de los registros, por ejemplo
               ("100", "101") o REGISTROS_MITDB para todos
    base: Coleccion de PhysioNet
    canal: Cual de los dos canales de cada registro se usa
    tam: Cuantas muestras por ventana
    paso: Separacion entre inicios de ventana

    Returns:
    -------
    tuple: (X de tam por total de ventanas, arreglo con el registro de
            origen de cada columna, frecuencia de muestreo en Hz)

    """
    bloques, origen = [], []
    fs = None

    for registro in registros:
        senal, fs = cargar_ecg(registro, base, canal)
        x = construir_x(senal, tam, paso)
        bloques.append(x)
        origen.extend([registro] * x.shape[1])

    return np.hstack(bloques), np.array(origen), fs


def main():
    """
    Prueba de humo: baja el registro y reporta la X que sale.

    Inputs:
    -------
    None

    Returns:
    -------
    None: Solo imprime

    """
    senal, fs = cargar_ecg()
    print(f"registro {REGISTRO} de {BASE_PHYSIONET}, canal {CANAL}")
    print(f"  {len(senal)} muestras a {fs} Hz, "
          f"{len(senal) / fs / 60:.1f} minutos")

    x = construir_x(senal)
    print(f"\nX de {x.shape[0]} x {x.shape[1]}, "
          f"ventanas de {TAM_VENTANA} muestras "
          f"({TAM_VENTANA / fs * 1000:.0f} ms)")
    print(f"  normas de columna: min {np.linalg.norm(x, axis=0).min():.4f}"
          f"  max {np.linalg.norm(x, axis=0).max():.4f}")


if __name__ == "__main__":
    main()


############################### END OF DATOS.PY ################################
################################################################################
