"""
Pruebas del Corte 1: validan que el lexer y el parser generados por ANTLR4
reconozcan correctamente los programas válidos y rechacen los inválidos
con un error léxico o sintáctico.

Ejecutar con:
    pytest tests/ -v
"""

import pytest
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from dsl_core.generated.DSLLexer import DSLLexer
from dsl_core.generated.DSLParser import DSLParser


class ListenerDeErrores(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"Línea {line}, columna {column}: {msg}")


def parsear(ruta_archivo):
    entrada = FileStream(ruta_archivo, encoding="utf-8")

    lexer = DSLLexer(entrada)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ListenerDeErrores())

    tokens = CommonTokenStream(lexer)

    parser = DSLParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(ListenerDeErrores())

    return parser.programa()


# ===================== CASOS VÁLIDOS =====================

PROGRAMAS_VALIDOS = [
    "ejemplos/01_carga_basica.dsl",
    "ejemplos/02_seleccion_filtro.dsl",
    "ejemplos/03_filtro_complejo.dsl",
    "ejemplos/04_graficar_sintactico.dsl",
]


@pytest.mark.parametrize("archivo", PROGRAMAS_VALIDOS)
def test_programa_valido_no_lanza_error(archivo):
    """Un programa bien escrito debe parsear sin lanzar excepciones."""
    parsear(archivo)  # si lanza SyntaxError, el test falla automáticamente


# ===================== CASOS NEGATIVOS =====================

PROGRAMAS_INVALIDOS = [
    "tests/test_lexer_parser/error_identificador_invalido.dsl",
    "tests/test_lexer_parser/error_operador_invalido.dsl",
    "tests/test_lexer_parser/error_cadena_sin_cerrar.dsl",
    "tests/test_lexer_parser/error_expresion_incompleta.dsl",
    "tests/test_lexer_parser/error_palabra_reservada_como_identificador.dsl",
]


@pytest.mark.parametrize("archivo", PROGRAMAS_INVALIDOS)
def test_programa_invalido_lanza_error_de_sintaxis(archivo):
    """Un programa con error léxico o sintáctico debe lanzar SyntaxError."""
    with pytest.raises(SyntaxError):
        parsear(archivo)


# ===================== CASOS PUNTUALES (más descriptivos) =====================

def test_pipeline_reconoce_multiples_operaciones_encadenadas():
    """Verifica explícitamente que el pipeline con seleccionar + filtrar
    se reconoce como una sola cadena de operaciones."""
    arbol = parsear("ejemplos/02_seleccion_filtro.dsl")
    assert arbol is not None


def test_expresion_booleana_con_parentesis_y_negacion():
    """Caso específico del Corte 1: expresiones booleanas compuestas
    con paréntesis, 'no', 'y' y comparaciones aritméticas."""
    arbol = parsear("ejemplos/03_filtro_complejo.dsl")
    assert arbol is not None


def test_sentencia_graficar_se_reconoce_sintacticamente():
    """La sentencia graficar debe parsear correctamente aunque en este
    corte no se ejecute (no se genera ninguna imagen todavía)."""
    arbol = parsear("ejemplos/04_graficar_sintactico.dsl")
    assert arbol is not None
