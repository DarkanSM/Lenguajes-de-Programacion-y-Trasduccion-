grammar Amb1;
// Diapositiva 15 tal cual:  E -> E + E | E * E | num
// '+' se escribe primero  => ANTLR le da MAYOR precedencia
prog : e EOF ;
e : e '+' e
  | e '*' e
  | NUM
  ;
NUM : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
