# Proyecto: EDTS para una Gramática Independiente del Contexto Aritmética

Este proyecto implementa un **Esquema de Traducción Dirigido por la Sintaxis (EDTS)** para una **gramática independiente del contexto (GIC)** que reconoce y evalúa expresiones aritméticas con asignaciones.
El sistema realiza análisis **léxico, sintáctico, construcción del AST (árbol sintáctico abstracto)**, **decoración semántica** y **generación de tabla de símbolos**.

---

## 1. Objetivo

Construir un analizador que procese expresiones aritméticas con las operaciones:

```
+   suma
-   resta
*   multiplicación
/   división
```

y soporte **asignaciones y expresiones anidadas**, como:

```
x = 2 + 3 * 4;
y = (x - 5) / 3;
x + y
```

El sistema genera automáticamente:

1. **El AST decorado**, mostrando los valores calculados.
2. **La tabla de símbolos**, con los identificadores y sus valores.

---

## 2. Estructura del proyecto

```
edts-arit/
├── examples/
│   ├── ok.txt         # Ejemplo válido
│   └── bad.txt        # Ejemplo con error
├── src/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada principal
│   ├── lexer.py             # Analizador léxico
│   ├── parser_ll1.py        # Analizador sintáctico LL(1)
│   ├── ast_nodes.py         # Definición de nodos del AST
│   ├── decorate.py          # Decoración semántica del AST
│   ├── symbols.py           # Implementación de tabla de símbolos
│   └── pretty.py            # Impresión formateada de AST y símbolos
└── README.md
```

---

## 3. Gramática utilizada

### Gramática independiente del contexto (GIC)

```
E  → T E'
E' → + T E' | - T E' | ε
T  → F T'
T' → * F T' | / F T' | ε
F  → ( E ) | id | num
```

### Extensión con asignaciones y listas de sentencias

```
StmtList → Stmt (‘;’ Stmt)*
Stmt     → id = E | E
```

---

## 4. Gramática de atributos

| Producción                                                   | Regla semántica / Atributos |
| ------------------------------------------------------------ | --------------------------- |
| Num.lex → Num.val = float(lex)                               |                             |
| Id.name → Id.val = σ[name]                                   |                             |
| BinOp('+').val = E1.val + E2.val                             |                             |
| BinOp('-').val = E1.val - E2.val                             |                             |
| BinOp('*').val = E1.val * E2.val                             |                             |
| BinOp('/').val = E1.val / E2.val                             |                             |
| Assign.id = name; Assign.val = expr.val; σ[name] := expr.val |                             |
| StmtList.val = último(Stmt.val)                              |                             |

---

## 5. Componentes principales

### **1. Analizador Léxico (`lexer.py`)**

Divide la entrada en tokens:

```
NUM, ID, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ASSIGN, SEMI, EOF
```

Ejemplo de tokens:

```
x=2+3*4;
→ ID('x'), ASSIGN('='), NUM('2'), PLUS('+'), NUM('3'), MUL('*'), NUM('4'), SEMI(';')
```

---

### **2. Analizador Sintáctico (`parser_ll1.py`)**

Implementa un **parser recursivo descendente LL(1)**.
Construye el **AST** según las reglas de la gramática y valida la estructura sintáctica.

Ejemplo:

```
E → T E'
E' → + T E' | ε
```

---

### **3. Decorador Semántico (`decorate.py`)**

Recorre el AST y evalúa los valores de cada nodo.
Aplica las ecuaciones semánticas y actualiza la tabla de símbolos.

---

### **4. Tabla de Símbolos (`symbols.py`)**

Estructura tipo diccionario:

```
σ = { "x": 14.0, "y": 3.0 }
```

Usada para almacenar y recuperar valores de identificadores.

---

### **5. Impresor (`pretty.py`)**

Muestra el AST decorado con indentación y los valores de cada nodo.
Ejemplo de salida:

```
== AST Decorado ==
StmtList
  Assign name=x, val=14.0
  Assign name=y, val=3.0
  BinOp op='+', val=17.0
    Id name=x, val=14.0
    Id name=y, val=3.0
```

---

## 6. Ejecución

### 1. Desde cadena directa

```bash
python -m src.main --string "x=2+3*4; y=(x-5)/3; x+y" --print-ast --print-syms
```

### 2. Desde archivo

```bash
python -m src.main --input examples/ok.txt --print-ast --print-syms
```

### 3. Archivo con error

```bash
python -m src.main --input examples/bad.txt --strict
```

---

## 7. Ejemplo de salida

```
✓ Análisis y decoración completados con éxito.

== AST Decorado ==
StmtList
  Assign name=x, val=14.0
    BinOp op='+', val=14.0
      Num lex=2, val=2.0
      BinOp op='*', val=12.0
        Num lex=3, val=3.0
        Num lex=4, val=4.0
  Assign name=y, val=3.0
    BinOp op='/', val=3.0
      BinOp op='-', val=9.0
        Id name=x, val=14.0
        Num lex=5, val=5.0
      Num lex=3, val=3.0
  BinOp op='+', val=17.0
    Id name=x, val=14.0
    Id name=y, val=3.0

== Símbolos ==
Tabla de símbolos:
x = 14.0
y = 3.0
```

---

## 8. Interpretación y Sustentación

El sistema implementa un **EDTS completo**:

1. **Gramática definida:** LL(1) aritmética.
2. **Atributos calculados:** valores numéricos y referencias de variables.
3. **Conjuntos F, S, P:** verificados en proyecto previo LL(1).
4. **AST decorado:** representación visual del árbol con valores.
5. **Tabla de símbolos:** mantiene el contexto semántico.
6. **ETDS implementado:** cada paso del análisis y traducción se deriva de la estructura sintáctica.

Este enfoque demuestra la relación directa entre gramática, semántica y ejecución, consolidando el proceso de análisis y traducción de un lenguaje formal aritmético.
