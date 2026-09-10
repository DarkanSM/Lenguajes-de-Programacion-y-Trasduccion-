grammar DSL;

// =========================================================
// Corte 1 — Alcance: asignaciones, expresiones, cargar,
// seleccionar, filtrar, y reconocimiento sintáctico de graficar.
// Dominio de ejemplo: ventas / comercio. Vocabulario en español.
// =========================================================

// ===================== PARSER =====================

programa
    : sentencia* EOF
    ;

sentencia
    : asignacion
    | sentenciaGraficar
    ;

asignacion
    : IDENTIFICADOR '=' expresionPipeline
    ;

expresionPipeline
    : fuenteDatos ( PIPE operacion )*
    ;

fuenteDatos
    : CARGAR CADENA
    | IDENTIFICADOR
    ;

operacion
    : SELECCIONAR '[' listaIdentificadores ']'      # opSeleccionar
    | FILTRAR DONDE expresionBooleana                # opFiltrar
    ;

expresionBooleana
    : NO expresionBooleana                           # boolNegacion
    | expresionBooleana OP_AND expresionBooleana      # boolAnd
    | expresionBooleana OP_OR expresionBooleana       # boolOr
    | expresionRelacional                            # boolRelacional
    | '(' expresionBooleana ')'                      # boolParentesis
    ;

expresionRelacional
    : expresionAritmetica ( OP_REL expresionAritmetica )?
    ;

expresionAritmetica
    : expresionAritmetica ( '+' | '-' ) termino       # aritSuma
    | termino                                        # aritTermino
    ;

termino
    : termino ( '*' | '/' | '%' ) factor              # termMulDiv
    | factor                                         # termFactor
    ;

factor
    : factor '^' factor                              # factorPotencia
    | primario                                       # factorPrimario
    ;

primario
    : NUMERO_DECIMAL                                 # primDecimal
    | NUMERO_ENTERO                                  # primEntero
    | CADENA                                         # primCadena
    | BOOLEANO                                       # primBooleano
    | IDENTIFICADOR                                  # primIdentificador
    | '(' expresionAritmetica ')'                    # primParentesis
    ;

sentenciaGraficar
    : GRAFICAR tipoGrafica IDENTIFICADOR
      ( 'x' IDENTIFICADOR )?
      ( 'y' IDENTIFICADOR )?
      ( TITULO CADENA )?
      ( GUARDAR COMO CADENA )?
    ;

tipoGrafica
    : BARRAS | LINEAS | HISTOGRAMA | DISPERSION | CAJA
    ;

listaIdentificadores
    : IDENTIFICADOR ( ',' IDENTIFICADOR )*
    ;

// ===================== LEXER =====================
// IMPORTANTE: las palabras reservadas van ANTES que IDENTIFICADOR,
// porque ANTLR resuelve por orden de declaración + longest match.

CARGAR       : 'cargar' ;
SELECCIONAR  : 'seleccionar' ;
FILTRAR      : 'filtrar' ;
DONDE        : 'donde' ;
GRAFICAR     : 'graficar' ;
TITULO       : 'titulo' ;
GUARDAR      : 'guardar' ;
COMO         : 'como' ;

BARRAS       : 'barras' ;
LINEAS       : 'lineas' ;
HISTOGRAMA   : 'histograma' ;
DISPERSION   : 'dispersion' ;
CAJA         : 'caja' ;

OP_AND       : 'y' ;
OP_OR        : 'o' ;
NO           : 'no' ;

BOOLEANO     : 'verdadero' | 'falso' ;

PIPE         : '|>' ;
OP_REL       : '==' | '!=' | '<=' | '>=' | '<' | '>' ;

NUMERO_DECIMAL : [0-9]+ '.' [0-9]+ ;
NUMERO_ENTERO  : [0-9]+ ;
CADENA         : '"' (~["\r\n])* '"' ;
IDENTIFICADOR  : [a-zA-Z_][a-zA-Z_0-9]* ;

COMENTARIO   : '#' ~[\r\n]* -> skip ;
ESPACIO      : [ \t\r\n]+ -> skip ;
