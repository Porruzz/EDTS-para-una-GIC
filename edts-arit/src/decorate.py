# -*- coding: utf-8 -*-
from __future__ import annotations
from .ast_nodes import StmtList, Assign, BinOp, Num, Id, Node
from .symbols import SymbolTable

def decorate(ast: StmtList, sym: SymbolTable) -> None:
    """
    Recorre el AST y sintetiza 'val' en cada nodo.
    Para Assign, actualiza la tabla de símbolos y también deja val del Assign = expr.val
    """

    def eval_node(n: Node) -> float:
        if isinstance(n, Num):
            n.val = float(n.lex)
            return n.val
        if isinstance(n, Id):
            v = sym.get(n.name)
            n.val = float(v)
            return n.val
        if isinstance(n, BinOp):
            lv = eval_node(n.left)
            rv = eval_node(n.right)
            if n.op == "+": n.val = lv + rv
            elif n.op == "-": n.val = lv - rv
            elif n.op == "*": n.val = lv * rv
            elif n.op == "/": n.val = lv / rv
            else: raise ValueError(f"Operador desconocido: {n.op}")
            return n.val
        raise TypeError(f"Nodo no evaluable: {type(n).__name__}")

    for st in ast.items or []:
        if isinstance(st, Assign):
            val = eval_node(st.expr)
            sym.set(st.name, val)
            st.val = val
        else:
            # expresión suelta
            st.val = eval_node(st)
