# 🖋️ Arabic Compiler – Lexical, Syntax, and Semantic Analyzer

[![Language](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **simple compiler** for a custom **Arabic-like programming language**, implemented in **Python**.  
This project demonstrates **compiler construction**, **language design**, and **semantic analysis** concepts. 🚀

---

## ✨ Features

- **📝 Lexical Analysis:** Tokenizes Arabic keywords (`متغير`, `اذا`, `طالما`), identifiers, numbers, and operators.  
- **📚 Syntax Analysis:** Recursive descent parser validates program grammar and structure.  
- **🔍 Semantic Analysis:**  
  - Multi-level scope management  
  - Symbol table for variable declarations, initializations, and values  
  - Detects semantic errors like undeclared or uninitialized variables  
- **➗ Expression Evaluation:** Supports arithmetic operations (`+`, `-`, `*`, `/`) and relational expressions (`>`, `<`, `==`, etc.)  
- **🗂 Scope Handling:** Properly manages nested `if` and `while` blocks with local and global scopes  

---

## ⚡ Example Usage

```python
program = """
متغير x = 3;
اذا (x > 2) {
    متغير y = x * 2;
}
طالما (x < 10) {
    x = x + 1;
}
"""
tokens = tokenize_arabic(program)
parser = ArabicParser(tokens)
parser.parse()
```
## ✅ Behavior

- Syntax validation  
- Semantic checking for undeclared/uninitialized variables  
- Tracks variable values and scopes  

---

## 🛠️ Tools & Technologies

- Python 3  
- Regular Expressions (`re`)  
- Concepts: Lexer, Parser, Semantic Analyzer, Symbol Table, Scope Management  

---


