# Grammar Specification

Generated from `src/grammar.py`. Re-run `python -m src.docgen` after grammar changes.

## Terminals

| Token | Lexeme | Meaning |
| --- | --- | --- |
| `AGENT` | `agent` | agent keyword |
| `TOOL` | `tool` | tool keyword |
| `TASK` | `task` | task keyword |
| `SYSTEM` | `system` | system keyword |
| `ACTION` | `action` | action keyword |
| `RUN` | `run` | run keyword |
| `IF` | `if` | if keyword |
| `FOR` | `for` | for keyword |
| `IN` | `in` | in keyword |
| `TYPE_STRING` | `string` | string type keyword |
| `TYPE_INT` | `int` | int type keyword |
| `TYPE_BOOL` | `bool` | bool type keyword |
| `TYPE_LIST` | `list` | list type keyword |
| `IDENT` | `identifier` | identifier |
| `STRING_LITERAL` | `string_literal` | double-quoted string literal |
| `INT_LITERAL` | `int_literal` | integer literal |
| `TRUE` | `true` | boolean literal true |
| `FALSE` | `false` | boolean literal false |
| `LBRACE` | `{` | left brace |
| `RBRACE` | `}` | right brace |
| `LPAREN` | `(` | left parenthesis |
| `RPAREN` | `)` | right parenthesis |
| `LBRACKET` | `[` | left bracket |
| `RBRACKET` | `]` | right bracket |
| `COMMA` | `,` | comma |
| `COLON` | `:` | colon |
| `ARROW` | `->` | arrow |
| `DOT` | `.` | dot |
| `ASSIGN` | `=` | assignment operator |
| `EQEQ` | `==` | equality operator |
| `PLUS` | `+` | addition operator |
| `EOF` | `$` | end of file |

## Nonterminals

`Program`, `AgentDeclList`, `AgentDecl`, `AgentItemList`, `AgentItem`, `ToolDecl`, `TaskDecl`, `ParamListOpt`, `ParamList`, `ParamListTail`, `Param`, `Type`, `ActionStmtList`, `ActionStmt`, `ArgListOpt`, `ArgList`, `ArgListTail`, `SystemDecl`, `SystemStmtList`, `SystemStmt`, `VarDecl`, `Assignment`, `AssignRHS`, `RunCall`, `IfStmt`, `ForStmt`, `Expr`, `ExprEqTail`, `AddExpr`, `AddTail`, `Primary`, `ListLiteral`, `ListItemsOpt`, `ListItemsTail`

## Productions

1. `Program -> AgentDeclList SystemDecl $`
2. `AgentDeclList -> AgentDecl AgentDeclList`
3. `AgentDeclList -> epsilon`
4. `AgentDecl -> agent identifier { AgentItemList }`
5. `AgentItemList -> AgentItem AgentItemList`
6. `AgentItemList -> epsilon`
7. `AgentItem -> ToolDecl`
8. `AgentItem -> TaskDecl`
9. `ToolDecl -> tool identifier`
10. `TaskDecl -> task identifier ( ParamListOpt ) -> Type identifier { ActionStmtList }`
11. `ParamListOpt -> ParamList`
12. `ParamListOpt -> epsilon`
13. `ParamList -> Param ParamListTail`
14. `ParamListTail -> , Param ParamListTail`
15. `ParamListTail -> epsilon`
16. `Param -> Type identifier`
17. `Type -> string`
18. `Type -> int`
19. `Type -> bool`
20. `Type -> list`
21. `ActionStmtList -> ActionStmt ActionStmtList`
22. `ActionStmtList -> epsilon`
23. `ActionStmt -> action : identifier ( ArgListOpt )`
24. `ArgListOpt -> ArgList`
25. `ArgListOpt -> epsilon`
26. `ArgList -> Expr ArgListTail`
27. `ArgListTail -> , Expr ArgListTail`
28. `ArgListTail -> epsilon`
29. `SystemDecl -> system { SystemStmtList }`
30. `SystemStmtList -> SystemStmt SystemStmtList`
31. `SystemStmtList -> epsilon`
32. `SystemStmt -> VarDecl`
33. `SystemStmt -> Assignment`
34. `SystemStmt -> IfStmt`
35. `SystemStmt -> ForStmt`
36. `VarDecl -> Type identifier = AssignRHS`
37. `Assignment -> identifier = AssignRHS`
38. `AssignRHS -> RunCall`
39. `AssignRHS -> Expr`
40. `RunCall -> run identifier . identifier ( ArgListOpt )`
41. `IfStmt -> if Expr { SystemStmtList }`
42. `ForStmt -> for identifier in identifier { SystemStmtList }`
43. `Expr -> AddExpr ExprEqTail`
44. `ExprEqTail -> == AddExpr ExprEqTail`
45. `ExprEqTail -> epsilon`
46. `AddExpr -> Primary AddTail`
47. `AddTail -> + Primary AddTail`
48. `AddTail -> epsilon`
49. `Primary -> identifier`
50. `Primary -> string_literal`
51. `Primary -> int_literal`
52. `Primary -> true`
53. `Primary -> false`
54. `Primary -> ListLiteral`
55. `Primary -> ( Expr )`
56. `ListLiteral -> [ ListItemsOpt ]`
57. `ListItemsOpt -> Expr ListItemsTail`
58. `ListItemsOpt -> epsilon`
59. `ListItemsTail -> , Expr ListItemsTail`
60. `ListItemsTail -> epsilon`
