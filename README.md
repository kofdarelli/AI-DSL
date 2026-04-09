# AI-DSL

Phase 1 deliverables for the EECE 334 multi-agent workflow DSL.

## Usage

```bash
python main.py examples/valid/full_workflow.dsl
```

## Layout

- `src/` contains the lexer, grammar metadata, parse-table generation, parser, CLI, and doc generator.
- `docs/` contains the written deliverables.
- `examples/` contains valid and invalid sample DSL programs.
- `tests/` contains a small verification suite.

## Commands

```bash
python -m src.docgen
python -m src.docgen --check
python -m unittest discover -s tests
```
