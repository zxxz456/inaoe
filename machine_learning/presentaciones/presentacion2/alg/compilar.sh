#!/usr/bin/env bash
# Compila cada algN_*.tex a ../img/algN_*.svg (recortado al contenido).
set -e
cd "$(dirname "$0")"
for f in alg[0-9]*_*.tex; do
  b="${f%.tex}"
  pdflatex -interaction=nonstopmode -halt-on-error "$f" > /dev/null || { echo "fallo $f"; tail -30 "$b.log"; exit 1; }
  pdfcrop --margins 4 "$b.pdf" "$b-crop.pdf" > /dev/null
  pdftocairo -svg "$b-crop.pdf" "../img/$b.svg"
  echo "$b -> img/$b.svg"
done
rm -f *.aux *.log *-crop.pdf
