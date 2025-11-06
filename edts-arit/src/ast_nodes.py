# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class Node:
    """Nodo base para el AST. Se le podrá colgar 'val' al decorar."""
    val: Optional[float] = None

@dataclass
class Num(Node):
    lex: str = ""

@dataclass
class Id(Node):
    name: str = ""

@dataclass
class BinOp(Node):
    op: str = ""
    left: Node = None
    right: Node = None

@dataclass
class Assign(Node):
    name: str = ""
    expr: Node = None

@dataclass
class StmtList(Node):
    items: list[Node] = None
