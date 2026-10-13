#!/usr/bin/env bash
# Instala dependencias (Ubuntu/Debian) y genera los parsers de ANTLR.
set -e
sudo apt update
sudo apt install -y antlr4 default-jre python3 python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requisitos.txt
for d in ej1 ej3; do
  (cd $d && for g in *.g4; do antlr4 -Dlanguage=Python3 -visitor -listener "$g"; done)
done
echo "Listo. Ahora ejecuta: ./run_all.sh"
