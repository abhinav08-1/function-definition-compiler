import re
KEYWORDS = {"def", "return"}
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
    tokens=[]; line=1; col=1
    for m in TOKEN_PATTERN.finditer(source_code):
        kind,value=m.lastgroup,m.group(); tl,tc=line,col
        if kind == "NEWLINE": line += 1; col = 1; continue
        col += len(value)
        if kind in ("WHITESPACE", "COMMENT"): continue
        if kind == "MISMATCH":
            raise SyntaxError(f"Lexical error at line {tl}, column {tc}: Unexpected character {value!r}")
        if kind == "IDENTIFIER" and value in KEYWORDS: kind="KEYWORD"
        tokens.append((kind,value,tl,tc))
    return tokens
