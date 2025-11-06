# -*- coding: utf-8 -*-
import argparse
import sys
import pathlib
from .parser_ll1 import parse_string, ParseError
from .decorate import decorate
from .symbols import SymbolTable
from .pretty import print_ast, print_symbols


def main():
    # === PARÁMETROS DE EJECUCIÓN ===
    ap = argparse.ArgumentParser(
        description="EDTS para una GIC aritmética: + - * / con asignaciones opcionales."
    )
    ap.add_argument("--input", help="Ruta del archivo de entrada (ej: examples/ok.txt)")
    ap.add_argument("--string", help="Cadena directa a analizar (ej: \"x=2+3*4; y=x/2\")")
    ap.add_argument("--print-ast", action="store_true", help="Imprime el AST decorado")
    ap.add_argument("--print-syms", action="store_true", help="Imprime la tabla de símbolos")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Si está activo, detiene la ejecución ante errores sintácticos.",
    )
    args = ap.parse_args()

    # === VALIDACIÓN DE ENTRADA ===
    if not args.input and not args.string:
        print("⚠️  Usa --input archivo.txt o --string \"a=2+3; b=a*4\".", file=sys.stderr)
        sys.exit(2)

    if args.string:
        src = args.string
    else:
        p = pathlib.Path(args.input)
        if not p.exists():
            print(f"✗ Archivo no encontrado: {p}", file=sys.stderr)
            sys.exit(1)
        src = p.read_text(encoding="utf-8")

    # === ANÁLISIS SINTÁCTICO ===
    try:
        ast = parse_string(src)
    except ParseError as e:
        print(f"✗ Error sintáctico detectado: {e}")
        if args.strict:
            sys.exit(1)
        else:
            print("RECHAZADO — la entrada no cumple la gramática LL(1).")
            sys.exit(0)

    # === DECORACIÓN Y EVALUACIÓN ===
    sym = SymbolTable()
    decorate(ast, sym)

    # === SALIDA FINAL ===
    print("✓ Análisis y decoración completados con éxito.")
    if args.print_ast:
        print("\n== AST Decorado ==")
        print_ast(ast)
    if args.print_syms:
        print("\n== Símbolos ==")
        print_symbols(sym)


if __name__ == "__main__":
    main()
