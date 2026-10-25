"""Recursive-descent parser for the Function Definition Compiler mini-language.

Syntax supported:
    def add(a, b): return a + b;
    add(2, 3);

The parser uses the existing lexer.py and its token format:
(token_type, lexeme, line_number, column_number)
"""

from lexer import tokenize


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ("EOF", "EOF", 0, 0)

    def peek(self, distance=1):
        index = self.position + distance
        if index < len(self.tokens):
            return self.tokens[index]
        return ("EOF", "EOF", 0, 0)

    def advance(self):
        token = self.current()
        if self.position < len(self.tokens):
            self.position += 1
        return token

    def error(self, message):
        kind, value, line, column = self.current()
        raise SyntaxError(
            f"Syntax error at line {line}, column {column}: {message}; "
            f"found {value!r} ({kind})"
        )

    def expect(self, value):
        if self.current()[1] == value:
            return self.advance()
        self.error(f"expected {value!r}")

    def expect_identifier(self):
        if self.current()[0] == "IDENTIFIER":
            return self.advance()
        self.error("expected an identifier")

    def parse_program(self):
        """Program -> (FunctionDef | CallStmt)* EOF"""
        while self.current()[0] != "EOF":
            if self.current()[1] == "def":
                self.parse_function()
            elif self.current()[0] == "IDENTIFIER" and self.peek()[1] == "(":
                self.parse_call()
                self.expect(";")
            else:
                self.error("expected a function definition or function call")
        return True

    def parse_function(self):
        """FunctionDef -> def id ( ParamsOpt ) : return Expr ;"""
        self.expect("def")
        self.expect_identifier()
        self.expect("(")
        self.parse_parameters()
        self.expect(")")
        self.expect(":")
        self.expect("return")
        self.parse_expression()
        self.expect(";")

    def parse_parameters(self):
        """ParamsOpt -> id (',' id)* | epsilon"""
        if self.current()[1] == ")":
            return
        self.expect_identifier()
        while self.current()[1] == ",":
            self.advance()
            self.expect_identifier()

    def parse_call(self):
        """Call -> id ( ArgsOpt )"""
        self.expect_identifier()
        self.expect("(")
        self.parse_arguments()
        self.expect(")")

    def parse_arguments(self):
        """ArgsOpt -> Expr (',' Expr)* | epsilon"""
        if self.current()[1] == ")":
            return
        self.parse_expression()
        while self.current()[1] == ",":
            self.advance()
            self.parse_expression()

    def parse_expression(self):
        """Expr -> Term (('+' | '-') Term)*"""
        self.parse_term()
        while self.current()[1] in ("+", "-"):
            self.advance()
            self.parse_term()

    def parse_term(self):
        """Term -> Factor (('*' | '/') Factor)*"""
        self.parse_factor()
        while self.current()[1] in ("*", "/"):
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        """Factor -> number | id FactorTail | '(' Expr ')'"""
        kind, value, line, column = self.current()

        if kind == "NUMBER":
            self.advance()
            return

        if value == "(":
            self.advance()
            self.parse_expression()
            self.expect(")")
            return

        if kind == "IDENTIFIER":
            self.advance()
            if self.current()[1] == "(":
                self.expect("(")
                self.parse_arguments()
                self.expect(")")
            return

        self.error("expected a number, identifier, function call, or '(' expression ')'")


def parse_source(source_code):
    """Tokenize and parse source code. Returns True if syntax is valid."""
    tokens = tokenize(source_code)
    parser = Parser(tokens)
    return parser.parse_program()


def main():
    print("=" * 58)
    print(" FUNCTION DEFINITION COMPILER - SYNTAX PARSER")
    print("=" * 58)
    print("Enter your program. Type END on a separate line to finish.")
    print("Example: def add(a, b): return a + b;")
    print("-" * 58)

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)

    source_code = "\n".join(lines)
    if not source_code.strip():
        print("No program entered.")
        return

    try:
        token_list = tokenize(source_code)
        parser = Parser(token_list)
        parser.parse_program()
        print("\nSyntax analysis completed successfully.")
        print("The program follows the grammar.")
    except SyntaxError as error:
        print(f"\n{error}")


if __name__ == "__main__":
    main()
