# DSL de Ciencia de Datos y Visualización — Corte 1

DSL declarativo para flujos de análisis de datos (dominio: ventas/comercio),
construido con ANTLR4 + Python. Corte 1: gramática, lexer/parser, sin ejecución
todavía (eso es Corte 2 y 3).

## Requisitos

- Ubuntu con Java (JDK) instalado: `sudo apt install -y default-jdk`
- Python 3.11+
- ANTLR4 (versión 4.13.2, debe coincidir con `antlr4-python3-runtime`)

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install antlr4-tools   # o usar el .jar directamente, ver abajo
```

## Generar el lexer y el parser

```bash
cd grammar
antlr4 -Dlanguage=Python3 -visitor -o ../dsl_core/generated DSL.g4
cd ..
```

Si usan el `.jar` en vez de `antlr4-tools`:

```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o dsl_core/generated grammar/DSL.g4
```

Esto crea `dsl_core/generated/DSLLexer.py`, `DSLParser.py` y `DSLVisitor.py`.
Asegúrense de que `dsl_core/` tenga un `__init__.py` (puede estar vacío) para
que sea importable como paquete Python.

## Probar el parser manualmente

```bash
python cli/probar_parser.py ejemplos/01_carga_basica.dsl
```

Debe imprimir el árbol de análisis sintáctico si el programa es válido, o el
error con línea y columna si no lo es.

## Correr las pruebas automatizadas

```bash
pytest tests/ -v
```

## Estructura de este corte

```
grammar/DSL.g4                        # gramática ANTLR4
dsl_core/generated/                   # generado por ANTLR (no se edita a mano)
ejemplos/*.dsl                        # programas válidos de referencia
tests/test_lexer_parser/*.dsl         # casos negativos (errores esperados)
tests/test_lexer_parser/test_programas.py   # pruebas con pytest
cli/probar_parser.py                  # herramienta de desarrollo
docs/gramatica.md                     # especificación completa + EBNF + justificación
```

## Alcance de este corte

Implementado: asignaciones, expresiones aritméticas/booleanas, `cargar`,
`seleccionar`, `filtrar`, reconocimiento sintáctico de `graficar`.

Fuera de alcance (Corte 2/3): ejecución real sobre datos, `ordenar`,
`renombrar`, `eliminar_duplicados`, `crear`, `agrupar`/`resumir`, `guardar`,
generación real de gráficas.
