# Generated from Expr.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13")
        buf.write(",\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\3\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\7\3\24\n\3\f\3\16\3\27\13\3\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\7\4\37\n\4\f\4\16\4\"\13\4\3\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\5\5*\n\5\3\5\2\4\4\6\6\2\4\6\b\2\4\3\2\3")
        buf.write("\4\3\2\5\6\2+\2\n\3\2\2\2\4\r\3\2\2\2\6\30\3\2\2\2\b)")
        buf.write("\3\2\2\2\n\13\5\4\3\2\13\f\7\2\2\3\f\3\3\2\2\2\r\16\b")
        buf.write("\3\1\2\16\17\5\6\4\2\17\25\3\2\2\2\20\21\f\4\2\2\21\22")
        buf.write("\t\2\2\2\22\24\5\6\4\2\23\20\3\2\2\2\24\27\3\2\2\2\25")
        buf.write("\23\3\2\2\2\25\26\3\2\2\2\26\5\3\2\2\2\27\25\3\2\2\2\30")
        buf.write("\31\b\4\1\2\31\32\5\b\5\2\32 \3\2\2\2\33\34\f\4\2\2\34")
        buf.write("\35\t\3\2\2\35\37\5\b\5\2\36\33\3\2\2\2\37\"\3\2\2\2 ")
        buf.write("\36\3\2\2\2 !\3\2\2\2!\7\3\2\2\2\" \3\2\2\2#*\7\t\2\2")
        buf.write("$*\7\n\2\2%&\7\7\2\2&\'\5\4\3\2\'(\7\b\2\2(*\3\2\2\2)")
        buf.write("#\3\2\2\2)$\3\2\2\2)%\3\2\2\2*\t\3\2\2\2\5\25 )")
        return buf.getvalue()


class ExprParser ( Parser ):

    grammarFileName = "Expr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "ID", "NUM", 
                      "WS" ]

    RULE_prog = 0
    RULE_e = 1
    RULE_t = 2
    RULE_f = 3

    ruleNames =  [ "prog", "e", "t", "f" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    ID=7
    NUM=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def e(self):
            return self.getTypedRuleContext(ExprParser.EContext,0)


        def EOF(self):
            return self.getToken(ExprParser.EOF, 0)

        def getRuleIndex(self):
            return ExprParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProg" ):
                return visitor.visitProg(self)
            else:
                return visitor.visitChildren(self)




    def prog(self):

        localctx = ExprParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.e(0)
            self.state = 9
            self.match(ExprParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExprParser.RULE_e

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class EaTContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.EContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def t(self):
            return self.getTypedRuleContext(ExprParser.TContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEaT" ):
                listener.enterEaT(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEaT" ):
                listener.exitEaT(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEaT" ):
                return visitor.visitEaT(self)
            else:
                return visitor.visitChildren(self)


    class SumaRestaContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.EContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def e(self):
            return self.getTypedRuleContext(ExprParser.EContext,0)

        def t(self):
            return self.getTypedRuleContext(ExprParser.TContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSumaResta" ):
                listener.enterSumaResta(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSumaResta" ):
                listener.exitSumaResta(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSumaResta" ):
                return visitor.visitSumaResta(self)
            else:
                return visitor.visitChildren(self)



    def e(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExprParser.EContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_e, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = ExprParser.EaTContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 12
            self.t(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 19
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ExprParser.SumaRestaContext(self, ExprParser.EContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_e)
                    self.state = 14
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 15
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==ExprParser.T__0 or _la==ExprParser.T__1):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 16
                    self.t(0) 
                self.state = 21
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class TContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExprParser.RULE_t

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class MulDivContext(TContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.TContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def t(self):
            return self.getTypedRuleContext(ExprParser.TContext,0)

        def f(self):
            return self.getTypedRuleContext(ExprParser.FContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDiv" ):
                listener.enterMulDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDiv" ):
                listener.exitMulDiv(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDiv" ):
                return visitor.visitMulDiv(self)
            else:
                return visitor.visitChildren(self)


    class TaFContext(TContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.TContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def f(self):
            return self.getTypedRuleContext(ExprParser.FContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTaF" ):
                listener.enterTaF(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTaF" ):
                listener.exitTaF(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTaF" ):
                return visitor.visitTaF(self)
            else:
                return visitor.visitChildren(self)



    def t(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExprParser.TContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_t, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = ExprParser.TaFContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 23
            self.f()
            self._ctx.stop = self._input.LT(-1)
            self.state = 30
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ExprParser.MulDivContext(self, ExprParser.TContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_t)
                    self.state = 25
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 26
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==ExprParser.T__2 or _la==ExprParser.T__3):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 27
                    self.f() 
                self.state = 32
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class FContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExprParser.RULE_f

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParensContext(FContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.FContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def e(self):
            return self.getTypedRuleContext(ExprParser.EContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParens" ):
                listener.enterParens(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParens" ):
                listener.exitParens(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParens" ):
                return visitor.visitParens(self)
            else:
                return visitor.visitChildren(self)


    class NumContext(FContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.FContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(ExprParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNum" ):
                listener.enterNum(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNum" ):
                listener.exitNum(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNum" ):
                return visitor.visitNum(self)
            else:
                return visitor.visitChildren(self)


    class IdContext(FContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.FContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ExprParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterId" ):
                listener.enterId(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitId" ):
                listener.exitId(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitId" ):
                return visitor.visitId(self)
            else:
                return visitor.visitChildren(self)



    def f(self):

        localctx = ExprParser.FContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_f)
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ExprParser.ID]:
                localctx = ExprParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 33
                self.match(ExprParser.ID)
                pass
            elif token in [ExprParser.NUM]:
                localctx = ExprParser.NumContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 34
                self.match(ExprParser.NUM)
                pass
            elif token in [ExprParser.T__4]:
                localctx = ExprParser.ParensContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 35
                self.match(ExprParser.T__4)
                self.state = 36
                self.e(0)
                self.state = 37
                self.match(ExprParser.T__5)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.e_sempred
        self._predicates[2] = self.t_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def e_sempred(self, localctx:EContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

    def t_sempred(self, localctx:TContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         




