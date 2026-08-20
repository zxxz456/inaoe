<!--
ReferenciaLatex.md
========================


Descripción:
------------
Chuleta de LaTeX para tomar apuntes: los comandos y las fórmulas que
salen a cada rato, con el resultado descrito en palabras para no tener
que compilar solo por ver qué hace uno. Acompaña a
PlantillaApuntes.tex, y las secciones de entornos, cajas y
pseudocódigo asumen el preámbulo de Preambulo.tex.


Considerations:
------------
- Todo el código va en bloques cercados, que es lo que el checker de
  estilo omite; la prosa se queda en ASCII salvo los acentos
- La columna "Qué produce" describe el símbolo con palabras a
  propósito: pegar el símbolo Unicode en la tabla viola la regla 10
- Solo entra lo que se usa de verdad en clase, no el manual completo
- Los ejemplos se compilaron contra PlantillaApuntes.tex antes de
  quedar aquí


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.3.0
* License: Copyright (c) 2026 Bryan Violante Arriaga.


History:
------------
Author      Date            Description
zxxz6       19/08/2026      Documente \profesor con varios nombres
zxxz6       18/08/2026      Documente el preambulo compartido
zxxz6       18/08/2026      Agregue la seccion de pseudocodigo
zxxz6       18/08/2026      Creation


-->

# Referencia rápida de LaTeX

Chuleta para llenar [`PlantillaApuntes.tex`](PlantillaApuntes.tex). Lo que se usa seguido está arriba; lo que se consulta una vez al mes, abajo.

## Empezar una libreta

El preámbulo no se copia: vive en [`Preambulo.tex`](Preambulo.tex) y cada documento lo carga con `\input`. Un arreglo ahí llega a todas las libretas de una vez.

```latex
\documentclass[11pt,letterpaper]{article}

\newcommand{\materia}{Analisis y Diseno de Algoritmos}
\newcommand{\profesor}{Dr. Jose Martinez Carranza}
\newcommand{\periodo}{Otono 2026}
\newcommand{\alumno}{Bryan Ezequiel Violante Arriaga}

\input{../../templates/Preambulo.tex}

\begin{document}
\portadilla
\newpage

\clase{Tema de la sesion}{18 de agosto de 2026}
...
\end{document}
```

Tres cosas que truenan si se hacen al revés:

- **Los cuatro datos van antes del `\input`.** hyperref expande `\materia` al cargarse; si todavía no existe, la compilación falla con `Undefined control sequence`.
- **La ruta del `\input` es relativa al documento**, no a la raíz del repo. Desde `ada/apuntes/` son `../../templates/`. `\usepackage` no sirve aquí: solo busca en la carpeta del documento y en el árbol de TeX.
- **Un `\newcommand` por dato, nunca dos.** El segundo falla con `Command \profesor already defined`.

### Materias con dos o más profesores

Los nombres van en un solo `\profesor`, separados por `\\`:

```latex
\newcommand{\profesor}{Dra. Delia Irazu Hernandez Farias \\
                       Dr. Manuel Montes y Gomez}
```

Salen apilados y centrados debajo del título, uno por renglón. Funciona porque la portadilla imprime ese renglón dentro de un `center`, que es donde `\\` corta línea. No hay límite de nombres y el caso de un solo profesor no cambia.

`latexmk` se da cuenta de que `Preambulo.tex` es una dependencia, así que recompila solo cuando cambia.

---

## Compilar

```bash
pdflatex Apuntes.tex     # dos veces: la segunda arma el indice
latexmk -pdf Apuntes.tex # o esto, que repite las pasadas solo
latexmk -c               # borra los .aux, .log y demas basura
```

---

## 1. Texto

| Comando | Qué produce |
|---|---|
| `\textbf{texto}` | Negrita |
| `\emph{texto}` | Cursiva |
| `\texttt{texto}` | Monoespaciado, para nombres de variables |
| `\underline{texto}` | Subrayado |
| `\footnote{nota}` | Nota al pie |
| `\\` | Salto de línea forzado |
| `\par` o línea en blanco | Párrafo nuevo |
| `\newpage` | Salta a la página siguiente |
| `%` | Comentario: LaTeX ignora el resto de la línea |

Los caracteres `# $ % & _ { } ~ ^ \` son especiales. Para escribirlos tal cual:

```latex
\# \$ \% \& \_ \{ \} \textasciitilde{} \textasciicircum{} \textbackslash{}
```

Espaciado que a veces hace falta:

```latex
palabra~siguiente   % espacio que no se parte al final del renglon
\quad  \qquad       % espacio horizontal mediano y grande
\vspace{1em}        % espacio vertical
\hfill              % empuja lo que sigue hasta el margen derecho
```

---

## 2. Secciones y listas

```latex
\section{Titulo}          \subsection{Subtitulo}
\subsubsection{Sub-sub}   \paragraph{Titulillo en linea}
\section*{Sin numero}     % el asterisco lo saca del indice
```

```latex
\begin{itemize}
  \item Sin numerar
\end{itemize}

\begin{enumerate}[label=\arabic*., itemsep=0.2em]
  \item Numerado; label acepta \alph*, \roman*, \Roman*
\end{enumerate}

\begin{description}
  \item[Termino] Su explicacion. Sirve para glosarios.
\end{description}
```

---

## 3. Matemáticas: las dos formas

```latex
En medio de la frase va $f(n) = n^2$, entre signos de pesos.

Aparte y centrada, sin numero:
\[
  f(n) = n^2
\]

Aparte y numerada, para poder referirla:
\begin{equation}\label{eq:cuadratica}
  f(n) = n^2
\end{equation}
```

Dentro de matemáticas, el texto normal necesita `\text{...}`:

```latex
\[ x \geq 0 \quad \text{para toda } x \in \R \]
```

---

## 4. Subíndices, potencias, fracciones, raíces

```latex
x^2          x^{n+1}        % potencia; con mas de un caracter, llaves
x_i          x_{i,j}        % subindice
x_i^2                       % los dos juntos
\frac{a}{b}                 % fraccion
\tfrac{a}{b}                % fraccion chica, para texto en linea
\sqrt{x}     \sqrt[3]{x}    % raiz cuadrada y cubica
\binom{n}{k}                % coeficiente binomial
\overline{x}  \hat{x}  \vec{v}  \dot{x}   % acentos matematicos
```

---

## 5. Símbolos que salen a cada rato

**Letras griegas.** Minúscula con el nombre en minúsculas, mayúscula con la inicial en mayúscula:

```latex
\alpha \beta \gamma \delta \epsilon \varepsilon \theta \lambda
\mu \pi \rho \sigma \tau \phi \varphi \omega
\Gamma \Delta \Theta \Lambda \Pi \Sigma \Phi \Omega
```

**Relaciones.**

| Comando | Qué produce |
|---|---|
| `\leq` `\geq` | Menor o igual, mayor o igual |
| `\neq` | Distinto |
| `\approx` | Aproximadamente igual |
| `\equiv` | Equivalente, congruente |
| `\sim` | Semejante, del orden de |
| `\propto` | Proporcional a |
| `\ll` `\gg` | Mucho menor, mucho mayor |

**Conjuntos y lógica.**

| Comando | Qué produce |
|---|---|
| `\in` `\notin` | Pertenece, no pertenece |
| `\subset` `\subseteq` | Subconjunto, subconjunto o igual |
| `\cup` `\cap` | Unión, intersección |
| `\setminus` | Diferencia de conjuntos |
| `\emptyset` | Conjunto vacío |
| `\forall` `\exists` | Para todo, existe |
| `\land` `\lor` `\lnot` | Y, o, negación |
| `\mid` | Barra vertical: "tal que" o "divide a" |

**Flechas y otros.**

| Comando | Qué produce |
|---|---|
| `\to` o `\rightarrow` | Flecha a la derecha; funciones y límites |
| `\Rightarrow` | Flecha doble: implica |
| `\iff` o `\Leftrightarrow` | Si y solo si |
| `\mapsto` | Flecha con barra: "va a dar a" |
| `\cdot` | Punto de multiplicación |
| `\times` | Aspa: producto cartesiano o multiplicación |
| `\infty` | Infinito |
| `\ldots` `\cdots` | Puntos suspensivos, en línea base y centrados |
| `\pm` | Más menos |

Los conjuntos numéricos ya vienen abreviados en la plantilla: `\N \Z \Q \R \C`. Sin ella se escriben `\mathbb{N}` y hace falta `amssymb`.

---

## 6. Sumas, productos, integrales, límites

```latex
\sum_{i=1}^{n} i           \prod_{i=1}^{n} a_i
\int_{a}^{b} f(x)\,dx      \iint  \oint
\lim_{n \to \infty} a_n    \max_{x \in S} f(x)
\bigcup_{i=1}^{n} A_i      \bigcap_{i=1}^{n} A_i
```

En modo display los límites salen arriba y abajo; en línea, al lado. Para forzarlo: `\sum\limits_{i=1}^{n}`.

El `\,` antes de `dx` es un espacio fino, y sin él la integral se ve apretada.

---

## 7. Delimitadores que crecen

```latex
\left( \frac{a}{b} \right)    % parentesis del tamano del contenido
\left[ ... \right]            % corchetes
\left\{ ... \right\}          % llaves; ojo con la barra invertida
\left\lvert x \right\rvert    % valor absoluto
\left\lVert v \right\rVert    % norma
\left. ... \right|            % solo un lado: el punto es el lado mudo
```

La plantilla ya trae `\abs{x}`, `\norm{v}` y `\set{...}` para no escribir todo eso.

---

## 8. Matrices y vectores

```latex
\begin{pmatrix} a & b \\ c & d \end{pmatrix}   % parentesis
\begin{bmatrix} a & b \\ c & d \end{bmatrix}   % corchetes
\begin{vmatrix} a & b \\ c & d \end{vmatrix}   % determinante
```

`&` separa columnas y `\\` separa renglones. Para una matriz con puntos suspensivos:

```latex
\begin{bmatrix}
  a_{11} & \cdots & a_{1n} \\
  \vdots & \ddots & \vdots \\
  a_{m1} & \cdots & a_{mn}
\end{bmatrix}
```

---

## 9. Varias líneas alineadas y casos

```latex
\begin{align}
  T(n) &= 2T(n/2) + n \\      % el & marca por donde alinea
       &= 4T(n/4) + 2n \nonumber \\   % nonumber quita el numero
       &= \Ord{n \log n}
\end{align}
```

`align*` no numera nada. Para partir una sola ecuación larga se usa `split` dentro de `equation`.

Definición por casos:

```latex
f(n) =
\begin{cases}
  1              & \text{si } n = 0, \\
  n \cdot f(n-1) & \text{si } n > 0.
\end{cases}
```

---

## 10. Entornos de la plantilla

Numeran por sección, o sea que reinician en cada clase. Todos aceptan un título opcional entre corchetes. El nombre va sin acento aunque el rótulo impreso sí lo lleve.

```latex
\begin{definicion}[Grafo conexo] ... \end{definicion}
\begin{teorema}[Handshake] ... \end{teorema}
\begin{lema} ... \end{lema}
\begin{corolario} ... \end{corolario}
\begin{proposicion} ... \end{proposicion}
\begin{ejemplo} ... \end{ejemplo}
\begin{ejercicio} ... \end{ejercicio}
\begin{observacion} ... \end{observacion}   % sin numero
\begin{proof} ... \end{proof}               % pone el cuadrito al final
```

Las tres cajas de color:

```latex
\begin{idea} Lo que hay que recordar. \end{idea}
\begin{ojo} Donde siempre me equivoco. \end{ojo}
\begin{pendiente} Lo que hay que preguntar. \end{pendiente}
```

Y el encabezado de cada sesión, con la fecha alineada a la derecha:

```latex
\clase{Arboles binarios de busqueda}{18 de agosto de 2026}
```

---

## 11. Tablas

```latex
\begin{table}[htbp]
  \centering
  \begin{tabular}{lcr}     % l izquierda, c centro, r derecha
    \toprule
    \textbf{Caso} & \textbf{Costo} & \textbf{Nota} \\
    \midrule
    Mejor  & $\Ord{1}$      & Primer intento  \\
    Peor   & $\Ord{n}$      & Recorre todo    \\
    \bottomrule
  \end{tabular}
  \caption{Lo que compara la tabla.}
  \label{tab:costos}
\end{table}
```

`p{3cm}` en vez de `l` da una columna de ancho fijo que parte el texto en varios renglones. `\multicolumn{2}{c}{Titulo}` junta dos celdas.

---

## 12. Figuras

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\linewidth]{pizarron.png}
  \caption{Lo que dibujo el profesor.}
  \label{fig:pizarron}
\end{figure}
```

El `[htbp]` es el orden en que LaTeX intenta colocarla: aquí, arriba, abajo, página aparte. Formatos que acepta pdflatex: `.png`, `.jpg`, `.pdf`. Nada de `.svg` sin convertir antes.

---

## 13. Código

```latex
\begin{lstlisting}[language=Python,caption={Factorial}]
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)
\end{lstlisting}
```

`language` acepta `C`, `C++`, `Python`, `Java`, `bash` y varios más. Para una línea suelta en medio del texto: `\lstinline|printf("hola")|`. Para pegar un archivo entero sin copiarlo:

```latex
\lstinputlisting[language=C,firstline=10,lastline=40]{Lista.c}
```

---

## 14. Pseudocódigo

Cuando lo del pizarrón es el algoritmo y no el programa. El flotante lo pone `algorithm` y el cuerpo `algorithmicx`; se numera por sesión, igual que los teoremas.

```latex
\begin{algorithm}[htbp]
  \caption{Busqueda binaria}
  \label{alg:binaria}
  \begin{algorithmic}[1]
    \Require arreglo ordenado $A[1 \ldots n]$, valor $x$
    \Ensure el indice de $x$ en $A$, o $-1$ si no esta
    \Procedure{BusquedaBinaria}{$A, n, x$}
      \State $\mathit{izq} \gets 1$
      \State $\mathit{der} \gets n$
      \While{$\mathit{izq} \le \mathit{der}$}
        \State $m \gets \lfloor (\mathit{izq} + \mathit{der}) / 2 \rfloor$
        \If{$A[m] = x$}
          \State \Return $m$
        \ElsIf{$A[m] < x$}
          \State $\mathit{izq} \gets m + 1$
        \Else
          \State $\mathit{der} \gets m - 1$
        \EndIf
      \EndWhile
      \State \Return $-1$
    \EndProcedure
  \end{algorithmic}
\end{algorithm}
```

Las palabras clave se escriben en inglés y salen impresas en español, porque el preámbulo las renombra una por una:

| Se escribe | Sale impreso |
|---|---|
| `\Require` / `\Ensure` | **Entrada:** / **Salida:** |
| `\If{...}` ... `\ElsIf{...}` ... `\Else` ... `\EndIf` | **si** ... **entonces** / **si no** / **fin si** |
| `\For{...}` ... `\EndFor` | **para** ... **hacer** / **fin para** |
| `\ForAll{...}` ... `\EndFor` | **para todo** ... **hacer** / **fin para** |
| `\While{...}` ... `\EndWhile` | **mientras** ... **hacer** / **fin mientras** |
| `\Repeat` ... `\Until{...}` | **repetir** / **hasta que** |
| `\Procedure{Nombre}{args}` ... `\EndProcedure` | **procedimiento** Nombre(args) / **fin procedimiento** |
| `\Function{Nombre}{args}` ... `\EndFunction` | **función** Nombre(args) / **fin función** |
| `\Return` | **devolver** |
| `\Hasta` | **hasta**, para el `\For` |
| `\Intercambiar` | **intercambiar** |

Lo demás que hace falta:

```latex
\State  ...          % una linea suelta del algoritmo
\Statex ...          % linea sin numero, sirve para separar procedimientos
\Comment{por que}   % comentario a la derecha, en verde
\Call{Nombre}{args} % llamada a otro procedimiento, en versalitas
$a \gets b$          % la flecha de asignacion
```

`\Hasta` e `\Intercambiar` no vienen en el paquete, las define la plantilla. Los nombres de variable de más de una letra van en `\mathit{...}`, si no LaTeX los lee como un producto y los separa.

---

## 15. Referencias cruzadas

```latex
\label{eq:cuadratica}     % justo despues del caption o dentro del entorno
\eqref{eq:cuadratica}     % ecuaciones, con los parentesis puestos
\ref{tab:costos}          % tablas, figuras, secciones
\autoref{fig:pizarron}    % agrega la palabra "Figura" solo, con hyperref
\pageref{sec:intro}       % en que pagina quedo
```

Los prefijos `eq:`, `fig:`, `tab:`, `sec:` no son obligatorios, pero cuando hay cincuenta etiquetas se agradecen. Las referencias necesitan dos pasadas de `pdflatex`; si salen como `??`, falta compilar otra vez.

---

## 16. Acentos y español

Con `\usepackage[utf8]{inputenc}` se escriben directo desde el teclado: más, niño, acción. Los comandos solo hacen falta si algo se rompe:

```latex
\'a \'e \'i \'o \'u    % acento agudo
\~n \~N                % enie
\"u                    % dieresis
?` !`                  % signos de apertura
```

En modo matemático no se escriben acentos: se usa `\text{...}` para meter una palabra acentuada dentro de una fórmula.

La plantilla carga babel con `es-noshorthands`. Sin esa opción, el español deja activo el carácter de comilla recta y se come el texto que le sigue, además de romper `listings` y las URL.

---

## 17. Lo que suele romper la compilación

| Síntoma | Causa casi siempre |
|---|---|
| `Missing $ inserted` | Un `_`, `^` o `\alpha` fuera de modo matemático |
| `Undefined control sequence` | Comando mal escrito, o falta el paquete que lo define |
| `Missing \begin{document}` | Algo de texto quedó arriba del `\begin{document}` |
| Referencias en `??` | Falta la segunda pasada de pdflatex |
| `Runaway argument` | Falta una llave de cierre, o hay una línea en blanco dentro de un comando |
| `File not found` | La imagen no está en la carpeta, o falta la extensión |
| La tabla se sale de la hoja | Cambiar columnas a `p{3cm}`, o usar `\small` |
| Una figura se va al final | Normal: LaTeX la reacomoda. Con `[H]` y `float` se clava en su lugar |

Cuando el error no se entiende, se busca la primera línea del `.log` que empieza con `!`: esa es la real, las de abajo son consecuencia.

<!--
########################## END OF REFERENCIALATEX.MD ###########################
################################################################################
-->
