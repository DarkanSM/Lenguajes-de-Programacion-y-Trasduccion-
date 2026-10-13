grammar Amb3;
// Forma que ANTLR NO puede "arreglar" con precedencia: la ambigüedad
// se escribe sin la plantilla 'e op e'.
//   alt 1: NUM op e   (derecha:  2 + (3*4) )
//   alt 2: e op NUM   (izquierda: (2+3) * 4)
prog : e EOF ;
e : NUM op e
  | e op NUM
  | NUM
  ;
op : '+' | '*' ;
NUM : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
