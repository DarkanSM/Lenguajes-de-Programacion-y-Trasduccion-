# Análisis sintáctico con ANTLR 4 (target Python)

Lenguajes de Programación y Traducción – Actividades de la sesión "Análisis Sintáctico".

| Carpeta | Contenido |
|---|---|
| `ej1/` | Ejercicio 1 y 2: gramática de la diapositiva 11 + formas de árbol sintáctico (diap. 12) |
| `ej3/` | Ejercicio 3: gramática ambigua de la diapositiva 15 y pruebas de ambigüedad |

## Instalación y ejecución (Ubuntu)
    ./setup.sh      # instala antlr4, java, venv y genera los parsers
    ./run_all.sh    # ejecuta los tres ejercicios

## Ejecución manual
    sudo apt install antlr4 default-jre python3-venv
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requisitos.txt
    cd ej1 && antlr4 -Dlanguage=Python3 -visitor -listener Expr.g4
    python3 pruebas.py
    python3 arboles.py "3 + 4 * 5"
    cd ../ej3 && for g in Amb1 Amb2 Amb3; do antlr4 -Dlanguage=Python3 $g.g4; done
    python3 ambiguedad.py

> La versión del runtime de Python (`antlr4-python3-runtime`) debe coincidir con la de la herramienta `antlr4` (4.9.2 en Ubuntu 22.04/24.04).
