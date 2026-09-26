<!--
README.md
========================

Descripción:
------------
Cómo instalar Quarto y ver las presentaciones de esta carpeta en
Windows, Linux y macOS, más los atajos de teclado para exponer con la
vista del presentador.


Considerations:
------------
- Probado con Quarto 1.10.18 en macOS
- Las presentaciones se compilan con `embed-resources`: el `.html` sale
  como un solo archivo con reveal.js, imágenes, KaTeX y fuentes adentro,
  así que se puede mandar solo y abrir sin internet ni Quarto


Metadata:
----------
* Author: zxxz6 (Bryan Violante Arriaga)
* Version: 1.1.0
* License: Copyright (c) 2026 Bryan Violante Arriaga.


History:
------------
Author      Date            Description
zxxz6       26/09/2026      El HTML ahora es un solo archivo
zxxz6       26/09/2026      Creation


-->

# Presentaciones

Exposiciones de Aprendizaje Computacional hechas en
[Quarto](https://quarto.org) con reveal.js.

- `Tame.qmd`: TAME, destilación de datos tabulares por alineación de
  momentos. Las figuras viven en `img/`.

## 1. Instalar Quarto

Solo se hace una vez. Después de instalar, abre una terminal nueva y
confirma con `quarto --version`.

### macOS

Con [Homebrew](https://brew.sh):

```bash
brew install --cask quarto
```

### Windows

En PowerShell:

```powershell
winget install --id Posit.Quarto
```

Si no tienes `winget`, descarga el instalador `.msi` de
<https://quarto.org/docs/get-started/> y sigue el asistente.

### Linux

Debian y Ubuntu:

```bash
curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
sudo dpkg -i quarto-linux-amd64.deb
```

Otras distribuciones: descarga el `.tar.gz` de
<https://quarto.org/docs/get-started/>, descomprímelo y agrega su
carpeta `bin/` al `PATH`.

## 2. Ver la presentación

Desde la raíz del repositorio, entra a esta carpeta:

```bash
cd machine_learning/presentaciones
```

**Opción A, vista previa.** Compila, abre el navegador y recarga sola
cada vez que guardas el `.qmd`. Es la forma cómoda de editar:

```bash
quarto preview Tame.qmd
```

Se detiene con `Ctrl+C`.

**Opción B, compilar y abrir.** Genera `Tame.html`, un solo archivo
con todo adentro; después se abre como cualquier página:

```bash
quarto render Tame.qmd
```

| Sistema | Abrir el HTML |
|---|---|
| macOS | `open Tame.html` |
| Linux | `xdg-open Tame.html` |
| Windows (PowerShell) | `Start-Process Tame.html` |
| Windows (cmd) | `start Tame.html` |

Ese `Tame.html` se puede copiar solo a otra máquina, mandar por correo
o abrir desde una USB: no necesita Quarto, internet ni otros archivos.
Compilarlo tarda más que la vista previa porque incrusta todo.

## 3. Exponer

Con la presentación abierta en el navegador:

| Tecla | Qué hace |
|---|---|
| Flechas o espacio | Avanzar y retroceder, incluidos los pasos animados |
| `S` | Vista del presentador en otra ventana: notas, siguiente diapositiva y cronómetro |
| `F` | Pantalla completa |
| `Esc` u `O` | Vista general de todas las diapositivas |
| `M` | Menú con el índice |

La vista del presentador se abre como ventana emergente: si no aparece,
permite las ventanas emergentes para esa página. En el proyector se
deja la ventana original a pantalla completa y la del presentador en la
laptop.

<!--
############################### END OF README.MD ###############################
################################################################################
-->
