#!/usr/bin/env bash
# Ejecuta los tres ejercicios.
set -e
source .venv/bin/activate
echo "##### EJERCICIO 1 y 2: pruebas #####";   (cd ej1 && python3 pruebas.py)
echo; echo "##### EJERCICIO 2: formas de árbol #####"; (cd ej1 && python3 arboles.py "3 + 4 * 5")
echo; echo "##### EJERCICIO 3: ambigüedad #####";  (cd ej3 && python3 ambiguedad.py)
