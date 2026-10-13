"""
Ejercicio 3: gramática de la diapositiva 15   E -> E + E | E * E | num
Se prueba si es ambigua de 3 maneras:
  A) ANTLR con la regla tal cual (reescritura por precedencia)
  B) ANTLR con una variante donde la ambigüedad no puede ocultarse
     + detector de ambigüedad de ANTLR (LL_EXACT_AMBIG_DETECTION)
  C) Conteo independiente de árboles de derivación (Catalán)
"""
import importlib
from functools import lru_cache
from antlr4 import InputStream, CommonTokenStream
from antlr4.atn.PredictionMode import PredictionMode
from antlr4.error.ErrorListener import ErrorListener


class Detector(ErrorListener):
    """Registra los reportes de ambigüedad que emite el parser."""
    def __init__(self):
        self.ambiguedades, self.errores = [], []
    def reportAmbiguity(self, recognizer, dfa, start, stop, exact, alts, configs):
        regla = recognizer.ruleNames[dfa.atnStartState.ruleIndex]
        self.ambiguedades.append((regla, start, stop, sorted(alts) if alts else None, exact))
    def syntaxError(self, recognizer, sym, line, col, msg, e):
        self.errores.append(f"{line}:{col} {msg}")


def correr(gramatica, texto, detectar=True):
    L = importlib.import_module(f"{gramatica}Lexer")
    P = importlib.import_module(f"{gramatica}Parser")
    lexer = getattr(L, f"{gramatica}Lexer")(InputStream(texto))
    parser = getattr(P, f"{gramatica}Parser")(CommonTokenStream(lexer))
    det = Detector()
    parser.removeErrorListeners(); parser.addErrorListener(det)
    if detectar:
        parser._interp.predictionMode = PredictionMode.LL_EXACT_AMBIG_DETECTION
    tree = parser.prog()
    return tree.toStringTree(recog=parser), det


# ----------------------------------------------------------------- A y B
def seccion(titulo):
    print("\n" + "=" * 72 + f"\n{titulo}\n" + "=" * 72)


def prueba_antlr():
    entradas = ["2 + 3 * 4", "2 * 3 + 4", "2 + 3 + 4", "2 * 3 * 4"]
    for g, desc in [("Amb1", "A1) e : e '+' e | e '*' e | NUM      ('+' primero)"),
                    ("Amb2", "A2) e : e '*' e | e '+' e | NUM      ('*' primero)"),
                    ("Amb3", "B ) e : NUM op e | e op NUM | NUM    (ambigüedad explícita)")]:
        seccion(desc)
        for s in entradas:
            arbol, det = correr(g, s)
            amb = "AMBIGUA" if det.ambiguedades else "sin ambigüedad detectada"
            print(f"  {s:<11} -> {arbol}")
            print(f"{'':15}[{amb}] {det.ambiguedades if det.ambiguedades else ''}")


# --------------------------------------------------------------------- C
def contar_arboles(tokens):
    """Nº de árboles de derivación de la gramática E -> E+E | E*E | num
    (programación dinámica sobre rangos de tokens)."""
    @lru_cache(None)
    def n(i, j):                       # tokens[i:j] derivado desde E
        if j - i == 1:
            return 1 if tokens[i] == "num" else 0
        total = 0
        for k in range(i + 1, j - 1):  # k = posición del operador raíz
            if tokens[k] in "+*":
                total += n(i, k) * n(k + 1, j)
        return total
    return n(0, len(tokens))


def prueba_conteo():
    seccion("C) Conteo independiente de árboles de derivación")
    print(f"  {'entrada':<46}{'operadores':>11}{'árboles':>9}")
    for ops in range(1, 8):
        toks = ["num"]
        for i in range(ops):
            toks += ["+" if i % 2 == 0 else "*", "num"]
        print(f"  {' '.join(toks):<46}{ops:>11}{contar_arboles(tuple(toks)):>9}")
    print("\n  Secuencia 1, 2, 5, 14, 42, 132, 429 = números de Catalán -> crece sin límite.")
    print("  Con 2 o más operadores hay >1 árbol ⇒ la gramática ES ambigua.")


# -------------------------------------------- enumerar los árboles de 2+3*4
def enumerar(tokens):
    @lru_cache(None)
    def arboles(i, j):
        if j - i == 1:
            return [tokens[i]]
        res = []
        for k in range(i + 1, j - 1):
            if tokens[k] in "+*":
                for l in arboles(i, k):
                    for r in arboles(k + 1, j):
                        res.append(f"({l} {tokens[k]} {r})")
        return res
    return arboles(0, len(tokens))


def prueba_enumeracion():
    seccion("Árboles de derivación de  2 + 3 * 4  según la gramática")
    for a in enumerar(("2", "+", "3", "*", "4")):
        print("  ", a)


if __name__ == "__main__":
    prueba_antlr()
    prueba_conteo()
    prueba_enumeracion()
