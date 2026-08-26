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

## Instalación en Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y default-jdk antlr4 libantlr4-runtime-java
```

Verifica que todo quedó instalado:

```bash
java -version
antlr4
```

> Si usas otra distribución o prefieres la versión más reciente de ANTLR descargada directamente de [antlr.org](https://www.antlr.org/download.html), basta con ajustar la ruta del `.jar` del runtime en los comandos de compilación/ejecución más abajo.

## Cómo clonar y ejecutar

```bash
git clone <URL-DE-TU-REPOSITORIO>
cd ScientificCalculator

# 1. Generar el lexer, parser y visitor a partir de la gramática
antlr4 -no-listener -visitor ScientificCalc.g4

# 2. Compilar
javac -cp .:/usr/share/java/antlr4-runtime.jar *.java

# 3. Ejecutar en modo interactivo (Ctrl+D para salir)
java -cp .:/usr/share/java/antlr4-runtime.jar Main

# (opcional) Ejecutar con el archivo de ejemplos
java -cp .:/usr/share/java/antlr4-runtime.jar Main < ejemplos.txt
```

Cada vez que modifiques `ScientificCalc.g4`, vuelve a correr el paso 1 antes de recompilar.

### Prueba rápida

```bash
echo "2+2" | java -cp .:/usr/share/java/antlr4-runtime.jar Main
# 4.0
```

### Graficar una función

```
plot(sin(x), -6.28, 6.28)
plot(x^2, -10, 10)
```

Cada `plot` abre una ventana independiente con la curva dibujada (requiere entorno gráfico / X11).

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
