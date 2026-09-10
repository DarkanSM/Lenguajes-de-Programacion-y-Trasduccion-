# Gramática del DSL — Vocabulario y EBNF completa

Dominio: ciencia de datos y visualización, caso de estudio: ventas/comercio.
Palabras reservadas en español. Alcance del Corte 1 marcado explícitamente.

---

## 1. Vocabulario léxico

### Palabras reservadas

```
cargar  guardar  como
seleccionar  filtrar  donde  ordenar  por  ascendente  descendente
renombrar  eliminar_duplicados
crear
agrupar  resumir
graficar  x  y  titulo
funcion  retornar
si  entonces  sino
y  o  no
verdadero  falso
```

### Funciones de agregación (reservadas, usadas dentro de `resumir`)
```
contar  suma  promedio  mediana  minimo  maximo  desviacion_estandar
```

### Tipos de gráfica (reservadas, usadas dentro de `graficar`)
```
barras  lineas  histograma  dispersion  caja
```

### Operadores
```
Aritméticos:   +  -  *  /  %  ^
Relacionales:  ==  !=  <  >  <=  >=
Lógicos:       y  o  no
Pipeline:      |>
Asignación:    =
```

### Literales
```
NUMERO_ENTERO   : dígitos, ej. 42
NUMERO_DECIMAL  : dígitos.dígitos, ej. 3.14
CADENA          : "texto entre comillas dobles"
BOOLEANO        : verdadero | falso
```

### Identificadores
```
IDENTIFICADOR : (letra | '_') (letra | dígito | '_')*
```
No puede coincidir con ninguna palabra reservada.

### Comentarios
```
# comentario de línea completa
```

---

## 2. EBNF completa del lenguaje

> Las reglas marcadas con **[Corte 1]** son las implementadas en esta fase.
> Las marcadas con **[Corte 2]** / **[Corte 3]** se documentan ahora para que el diseño sea consistente, pero se implementan en fases posteriores.

```ebnf
(* ===================== ESTRUCTURA GENERAL ===================== *)

programa            ::= (sentencia)* ;                                    (* [Corte 1] *)

sentencia            ::= asignacion
                        | sentenciaGraficar
                        | sentenciaGuardar                                  (* [Corte 2] *)
                        | sentenciaFuncion                                  (* [Corte 3, opcional] *)
                        | sentenciaSi ;                                     (* [Corte 3, opcional] *)

(* ===================== ASIGNACIÓN Y PIPELINE ===================== *)

asignacion           ::= IDENTIFICADOR '=' expresionPipeline ;             (* [Corte 1] *)

expresionPipeline    ::= fuenteDatos ( '|>' operacion )* ;                 (* [Corte 1 parcial: solo cargar+seleccionar+filtrar] *)

fuenteDatos          ::= 'cargar' CADENA                                   (* [Corte 1] *)
                        | IDENTIFICADOR ;                                  (* [Corte 1] *)

operacion            ::= opSeleccionar                                     (* [Corte 1] *)
                        | opFiltrar                                        (* [Corte 1] *)
                        | opOrdenar                                        (* [Corte 2] *)
                        | opRenombrar                                      (* [Corte 2] *)
                        | opEliminarDuplicados                             (* [Corte 2] *)
                        | opCrearColumna                                   (* [Corte 2] *)
                        | opAgrupar                                        (* [Corte 2] *)
                        | opResumir ;                                      (* [Corte 2] *)

opSeleccionar        ::= 'seleccionar' '[' listaIdentificadores ']' ;      (* [Corte 1] *)

opFiltrar            ::= 'filtrar' 'donde' expresionBooleana ;             (* [Corte 1] *)

opOrdenar            ::= 'ordenar' 'por' '[' listaIdentificadores ']'
                          ( 'ascendente' | 'descendente' )? ;              (* [Corte 2] *)

opRenombrar          ::= 'renombrar' IDENTIFICADOR 'como' IDENTIFICADOR
                          ( ',' IDENTIFICADOR 'como' IDENTIFICADOR )* ;    (* [Corte 2] *)

opEliminarDuplicados ::= 'eliminar_duplicados' ;                          (* [Corte 2] *)

opCrearColumna       ::= 'crear' IDENTIFICADOR '=' expresionAritmetica ;   (* [Corte 2] *)

opAgrupar            ::= 'agrupar' 'por' '[' listaIdentificadores ']' ;    (* [Corte 2] *)

opResumir            ::= 'resumir' listaResumenes ;                        (* [Corte 2] *)
                        (* Operación independiente: puede aparecer sola en el pipeline
                           (resumen global de toda la tabla, un único grupo implícito)
                           o inmediatamente después de opAgrupar (resumen por grupo). *)

listaResumenes       ::= resumenItem ( ',' resumenItem )* ;                (* [Corte 2] *)

resumenItem          ::= IDENTIFICADOR '=' funcionAgregacion '(' (IDENTIFICADOR)? ')' ;  (* [Corte 2] *)

funcionAgregacion    ::= 'contar' | 'suma' | 'promedio' | 'mediana'
                        | 'minimo' | 'maximo' | 'desviacion_estandar' ;    (* [Corte 2] *)

(* ===================== EXPRESIONES ===================== *)

expresionBooleana    ::= expresionBooleana ( 'y' | 'o' ) expresionBooleana (* [Corte 1] *)
                        | 'no' expresionBooleana
                        | expresionRelacional
                        | '(' expresionBooleana ')' ;

expresionRelacional  ::= expresionAritmetica ( OP_REL expresionAritmetica )? ;  (* [Corte 1] *)

expresionAritmetica  ::= expresionAritmetica ( '+' | '-' ) termino          (* [Corte 1] *)
                        | termino ;

termino              ::= termino ( '*' | '/' | '%' ) factor                (* [Corte 1] *)
                        | factor ;

factor                ::= factor '^' factor                                (* [Corte 1] *)
                        | primario ;

primario              ::= NUMERO_ENTERO | NUMERO_DECIMAL | CADENA
                        | BOOLEANO | IDENTIFICADOR
                        | '(' expresionAritmetica ')' ;                    (* [Corte 1] *)

listaIdentificadores  ::= IDENTIFICADOR ( ',' IDENTIFICADOR )* ;           (* [Corte 1] *)

(* ===================== VISUALIZACIÓN ===================== *)

sentenciaGraficar     ::= 'graficar' tipoGrafica IDENTIFICADOR
                          ( 'x' IDENTIFICADOR )?
                          ( 'y' IDENTIFICADOR )?
                          ( 'titulo' CADENA )?
                          ( 'guardar' 'como' CADENA )? ;                   (* [Corte 1: solo sintaxis] / [Corte 3: ejecución real] *)

tipoGrafica           ::= 'barras' | 'lineas' | 'histograma'
                        | 'dispersion' | 'caja' ;                          (* [Corte 1] *)

(* ===================== ALMACENAMIENTO ===================== *)

sentenciaGuardar      ::= 'guardar' IDENTIFICADOR 'como' CADENA ;          (* [Corte 2] *)

(* ===================== ABSTRACCIÓN (opcional, Corte 3) ===================== *)

sentenciaFuncion      ::= 'funcion' IDENTIFICADOR '(' (listaIdentificadores)? ')'
                          '{' (sentencia)* 'retornar' expresionAritmetica '}' ;

sentenciaSi           ::= 'si' expresionBooleana 'entonces' '{' (sentencia)* '}'
                          ( 'sino' '{' (sentencia)* '}' )? ;
```

---

## 3. Alcance exacto que se implementa en el Corte 1

Reglas activas en `grammar/DSL.g4` para esta fase:

- `programa`, `sentencia` (solo `asignacion` y `sentenciaGraficar`)
- `asignacion`, `expresionPipeline`, `fuenteDatos`
- `operacion` → solo `opSeleccionar` y `opFiltrar`
- Todo el árbol de expresiones (`expresionBooleana` → ... → `primario`)
- `sentenciaGraficar` (reconocimiento sintáctico, sin ejecución)
- `listaIdentificadores`

Quedan **fuera del Corte 1** (se agregan en Corte 2/3): `ordenar`, `renombrar`, `eliminar_duplicados`, `crear`, `agrupar`/`resumir`, `guardar`, `funcion`/`retornar`, `si`/`entonces`/`sino`.

---

## 4. Justificación de diseño

- **Vocabulario 100% en español** con palabras completas (no símbolos como `&&`), priorizando legibilidad para el dominio de ventas — decisión validada con el equipo.
- **Funciones de agregación y tipos de gráfica como categorías léxicas separadas** (no identificadores genéricos): permite detectar en el análisis semántico (Corte 2) si alguien escribe una función o tipo de gráfica inexistente, en vez de tratarlo como un error de "variable no declarada" genérico.
- **Pipeline `|>`** se mantiene simbólico: no tiene traducción natural corta al español sin volverse verboso, y es un símbolo ya reconocible en lenguajes de datos (R, Elixir).
- **`agrupar` y `resumir` como operaciones independientes del pipeline** (no una sola regla compuesta): se decidió separarlas porque un DSL de ciencia de datos necesita poder expresar tanto un **resumen por grupos** como un **resumen global de toda la tabla** (ej. "ingreso total de la empresa", sin agrupar por ciudad). Con la gramática, ambos casos son sintácticamente válidos:

  ```
  # Resumen por grupo (agrupar + resumir)
  resumen_ciudad = ventas_limpias
      |> agrupar por [ciudad]
      |> resumir ingreso = suma(total), promedio = promedio(total)

  # Resumen global (solo resumir, sin agrupar antes)
  resumen_empresa = ventas_limpias
      |> resumir ingreso_total = suma(total), transacciones = contar()
  ```

  El costo de esta flexibilidad se traslada del análisis sintáctico al semántico: en el Corte 2, `resumir` sin un `agrupar` inmediatamente antes en el mismo pipeline se interpreta como **"un solo grupo implícito equivalente a toda la tabla"**, en vez de ser un error. Esta regla debe implementarse explícitamente en el Visitor (`dsl_core/visitor.py`) y probarse con casos específicos en `tests/test_dsl_data/` (resumen con agrupar, resumen sin agrupar, y — si se desea mantener acotado el alcance — un `agrupar` sin `resumir` después, que debe decidirse si es error o simplemente devuelve la tabla agrupada sin agregar).
