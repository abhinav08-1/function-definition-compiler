# Function Definition Compiler — Front End (Group 7)

Python educational compiler front end with lexical analysis, recursive-descent parsing, AST generation/display, and semantic checks.

## Supported syntax
```text
def add(a, b): return a + b;
add(2, 3);
```
Type a program in the terminal and enter `END` on its own line.

## Files
- `lexer.py`: tokenization and lexical error reporting
- `parser.py`: recursive-descent parser and AST node classes
- `semantic.py`: duplicate definitions/parameters, undefined names/functions, argument-count checks
- `ast_tools.py`: AST tree display
- `main.py`: connects the stages
- `grammar.txt`: supported grammar
- `tests/`: valid and invalid test cases

## Run
Python 3.9+; no third-party packages needed:
```bash
python main.py
python -m unittest discover -s tests -v
```

This is a small compiler front end, not a full Python/C compiler. It does not execute programs or generate machine code. The syntax is Python-like `def` with semicolon terminators; keep the report, grammar, and demonstration consistent.
