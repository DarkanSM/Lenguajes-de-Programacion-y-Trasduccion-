# Preguntas de análisis

**1. ¿Cuál es la diferencia entre un lexema y un token?**
Un lexema es la secuencia de caracteres tal como aparece en el texto de entrada (por ejemplo, `ventas`). Un token es la representación abstracta que el lexer asigna a ese lexema, formada por un tipo (por ejemplo `ID`) y, opcionalmente, el lexema asociado. Un mismo tipo de token puede corresponder a muchos lexemas distintos.

**2. ¿Cuál es la responsabilidad del lexer?**
Convertir la secuencia de caracteres de entrada en una secuencia de tokens, agrupando los caracteres según las reglas léxicas y descartando lo que no es relevante para el parser (como los espacios en blanco).

**3. ¿Cuál es la responsabilidad del parser?**
Tomar la secuencia de tokens producida por el lexer y verificar si su orden y estructura cumplen las reglas sintácticas del lenguaje, construyendo un árbol sintáctico como resultado.

**4. ¿Por qué las reglas léxicas comienzan con mayúscula en ANTLR?**
Es una convención de ANTLR que le permite distinguir automáticamente las reglas léxicas (que producen tokens) de las reglas sintácticas (que producen reglas del parser), sin necesidad de una palabra clave adicional.

**5. ¿Por qué las reglas sintácticas comienzan con minúscula?**
Por la misma convención: el uso de minúscula indica a ANTLR que la regla pertenece al parser y describe una estructura compuesta por tokens y/o otras reglas sintácticas.

**6. ¿Cuál es la función de `->skip`?**
Indica que los caracteres reconocidos por esa regla léxica deben descartarse y no enviarse al parser. Se usa típicamente para espacios en blanco, tabulaciones, saltos de línea y comentarios.

**7. ¿Qué representa `EOF`?**
Es un token especial que representa el final del flujo de entrada. Incluirlo en una regla sintáctica obliga a que toda la entrada haya sido consumida para que el reconocimiento sea válido, evitando que se acepte una entrada parcial.

**8. ¿Qué información representa un árbol sintáctico?**
Representa la estructura jerárquica que el parser reconoció en la entrada según las reglas de la gramática: los nodos internos corresponden a reglas sintácticas aplicadas y las hojas corresponden a los tokens reconocidos por el lexer.

**9. ¿Cuál es la diferencia entre Listener y Visitor?**
El Listener recorre el árbol de forma automática y dispara eventos (`enterX`/`exitX`) a medida que ANTLR visita cada nodo, sin que el desarrollador controle el orden del recorrido. El Visitor, en cambio, requiere que el desarrollador implemente explícitamente cómo se recorre cada nodo (llamando manualmente a `visit` sobre los hijos), lo que da más control, por ejemplo para decidir no visitar cierta rama o para devolver un valor calculado desde el recorrido.

**10. ¿Cómo podría utilizarse ANTLR para construir un lenguaje de dominio específico (DSL)?**
Definiendo una gramática `.g4` con las palabras clave y estructuras propias del dominio (como se hizo en este proyecto con `mostrar`, `cargar` y `graficar`), generando el lexer y el parser correspondientes, y luego usando un Visitor o Listener para traducir el árbol sintáctico reconocido en acciones concretas (ejecutar una consulta, generar una gráfica, invocar una API, etc.), sin tener que escribir un analizador manual desde cero.
