"""
Ejercicios 1 y 2: gramática de la diapositiva 11 en ANTLR (target Python)
y distintas representaciones del árbol sintáctico (diapositiva 12).
"""
import sys
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import TerminalNode
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from ExprListener import ExprListener


# ---------------------------------------------------------------- errores
class ErrorSintactico(Exception):
    pass


class Listener(ErrorListener):
    """Convierte los errores de ANTLR en excepciones (línea:columna)."""
    def syntaxError(self, recognizer, sym, line, col, msg, e):
        raise ErrorSintactico(f"line {line}:{col} {msg}")


def parsear(texto):
    lexer = ExprLexer(InputStream(texto))
    lexer.removeErrorListeners(); lexer.addErrorListener(Listener())
    parser = ExprParser(CommonTokenStream(lexer))
    parser.removeErrorListeners(); parser.addErrorListener(Listener())
    return parser.prog(), parser


# ------------------------------------------------- FORMA 1: texto estilo LISP
def forma_lisp(tree, parser):
    """toStringTree: (regla hijo hijo ...)"""
    return tree.toStringTree(recog=parser)


# ------------------------------------------- FORMA 2: parse tree en ASCII
def forma_ascii_parse(tree, parser, prefijo="", ultimo=True, raiz=True):
    nombres = parser.ruleNames
    if isinstance(tree, TerminalNode):
        etiqueta = f"'{tree.getText()}'"
    else:
        etiqueta = nombres[tree.getRuleIndex()]
    if raiz:
        lineas = [etiqueta]
        nuevo = ""
    else:
        lineas = [prefijo + ("└── " if ultimo else "├── ") + etiqueta]
        nuevo = prefijo + ("    " if ultimo else "│   ")
    if not isinstance(tree, TerminalNode):
        hijos = [tree.getChild(i) for i in range(tree.getChildCount())]
        for i, h in enumerate(hijos):
            lineas += forma_ascii_parse(h, parser, nuevo, i == len(hijos) - 1, False)
    return lineas


# ------------------------------------------------- FORMA 3: Graphviz DOT
def forma_dot(tree, parser):
    out, cont = ["digraph ParseTree {", "  node [shape=box, fontname=Helvetica];"], [0]

    def rec(n):
        mi = cont[0]; cont[0] += 1
        if isinstance(n, TerminalNode):
            out.append(f'  n{mi} [label="{n.getText()}", shape=ellipse, style=filled, fillcolor=lightyellow];')
        else:
            out.append(f'  n{mi} [label="{parser.ruleNames[n.getRuleIndex()]}"];')
            for i in range(n.getChildCount()):
                hi = rec(n.getChild(i))
                out.append(f"  n{mi} -> n{hi};")
        return mi
    rec(tree)
    out.append("}")
    return "\n".join(out)


# ------------------------------------------------- FORMA 4: AST (Visitor)
class Nodo:
    def __init__(self, etiqueta, *hijos):
        self.etiqueta, self.hijos = etiqueta, hijos

    def __repr__(self):  # forma parentizada
        if not self.hijos:
            return str(self.etiqueta)
        return f"({self.etiqueta} {' '.join(map(repr, self.hijos))})"

    def ascii(self, prefijo="", ultimo=True, raiz=True):
        if raiz:
            lineas, nuevo = [str(self.etiqueta)], ""
        else:
            lineas = [prefijo + ("└── " if ultimo else "├── ") + str(self.etiqueta)]
            nuevo = prefijo + ("    " if ultimo else "│   ")
        for i, h in enumerate(self.hijos):
            lineas += h.ascii(nuevo, i == len(self.hijos) - 1, False)
        return lineas


class ConstruyeAST(ExprVisitor):
    """Elimina no terminales intermedios (e, t, f) y paréntesis."""
    def visitProg(self, ctx):        return self.visit(ctx.e())
    def visitSumaResta(self, ctx):   return Nodo(ctx.op.text, self.visit(ctx.e()), self.visit(ctx.t()))
    def visitEaT(self, ctx):         return self.visit(ctx.t())
    def visitMulDiv(self, ctx):      return Nodo(ctx.op.text, self.visit(ctx.t()), self.visit(ctx.f()))
    def visitTaF(self, ctx):         return self.visit(ctx.f())
    def visitId(self, ctx):          return Nodo(ctx.ID().getText())
    def visitNum(self, ctx):         return Nodo(ctx.NUM().getText())
    def visitParens(self, ctx):      return self.visit(ctx.e())


# --------------------------------- FORMA 5: Visitor que evalúa (sobre el árbol)
class Evalua(ExprVisitor):
    def __init__(self, variables=None):
        self.v = variables or {}
    def visitProg(self, ctx):  return self.visit(ctx.e())
    def visitSumaResta(self, ctx):
        a, b = self.visit(ctx.e()), self.visit(ctx.t())
        return a + b if ctx.op.text == '+' else a - b
    def visitEaT(self, ctx):   return self.visit(ctx.t())
    def visitMulDiv(self, ctx):
        a, b = self.visit(ctx.t()), self.visit(ctx.f())
        return a * b if ctx.op.text == '*' else a / b
    def visitTaF(self, ctx):   return self.visit(ctx.f())
    def visitId(self, ctx):    return self.v[ctx.ID().getText()]
    def visitNum(self, ctx):   return int(ctx.NUM().getText())
    def visitParens(self, ctx): return self.visit(ctx.e())


# --------------------- FORMA 6: Listener (recorrido post-orden -> notación RPN)
class Postfija(ExprListener):
    def __init__(self): self.salida = []
    def exitSumaResta(self, ctx): self.salida.append(ctx.op.text)
    def exitMulDiv(self, ctx):    self.salida.append(ctx.op.text)
    def exitId(self, ctx):        self.salida.append(ctx.ID().getText())
    def exitNum(self, ctx):       self.salida.append(ctx.NUM().getText())


# ------------------------------------------------------------------ main
def mostrar_todo(texto, variables=None):
    print("=" * 70)
    print(f"ENTRADA: {texto}")
    print("=" * 70)
    tree, parser = parsear(texto)
    print("\n[1] Parse tree - forma LISP (toStringTree):")
    print("   ", forma_lisp(tree, parser))
    print("\n[2] Parse tree - ASCII:")
    print("\n".join("    " + l for l in forma_ascii_parse(tree, parser)))
    ast = ConstruyeAST().visit(tree)
    print("\n[3] AST - forma parentizada:")
    print("   ", ast)
    print("\n[4] AST - ASCII:")
    print("\n".join("    " + l for l in ast.ascii()))
    p = Postfija(); ParseTreeWalker().walk(p, tree)
    print("\n[5] Recorrido post-orden con Listener (notación postfija):")
    print("   ", " ".join(p.salida))
    print("\n[6] Evaluación con Visitor:", Evalua(variables).visit(tree))
    return tree, parser


if __name__ == "__main__":
    if len(sys.argv) > 1:
        mostrar_todo(" ".join(sys.argv[1:]))
    else:
        mostrar_todo("3 + 4 * 5")   # diapositiva 12
