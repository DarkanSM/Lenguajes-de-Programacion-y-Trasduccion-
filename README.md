# Lenguaje de instrucciones con ANTLR4

Proyecto de la actividad práctica de la guía de ANTLR 4 (sección 16), asignatura
Lenguajes de Programación. Reconoce instrucciones del tipo:

```
mostrar ventas
cargar clientes
graficar ingresos
```

## Estructura del repositorio

```
antlr-instrucciones/
├── src/
│   ├── Instrucciones.g4   # Gramática (lexer + parser combinados)
│   └── Main.java          # Driver que imprime tokens y árbol sintáctico
├── tests/
│   ├── entrada_valida.txt     # 5 instrucciones válidas
│   └── entrada_invalida.txt   # 3 casos que deben ser rechazados
├── docs/
│   ├── explicacion_reglas.md
│   ├── preguntas_analisis.md
│   └── conclusiones.md
└── README.md
```

## Cómo ejecutarlo

Requiere Java y ANTLR4 instalados (ver guía de instalación por separado).

```bash
cd src
antlr4 -visitor Instrucciones.g4
javac *.java
java Main ../tests/entrada_valida.txt
java Main ../tests/entrada_invalida.txt
```

## Documentación

- [`docs/explicacion_reglas.md`](docs/explicacion_reglas.md): explicación de cada regla léxica y sintáctica.
- [`docs/preguntas_analisis.md`](docs/preguntas_analisis.md): respuestas a las preguntas de análisis de la guía.
- [`docs/conclusiones.md`](docs/conclusiones.md): conclusiones, incluida la diferencia entre lexer y parser.

## Referencias

- Parr, T. (2013). *The Definitive ANTLR 4 Reference*. Pragmatic Bookshelf.
- Documentación oficial de ANTLR4: https://www.antlr.org
