#!/usr/bin/env python3
"""
AFD.py - Simulador de Autómatas Finitos Deterministas (AFD)

Uso:
    python3 AFD.py conf.txt cadenas.txt

Descripción:
    Lee la definición de un AFD desde un archivo de configuración (conf.txt)
    y prueba una o varias cadenas de entrada listadas en otro archivo
    (cadenas.txt), mostrando la secuencia completa de movimientos
    (delta(estado, símbolo) -> estado) para cada cadena, tal como se pide
    en el ejercicio 3.16 (pág. 149) del libro de Aho, Sethi y Ullman.

Formato de conf.txt:
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

    - Las líneas vacías o que comienzan con '#' se ignoran (comentarios).
    - Cada línea de TRANSICIONES tiene el formato: estado_origen,simbolo,estado_destino

Formato de cadenas.txt:
    Una cadena por línea. Ejemplo:
    ababbab
    aab
    bbb
"""

import sys
import os


class ErrorConfiguracionAFD(Exception):
    """Se lanza cuando el archivo de configuración del AFD es inválido."""
    pass


class AFD:
    """Representa un Autómata Finito Determinista y sabe simular cadenas."""

    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.finales = finales
        self.transiciones = transiciones  # dict {(estado, simbolo): estado}

    @classmethod
    def desde_archivo(cls, ruta_conf):
        """Construye un AFD a partir de un archivo de configuración de texto."""
        if not os.path.isfile(ruta_conf):
            raise ErrorConfiguracionAFD(
                f"No se encontró el archivo de configuración: {ruta_conf}"
            )

        estados = None
        alfabeto = None
        inicial = None
        finales = None
        transiciones = {}
        leyendo_transiciones = False

        with open(ruta_conf, "r", encoding="utf-8") as f:
            for num_linea, linea_original in enumerate(f, start=1):
                linea = linea_original.strip()

                # Ignorar líneas vacías y comentarios
                if not linea or linea.startswith("#"):
                    continue

                if leyendo_transiciones:
                    # Si la línea trae otra etiqueta (poco común), dejamos de
                    # leer transiciones y volvemos a procesar como encabezado
                    if ":" in linea and linea.split(":")[0].strip().upper() in (
                        "ESTADOS", "ALFABETO", "INICIAL", "FINALES", "TRANSICIONES"
                    ):
                        leyendo_transiciones = False
                    else:
                        partes = [p.strip() for p in linea.split(",")]
                        if len(partes) != 3:
                            raise ErrorConfiguracionAFD(
                                f"Línea {num_linea}: transición inválida '{linea}'. "
                                "Formato esperado: estado_origen,simbolo,estado_destino"
                            )
                        origen, simbolo, destino = partes
                        transiciones[(origen, simbolo)] = destino
                        continue

                if ":" not in linea:
                    raise ErrorConfiguracionAFD(
                        f"Línea {num_linea}: no se reconoce '{linea}'"
                    )

                etiqueta, _, valor = linea.partition(":")
                etiqueta = etiqueta.strip().upper()
                valor = valor.strip()

                if etiqueta == "ESTADOS":
                    estados = [s.strip() for s in valor.split(",") if s.strip()]
                elif etiqueta == "ALFABETO":
                    alfabeto = [s.strip() for s in valor.split(",") if s.strip()]
                elif etiqueta == "INICIAL":
                    inicial = valor
                elif etiqueta == "FINALES":
                    finales = [s.strip() for s in valor.split(",") if s.strip()]
                elif etiqueta == "TRANSICIONES":
                    leyendo_transiciones = True
                else:
                    raise ErrorConfiguracionAFD(
                        f"Línea {num_linea}: etiqueta desconocida '{etiqueta}'"
                    )

        # Validaciones básicas
        if estados is None:
            raise ErrorConfiguracionAFD("Falta la sección ESTADOS en conf.txt")
        if alfabeto is None:
            raise ErrorConfiguracionAFD("Falta la sección ALFABETO en conf.txt")
        if inicial is None:
            raise ErrorConfiguracionAFD("Falta la sección INICIAL en conf.txt")
        if finales is None:
            raise ErrorConfiguracionAFD("Falta la sección FINALES en conf.txt")
        if inicial not in estados:
            raise ErrorConfiguracionAFD(
                f"El estado inicial '{inicial}' no está en ESTADOS"
            )
        for qf in finales:
            if qf not in estados:
                raise ErrorConfiguracionAFD(
                    f"El estado final '{qf}' no está en ESTADOS"
                )
        for (origen, simbolo), destino in transiciones.items():
            if origen not in estados:
                raise ErrorConfiguracionAFD(
                    f"Transición inválida: el estado '{origen}' no está en ESTADOS"
                )
            if destino not in estados:
                raise ErrorConfiguracionAFD(
                    f"Transición inválida: el estado '{destino}' no está en ESTADOS"
                )
            if simbolo not in alfabeto:
                raise ErrorConfiguracionAFD(
                    f"Transición inválida: el símbolo '{simbolo}' no está en ALFABETO"
                )

        return cls(estados, alfabeto, inicial, set(finales), transiciones)

    def mover(self, estado, simbolo):
        """Devuelve el estado siguiente, o None si no hay transición definida."""
        return self.transiciones.get((estado, simbolo))

    def procesar_cadena(self, cadena):
        """
        Simula el AFD sobre 'cadena' y devuelve una tupla:
        (aceptada: bool, pasos: list[str], motivo_rechazo: str o None)

        'pasos' contiene el registro delta(estado, resto_de_entrada) -> estado
        igual a como se muestra en el libro (ej. ejercicio 3.16).
        """
        estado_actual = self.inicial
        pasos = []
        resto = cadena

        pasos.append(f"δ({estado_actual}, {resto if resto else 'ε'})")

        for i, simbolo in enumerate(cadena):
            if simbolo not in self.alfabeto:
                motivo = (
                    f"el símbolo '{simbolo}' no pertenece al alfabeto "
                    f"{{{', '.join(self.alfabeto)}}}"
                )
                return False, pasos, motivo

            siguiente = self.mover(estado_actual, simbolo)
            resto = cadena[i + 1:]

            if siguiente is None:
                motivo = (
                    f"no existe transición δ({estado_actual}, {simbolo}) "
                    "(cadena muerta / estado trampa no definido)"
                )
                pasos.append(
                    f"  --{simbolo}-->  [SIN TRANSICIÓN, cadena RECHAZADA]"
                )
                return False, pasos, motivo

            pasos.append(
                f"  --{simbolo}-->  δ({siguiente}, {resto if resto else 'ε'})"
            )
            estado_actual = siguiente

        aceptada = estado_actual in self.finales
        if not aceptada:
            motivo = (
                f"la cadena termina en el estado '{estado_actual}', "
                f"que no es un estado final {sorted(self.finales)}"
            )
            return False, pasos, motivo

        return True, pasos, None


def leer_cadenas(ruta_cadenas):
    """Lee las cadenas de prueba, una por línea. Ignora vacías y comentarios."""
    if not os.path.isfile(ruta_cadenas):
        raise ErrorConfiguracionAFD(
            f"No se encontró el archivo de cadenas: {ruta_cadenas}"
        )
    cadenas = []
    with open(ruta_cadenas, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n").rstrip("\r")
            if not linea.strip() or linea.strip().startswith("#"):
                continue
            cadenas.append(linea.strip())
    return cadenas


def imprimir_encabezado_afd(afd):
    print("AUTÓMATA FINITO DETERMINISTA CARGADO")
    print(f"Estados     : {{{', '.join(afd.estados)}}}")
    print(f"Alfabeto    : {{{', '.join(afd.alfabeto)}}}")
    print(f"Estado inicial : {afd.inicial}")
    print(f"Estados finales: {{{', '.join(sorted(afd.finales))}}}")
    print("Tabla de transiciones:")
    for (origen, simbolo), destino in sorted(afd.transiciones.items()):
        print(f"  δ({origen}, {simbolo}) = {destino}")
    print()


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 AFD.py <conf.txt> <cadenas.txt>")
        print("Ejemplo: python3 AFD.py conf.txt cadenas.txt")
        sys.exit(1)

    ruta_conf = sys.argv[1]
    ruta_cadenas = sys.argv[2]

    try:
        afd = AFD.desde_archivo(ruta_conf)
        cadenas = leer_cadenas(ruta_cadenas)
    except ErrorConfiguracionAFD as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    imprimir_encabezado_afd(afd)

    if not cadenas:
        print("El archivo de cadenas está vacío. No hay nada que procesar.")
        sys.exit(0)

    total = len(cadenas)
    aceptadas = 0

    for idx, cadena in enumerate(cadenas, start=1):
        print(f"Cadena {idx}/{total}: \"{cadena}\"")
        aceptada, pasos, motivo = afd.procesar_cadena(cadena)

        print("Secuencia de movimientos:")
        for paso in pasos:
            print(f"  {paso}")

        if aceptada:
            aceptadas += 1
            print(f'Resultado: ACEPTADA ✔  (la cadena "{cadena}" pertenece al lenguaje)')
        else:
            print(f'Resultado: RECHAZADA ✘  ({motivo})')
        print()

    print(f"Resumen: {aceptadas}/{total} cadenas aceptadas")


if __name__ == "__main__":
    main()
