import re
import sys
from collections import namedtuple

Token = namedtuple("Token", ["type", "value", "line", "column"])



KEYWORD_TYPES = {
    "agent":  "AGENT",
    "tool":   "TOOL",
    "task":   "TASK",
    "action": "ACTION",
    "system": "SYSTEM",
    "for":    "FOR",
    "in":     "IN",
    "if":     "IF",
    "run":    "RUN",
    "true":   "TRUE",
    "false":  "FALSE",
    "string": "STRING_TYPE",
    "int":    "INT_TYPE",
    "bool":   "BOOL_TYPE",
    "list":   "LIST_TYPE",
}


TOKEN_SPEC = [
    # We decided to make Multi-character operators come before their single-char prefixes, otherwise "==" would match "=" then "=" separately.
    ("ARROW",      r"->"),
    ("EQEQ",       r"=="),
    ("NEQ",        r"!="),
    ("LEQ",        r"<="),
    ("GEQ",        r">="),

    # Single-character operators
    ("LT",         r"<"),
    ("GT",         r">"),
    ("EQ",         r"="),
    ("PLUS",       r"\+"),
    ("MINUS",      r"-"),
    ("MULT",       r"\*"),
    ("DIV",        r"/"),

    # Delimiters
    ("LBRACE",     r"\{"),
    ("RBRACE",     r"\}"),
    ("LPAREN",     r"\("),
    ("RPAREN",     r"\)"),
    ("LBRACKET",   r"\["),
    ("RBRACKET",   r"\]"),
    ("COMMA",      r","),
    ("COLON",      r":"),
    ("DOT",        r"\."),

 
    ("STRING_LIT", r'"([^"\\]|\\.)*"'),

  
    ("INT_LIT",    r"[0-9]+"),

    ("ID",         r"[a-zA-Z_][a-zA-Z0-9_]*"),

    # Whitespace and comments are skipped; newlines tracked for line numbers
    ("NEWLINE",    r"\n"),
    ("SKIP",       r"[ \t\r]+"),
    ("COMMENT",    r"#[^\n]*"),   # single-line DSL comment starts with #

    # Anything else is unexpected
    ("MISMATCH",   r"."),
]


_master_re = re.compile(
    "|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC)
)


def tokenize(source_code):
    """
    Convert DSL source text into a list of Token objects.

    We designed it as such: 
      • Longest-prefix match 
      • Keyword-before-identifier priority
      • Whitespace and comments are ignored (treated as separators)
      • Raises SyntaxError on an unrecognised character
    """
    tokens = []
    line_num = 1
    line_start = 0 

    for match in _master_re.finditer(source_code):
        kind  = match.lastgroup          # which alternative matched
        value = match.group()            # matched text
        col   = match.start() - line_start + 1

        # Whitespace /comments 
        if kind == "NEWLINE":
            line_num  += 1
            line_start = match.end()
            continue

        if kind in ("SKIP", "COMMENT"):
            # Track newlines inside multi-line constructs if ever needed
            continue

        # Unexpected character 
        if kind == "MISMATCH":
            raise SyntaxError(
                f"Unexpected character {value!r} "
                f"at line {line_num}, column {col}"
            )

        #Keyword check 
        # If we matched an ID, check whether it is actually a reserved keyword.
        if kind == "ID" and value in KEYWORD_TYPES:
            kind = KEYWORD_TYPES[value]

        tokens.append(Token(kind, value, line_num, col))

    return tokens

 
#Here we used the help from chatgpt to learn how we can run our parser and lexer to test our code.
 
def main():
    if len(sys.argv) != 2:
        print("Usage: python dsl_lexer.py <dsl_source_file>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    try:
        tokens = tokenize(source)
    except SyntaxError as e:
        print("Lexical error:", e)
        sys.exit(1)

    # print the token stream
    print(f"{'TYPE':<16} {'VALUE':<25} POSITION")
    print("-" * 55)
    for tok in tokens:
        print(f"{tok.type:<16} {tok.value:<25} line {tok.line}, col {tok.column}")


if __name__ == "__main__":
    main()
