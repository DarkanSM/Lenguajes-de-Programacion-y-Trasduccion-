%{
#include "Ejemplo5.tab.h"
%}

%%
"+"     { return ADD; }
"-"     { return SUB; }
"*"     { return MUL; }
"/"     { return DIV; }
"|"     { return ABS; }
[0-9]+  { yylval = atoi(yytext); return NUMBER; }
\n      { return EOL; }
[ \t]   { /* ignorar espacios y tabulaciones */ }
.       { printf("Mysterio character %c\n", *yytext); }
%%
