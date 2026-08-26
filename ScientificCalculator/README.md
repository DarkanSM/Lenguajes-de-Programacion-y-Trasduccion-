# Calculadora Científica Graficadora con ANTLR

Intérprete de un pequeño lenguaje matemático construido con **ANTLR4** y el **patrón de diseño Visitor**, como parte del laboratorio del curso *Lenguajes de Programación y Traducción*.

El lenguaje permite evaluar expresiones aritméticas, definir variables, usar funciones y constantes matemáticas, y graficar funciones en una ventana gráfica (Swing).

```
radio = 10
area = pi * radio^2
area

angulo = pi/4
sin(angulo)
cos(angulo)

vars

plot(sin(x), -6.28, 6.28)
plot(x^2, -10, 10)
```

## Características

- Expresiones aritméticas con precedencia correcta: `+`, `-`, `*`, `/`, `^` (potencia, asociativa a la derecha).
- Números reales y operadores unarios (`-10`, `abs(-10)`).
- Variables: asignación (`radio = 10`) y uso (`area = pi * radio^2`).
- Constantes matemáticas: `pi`, `e`.
- Funciones científicas: `sin`, `cos`, `tan`, `sqrt`, `log`, `ln`, `abs`, `exp`.
- Comandos: `clear` (borra la memoria) y `vars` (lista las variables definidas).
- Graficación de funciones: `plot(expresion, xmin, xmax)`, abre una ventana con la curva.
- Manejo de discontinuidades al graficar (se descartan automáticamente los puntos `Infinity`/`NaN`).

## Arquitectura

```
Entrada de texto
      ↓
   Lexer            (ScientificCalcLexer, generado por ANTLR)
      ↓
   Tokens
      ↓
   Parser           (ScientificCalcParser, generado por ANTLR)
      ↓
Árbol sintáctico
      ↓
   Visitor          (ScientificEvalVisitor, escrito a mano)
      ↓
   Resultado
```

La gramática (`ScientificCalc.g4`) define únicamente la **sintaxis** del lenguaje. Toda la **semántica** (qué significa cada operación, cómo se evalúa, cómo se grafica) vive en `ScientificEvalVisitor.java`, siguiendo el patrón Visitor. Esta separación permite extender el lenguaje sin acoplar la gramática a la lógica de la aplicación.

## Estructura del proyecto

```
ScientificCalculator/
├── ScientificCalc.g4          # Gramática ANTLR (lexer + parser)
├── Main.java                  # Punto de entrada: lee stdin, arma el árbol, lo visita
├── ScientificEvalVisitor.java # Implementación del patrón Visitor (semántica del lenguaje)
├── PlotWindow.java            # Ventana Swing que dibuja la función muestreada
├── ejemplos.txt               # Casos de prueba de ejemplo
└── README.md
```

> Los archivos `ScientificCalcLexer.java`, `ScientificCalcParser.java`, `ScientificCalcVisitor.java` y `ScientificCalcBaseVisitor.java` **no están en el repositorio**: ANTLR los genera automáticamente a partir de `ScientificCalc.g4` (ver instrucciones abajo). No deben editarse a mano ni versionarse.

## Requisitos

- Java JDK 11 o superior.
- ANTLR4 (herramienta de generación + runtime).

## Pasos 1–2: Introducción y objetivo
Se explicó la metodología del laboratorio: avanzar en pasos pequeños (explicación → cambio en gramática/código → prueba → actividad).
Se definió la meta final: un lenguaje capaz de evaluar expresiones matemáticas (2+3*4), manejar variables (radio=10), evaluar funciones (sin(pi/2)) y graficar (plot(sin(x), -6.28, 6.28)).
Se presentó la arquitectura general que seguiría todo el proyecto: Entrada → Lexer → Tokens → Parser → Árbol sintáctico → Visitor → Resultado.

## Paso 3: Recordar la calculadora base del libro
Se repasó una gramática de ejemplo (MulDiv, AddSub, int, id, parens) para entender el concepto de las etiquetas (#nombre) en las alternativas de una regla, y cómo cada una genera su propio nodo en el árbol y su propio método visit.

## Paso 4: Crear el proyecto
Creamos la carpeta ScientificCalculator/ con los archivos base: ScientificCalc.g4, Main.java, ScientificEvalVisitor.java, PlotWindow.java, ejemplos.txt.

## Paso 5: Primera gramática
Escribimos ScientificCalc.g4 con las reglas prog, stat (printExpr, assign, blank) y expr (mulDiv, addSub, number, id, parens), más los tokens MUL, DIV, ADD, SUB, NUMBER, ID, NEWLINE, WS.

## Paso 6: Entender qué reconoce la gramática
Se analizó qué cadenas acepta NUMBER (enteros y decimales) y ID (identificadores tipo variable), y se identificaron casos inválidos como 2x o variable-final.

## Paso 7: Generar el Visitor
Ejecutamos:
bash
  antlr4 -no-listener -visitor ScientificCalc.g4
  
Esto generó automáticamente ScientificCalcLexer.java, ScientificCalcParser.java, ScientificCalcVisitor.java y ScientificCalcBaseVisitor.java, con métodos como visitAddSub, visitMulDiv, visitNumber, visitId, visitParens.

## Paso 8: Crear el Visitor propio
Creamos ScientificEvalVisitor.java, heredando de ScientificCalcBaseVisitor<Double> (trabajando con Double en vez de enteros), con la tabla de símbolos:
java
  Map<String, Double> memory = new HashMap<>();
## Paso 9: Interpretar números
Implementamos visitNumber, convirtiendo el texto del token (ctx.NUMBER().getText()) a double con Double.parseDouble(...).

## Paso 10: Suma y resta (y, como ejercicio, multiplicación/división)
Implementamos visitAddSub, visitando los dos subárboles (ctx.expr(0), ctx.expr(1)) y decidiendo la operación según ctx.op.getType().
Como actividad ("hazlo tú"), implementamos también visitMulDiv con la misma lógica, incluyendo control de división por cero.

## Paso 11: Paréntesis
Implementamos visitParens, simplemente delegando con return visit(ctx.expr()) — los paréntesis no cambian el valor, solo la estructura del árbol (y por tanto la precedencia).

## Paso 12: Programa principal
Creamos Main.java, encadenando el flujo completo: CharStreams.fromStream(System.in) → ScientificCalcLexer → CommonTokenStream → ScientificCalcParser → parser.prog() (árbol) → new ScientificEvalVisitor().visit(tree).

# Pruebas y Complementacion 
Hasta este momento solo hemos realizado la construccion paso a paso de las bases de nuestra calculadora, ahora a la par que realizamos pruebas, seguiremos implementando distintas funciones

## Paso 13: Mostrar los resultados
Implementamos visitPrintExpr, que visita la expresión de una línea y hace System.out.println(value) antes de retornarlo.

<img width="644" height="84" alt="imagen" src="https://github.com/user-attachments/assets/1d47c059-2891-4a6a-b447-9aecb100a117" />

## Paso 14: Primera prueba del intérprete
Compilación (javac *.java) y ejecución (java Main) de las primeras operaciones básicas (2+2, 10-3, 10*5, 20/4, 2+3*4, (2+3)*4) para confirmar que la precedencia de operadores funciona correctamente.

<img width="643" height="297" alt="imagen" src="https://github.com/user-attachments/assets/a5ce604b-5ada-4713-9763-9357b57a8b25" />

## Paso 15: Incorporar variables
Implementamos visitAssign (guarda ID = valor en memory) y visitId (lee una variable de memory, o imprime error si no está definida).

## Paso 16: Compruebe las variables
Prueba de asignación y uso: a=10, b=20, a+b, a*b.

<img width="647" height="186" alt="imagen" src="https://github.com/user-attachments/assets/aca31ead-29e7-46d9-9572-0232e24d1d5b" />

## Paso 17: Agregar potencia
Se añadió a la gramática:
antlr
  <assoc=right> expr '^' expr # power

Nota la asociatividad a la derecha (assoc=right), necesaria porque la potencia se evalúa de derecha a izquierda (2^3^2 = 2^(3^2), no (2^3)^2).

Se regeneró el proyecto con antlr4 -no-listener -visitor y se implementó visitPower con Math.pow(base, exponente).

## Paso 18: Compruebe la potencia
Prueba de 2^8, 10^2, 2^3+4, 2*3^2, verificando que la potencia tiene mayor precedencia que suma y multiplicación.

<img width="651" height="222" alt="imagen" src="https://github.com/user-attachments/assets/3f5f944d-2717-4c2e-a620-0db3a9388e79" />

## Paso 19: Funciones matemáticas
Se agregó la regla function (con sin, cos, tan, sqrt, log, ln, abs, exp) y la alternativa function '(' expr ')' # functionCall en expr.

## Paso 20: Implementar las funciones
Se implementó visitFunctionCall: obtiene el nombre de la función con ctx.function().getText(), evalúa el argumento, y despacha con un switch a Math.sin, Math.cos, Math.log10 (para log), Math.log (para ln), etc.

## Paso 21: Pruebe las funciones
Prueba de sqrt(25), cos(0), log(100), abs(-10) — este último expone la necesidad de números negativos, motivo del siguiente paso.

<img width="651" height="222" alt="imagen" src="https://github.com/user-attachments/assets/74750031-5d5a-4bfc-b898-9a4bfbb645ab" />

## Paso 22: Operadores unarios
Se agregó a expr la alternativa op=('+'|'-') expr # unary, y se implementó visitUnary: si el operador es -, invierte el signo del valor.

<img width="651" height="187" alt="imagen" src="https://github.com/user-attachments/assets/ddfac66d-2b0a-4817-a72e-87eef8c0ebe7" />

## Paso 23: Constantes matemáticas
Se agregó la regla constant (pi, e) y la alternativa constant # constantExpr, con visitConstantExpr devolviendo Math.PI o Math.E según el texto reconocido.

## Paso 24: Nuestra primera calculadora científica
Prueba integral combinando todo lo anterior: pi, 2*pi, sin(pi/2), cos(0), log(100), ln(e), sqrt(25), 2^8.

<img width="651" height="474" alt="imagen" src="https://github.com/user-attachments/assets/a851983f-6ebe-4cf6-90b6-e3daa23b00c8" />

## Paso 25: Crear el comando clear
Se agregó 'clear' NEWLINE # clear a stat, y visitClear vacía el mapa memory e imprime un mensaje de confirmación.

<img width="651" height="297" alt="imagen" src="https://github.com/user-attachments/assets/39c5c45e-0172-43a0-a0f9-f1fc544d1695" />

## Paso 26: Crear el comando vars
Se agregó 'vars' NEWLINE # showVars a stat, y visitShowVars recorre memory.entrySet() imprimiendo cada identificador = valor (o un mensaje si está vacío).

<img width="646" height="239" alt="imagen" src="https://github.com/user-attachments/assets/acb6185d-1a8a-4fb1-8623-2d0efa6cf33d" />

## Paso 27: Llegó el momento de graficar
Se explicó el concepto clave para graficar: una función se debe evaluar muchas veces (no una sola), cambiando el valor de x en cada evaluación, para obtener una tabla de puntos (x, y).

## Paso 28: Diseñar el comando plot
Se definió la sintaxis plot(expresion, xmin, xmax) y se agregó a la gramática:
antlr
  'plot' '(' expr ',' expr ',' expr ')' NEWLINE # plotExpr

## Paso 29: ¿Qué representan las tres expresiones?
Se identificó que ctx.expr(0) es la función a graficar, ctx.expr(1) es xmin y ctx.expr(2) es xmax.

## Paso 30: Muestrear una función
Se explicó la fórmula de muestreo (dividir el intervalo [xmin, xmax] en N puntos equiespaciados) y la idea de actualizar memory.put("x", x) antes de cada evaluación del árbol.

## Paso 31: Implemente visitPlotExpr
Se implementó el método completo: ciclo de 800 muestras, actualización de x en memory, evaluación de ctx.expr(0) en cada muestra, y almacenamiento de los pares (x, y) en listas.

## Paso 32: Un problema interesante
Se identificó que funciones como 1/x pueden producir Infinity, -Infinity o NaN en discontinuidades, y se agregó el filtro Double.isFinite(y) para descartar esos puntos antes de graficarlos.

## Paso 33: Crear la ventana gráfica
Se creó PlotWindow.java, extendiendo JPanel, con un constructor que recibe las listas de x e y, crea un JFrame de 800×600 y lo hace visible.

## Paso 34: Encontrar ymin y ymax
Se calcularon los límites verticales automáticamente a partir de los datos muestreados, usando .stream().mapToDouble(...).min()/.max().

## Paso 35: Transformar coordenadas
Se definieron las fórmulas para convertir coordenadas matemáticas (x, y) a píxeles de pantalla, notando que el eje vertical de Java crece hacia abajo (de ahí el getHeight() - ... en el cálculo de py).

## Paso 36: Dibujar la función
Se implementó paintComponent, recorriendo los puntos muestreados de a pares consecutivos y dibujando segmentos de línea (g2.drawLine(...)) entre ellos.

## Paso 37: Primera gráfica
Prueba visual: plot(x^2,-10,10) debe mostrar una parábola; plot(sin(x),-6.28,6.28) debe mostrar una onda seno.

<img width="763" height="501" alt="imagen" src="https://github.com/user-attachments/assets/3f71b08a-bceb-437c-a223-bb67f8315661" />

<img width="783" height="459" alt="imagen" src="https://github.com/user-attachments/assets/2622da1a-013f-47a9-a9c3-60e94fec92c0" />

## Paso 38: Archivo de pruebas
Se creó ejemplos.txt con una batería de instrucciones cubriendo todo el lenguaje construido hasta ese punto (aritmética, variables, funciones, constantes, vars, plot), para poder probar todo de una sola vez con java Main < ejemplos.txt.

## Paso 39: Explore el árbol sintáctico
Ejercicio de análisis (sin código nuevo): identificar, para una expresión como sin(x) + 2*x^2, qué parte del árbol corresponde a cada operación (suma, función, multiplicación, potencia, identificador, número), reforzando que visit(ctx.expr()) recorre una estructura de árbol, no una cadena de texto.

## Paso 40: Compruebe todo el lenguaje
Prueba final integradora con el ejemplo completo (radio, area, angulo, sin/cos, vars, dos plot), confirmando que el lenguaje completo funciona de punta a punta — exactamente el caso que ya verificaste con tu captura de pantalla en la conversación.

<img width="1300" height="477" alt="imagen" src="https://github.com/user-attachments/assets/dafd170a-b3b5-47dc-ba69-76b160ec77b5" />

## Resultados de referencia

| Expresión | Resultado |
|---|---|
| `2+2` | `4.0` |
| `2+3*4` | `14.0` |
| `(2+3)*4` | `20.0` |
| `sqrt(25)` | `5.0` |
| `2^8` | `256.0` |
| `sin(pi/2)` | `1.0` |
| `cos(0)` | `1.0` |
| `log(100)` | `2.0` |
| `ln(e)` | `1.0` |

---

## Preguntas finales

**1. ¿Cuál es la responsabilidad del Lexer?**

Convertir el texto plano de entrada en una secuencia de tokens. El lexer no entiende sintaxis ni significado; solo reconoce patrones de caracteres y les asigna una etiqueta. Por ejemplo, ante `radio = 10`, el lexer produce `ID("radio")`, `'='`, `NUMBER("10")`, `NEWLINE`.

**2. ¿Cuál es la responsabilidad del Parser?**

Tomar la secuencia de tokens y verificar que respete la estructura gramatical (las reglas `prog`, `stat`, `expr`), construyendo un árbol sintáctico. El parser es quien garantiza que `2+3*4` se agrupe como `2+(3*4)` y no como `(2+3)*4`, gracias al orden de las alternativas definido en la regla `expr`.

**3. ¿Qué función cumplen las etiquetas como `#addSub` o `#functionCall`?**

Le indican a ANTLR que cada alternativa etiquetada es conceptualmente distinta y debe generar su propio tipo de nodo (contexto) y su propio método `visit`. Sin ellas, todas las alternativas de `expr` compartirían un único `ExprContext` genérico. Con las etiquetas se obtienen automáticamente clases como `AddSubContext` o `FunctionCallContext`, cada una con sus propios campos (`ctx.op`, `ctx.function()`, `ctx.expr(0)`...).

**4. ¿Qué ventaja ofrece el patrón Visitor?**

Separa la sintaxis de la semántica. La gramática solo describe qué se puede escribir; el Visitor decide qué significa cada construcción. Esto permite, por ejemplo, evaluar el mismo árbol de una expresión una sola vez (`sin(pi/2)`) o evaluarlo repetidamente cambiando una variable (`plot(sin(x), ...)`), sin tener que modificar la gramática. También permitiría, en teoría, crear visitors alternativos (por ejemplo, uno de depuración) sin tocar el evaluador original.

**5. ¿Qué representa la tabla de símbolos?**

El `Map<String, Double> memory` declarado en el Visitor. Es la memoria del intérprete: asocia cada identificador (`radio`, `area`, `angulo`, y también `x` durante un `plot`) con su valor numérico actual. Es justamente lo que se observa al ejecutar `vars`.

**6. ¿Por qué la variable `x` cambia continuamente durante una gráfica?**

Porque graficar una función implica evaluarla en muchos puntos distintos del eje horizontal. `visitPlotExpr` recorre un ciclo de 800 muestras y, en cada iteración, hace `memory.put("x", x)` antes de volver a visitar la expresión. Así, cada vez que el árbol pide el valor de `x` (en `visitId`), obtiene un valor diferente.

**7. ¿Por qué podemos evaluar el mismo árbol sintáctico varias veces?**

Porque el árbol es una estructura inmutable y sin estado propio: solo describe la forma de la expresión, no guarda ningún valor calculado. Todo el estado que cambia entre evaluaciones vive afuera del árbol, en la tabla de símbolos. Por eso es posible llamar `visit(mismoArbol)` cientos de veces y obtener resultados distintos cada vez, sin volver a parsear el texto ni modificar el árbol.

**8. ¿Qué sucede cuando se intenta graficar una función con una discontinuidad?**

Java no lanza una excepción al dividir por cero con `double`; produce valores especiales como `Infinity`, `-Infinity` o `NaN` (por ejemplo, `1/x` en `x = 0`). Si esos valores llegaran sin filtrar a `PlotWindow`, la curva se dispararía fuera de la ventana o rompería la escala del gráfico. Por eso `visitPlotExpr` descarta esos puntos con `Double.isFinite(y)` antes de almacenarlos, y la curva simplemente se "corta" alrededor de la discontinuidad.

**9. ¿Qué modificaciones serían necesarias para implementar funciones con dos argumentos?**

No basta con reutilizar la regla `function` (que asume un solo `expr` entre paréntesis); haría falta una regla nueva (por ejemplo `function2`) y una alternativa nueva en `expr` con dos `expr` separados por coma (`function2 '(' expr ',' expr ')'`). Luego habría que regenerar el parser con `antlr4 -no-listener -visitor` para obtener el nuevo contexto y su método `visit`, e implementarlo en el Visitor evaluando ambos argumentos y despachando según el nombre de la función.

**10. ¿Por qué la calculadora desarrollada puede considerarse un lenguaje de dominio específico (DSL)?**

Porque tiene sintaxis propia (una gramática formal, no un fragmento de otro lenguaje de propósito general), está restringido a un dominio concreto (expresiones matemáticas, variables, funciones y graficación) y no pretende ser de propósito general: no tiene estructuras de control como `if`/`while` porque no las necesita para resolver su dominio. Contrasta con Java, el lenguaje de propósito general en el que está implementado el intérprete, que sí busca poder expresar cualquier programa.

## Reflexión final

El desarrollo de este laboratorio partió de una gramática muy pequeña para expresiones aritméticas y fue creciendo progresivamente hasta convertirse en un lenguaje con variables, funciones científicas, constantes, comandos y graficación. La arquitectura final puede resumirse como:

```
Gramática → Lexer → Parser → Árbol → Visitor
```

La idea central es que **la gramática define la sintaxis** y **el Visitor implementa la semántica**. Gracias a esta separación fue posible extender el lenguaje —agregar potencia, funciones, constantes, comandos y graficación— sin introducir toda la lógica de la aplicación dentro de la gramática, ni reescribir el intérprete completo en cada paso.

Esta misma estrategia constituye la base para construir sistemas mucho más complejos: intérpretes, compiladores, traductores, analizadores de código y lenguajes de consulta. La calculadora científica desarrollada en este laboratorio es, en definitiva, un primer ejemplo de construcción de un pequeño DSL (lenguaje de dominio específico) matemático.
