# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List, Iterator
from .lexer import Tok, lex
from .ast_nodes import Num, Id, BinOp, Assign, StmtList

class ParseError(Exception):
    pass

class Parser:
    """
    Parser LL(1) para la gramática dada. Construye un AST.
    ETDS: las “acciones” se materializan al construir el AST.
    """

    def __init__(self, tokens: Iterator[Tok]):
        self.tokens: List[Tok] = list(tokens)
        self.i = 0

    # utilidades
    def la(self) -> Tok:
        return self.tokens[self.i]

    def eat(self, ttype: str) -> Tok:
        t = self.la()
        if t.type != ttype:
            raise ParseError(f"<pos {t.pos}> Esperaba {ttype}, llegó {t.type} ('{t.lex}')")
        self.i += 1
        return t

    def accept(self, ttype: str) -> bool:
        if self.la().type == ttype:
            self.i += 1
            return True
        return False

    # S → StmtList
    def parse(self) -> StmtList:
        items = self.parse_stmtlist()
        # EOF
        self.eat("EOF")
        return StmtList(items=items)

    # StmtList → Stmt (';' Stmt)*
    def parse_stmtlist(self):
        items = []
        if self.la().type in ("ID","LP","NUM"):
            items.append(self.parse_stmt())
            while self.accept("SC"):
                items.append(self.parse_stmt())
        # ε permitido si entrada vacía
        return items

    # Stmt → id '=' E | E
    def parse_stmt(self):
        if self.la().type == "ID":
            # lookahead para decidir si es asignación
            t_id = self.la()
            if self.tokens[self.i+1].type == "EQ":
                self.eat("ID")
                self.eat("EQ")
                expr = self.parse_E()
                return Assign(name=t_id.lex, expr=expr)
        # si no fue "id = E", entonces es E
        return self.parse_E()

    # E → T E'
    def parse_E(self):
        left = self.parse_T()
        return self.parse_Ep(left)

    # E' → '+' T E' | '-' T E' | ε
    def parse_Ep(self, left):
        while self.la().type in ("PLUS","MINUS"):
            op = self.eat(self.la().type).lex
            right = self.parse_T()
            left = BinOp(op=op, left=left, right=right)
        return left

    # T → F T'
    def parse_T(self):
        left = self.parse_F()
        return self.parse_Tp(left)

    # T' → '*' F T' | '/' F T' | ε
    def parse_Tp(self, left):
        while self.la().type in ("MUL","DIV"):
            op = self.eat(self.la().type).lex
            right = self.parse_F()
            left = BinOp(op=op, left=left, right=right)
        return left

    # F → '(' E ')' | id | num
    def parse_F(self):
        la = self.la()
        if la.type == "LP":
            self.eat("LP")
            node = self.parse_E()
            self.eat("RP")
            return node
        elif la.type == "ID":
            name = self.eat("ID").lex
            return Id(name=name)
        elif la.type == "NUM":
            lex = self.eat("NUM").lex
            return Num(lex=lex)
        raise ParseError(f"<pos {la.pos}> Token inesperado: {la.type} ('{la.lex}')")

def parse_string(s: str) -> StmtList:
    return Parser(lex(s)).parse()
