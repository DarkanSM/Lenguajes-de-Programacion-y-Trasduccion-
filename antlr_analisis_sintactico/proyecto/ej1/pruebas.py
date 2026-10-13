from arboles import parsear, ConstruyeAST, Evalua, ErrorSintactico, forma_lisp

VARS = {"a": 2, "b": 3, "c": 4, "x": 10}

# (entrada, AST esperado, valor esperado)
VALIDAS = [
    ("2 + 3 * 4",        "(+ 2 (* 3 4))",              14),   # diap. 11
    ("2 + 3 - 4",        "(- (+ 2 3) 4)",               1),   # diap. 11
    ("2 + 3 * (4 - 5)",  "(+ 2 (* 3 (- 4 5)))",        -1),   # diap. 11
    ("3 + 4 * 5",        "(+ 3 (* 4 5))",              23),   # diap. 12
    ("(2 + 3) * 4",      "(* (+ 2 3) 4)",              20),   # paréntesis alteran precedencia
    ("4 - 3 - 2",        "(- (- 4 3) 2)",              -1),   # asociatividad izquierda (diap. 27)
    ("8 / 4 / 2",        "(/ (/ 8 4) 2)",             1.0),   # asociatividad izquierda
    ("a + b * c",        "(+ a (* b c))",              14),   # diap. 31 con a=2,b=3,c=4
    ("((7))",            "7",                           7),
    ("x",                "x",                          10),
    ("1 + 2 + 3 + 4",    "(+ (+ (+ 1 2) 3) 4)",        10),
    ("2 * 3 + 4 * 5",    "(+ (* 2 3) (* 4 5))",        26),
]

INVALIDAS = ["2 +", "+ 2", "2 3", "(2 + 3", "2 + 3)", "()", "2 * * 3", "", "2 + $"]

ok = fallos = 0
print("PRUEBAS VÁLIDAS")
for texto, ast_esp, val_esp in VALIDAS:
    tree, _ = parsear(texto)
    ast = repr(ConstruyeAST().visit(tree))
    val = Evalua(VARS).visit(tree)
    bien = (ast == ast_esp and val == val_esp)
    ok += bien; fallos += (not bien)
    print(f"  [{'OK' if bien else 'FALLO'}] {texto:<18} AST={ast:<26} valor={val}")

print("\nPRUEBAS INVÁLIDAS (deben producir error sintáctico)")
for texto in INVALIDAS:
    try:
        parsear(texto)
        print(f"  [FALLO] {texto!r} fue aceptada"); fallos += 1
    except ErrorSintactico as e:
        print(f"  [OK] {texto!r:<10} -> {e}"); ok += 1

print(f"\nResultado: {ok} correctas, {fallos} fallidas")
raise SystemExit(1 if fallos else 0)
