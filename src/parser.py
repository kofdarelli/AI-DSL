from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.grammar import (
    NONTERMINALS,
    START_SYMBOL,
    TERMINAL_DISPLAY,
    TERMINAL_ORDER,
    build_parse_table,
    compute_first_sets,
    compute_follow_sets,
    expected_terminals,
    human_symbol,
    is_terminal,
)
from src.lexer import LexerError, Token, tokenize


@dataclass(frozen=True)
class ParseResult:
    token_count: int


class DSLSyntaxError(Exception):
    def __init__(self, token: Token, expected: list[str], detail: str | None = None) -> None:
        self.token = token
        self.expected = expected
        self.detail = detail
        message = self._build_message()
        super().__init__(message)

    def _build_message(self) -> str:
        found = TERMINAL_DISPLAY.get(self.token.type, self.token.type)
        lexeme = self.token.lexeme if self.token.type != "EOF" else "EOF"
        expected = ", ".join(self.expected) if self.expected else "no valid continuation"
        message = (
            f"Syntax error at line {self.token.line}, column {self.token.column}: "
            f"found {lexeme!r} ({found}), expected one of: {expected}"
        )
        if self.detail:
            message += f" [{self.detail}]"
        return message


FIRST_SETS = compute_first_sets()
FOLLOW_SETS = compute_follow_sets(FIRST_SETS)
PARSE_TABLE = build_parse_table(FIRST_SETS, FOLLOW_SETS)


def _raise_unexpected_terminal(token: Token, expected_symbol: str) -> None:
    raise DSLSyntaxError(token, [human_symbol(expected_symbol)], detail="terminal mismatch")


def parse_tokens(tokens: list[Token]) -> ParseResult:
    stack: list[str] = [START_SYMBOL]
    index = 0

    while stack:
        top = stack.pop()
        token = tokens[index]

        if top == "EPSILON":
            continue

        if is_terminal(top):
            if top == token.type:
                index += 1
                continue
            _raise_unexpected_terminal(token, top)

        if top not in NONTERMINALS:
            raise ValueError(f"Unknown grammar symbol on parser stack: {top}")

        production = PARSE_TABLE[top].get(token.type)
        if not production:
            raise DSLSyntaxError(token, expected_terminals(top, PARSE_TABLE), detail=f"while expanding {top}")

        for symbol in reversed(production.rhs):
            if symbol != "EPSILON":
                stack.append(symbol)

    if index != len(tokens):
        token = tokens[index]
        raise DSLSyntaxError(token, [human_symbol("EOF")], detail="extra trailing input")

    return ParseResult(token_count=len(tokens) - 1)


def parse_text(text: str) -> ParseResult:
    tokens = tokenize(text)
    return parse_tokens(tokens)


def parse_file(path: str | Path) -> ParseResult:
    source_path = Path(path)
    try:
        text = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(f"Could not read {source_path}: {exc}") from exc
    return parse_text(text)


def syntax_check(path: str | Path) -> ParseResult:
    try:
        return parse_file(path)
    except LexerError as exc:
        token = Token("EOF", "", exc.line, exc.column)
        raise DSLSyntaxError(token, [], detail=exc.message) from exc
