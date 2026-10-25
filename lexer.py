import re

KEYWORDS = {
    "def", "return", "if", "else", "elif",
    "while", "for", "in",
    "int", "float", "string", "char", "bool", "void",
    "true", "false", "None",
    "break", "continue", "pass",
    "and", "or", "not",
}

TOKEN_PATTERN = re.compile(
   r"(?P<WHITESPACE>[ \t]+)|"
r"(?P<NEWLINE>\r\n|\r|\n)|"
r"(?P<COMMENT>\#.*)|"
       r"(?P<STRING>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*')|"
    r"(?P<NUMBER>\d+(?:\.\d+)?)|"
    r"(?P<IDENTIFIER>[A-Za-z_][A-Za-z0-9_]*)|"
  r"(?P<OPERATOR>==|!=|<=|>=|[+\-*/%=<>!])|"
    r"(?P<PUNCTUATION>[(),:;{}])|"
    r"(?P<MISMATCH>.)"
)


def tokenize(source_code):
    """Return (token_type, lexeme, line_number, column_number) tuples."""
    tokens = []
    line = 1
    column = 1

    for match in TOKEN_PATTERN.finditer(source_code):
        kind = match.lastgroup
        value = match.group()
        token_line = line
        token_column = column

        if kind == "NEWLINE":
            line += 1
            column = 1
            continue

        column += len(value)

        if kind in ("WHITESPACE", "COMMENT"):
            continue

        if kind == "MISMATCH":
            raise SyntaxError(
                f"Lexical error at line {token_line}, "
                f"column {token_column}: Unexpected character {value!r}"
            )

        if kind == "IDENTIFIER" and value in KEYWORDS:
            kind = "KEYWORD"

        tokens.append((kind, value, token_line, token_column))

    return tokens


def main():
    print("=" * 58)
    print(" FUNCTION DEFINITION COMPILER - LEXICAL ANALYZER")
    print("=" * 58)
    print("Type or paste your complete program.")
    print("Enter END on a separate line to finish.")
    print("-" * 58)

    lines = []
    while True:
        try:
            current_line = input()
        except EOFError:
            break
        if current_line.strip() == "END":
            break
        lines.append(current_line)

    source_code = "\n".join(lines)
    if not source_code.strip():
        print("No program entered.")
        return

    try:
        tokens = tokenize(source_code)
        print("\nGenerated Tokens:")
        print("-" * 76)
        print(f"{'TOKEN TYPE':<18}{'LEXEME':<22}{'LINE':<12}COLUMN")
        print("-" * 76)
        for kind, value, token_line, token_column in tokens:
            print(f"{kind:<18}{value!r:<22}{token_line:<12}{token_column}")
        print("-" * 76)
        print(f"Total tokens: {len(tokens)}")
        print("Lexical analysis completed successfully.")
    except SyntaxError as error:
        print(f"\n{error}")


if __name__ == "__main__":
    main()