# -*- coding: utf-8 -*-
import re
from typing import NamedTuple, Iterator

class Tok(NamedTuple):
    type: str
    lex: str
    pos: int

TOKEN_SPEC = [
    ("NUM",   r"\d+(\.\d+)?"),
    ("ID",    r"[A-Za-z_][A-Za-z0-9_]*"),
    ("PLUS",  r"\+"),
    ("MINUS", r"-"),
    ("MUL",   r"\*"),
    ("DIV",   r"/"),
    ("LP",    r"\("),
    ("RP",    r"\)"),
    ("EQ",    r"="),
    ("SC",    r";"),
    ("WS",    r"[ \t\r\n]+"),
]

MASTER = re.compile("|".join(f"(?P<{t}>{p})" for t,p in TOKEN_SPEC))

def lex(s: str) -> Iterator[Tok]:
    pos = 0
    for m in MASTER.finditer(s):
        typ = m.lastgroup
        lex = m.group()
        if typ == "WS":
            pass
        else:
            yield Tok(typ, lex, pos)
        pos = m.end()
    yield Tok("EOF", "", pos)
