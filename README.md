# AI-DSL

[![CI](https://github.com/kofdarelli/AI-DSL/actions/workflows/ci.yml/badge.svg)](https://github.com/kofdarelli/AI-DSL/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10+-1a1a1a?logo=python&logoColor=white)](src)
[![Parser: LL(1)](https://img.shields.io/badge/Parser-LL%281%29-8c2f26)](docs/design.md)

A hand-written lexer, predictive parser, and documentation toolchain for describing multi-agent workflows in a readable domain-specific language.

```text
agent Researcher {
    tool web_search

    task gather(string topic) -> string data {
        action: web_search(topic)
    }
}

system {
    string data = run Researcher.gather("AI safety")
}
```

AI-DSL is an AUB EECE 334 language-design project. The current phase performs syntax analysis rather than executing agents or validating workflow semantics.

## What it demonstrates

- A regex-based lexer that preserves line and column positions.
- An LL(1)-friendly grammar for agents, tools, typed tasks, actions, variables, lists, conditionals, loops, and task calls.
- FIRST and FOLLOW set computation.
- Predictive parse-table generation from the same grammar metadata.
- A table-driven parser with explicit stack processing.
- Syntax errors that report the found token and valid alternatives.
- Generated grammar, FIRST/FOLLOW, and parsing-table documentation checked in CI.

## Pipeline

```mermaid
flowchart LR
    S[DSL source] --> L[Lexer]
    L --> T[Positioned tokens]
    T --> P[LL(1) parser]
    G[Grammar metadata] --> P
    G --> D[Generated documentation]
    P --> R[Accepted workflow or syntax error]
```

## Quick start

The implementation uses only the Python standard library.

```bash
git clone https://github.com/kofdarelli/AI-DSL.git
cd AI-DSL
python main.py examples/valid/full_workflow.dsl
```

Successful input prints the source path and token count:

```text
Parse successful: examples/valid/full_workflow.dsl (... tokens)
```

Run the verification suite:

```bash
python -m unittest discover -s tests
python -m src.docgen --check
```

Regenerate the grammar documentation after changing `src/grammar.py`:

```bash
python -m src.docgen
```

## Language shape

An AI-DSL program contains zero or more `agent` blocks followed by one `system` block. Agents declare tools and typed tasks. The system block can declare and assign variables, invoke tasks with `run`, branch with `if`, and iterate lists with `for`.

See:

- [Grammar specification](docs/grammar.md)
- [FIRST and FOLLOW sets](docs/first_follow.md)
- [Predictive parsing table](docs/parsing_table.md)
- [Implementation design notes](docs/design.md)
- [Valid and invalid examples](examples)

## Project layout

```text
src/        lexer, grammar metadata, parser, CLI, and doc generator
examples/   valid and intentionally invalid DSL programs
tests/      parser and generated-document verification
docs/       generated grammar artifacts and design notes
main.py     command-line entry point
```

## Current boundaries

- The parser validates syntax but does not build an abstract syntax tree.
- Semantic validation and workflow execution are intentionally outside this phase.
- The checked-in course brief may have separate ownership from the implementation. No repository-wide open-source license is declared until those materials are separated or their reuse rights are confirmed.

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Report vulnerabilities privately using [SECURITY.md](SECURITY.md).
