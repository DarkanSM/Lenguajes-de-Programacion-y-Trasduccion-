"""
Herramienta de desarrollo del Corte 1.

Uso:
    python cli/probar_parser.py ejemplos/01_carga_basica.dsl

Imprime el árbol de análisis sintáctico (parse tree) generado por ANTLR4,
o el error léxico/sintáctico si el programa no es válido.

NOTA: este script requiere que ya se haya generado el lexer y el parser
con ANTLR4 dentro de dsl_core/generated/ (ver Paso 6 del documento
"Paso a Paso — Corte 1").
"""

import sys
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from dsl_core.generated.DSLLexer import DSLLexer
from dsl_core.generated.DSLParser import DSLParser


class ListenerDeErrores(ErrorListener):
    """Convierte los errores internos de ANTLR en excepciones de Python
    con línea y columna, en vez de solo imprimirlos por stderr."""

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"Línea {line}, columna {column}: {msg}")


def parsear_archivo(ruta_archivo):
    entrada = FileStream(ruta_archivo, encoding="utf-8")

    lexer = DSLLexer(entrada)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ListenerDeErrores())

    tokens = CommonTokenStream(lexer)

    parser = DSLParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(ListenerDeErrores())

    return parser.programa()


def main():
    if len(sys.argv) != 2:
        print("Uso: python cli/probar_parser.py <archivo.dsl>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]

    try:
        arbol = parsear_archivo(ruta_archivo)
        print(f"✔ '{ruta_archivo}' es sintácticamente válido.\n")
        print("Árbol de análisis (parse tree):")
        # Nota: para imprimir con nombres de reglas legibles se necesita
        # el objeto parser; aquí se reconstruye rápido para el toString.
        entrada = FileStream(ruta_archivo, encoding="utf-8")
        lexer = DSLLexer(entrada)
        tokens = CommonTokenStream(lexer)
        parser = DSLParser(tokens)
        print(arbol.toStringTree(recog=parser))
    except SyntaxError as error:
        print(f"✘ Error en '{ruta_archivo}':")
        print(f"  {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
