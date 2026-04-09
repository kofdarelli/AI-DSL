from __future__ import annotations

from pathlib import Path
import sys

from src.grammar import generated_docs


def _write_docs() -> int:
    for path, contents in generated_docs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    return 0


def _check_docs() -> int:
    mismatches: list[Path] = []
    for path, contents in generated_docs().items():
        if not path.exists() or path.read_text(encoding="utf-8") != contents:
            mismatches.append(path)

    if mismatches:
        for path in mismatches:
            print(f"Out of date: {path}")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--check"]:
        return _check_docs()
    if args:
        print("Usage: python -m src.docgen [--check]", file=sys.stderr)
        return 2
    return _write_docs()


if __name__ == "__main__":
    raise SystemExit(main())
