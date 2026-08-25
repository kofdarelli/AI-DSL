from __future__ import annotations

from pathlib import Path
import sys
from src.lexer import tokenize, LexerError

from src.parser import DSLSyntaxError, syntax_check


USAGE = "Usage: python main.py [--token] <file.dsl>"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    dump_token = "--token" in args

    args.remove("--token")

    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    source = Path(args[0])

    if dump_token:
        try:
            content = source.read_text(encoding="utf-8")
            content_tokenized = tokenize(content)
        except (LexerError, OSError) as exception:
            print(str(exception), file=sys.stderr)
            return 1 
        for item in content_tokenized:
            print(f"{item.line}:{item.column} {item.type} {item.lexeme!r}")         
        return 0               
                 
    try:
        result = syntax_check(source)
    except (DSLSyntaxError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Parse successful: {source} ({result.token_count} tokens)")
    return 0
