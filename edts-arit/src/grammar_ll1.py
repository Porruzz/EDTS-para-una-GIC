# -*- coding: utf-8 -*-
"""
Gramática LL(1) y conjuntos FIRST/FOLLOW/PREDICT documentados.

S  → StmtList
StmtList → Stmt (';' Stmt)*
Stmt → id '=' E | E
E  → T E'
E' → '+' T E' | '-' T E' | ε
T  → F T'
T' → '*' F T' | '/' F T' | ε
F  → '(' E ')' | id | num

FIRST:
  E:  {(, id, num}      E': {+, -, ε}
  T:  {(, id, num}      T': {*, /, ε}
  F:  {(, id, num}      Stmt: {id, (, num}
  StmtList: {id, (, num, ε}

FOLLOW (síntesis estándar):
  E:  {EOF, ), ;}      E': {EOF, ), ;}
  T:  {EOF, ), ;, +, -} T': {EOF, ), ;, +, -}
  F:  {EOF, ), ;, +, -, *, /}
  Stmt: {EOF, ;}
  StmtList: {EOF}

PREDICT (sin conflictos) — ver parser_ll1.py para construcción directa.
"""
