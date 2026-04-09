from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EPSILON = "EPSILON"
START_SYMBOL = "Program"


@dataclass(frozen=True)
class Production:
    number: int
    lhs: str
    rhs: tuple[str, ...]


TERMINAL_DISPLAY = {
    "AGENT": "agent",
    "TOOL": "tool",
    "TASK": "task",
    "SYSTEM": "system",
    "ACTION": "action",
    "RUN": "run",
    "IF": "if",
    "FOR": "for",
    "IN": "in",
    "TYPE_STRING": "string",
    "TYPE_INT": "int",
    "TYPE_BOOL": "bool",
    "TYPE_LIST": "list",
    "IDENT": "identifier",
    "STRING_LITERAL": "string_literal",
    "INT_LITERAL": "int_literal",
    "TRUE": "true",
    "FALSE": "false",
    "LBRACE": "{",
    "RBRACE": "}",
    "LPAREN": "(",
    "RPAREN": ")",
    "LBRACKET": "[",
    "RBRACKET": "]",
    "COMMA": ",",
    "COLON": ":",
    "ARROW": "->",
    "DOT": ".",
    "ASSIGN": "=",
    "EQEQ": "==",
    "PLUS": "+",
    "EOF": "$",
}

TERMINAL_DESCRIPTIONS = {
    "AGENT": "agent keyword",
    "TOOL": "tool keyword",
    "TASK": "task keyword",
    "SYSTEM": "system keyword",
    "ACTION": "action keyword",
    "RUN": "run keyword",
    "IF": "if keyword",
    "FOR": "for keyword",
    "IN": "in keyword",
    "TYPE_STRING": "string type keyword",
    "TYPE_INT": "int type keyword",
    "TYPE_BOOL": "bool type keyword",
    "TYPE_LIST": "list type keyword",
    "IDENT": "identifier",
    "STRING_LITERAL": "double-quoted string literal",
    "INT_LITERAL": "integer literal",
    "TRUE": "boolean literal true",
    "FALSE": "boolean literal false",
    "LBRACE": "left brace",
    "RBRACE": "right brace",
    "LPAREN": "left parenthesis",
    "RPAREN": "right parenthesis",
    "LBRACKET": "left bracket",
    "RBRACKET": "right bracket",
    "COMMA": "comma",
    "COLON": "colon",
    "ARROW": "arrow",
    "DOT": "dot",
    "ASSIGN": "assignment operator",
    "EQEQ": "equality operator",
    "PLUS": "addition operator",
    "EOF": "end of file",
}

TERMINAL_ORDER = (
    "AGENT",
    "TOOL",
    "TASK",
    "SYSTEM",
    "ACTION",
    "RUN",
    "IF",
    "FOR",
    "IN",
    "TYPE_STRING",
    "TYPE_INT",
    "TYPE_BOOL",
    "TYPE_LIST",
    "IDENT",
    "STRING_LITERAL",
    "INT_LITERAL",
    "TRUE",
    "FALSE",
    "LBRACE",
    "RBRACE",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "COLON",
    "ARROW",
    "DOT",
    "ASSIGN",
    "EQEQ",
    "PLUS",
    "EOF",
)

PRODUCTIONS = (
    Production(1, "Program", ("AgentDeclList", "SystemDecl", "EOF")),
    Production(2, "AgentDeclList", ("AgentDecl", "AgentDeclList")),
    Production(3, "AgentDeclList", (EPSILON,)),
    Production(4, "AgentDecl", ("AGENT", "IDENT", "LBRACE", "AgentItemList", "RBRACE")),
    Production(5, "AgentItemList", ("AgentItem", "AgentItemList")),
    Production(6, "AgentItemList", (EPSILON,)),
    Production(7, "AgentItem", ("ToolDecl",)),
    Production(8, "AgentItem", ("TaskDecl",)),
    Production(9, "ToolDecl", ("TOOL", "IDENT")),
    Production(
        10,
        "TaskDecl",
        (
            "TASK",
            "IDENT",
            "LPAREN",
            "ParamListOpt",
            "RPAREN",
            "ARROW",
            "Type",
            "IDENT",
            "LBRACE",
            "ActionStmtList",
            "RBRACE",
        ),
    ),
    Production(11, "ParamListOpt", ("ParamList",)),
    Production(12, "ParamListOpt", (EPSILON,)),
    Production(13, "ParamList", ("Param", "ParamListTail")),
    Production(14, "ParamListTail", ("COMMA", "Param", "ParamListTail")),
    Production(15, "ParamListTail", (EPSILON,)),
    Production(16, "Param", ("Type", "IDENT")),
    Production(17, "Type", ("TYPE_STRING",)),
    Production(18, "Type", ("TYPE_INT",)),
    Production(19, "Type", ("TYPE_BOOL",)),
    Production(20, "Type", ("TYPE_LIST",)),
    Production(21, "ActionStmtList", ("ActionStmt", "ActionStmtList")),
    Production(22, "ActionStmtList", (EPSILON,)),
    Production(23, "ActionStmt", ("ACTION", "COLON", "IDENT", "LPAREN", "ArgListOpt", "RPAREN")),
    Production(24, "ArgListOpt", ("ArgList",)),
    Production(25, "ArgListOpt", (EPSILON,)),
    Production(26, "ArgList", ("Expr", "ArgListTail")),
    Production(27, "ArgListTail", ("COMMA", "Expr", "ArgListTail")),
    Production(28, "ArgListTail", (EPSILON,)),
    Production(29, "SystemDecl", ("SYSTEM", "LBRACE", "SystemStmtList", "RBRACE")),
    Production(30, "SystemStmtList", ("SystemStmt", "SystemStmtList")),
    Production(31, "SystemStmtList", (EPSILON,)),
    Production(32, "SystemStmt", ("VarDecl",)),
    Production(33, "SystemStmt", ("Assignment",)),
    Production(34, "SystemStmt", ("IfStmt",)),
    Production(35, "SystemStmt", ("ForStmt",)),
    Production(36, "VarDecl", ("Type", "IDENT", "ASSIGN", "AssignRHS")),
    Production(37, "Assignment", ("IDENT", "ASSIGN", "AssignRHS")),
    Production(38, "AssignRHS", ("RunCall",)),
    Production(39, "AssignRHS", ("Expr",)),
    Production(40, "RunCall", ("RUN", "IDENT", "DOT", "IDENT", "LPAREN", "ArgListOpt", "RPAREN")),
    Production(41, "IfStmt", ("IF", "Expr", "LBRACE", "SystemStmtList", "RBRACE")),
    Production(42, "ForStmt", ("FOR", "IDENT", "IN", "IDENT", "LBRACE", "SystemStmtList", "RBRACE")),
    Production(43, "Expr", ("AddExpr", "ExprEqTail")),
    Production(44, "ExprEqTail", ("EQEQ", "AddExpr", "ExprEqTail")),
    Production(45, "ExprEqTail", (EPSILON,)),
    Production(46, "AddExpr", ("Primary", "AddTail")),
    Production(47, "AddTail", ("PLUS", "Primary", "AddTail")),
    Production(48, "AddTail", (EPSILON,)),
    Production(49, "Primary", ("IDENT",)),
    Production(50, "Primary", ("STRING_LITERAL",)),
    Production(51, "Primary", ("INT_LITERAL",)),
    Production(52, "Primary", ("TRUE",)),
    Production(53, "Primary", ("FALSE",)),
    Production(54, "Primary", ("ListLiteral",)),
    Production(55, "Primary", ("LPAREN", "Expr", "RPAREN")),
    Production(56, "ListLiteral", ("LBRACKET", "ListItemsOpt", "RBRACKET")),
    Production(57, "ListItemsOpt", ("Expr", "ListItemsTail")),
    Production(58, "ListItemsOpt", (EPSILON,)),
    Production(59, "ListItemsTail", ("COMMA", "Expr", "ListItemsTail")),
    Production(60, "ListItemsTail", (EPSILON,)),
)

NONTERMINALS = tuple(dict.fromkeys(production.lhs for production in PRODUCTIONS))
TERMINALS = frozenset(TERMINAL_DISPLAY)


def is_terminal(symbol: str) -> bool:
    return symbol in TERMINALS


def grammar_by_lhs() -> dict[str, list[Production]]:
    grouped: dict[str, list[Production]] = {nonterminal: [] for nonterminal in NONTERMINALS}
    for production in PRODUCTIONS:
        grouped[production.lhs].append(production)
    return grouped


def first_of_sequence(
    sequence: Iterable[str],
    first_sets: dict[str, set[str]],
) -> set[str]:
    symbols = list(sequence)
    if not symbols:
        return {EPSILON}

    result: set[str] = set()
    for symbol in symbols:
        symbol_first = first_sets[symbol] if symbol in first_sets else {symbol}
        result.update(symbol_first - {EPSILON})
        if EPSILON not in symbol_first:
            break
    else:
        result.add(EPSILON)
    return result


def compute_first_sets() -> dict[str, set[str]]:
    first_sets: dict[str, set[str]] = {terminal: {terminal} for terminal in TERMINALS}
    first_sets[EPSILON] = {EPSILON}
    for nonterminal in NONTERMINALS:
        first_sets.setdefault(nonterminal, set())

    changed = True
    while changed:
        changed = False
        for production in PRODUCTIONS:
            before = set(first_sets[production.lhs])
            first_sets[production.lhs].update(first_of_sequence(production.rhs, first_sets))
            if first_sets[production.lhs] != before:
                changed = True

    return {symbol: values for symbol, values in first_sets.items() if symbol in NONTERMINALS}


def compute_follow_sets(first_sets: dict[str, set[str]]) -> dict[str, set[str]]:
    follow_sets: dict[str, set[str]] = {nonterminal: set() for nonterminal in NONTERMINALS}
    follow_sets[START_SYMBOL].add("EOF")

    changed = True
    while changed:
        changed = False
        for production in PRODUCTIONS:
            trailer = set(follow_sets[production.lhs])
            for symbol in reversed(production.rhs):
                if symbol == EPSILON:
                    continue
                if symbol in NONTERMINALS:
                    before = set(follow_sets[symbol])
                    follow_sets[symbol].update(trailer)
                    if follow_sets[symbol] != before:
                        changed = True

                    if EPSILON in first_sets[symbol]:
                        trailer = trailer | (first_sets[symbol] - {EPSILON})
                    else:
                        trailer = first_sets[symbol] - {EPSILON}
                else:
                    trailer = {symbol}

    return follow_sets


def build_parse_table(
    first_sets: dict[str, set[str]],
    follow_sets: dict[str, set[str]],
) -> dict[str, dict[str, Production]]:
    table: dict[str, dict[str, Production]] = {nonterminal: {} for nonterminal in NONTERMINALS}

    for production in PRODUCTIONS:
        rhs_first = first_of_sequence(production.rhs, {**first_sets, EPSILON: {EPSILON}})
        for terminal in rhs_first - {EPSILON}:
            existing = table[production.lhs].get(terminal)
            if existing and existing != production:
                raise ValueError(
                    f"Grammar is not LL(1): conflict on {production.lhs} with lookahead {terminal}"
                )
            table[production.lhs][terminal] = production

        if EPSILON in rhs_first:
            for terminal in follow_sets[production.lhs]:
                existing = table[production.lhs].get(terminal)
                if existing and existing != production:
                    raise ValueError(
                        f"Grammar is not LL(1): conflict on {production.lhs} with lookahead {terminal}"
                    )
                table[production.lhs][terminal] = production

    return table


def human_symbol(symbol: str) -> str:
    if symbol == EPSILON:
        return "epsilon"
    return TERMINAL_DISPLAY.get(symbol, symbol)


def symbol_sequence_text(symbols: Iterable[str]) -> str:
    items = [human_symbol(symbol) for symbol in symbols]
    return " ".join(items) if items else "epsilon"


def production_lookup() -> dict[int, Production]:
    return {production.number: production for production in PRODUCTIONS}


def render_grammar_markdown() -> str:
    lines = [
        "# Grammar Specification",
        "",
        "Generated from `src/grammar.py`. Re-run `python -m src.docgen` after grammar changes.",
        "",
        "## Terminals",
        "",
        "| Token | Lexeme | Meaning |",
        "| --- | --- | --- |",
    ]
    for token in TERMINAL_ORDER:
        lines.append(
            f"| `{token}` | `{TERMINAL_DISPLAY[token]}` | {TERMINAL_DESCRIPTIONS[token]} |"
        )

    lines.extend(
        [
            "",
            "## Nonterminals",
            "",
            ", ".join(f"`{nonterminal}`" for nonterminal in NONTERMINALS),
            "",
            "## Productions",
            "",
        ]
    )

    for production in PRODUCTIONS:
        lines.append(
            f"{production.number}. `{production.lhs} -> {symbol_sequence_text(production.rhs)}`"
        )
    return "\n".join(lines) + "\n"


def render_first_follow_markdown() -> str:
    first_sets = compute_first_sets()
    follow_sets = compute_follow_sets(first_sets)
    lines = [
        "# FIRST and FOLLOW Sets",
        "",
        "Generated from `src/grammar.py`. Re-run `python -m src.docgen` after grammar changes.",
        "",
        "| Nonterminal | FIRST | FOLLOW |",
        "| --- | --- | --- |",
    ]
    for nonterminal in NONTERMINALS:
        first_text = ", ".join(sorted(human_symbol(item) for item in first_sets[nonterminal]))
        follow_text = ", ".join(sorted(human_symbol(item) for item in follow_sets[nonterminal]))
        lines.append(f"| `{nonterminal}` | `{first_text}` | `{follow_text}` |")
    return "\n".join(lines) + "\n"


def render_parse_table_markdown() -> str:
    first_sets = compute_first_sets()
    follow_sets = compute_follow_sets(first_sets)
    table = build_parse_table(first_sets, follow_sets)

    headers = ["Nonterminal"] + [TERMINAL_DISPLAY[token] for token in TERMINAL_ORDER]
    lines = [
        "# Predictive Parsing Table",
        "",
        "Generated from `src/grammar.py`. Cell values are production numbers from `docs/grammar.md`.",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for nonterminal in NONTERMINALS:
        row = [f"`{nonterminal}`"]
        for terminal in TERMINAL_ORDER:
            production = table[nonterminal].get(terminal)
            row.append(str(production.number) if production else "")
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines) + "\n"


def expected_terminals(nonterminal: str, parse_table: dict[str, dict[str, Production]]) -> list[str]:
    return [human_symbol(token) for token in TERMINAL_ORDER if token in parse_table[nonterminal]]


def generated_docs() -> dict[Path, str]:
    docs_root = Path("docs")
    return {
        docs_root / "grammar.md": render_grammar_markdown(),
        docs_root / "first_follow.md": render_first_follow_markdown(),
        docs_root / "parsing_table.md": render_parse_table_markdown(),
    }
