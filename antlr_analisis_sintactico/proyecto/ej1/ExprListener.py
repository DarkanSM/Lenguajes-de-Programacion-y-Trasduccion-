# Generated from Expr.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):

    # Enter a parse tree produced by ExprParser#prog.
    def enterProg(self, ctx:ExprParser.ProgContext):
        pass

    # Exit a parse tree produced by ExprParser#prog.
    def exitProg(self, ctx:ExprParser.ProgContext):
        pass


    # Enter a parse tree produced by ExprParser#EaT.
    def enterEaT(self, ctx:ExprParser.EaTContext):
        pass

    # Exit a parse tree produced by ExprParser#EaT.
    def exitEaT(self, ctx:ExprParser.EaTContext):
        pass


    # Enter a parse tree produced by ExprParser#SumaResta.
    def enterSumaResta(self, ctx:ExprParser.SumaRestaContext):
        pass

    # Exit a parse tree produced by ExprParser#SumaResta.
    def exitSumaResta(self, ctx:ExprParser.SumaRestaContext):
        pass


    # Enter a parse tree produced by ExprParser#MulDiv.
    def enterMulDiv(self, ctx:ExprParser.MulDivContext):
        pass

    # Exit a parse tree produced by ExprParser#MulDiv.
    def exitMulDiv(self, ctx:ExprParser.MulDivContext):
        pass


    # Enter a parse tree produced by ExprParser#TaF.
    def enterTaF(self, ctx:ExprParser.TaFContext):
        pass

    # Exit a parse tree produced by ExprParser#TaF.
    def exitTaF(self, ctx:ExprParser.TaFContext):
        pass


    # Enter a parse tree produced by ExprParser#Id.
    def enterId(self, ctx:ExprParser.IdContext):
        pass

    # Exit a parse tree produced by ExprParser#Id.
    def exitId(self, ctx:ExprParser.IdContext):
        pass


    # Enter a parse tree produced by ExprParser#Num.
    def enterNum(self, ctx:ExprParser.NumContext):
        pass

    # Exit a parse tree produced by ExprParser#Num.
    def exitNum(self, ctx:ExprParser.NumContext):
        pass


    # Enter a parse tree produced by ExprParser#Parens.
    def enterParens(self, ctx:ExprParser.ParensContext):
        pass

    # Exit a parse tree produced by ExprParser#Parens.
    def exitParens(self, ctx:ExprParser.ParensContext):
        pass



del ExprParser