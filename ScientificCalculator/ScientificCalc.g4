grammar ScientificCalc;

prog
    : stat+ EOF
    ;

stat
    : expr NEWLINE                                                        # printExpr
    | ID '=' expr NEWLINE                                                 # assign
    | ID '(' ID ')' '=' expr NEWLINE                                      # funcDef
    | 'clear' NEWLINE                                                     # clear
    | 'vars' NEWLINE                                                      # showVars
    | 'plot' '(' expr ',' expr ',' expr (',' expr ',' expr)? ')' NEWLINE  # plotExpr
    | 'plot' '(' expr (',' expr)+ ';' expr ',' expr ')' NEWLINE           # plotMulti
    | NEWLINE                                                             # blank
    ;

expr
    : <assoc=right> expr '^' expr        # power
    | op=('+'|'-') expr                  # unary
    | expr op=('*'|'/') expr             # mulDiv
    | expr op=('+'|'-') expr             # addSub
    | function '(' expr ')'              # functionCall
    | function2 '(' expr ',' expr ')'    # functionCall2
    | ID '(' expr ')'                    # userFunctionCall
    | constant                           # constantExpr
    | NUMBER                             # number
    | ID                                 # id
    | '(' expr ')'                       # parens
    ;

// Reto 1: nuevas funciones de un argumento (asin, acos, atan, floor, ceil)
function
    : 'sin'
    | 'cos'
    | 'tan'
    | 'sqrt'
    | 'log'
    | 'ln'
    | 'abs'
    | 'exp'
    | 'asin'
    | 'acos'
    | 'atan'
    | 'floor'
    | 'ceil'
    ;

// Reto 2: funciones con dos argumentos: pow(a,b), max(a,b), min(a,b)
function2
    : 'pow'
    | 'max'
    | 'min'
    ;

constant
    : 'pi'
    | 'e'
    ;

MUL : '*';
DIV : '/';
ADD : '+';
SUB : '-';
POW : '^';

NUMBER
    : [0-9]+ ('.' [0-9]+)?
    ;

ID
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

NEWLINE
    : '\r'? '\n'
    ;

WS
    : [ \t]+ -> skip
    ;
