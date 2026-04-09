from __future__ import annotations

from pathlib import Path
import sys

from src.parser import DSLSyntaxError, syntax_check


USAGE = "Usage: python main.py <file.dsl>"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(USAGE, file=sys.stderr)
        return 2

    source = Path(args[0])
    try:
        result = syntax_check(source)
    except (DSLSyntaxError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Parse successful: {source} ({result.token_count} tokens)")
    return 0
