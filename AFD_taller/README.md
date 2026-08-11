# AFD - Simulador de Autómatas Finitos Deterministas

Trabajo de Compiladores/Autómatas: implementación en Python de un
simulador genérico de AFD (Autómata Finito Determinista), configurable por
archivo de texto.

Ejercicio base: **3.16 (pág. 149)**, libro *Compiladores: Principios, Técnicas
y Herramientas* — Aho, Sethi, Ullman.

## Contenido

| Archivo | Descripción |
|---|---|
| `AFD.py` | Programa principal. Lee un AFD desde un archivo de configuración y prueba cadenas de entrada. |
| `conf_a.txt` / `cadenas_a.txt` | AFD y cadenas de prueba para el literal a): `(a\|b)*` |
| `conf_b.txt` / `cadenas_b.txt` | AFD y cadenas de prueba para el literal b): `(a*\|b*)*` |
| `conf_c.txt` / `cadenas_c.txt` | AFD y cadenas de prueba para el literal c): `((ε\|a)b*)*` |
| `conf_d.txt` / `cadenas_d.txt` | AFD y cadenas de prueba para el literal d): `(a\|b)*abb(a\|b)*` |

Cada literal tiene su propio par de archivos (configuración + cadenas), como
se pidió en clase.

## Uso

Cada literal se ejecuta por separado, pasando su configuración y su archivo
de cadenas correspondiente:

```bash
python3 AFD.py conf_a.txt cadenas_a.txt
python3 AFD.py conf_b.txt cadenas_b.txt
python3 AFD.py conf_c.txt cadenas_c.txt
python3 AFD.py conf_d.txt cadenas_d.txt
```

## Sobre los literales a), b) y c)

Los tres definen el mismo lenguaje: cualquier cadena formada por a's y b's.
Por eso el AFD de los tres es el mismo autómata de un solo estado (acepta
todo). Esto no es un error: es porque las tres expresiones regulares son
equivalentes entre sí, aunque se vean distintas.

## Sobre el literal d)

Se usó la expresión `(a|b)*abb(a|b)*`: el lenguaje de todas las cadenas que
contienen la subcadena "abb" en cualquier posición. Es el ejemplo trabajado
en el capítulo 3 del libro, justo antes del ejercicio.

## Formato de los archivos `conf_x.txt`

```
ESTADOS: q0,q1,q2,q3
ALFABETO: a,b
INICIAL: q0
FINALES: q3
TRANSICIONES:
q0,a,q1
q0,b,q0
q1,a,q1
q1,b,q2
q2,a,q1
q2,b,q3
q3,a,q3
q3,b,q3
```

Cada línea de `TRANSICIONES` tiene el formato: `estado_origen,simbolo,estado_destino`.

## Formato de los archivos `cadenas_x.txt`

Una cadena de prueba por línea:

```
ababbab
abb
aab
```

## Salida del programa

Para cada cadena se muestra la secuencia completa de movimientos
δ(estado, resto_de_entrada) y si la cadena es **ACEPTADA** o **RECHAZADA**,
con el motivo del rechazo cuando aplica.

## Cómo ver el contenido de un archivo en la terminal

Para mostrar el contenido de cualquier archivo sin abrir un editor, usar:

```bash
cat cadenas_d.txt
```

Para editar un archivo (agregar o quitar cadenas de prueba) sí se puede usar
`nano`:

```bash
nano cadenas_d.txt
```

## Autores
Samuel Merchan, Diego Moreno
— Actividad "Implementar AFD en Python".
