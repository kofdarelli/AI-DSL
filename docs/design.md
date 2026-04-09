# Design Notes

## Scope

This Phase 1 implementation covers syntax analysis only. The parser accepts the DSL subset required by the handout:

- agent blocks with `tool` and `task` declarations
- task signatures with typed parameters and a typed return binding
- task bodies containing `action: tool_name(args)` statements
- one `system` block with typed declarations, assignments, `run` calls, `if`, `for`, list literals, and simple expressions

Semantic validation is intentionally deferred to Phase 2.

## Lexer

The lexer is implemented in `src/lexer.py` with the Python standard library `re` module. It uses a single master regular expression and then remaps identifiers into reserved keywords such as `agent`, `task`, `system`, and the type keywords.

Each token carries:

- token type
- original lexeme
- line number
- column number

That metadata is reused directly by the parser when formatting syntax errors.

## Grammar and LL(1) Strategy

The grammar lives in `src/grammar.py` as numbered productions. The same source drives:

- the `FIRST` sets
- the `FOLLOW` sets
- the predictive parsing table
- the generated Markdown deliverables in `docs/`

The grammar is written in LL(1)-friendly form:

- optional lists use explicit `Opt` nonterminals
- comma-separated sequences use tail productions
- expressions use precedence tiers for equality and addition
- `AssignRHS` splits `run` calls from normal expressions so there is no lookahead conflict

Because the parser and the written deliverables come from the same production list, the submission artifacts stay synchronized.

## Parser

The parser is table-driven, not recursive descent. `src/parser.py`:

1. tokenizes the source file
2. computes the parse table from the grammar metadata
3. pushes the start symbol on an explicit stack
4. repeatedly expands nonterminals or matches terminals

The parser does not build an AST in Phase 1. Its job is acceptance and clear syntax diagnostics.

## Error Reporting

On failure, the parser reports:

- line and column
- the found lexeme and token category
- the set of terminals that would have been valid at that point

This keeps the output compact while still making malformed input debuggable.

## Documentation Workflow

The files below are generated from `src/grammar.py`:

- `docs/grammar.md`
- `docs/first_follow.md`
- `docs/parsing_table.md`

Regenerate them with:

```bash
python -m src.docgen
```

Verify they are current with:

```bash
python -m src.docgen --check
```
