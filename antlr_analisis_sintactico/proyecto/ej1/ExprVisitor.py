# Generated from Expr.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#prog.
    def visitProg(self, ctx:ExprParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#EaT.
    def visitEaT(self, ctx:ExprParser.EaTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#SumaResta.
    def visitSumaResta(self, ctx:ExprParser.SumaRestaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#MulDiv.
    def visitMulDiv(self, ctx:ExprParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#TaF.
    def visitTaF(self, ctx:ExprParser.TaFContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Id.
    def visitId(self, ctx:ExprParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Num.
    def visitNum(self, ctx:ExprParser.NumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Parens.
    def visitParens(self, ctx:ExprParser.ParensContext):
        return self.visitChildren(ctx)



del ExprParser