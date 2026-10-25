# Function Definition Compiler — Grammar and Parsing

## 1. Language scope

This document describes the simplified language used by the current Python lexer/parser design. It uses Python-like function headers with a colon, but semicolons at the end of return statements and call statements.

Example:

```text
def add(a, b):
    return a + b;

add(2, 3);
```

This is a small project language, not standard Python or full C.

## 2. Context-Free Grammar (CFG)

### Terminals

`def`, `return`, `(`, `)`, `:`, `,`, `;`, `+`, `-`, `*`, `/`, identifiers (`id`), numbers (`number`), and end-of-input (`EOF`).

### Non-terminals

`Program`, `Item`, `FunctionDef`, `ParamsOpt`, `Params`, `ParamTail`,
`ReturnStmt`, `CallStmt`, `Call`, `ArgsOpt`, `Args`, `ArgTail`,
`Expr`, `ExprTail`, `Term`, `TermTail`, `Factor`.

### Production rules

```text
Program    -> Item Program | ε
Item       -> FunctionDef | CallStmt
FunctionDef -> def id ( ParamsOpt ) : ReturnStmt
ParamsOpt  -> Params | ε
Params     -> id ParamTail
ParamTail  -> , id ParamTail | ε
ReturnStmt -> return Expr ;
CallStmt   -> Call ;
Call       -> id ( ArgsOpt )
ArgsOpt    -> Args | ε
Args       -> Expr ArgTail
ArgTail    -> , Expr ArgTail | ε
Expr       -> Term ExprTail
ExprTail   -> + Term ExprTail | - Term ExprTail | ε
Term       -> Factor TermTail
TermTail   -> * Factor TermTail | / Factor TermTail | ε
Factor     -> number | id FactorTail | ( Expr )
FactorTail -> ( ArgsOpt ) | ε
```

## 3. Notes on the grammar

- `id` is an identifier such as `add`, `a`, or `result`.
- `number` is a numeric literal such as `2` or `15`.
- `ε` means an empty production. It permits empty parameter lists and empty argument lists.
- `Expr` and `Term` are arranged to avoid direct left recursion.
- `FactorTail` allows an identifier to be interpreted as a variable or as a function call depending on whether `(` follows it.
- This grammar intentionally supports a small subset of language constructs. It does not describe all of Python or C.
- The grammar shown here is the intended grammar for the parser. Always verify its rules against the actual `parser.py` and `lexer.py` versions in your repository before submitting.

## 4. Left-recursion removal

A conventional left-recursive arithmetic grammar can be written as:

```text
Expr -> Expr + Term | Expr - Term | Term
Term -> Term * Factor | Term / Factor | Factor
```

This is left-recursive because `Expr` or `Term` appears as the first symbol on its own right-hand side.

The general transformation is:

```text
A -> A α | β
```

to:

```text
A  -> β A'
A' -> α A' | ε
```

After transformation:

```text
Expr     -> Term ExprTail
ExprTail -> + Term ExprTail | - Term ExprTail | ε

Term     -> Factor TermTail
TermTail -> * Factor TermTail | / Factor TermTail | ε
```

The transformed rules consume a `Term` or `Factor` first, then process any following operators. This form is suitable for a recursive-descent parser.

The parameter and argument lists in this grammar use right recursion, so they do not need left-recursion removal.

## 5. Parsing technique: recursive-descent parsing

Recursive-descent parsing is a top-down technique. Each grammar rule is implemented as a function, and the parser checks tokens from left to right.

Typical function-to-rule mapping:

| Parser function | Grammar rule / responsibility |
|---|---|
| `parse_program()` | `Program`: parse the complete input |
| `parse_function()` | `FunctionDef`: parse a function header and body |
| `parse_parameters()` | `Params`: parse comma-separated parameter names |
| `parse_return()` | `ReturnStmt`: parse a return expression and semicolon |
| `parse_call()` | `Call`: parse a function name and argument list |
| `parse_arguments()` | `Args`: parse comma-separated argument expressions |
| `parse_expr()` | `Expr`: parse addition and subtraction |
| `parse_product()` | `Term`: parse multiplication and division |
| `parse_primary()` | `Factor`: parse identifiers, numbers, parentheses and calls |

Function names in this table are illustrative; keep the names consistent with the actual functions in your repository.

## 6. Syntax checking versus semantic checking

Syntax errors include missing parentheses, colons, commas, or semicolons, and incomplete expressions.

Semantic checks are separate. Examples include checking whether a called function exists, whether parameter names are duplicated, and whether the number of arguments matches a function's declared parameter count. These require additional symbol-table or semantic-analysis logic and should only be claimed if implemented.

## 7. Limitations

This grammar is a deliberately small language specification. It does not include general statements, multiple statements in a function body, strings, conditionals, loops, typed parameters, or complete Python/C syntax unless the project code is extended to support them.
