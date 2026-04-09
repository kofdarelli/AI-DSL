# FIRST and FOLLOW Sets

Generated from `src/grammar.py`. Re-run `python -m src.docgen` after grammar changes.

| Nonterminal | FIRST | FOLLOW |
| --- | --- | --- |
| `Program` | `agent, system` | `$` |
| `AgentDeclList` | `agent, epsilon` | `system` |
| `AgentDecl` | `agent` | `agent, system` |
| `AgentItemList` | `epsilon, task, tool` | `}` |
| `AgentItem` | `task, tool` | `task, tool, }` |
| `ToolDecl` | `tool` | `task, tool, }` |
| `TaskDecl` | `task` | `task, tool, }` |
| `ParamListOpt` | `bool, epsilon, int, list, string` | `)` |
| `ParamList` | `bool, int, list, string` | `)` |
| `ParamListTail` | `,, epsilon` | `)` |
| `Param` | `bool, int, list, string` | `), ,` |
| `Type` | `bool, int, list, string` | `identifier` |
| `ActionStmtList` | `action, epsilon` | `}` |
| `ActionStmt` | `action` | `action, }` |
| `ArgListOpt` | `(, [, epsilon, false, identifier, int_literal, string_literal, true` | `)` |
| `ArgList` | `(, [, false, identifier, int_literal, string_literal, true` | `)` |
| `ArgListTail` | `,, epsilon` | `)` |
| `SystemDecl` | `system` | `$` |
| `SystemStmtList` | `bool, epsilon, for, identifier, if, int, list, string` | `}` |
| `SystemStmt` | `bool, for, identifier, if, int, list, string` | `bool, for, identifier, if, int, list, string, }` |
| `VarDecl` | `bool, int, list, string` | `bool, for, identifier, if, int, list, string, }` |
| `Assignment` | `identifier` | `bool, for, identifier, if, int, list, string, }` |
| `AssignRHS` | `(, [, false, identifier, int_literal, run, string_literal, true` | `bool, for, identifier, if, int, list, string, }` |
| `RunCall` | `run` | `bool, for, identifier, if, int, list, string, }` |
| `IfStmt` | `if` | `bool, for, identifier, if, int, list, string, }` |
| `ForStmt` | `for` | `bool, for, identifier, if, int, list, string, }` |
| `Expr` | `(, [, false, identifier, int_literal, string_literal, true` | `), ,, ], bool, for, identifier, if, int, list, string, {, }` |
| `ExprEqTail` | `==, epsilon` | `), ,, ], bool, for, identifier, if, int, list, string, {, }` |
| `AddExpr` | `(, [, false, identifier, int_literal, string_literal, true` | `), ,, ==, ], bool, for, identifier, if, int, list, string, {, }` |
| `AddTail` | `+, epsilon` | `), ,, ==, ], bool, for, identifier, if, int, list, string, {, }` |
| `Primary` | `(, [, false, identifier, int_literal, string_literal, true` | `), +, ,, ==, ], bool, for, identifier, if, int, list, string, {, }` |
| `ListLiteral` | `[` | `), +, ,, ==, ], bool, for, identifier, if, int, list, string, {, }` |
| `ListItemsOpt` | `(, [, epsilon, false, identifier, int_literal, string_literal, true` | `]` |
| `ListItemsTail` | `,, epsilon` | `]` |
