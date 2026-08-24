# Explicación de las reglas

## Reglas léxicas

| Regla | Definición | Propósito |
|---|---|---|
| `MOSTRAR` | `'mostrar'` | Reconoce la palabra reservada `mostrar` como token independiente. |
| `CARGAR` | `'cargar'` | Reconoce la palabra reservada `cargar`. |
| `GRAFICAR` | `'graficar'` | Reconoce la palabra reservada `graficar`. |
| `ID` | `[a-zA-Z]+` | Reconoce cualquier secuencia de letras que actúe como el argumento de la instrucción (por ejemplo `ventas`, `clientes`, `datos`). Al estar definida después de las palabras reservadas, ANTLR prioriza estas últimas cuando el lexema coincide exactamente con una de ellas. |
| `WS` | `[ \t\r\n]+ -> skip` | Reconoce espacios, tabulaciones y saltos de línea, y los descarta (`skip`) para que nunca lleguen al parser. |

Las tres primeras reglas son literales de texto fijo, por lo que ANTLR las trata con mayor prioridad que `ID` en caso de coincidencia exacta (regla de "match más largo, y en empate, gana la regla declarada primero").

## Reglas sintácticas

```
programa
    : instruccion+ EOF
    ;

instruccion
    : MOSTRAR ID
    | CARGAR ID
    | GRAFICAR ID
    ;
```

- `programa` es la regla inicial: exige una o más instrucciones (`instruccion+`) seguidas del fin de archivo (`EOF`). Esto permite procesar un archivo con múltiples líneas de instrucciones, no solo una.
- `instruccion` define la estructura válida de cada línea: una palabra reservada (`MOSTRAR`, `CARGAR` o `GRAFICAR`) seguida obligatoriamente de un `ID`. El operador `|` expresa que solo una de las tres alternativas puede ocurrir por instrucción.

## Por qué esta estructura

- Se separó `programa` de `instruccion` para poder reutilizar la regla `instruccion` y repetirla, en lugar de limitar la gramática a una sola línea de entrada.
- No se usó una gramática separada en lexer/parser (`MyLexer.g4` / `MyParser.g4`) sino una gramática combinada (`grammar Instrucciones;`) porque el lenguaje es pequeño y no requiere reutilizar el lexer en múltiples parsers.
