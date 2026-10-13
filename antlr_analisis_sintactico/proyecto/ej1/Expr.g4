grammar Expr;

// ---------- Parser: gramática de la diapositiva 11 ----------
// E -> E + T | T
// T -> T * F | F
// F -> id | num | ( E )
// (se añaden - y / porque los ejemplos de la diapositiva usan '2 + 3 - 4')
//
// Se escribe con una regla por nivel (e, t, f) para que el parse tree
// conserve exactamente la estructura de la gramática.

prog : e EOF ;

e : e op=('+' | '-') t     # SumaResta
  | t                      # EaT
  ;

t : t op=('*' | '/') f     # MulDiv
  | f                      # TaF
  ;

f : ID                     # Id
  | NUM                    # Num
  | '(' e ')'              # Parens
  ;

// ---------- Lexer ----------
ID  : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUM : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
