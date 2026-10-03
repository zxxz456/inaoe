<!--
README.md
========================


Descripcion:
------------
Enunciado del proyecto 1 de Matematicas para la Computacion:
representaciones dispersas con Dictionary Learning, implementando
K-SVD sobre la descomposicion en valores singulares


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0


History:
------------
Author      Date            Description
zxxz6       03/10/2026      Quite la seccion Considerations del encabezado
zxxz6       03/10/2026      La documentacion pasa a un solo PDF
zxxz6       02/10/2026      Enlace a la documentacion de docs/
zxxz6       30/09/2026      Creation


-->

# Proyecto 1: Representaciones dispersas usando Dictionary Learning con SVD

## Objetivo

Implementar K-SVD y obtener una base entrenada para algun tipo de senal, de
manera que se pueda comparar la entrada (senal original) con su reconstruccion
respectiva, hecha a partir de la senal dispersa.

La explicacion completa del metodo, desde cero y con ejemplos resueltos a mano,
esta en [docs/ExplicacionKsvd.pdf](docs/ExplicacionKsvd.pdf). Su fuente es
`docs/ExplicacionKsvd.tex`, y se compila desde `docs/` con `latexmk -pdf`.

## Representaciones dispersas

Una senal `x` en R^n es **dispersa** si la mayoria de sus entradas son cero, es
decir, si el conjunto de posiciones distintas de cero

```
Lambda(x) = { i : 1 <= i <= n , x[i] != 0 }
```

tiene cardinalidad `k << n`.

Una senal `x` se modela como combinacion lineal de `m` senales elementales
llamadas **atomos**:

```
x = D alpha = suma_{i=1..m} alpha[i] d_i

  D       matriz diccionario, contiene las senales elementales
  d_i     atomo, la columna i de D
  alpha   vector de coeficientes
```

Las senales dispersas en `D` son las que se pueden escribir exactamente como
combinacion de una pequena fraccion de los atomos `d_i`.

Dado un diccionario hay dos operaciones posibles:

| Operacion | Que hace | Expresion |
|---|---|---|
| Analisis | dispersion | `alpha = D' x` |
| Sintesis | reconstruccion aproximada | `x ~= D alpha` |

## Construccion del diccionario

Hay dos caminos:

- **Diccionarios fijos (predefinidos).** Para senales de un tipo conocido.
  Menor tiempo de procesamiento.
- **Diccionarios aprendidos (entrenados).** Para senales sin un tipo bien
  definido. Mayor tiempo de procesamiento. Es lo que pide el proyecto.

El diccionario `D` contiene `m` formas de onda de longitud `k`, o sea que es de
`k x m`. Como `m > k`, el sistema `x = D alpha` queda subdeterminado y tiene
infinitas soluciones; de todas ellas se busca la mas dispersa.

Las dos preguntas que resuelve el proyecto:

1. Como se obtiene la mejor dispersion de una senal. Lo resuelve OMP.
2. Como se obtiene el diccionario que funciona mejor para nuestro tipo de
   senal. Lo resuelve K-SVD.

> El diccionario debe **aprender** a reconocer las senales de un tipo
> especifico.

## Orthogonal Matching Pursuit (OMP)

Busca una solucion aproximada para la dispersion de `x` en `D`, seleccionando y
combinando atomos que minimicen una restriccion de error.

```
Entradas: D, x, epsilon

  r_0 = x                      residual inicial
  e   = algo mucho mayor que epsilon
  j   = 1

  Mientras e > epsilon:
    i     = argmax | D' r_{j-1} |   atomo de mayor producto interno con el
                                    residual, o sea mayor correlacion
    I(j)  = i ,  j = j + 1          se agrega al conjunto de atomos elegidos
    alpha = pinv(D_I) x             coeficientes asociados a I
    r_j   = x - D_I alpha           residual de la j-esima descomposicion
    e     = ||r_j||_2 / ||x||_2     error relativo

Salidas: alpha, r_j
```

Encuentra los coeficientes `alpha` asociados a las senales elementales en que
fue descompuesta la senal `x`, y su respectivo residual `r`.

## Dictionary Learning con K-SVD

El objetivo es proveer una base `D` adecuada para obtener la mejor
representacion dispersa de las senales. Alterna dos pasos: con `D` fijo calcula
las dispersiones con OMP, y con las dispersiones fijas actualiza `D` atomo por
atomo.

```
Entradas: D_0, X, K

  Para k = 1..K:
    alpha_k = OMP(D_{k-1}, X, 0.1)        dispersion de todas las senales

    Para j = 1..m:
      w       = { l : alpha_k[j,l] != 0 } senales en cuya dispersion
                                          participa el j-esimo atomo
      alpha_w = alpha_k[:, w] con la fila j puesta a cero
      R       = X_w - D_k alpha_w         residual de la reconstruccion de X_w
      [U, Delta, V] = SVD(R)              factorizacion del residual
      d_j     = u_1                       actualizacion del atomo
      alpha_j = Delta(1,1) * v_1          actualizacion de sus coeficientes

Salida: D_T
```

**De donde sale la SVD.** El producto `d_j alpha_j'` es columna por renglon, o
sea una matriz de rango 1. Preguntar cual es el mejor atomo equivale a
preguntar cual es la mejor aproximacion de rango 1 del residual `R`, y eso lo
contesta el teorema de Eckart-Young: `R ~= sigma_1 u_1 v_1'`. De ahi salen
`d_j = u_1` y `alpha_j = sigma_1 v_1`. Una SVD por atomo y por iteracion, que
es lo que le da el nombre al algoritmo.

**Por que solo las senales de `w`.** Se asume que el residual corresponde al
j-esimo atomo porque, aunque esta involucrado en la descomposicion de las
senales en `w`, de momento no participa en su reconstruccion: su fila se puso a
cero. Si la actualizacion usara todas las senales y no solo las de `w`, el
atomo entraria en senales que no lo usaban y se destruiria la dispersion que
OMP acababa de construir.







<!--
############################### END OF README.MD ###############################
################################################################################
-->
