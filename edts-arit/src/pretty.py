# -*- coding: utf-8 -*-
from __future__ import annotations
from .ast_nodes import *
from .symbols import SymbolTable

def print_ast(n: Node, indent: str = "") -> None:
    tag = type(n).__name__
    extra = ""
    if isinstance(n, Num): extra = f" lex={n.lex}"
    if isinstance(n, Id):  extra = f" name={n.name}"
    if isinstance(n, BinOp): extra = f" op='{n.op}'"
    if isinstance(n, Assign): extra = f" name={n.name}"
    v = f", val={n.val}" if n.val is not None else ""
    print(f"{indent}{tag}{extra}{v}")
    if isinstance(n, StmtList):
        for it in n.items or []:
            print_ast(it, indent + "  ")
    elif isinstance(n, Assign):
        print_ast(n.expr, indent + "  ")
    elif isinstance(n, BinOp):
        print_ast(n.left, indent + "  ")
        print_ast(n.right, indent + "  ")

def print_symbols(sym: SymbolTable) -> None:
    print(sym.__repr__())
