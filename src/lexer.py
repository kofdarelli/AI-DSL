from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Token:
    type: str
    lexeme: str
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, line: int, column: int, message: str) -> None:
        self.line = line
        self.column = column
        self.message = message
        super().__init__(f"Syntax error at line {line}, column {column}: {message}")


KEYWORDS = {
    "agent": "AGENT",
    "tool": "TOOL",
    "task": "TASK",
    "system": "SYSTEM",
    "action": "ACTION",
    "run": "RUN",
    "if": "IF",
    "for": "FOR",
    "in": "IN",
    "string": "TYPE_STRING",
    "int": "TYPE_INT",
    "bool": "TYPE_BOOL",
    "list": "TYPE_LIST",
    "true": "TRUE",
    "false": "FALSE",
}

TOKEN_SPECS = (
    ("WHITESPACE", r"[ \t\r\n]+"),
    ("ARROW", r"->"),
    ("EQEQ", r"=="),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA", r","),
    ("COLON", r":"),
    ("DOT", r"\."),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("STRING_LITERAL", r'"([^"\\]|\\.)*"'),
    ("INT_LITERAL", r"\d+"),
    ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
)

MASTER_PATTERN = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS))


def _advance_position(lexeme: str, line: int, column: int) -> tuple[int, int]:
    newline_count = lexeme.count("\n")
    if newline_count == 0:
        return line, column + len(lexeme)

    line += newline_count
    column = len(lexeme.rsplit("\n", 1)[-1]) + 1
    return line, column


def tokenize(text: str) -> list[Token]:
    position = 0
    line = 1
    column = 1
    tokens: list[Token] = []

    while position < len(text):
        match = MASTER_PATTERN.match(text, position)
        if not match:
            bad_char = text[position]
            raise LexerError(line, column, f"unexpected character {bad_char!r}")

        token_type = match.lastgroup
        assert token_type is not None
        lexeme = match.group(token_type)

        if token_type != "WHITESPACE":
            if token_type == "IDENT":
                token_type = KEYWORDS.get(lexeme, "IDENT")
            tokens.append(Token(token_type, lexeme, line, column))

        line, column = _advance_position(lexeme, line, column)
        position = match.end()

    tokens.append(Token("EOF", "", line, column))
    return tokens
