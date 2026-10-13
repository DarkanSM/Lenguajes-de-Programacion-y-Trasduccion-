grammar Amb2;
// Misma gramática, pero '*' se escribe primero => '*' tiene MAYOR precedencia
prog : e EOF ;
e : e '*' e
  | e '+' e
  | NUM
  ;
NUM : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
