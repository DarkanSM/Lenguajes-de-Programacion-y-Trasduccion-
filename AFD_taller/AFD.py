import sys
import os


class ErrorConfiguracionAFD(Exception):
    pass


class AFD:
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.finales = finales
        self.transiciones = transiciones

    @classmethod
    def desde_archivo(cls, ruta):
        if not os.path.isfile(ruta):
            raise ErrorConfiguracionAFD(f"no encontre el archivo {ruta}")

        estados = None
        alfabeto = None
        inicial = None
        finales = None
        trans = {}
        leyendo = False

        f = open(ruta, "r", encoding="utf-8")
        n = 0
        for raw in f:
            n += 1
            l = raw.strip()

            if not l or l[0] == "#":
                continue

            if leyendo:
                etq = l.split(":")[0].strip().upper()
                if ":" in l and etq in ("ESTADOS", "ALFABETO", "INICIAL", "FINALES", "TRANSICIONES"):
                    leyendo = False
                else:
                    p = [x.strip() for x in l.split(",")]
                    if len(p) != 3:
                        raise ErrorConfiguracionAFD(f"linea {n}: transicion mal escrita -> '{l}'")
                    o, s, d = p
                    trans[(o, s)] = d
                    continue

            if ":" not in l:
                raise ErrorConfiguracionAFD(f"linea {n}: no entiendo esto -> '{l}'")

            etq, _, val = l.partition(":")
            etq = etq.strip().upper()
            val = val.strip()

            if etq == "ESTADOS":
                estados = [x.strip() for x in val.split(",") if x.strip()]
            elif etq == "ALFABETO":
                alfabeto = [x.strip() for x in val.split(",") if x.strip()]
            elif etq == "INICIAL":
                inicial = val
            elif etq == "FINALES":
                finales = [x.strip() for x in val.split(",") if x.strip()]
            elif etq == "TRANSICIONES":
                leyendo = True
            else:
                raise ErrorConfiguracionAFD(f"linea {n}: etiqueta rara '{etq}'")

        f.close()

        if estados is None:
            raise ErrorConfiguracionAFD("falta ESTADOS en el archivo de configuracion")
        if alfabeto is None:
            raise ErrorConfiguracionAFD("falta ALFABETO en el archivo de configuracion")
        if inicial is None:
            raise ErrorConfiguracionAFD("falta INICIAL en el archivo de configuracion")
        if finales is None:
            raise ErrorConfiguracionAFD("falta FINALES en el archivo de configuracion")

        if inicial not in estados:
            raise ErrorConfiguracionAFD(f"el inicial '{inicial}' no esta en ESTADOS")

        for qf in finales:
            if qf not in estados:
                raise ErrorConfiguracionAFD(f"el final '{qf}' no esta en ESTADOS")

        for k in trans:
            o, s = k
            d = trans[k]
            if o not in estados or d not in estados:
                raise ErrorConfiguracionAFD(f"hay una transicion con un estado que no existe ({o} -> {d})")
            if s not in alfabeto:
                raise ErrorConfiguracionAFD(f"el simbolo '{s}' de una transicion no esta en ALFABETO")

        return cls(estados, alfabeto, inicial, set(finales), trans)

    def mover(self, estado, simbolo):
        return self.transiciones.get((estado, simbolo))

    def procesar_cadena(self, cadena):
        actual = self.inicial
        pasos = [f"δ({actual}, {cadena if cadena else 'ε'})"]

        for i in range(len(cadena)):
            s = cadena[i]

            if s not in self.alfabeto:
                motivo = f"'{s}' no pertenece al alfabeto {{{', '.join(self.alfabeto)}}}"
                return False, pasos, motivo

            sig = self.mover(actual, s)
            resto = cadena[i + 1:]

            if sig is None:
                pasos.append(f"  --{s}-->  [no hay transicion, se muere aqui]")
                motivo = f"no existe δ({actual}, {s}), la cadena queda atrapada"
                return False, pasos, motivo

            pasos.append(f"  --{s}-->  δ({sig}, {resto if resto else 'ε'})")
            actual = sig

        if actual not in self.finales:
            motivo = f"termino en '{actual}' y ese no es final {sorted(self.finales)}"
            return False, pasos, motivo

        return True, pasos, None


def leer_cadenas(ruta):
    if not os.path.isfile(ruta):
        raise ErrorConfiguracionAFD(f"no encontre el archivo {ruta}")

    cadenas = []
    with open(ruta, "r", encoding="utf-8") as f:
        for raw in f:
            l = raw.strip()
            if not l or l.startswith("#"):
                continue
            cadenas.append(l)
    return cadenas


def mostrar_info(afd):
    print("AFD cargado")
    print(f"Estados  : {{{', '.join(afd.estados)}}}")
    print(f"Alfabeto : {{{', '.join(afd.alfabeto)}}}")
    print(f"Inicial  : {afd.inicial}")
    print(f"Finales  : {{{', '.join(sorted(afd.finales))}}}")
    print("Transiciones:")
    for k in sorted(afd.transiciones):
        o, s = k
        print(f"  δ({o}, {s}) = {afd.transiciones[k]}")
    print()


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 AFD.py <conf.txt> <cadenas.txt>")
        sys.exit(1)

    conf, cad = sys.argv[1], sys.argv[2]

    try:
        afd = AFD.desde_archivo(conf)
        cadenas = leer_cadenas(cad)
    except ErrorConfiguracionAFD as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    mostrar_info(afd)

    if not cadenas:
        print("no hay cadenas para procesar")
        return

    ok = 0
    for i, c in enumerate(cadenas, start=1):
        print(f'Cadena {i}/{len(cadenas)}: "{c}"')
        aceptada, pasos, motivo = afd.procesar_cadena(c)

        print("Pasos:")
        for p in pasos:
            print(f"  {p}")

        if aceptada:
            ok += 1
            print(f'Resultado: ACEPTADA ✔  ("{c}" pertenece al lenguaje)')
        else:
            print(f"Resultado: RECHAZADA ✘  ({motivo})")
        print()

    print(f"Total: {ok}/{len(cadenas)} aceptadas")


if __name__ == "__main__":
    main()
