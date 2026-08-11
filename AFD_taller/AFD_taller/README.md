# AFD - Simulador de Autómatas Finitos Deterministas

Trabajo de la materia de Compiladores/Autómatas: implementación en Python de un
simulador genérico de AFD (Autómata Finito Determinista), configurable por
archivo de texto.

Ejercicio base: **3.16 (pág. 149)**, libro *Compiladores: Principios, Técnicas
y Herramientas* — Aho, Sethi, Ullman.

## Contenido

| Archivo | Descripción |
|---|---|
| `AFD.py` | Programa principal. Lee un AFD desde un archivo de configuración y prueba cadenas de entrada. |
| `conf.txt` | Configuración del AFD para el inciso d): `(a\|b)*abb(a\|b)*` (contiene la subcadena "abb"). |
| `cadenas.txt` | Cadenas de prueba, incluye `ababbab` (la del ejercicio). |
| `conf_a.txt` | AFD para el inciso a): `(a\|b)*` |
| `conf_b.txt` | AFD para el inciso b): `(a*\|b*)*` (lenguaje idéntico al de a) |
| `conf_c.txt` | AFD para el inciso c): `((ε\|a)b*)*` (lenguaje idéntico al de a) |
| `conf_d_literal.txt` | AFD para el inciso d) tal como aparece impreso literalmente en el libro: `(b\|b)*abb(a\|b)*` |

## Uso

```bash
python3 AFD.py conf.txt cadenas.txt
```

Prueba con cualquier otro inciso:

```bash
python3 AFD.py conf_a.txt cadenas.txt
python3 AFD.py conf_b.txt cadenas.txt
python3 AFD.py conf_c.txt cadenas.txt
python3 AFD.py conf_d_literal.txt cadenas.txt
```

## Formato de `conf.txt`

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

- Líneas vacías o que empiezan con `#` se ignoran (comentarios).
- Cada línea de `TRANSICIONES` tiene el formato: `estado_origen,simbolo,estado_destino`.

## Formato de `cadenas.txt`

Una cadena de prueba por línea:

```
ababbab
abb
aab
```

## Salida

El programa muestra, para cada cadena, la secuencia completa de movimientos
δ(estado, resto_de_entrada) y si la cadena es **ACEPTADA** o **RECHAZADA**,
junto con el motivo del rechazo cuando aplica (símbolo fuera del alfabeto,
transición no definida, o estado final no alcanzado).

## Autores

Trabajo en grupo — Actividad "Implementar AFD en Python".
