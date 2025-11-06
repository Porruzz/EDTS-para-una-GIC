# -*- coding: utf-8 -*-
from __future__ import annotations

class SymbolTable:
    """Tabla de símbolos simple (scope único)."""
    def __init__(self):
        self.table: dict[str, float] = {}

    def set(self, name: str, val: float) -> None:
        self.table[name] = val

    def get(self, name: str) -> float:
        if name not in self.table:
            raise NameError(f"Identificador no definido: {name}")
        return self.table[name]

    def __repr__(self) -> str:
        if not self.table:
            return "<Símbolos vacíos>"
        rows = [f"{k} = {v}" for k, v in sorted(self.table.items())]
        return "Tabla de símbolos:\n" + "\n".join(rows)
