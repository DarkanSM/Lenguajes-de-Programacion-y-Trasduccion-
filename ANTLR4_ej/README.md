# Actividad práctica ANTLR 4 — Lenguaje de instrucciones

## Descripción
Se construyó un lenguaje simple con ANTLR 4 capaz de reconocer instrucciones del tipo:
`mostrar ventas`, `cargar clientes`, `graficar ingresos`.


## Archivo de gramática

Ver [`Instruccion.g4`](Instruccion.g4).

```antlr
grammar Instruccion;

programa
    : instruccion+ EOF
    ;

instruccion
    : MOSTRAR ID
    | CARGAR ID
    | GRAFICAR ID
    ;

MOSTRAR
    : 'mostrar'
    ;

CARGAR
    : 'cargar'
    ;

GRAFICAR
    : 'graficar'
    ;

ID
    : [a-zA-Z]+
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
```

## Cómo reproducir estos resultados

Requiere Java y ANTLR4 instalados (jar completo + alias `antlr4`/`grun`).

```bash
antlr4 Instruccion.g4
javac Instruccion*.java

grun Instruccion programa -tokens tests/pruebas_validas.txt
grun Instruccion programa -tree tests/pruebas_validas.txt
grun Instruccion programa -gui tests/pruebas_validas.txt

grun Instruccion programa -tree tests/error1.txt
grun Instruccion programa -tree tests/error2.txt
grun Instruccion programa -tree tests/error3.txt
```

## Explicación de las reglas léxicas

- **MOSTRAR, CARGAR, GRAFICAR**: reconocen literalmente las palabras clave `mostrar`, `cargar` y `graficar`. Comienzan con mayúscula porque en ANTLR toda regla léxica (token) debe iniciar con letra mayúscula.
- **ID**: reconoce uno o más caracteres alfabéticos (`[a-zA-Z]+`), usado para los nombres que acompañan a cada instrucción (ventas, clientes, ingresos, etc.).
- **WS**: reconoce espacios, tabulaciones y saltos de línea, y usa `-> skip` para indicarle al lexer que los descarte y no los envíe al parser.

## Explicación de las reglas sintácticas

- **programa**: regla inicial. Indica que un programa válido está compuesto por una o más instrucciones (`instruccion+`) seguidas del fin de archivo (`EOF`). Esto permite procesar varias instrucciones en un mismo archivo de entrada.
- **instruccion**: define que cada instrucción válida es una palabra clave (`MOSTRAR`, `CARGAR` o `GRAFICAR`) seguida de un identificador (`ID`).

## Evidencia de tokens reconocidos

Archivo de entrada: [`tests/pruebas_validas.txt`](tests/pruebas_validas.txt) (5 pruebas)

Comando ejecutado:
```
grun Instruccion programa -tokens tests/pruebas_validas.txt
```

Resultado:
```
[@0,0:6='mostrar',<'mostrar'>,1:0]
[@1,8:13='ventas',<ID>,1:8]
[@2,15:20='cargar',<'cargar'>,2:0]
[@3,22:29='clientes',<ID>,2:7]
[@4,31:38='graficar',<'graficar'>,3:0]
[@5,40:47='ingresos',<ID>,3:9]
[@6,49:55='mostrar',<'mostrar'>,4:0]
[@7,57:65='productos',<ID>,4:8]
[@8,67:72='cargar',<'cargar'>,5:0]
[@9,74:81='reportes',<ID>,5:7]
[@10,83:82='<EOF>',<EOF>,6:0]
```

![Tokens reconocidos](evidencia/tokens.png)

## Evidencia del árbol sintáctico

Comando ejecutado:
```
grun Instruccion programa -tree tests/pruebas_validas.txt
```

Resultado:
```
(programa (instruccion mostrar ventas) (instruccion cargar clientes) (instruccion graficar ingresos) (instruccion mostrar productos) (instruccion cargar reportes) <EOF>)
```

![Árbol sintáctico en texto](evidencia/arbol_texto.png)

![Árbol sintáctico gráfico](evidencia/arbol_grafico.png)

## Casos de error identificados

**Error 1** — orden incorrecto de tokens ([`tests/error1.txt`](tests/error1.txt): `ventas mostrar`)
```
line 1:0 extraneous input 'ventas' expecting {'mostrar', 'cargar', 'graficar'}
line 2:0 missing ID at '<EOF>'
```

![Error 1](evidencia/error1.png)

**Error 2** — instrucción incompleta, falta el ID ([`tests/error2.txt`](tests/error2.txt): `graficar`)
```
line 2:0 missing ID at '<EOF>'
```

![Error 2](evidencia/error2.png)

**Error 3** — palabra clave no definida en la gramática ([`tests/error3.txt`](tests/error3.txt): `eliminar ventas`)
```
line 1:0 mismatched input 'eliminar' expecting {'mostrar', 'cargar', 'graficar'}
```

![Error 3](evidencia/error3.png)

## Conclusiones sobre la diferencia entre lexer y parser

El lexer y el parser cumplen roles distintos y complementarios dentro del proceso de análisis de un lenguaje. El lexer trabaja a nivel de caracteres: agrupa el texto crudo en unidades con significado (tokens) como palabras clave e identificadores, y descarta lo que no aporta estructura, como los espacios en blanco. El parser, en cambio, trabaja a nivel de tokens: verifica que la secuencia generada por el lexer cumpla con el orden y la estructura definidos por las reglas sintácticas de la gramática, y construye el árbol sintáctico que representa esa estructura. En otras palabras, el lexer responde "¿qué es cada pedazo de texto?" mientras que el parser responde "¿estos pedazos están organizados correctamente?". Esta separación permite que ambas etapas se diseñen y depuren de forma independiente, y es la base sobre la que se construyen compiladores e intérpretes.


## Preguntas de análisis


1. ¿Cuál es la diferencia entre un lexema y un token?
El lexema es el texto crudo que aparece en el archivo, sin ningún tipo de interpretación: por ejemplo, la palabra mostrar tal cual fue escrita. El token es el resultado de clasificar ese lexema dentro de una categoría reconocida por la gramática, en este caso MOSTRAR. Varios lexemas distintos pueden mapear al mismo tipo de token, como ocurre con ID, que agrupa cualquier palabra como ventas, productos o reportes.

2. ¿Cuál es la responsabilidad del lexer?
Recorrer el texto de entrada carácter por carácter y agruparlo en tokens según las reglas léxicas definidas, dejando fuera del flujo hacia el parser cualquier elemento que no aporte información estructural, como los espacios en blanco o los saltos de línea.

3. ¿Cuál es la responsabilidad del parser?
Tomar la secuencia de tokens que entrega el lexer y comprobar si el orden en que aparecen respeta las reglas sintácticas de la gramática. Si la secuencia es válida, arma con ella un árbol sintáctico; si no lo es, reporta el punto exacto donde la estructura falla.

4. ¿Por qué las reglas léxicas comienzan con mayúscula en ANTLR?
Porque ANTLR usa esa mayúscula inicial como marca sintáctica para saber, sin ambigüedad, que se trata de una regla del lexer y no del parser, sin necesidad de escribir una palabra clave adicional que lo indique.

5. ¿Por qué las reglas sintácticas comienzan con minúscula?
Es la contraparte de la convención anterior: al empezar en minúscula, ANTLR sabe que esa regla pertenece al parser y describe cómo se combinan los tokens (y otras reglas) para formar estructuras del lenguaje.

6. ¿Cuál es la función de ->skip?
Le dice al lexer que, aunque el texto coincide con esa regla, el token generado no debe pasar al parser. Es útil para partes de la entrada que hay que reconocer pero que no tienen valor estructural, como los espacios.

7. ¿Qué representa EOF?
Es el marcador de fin de archivo. Colocarlo al final de la regla inicial obliga a que el parser consuma toda la entrada para dar por válido el reconocimiento, en lugar de aceptar solo un fragmento inicial y quedarse callado sobre el resto.

8. ¿Qué información representa un árbol sintáctico?
Muestra cómo se aplicaron las reglas de la gramática sobre la entrada: cada nodo interno es una regla sintáctica que se disparó, y cada hoja es un token concreto que el lexer identificó. En conjunto, refleja la estructura jerárquica que tiene el texto según el lenguaje definido.

9. ¿Cuál es la diferencia entre Listener y Visitor?
Con el Listener, es ANTLR quien recorre el árbol automáticamente y va avisando (mediante enterX/exitX) cada vez que entra o sale de un nodo, sin que el programador decida el orden. Con el Visitor, es el propio código el que controla explícitamente el recorrido, llamando a visit sobre los hijos que le interesan, lo que da más flexibilidad para, por ejemplo, calcular y devolver un valor a partir del árbol.

10. ¿Cómo podría utilizarse ANTLR para construir un lenguaje de dominio específico?
Se define una gramática que capture el vocabulario y la estructura propios del dominio en cuestión (como los comandos mostrar, cargar y graficar de este ejercicio), se genera el lexer y el parser a partir de ella, y luego se conecta un Listener o un Visitor que traduzca el árbol reconocido en acciones reales, como ejecutar una consulta o disparar un proceso

## Referencias

- Parr, T. (2013). *The Definitive ANTLR 4 Reference*. Pragmatic Bookshelf.
- Documentación oficial de ANTLR4: https://www.antlr.org
