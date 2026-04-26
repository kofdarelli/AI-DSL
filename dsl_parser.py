"""
Our Grammar Design:
  Program     → AgentList SystemBlock
  AgentList   → AgentDef AgentList | ε
  AgentDef    → agent ID { AgentBody }
  AgentBody   → AgentItem AgentBody | ε
  AgentItem   → ToolDecl | TaskDecl
  ToolDecl    → tool ID
  TaskDecl    → task ID ( ParamList ) ReturnSpec { ActionList }
  ParamList   → Param ParamListTail | ε
  ParamListTail → , Param ParamListTail | ε
  Param       → Type ID
  ReturnSpec  → -> Type ID | ε
  ActionList  → ActionStmt ActionList | ε
  ActionStmt  → action : ID ( ActionArgs )
  ActionArgs  → Arg ActionArgsTail | ε
  ActionArgsTail → , Arg ActionArgsTail | ε
  SystemBlock → system { StmtList }
  StmtList    → Stmt StmtList | ε
  Stmt        → Type ID = Expr          
              | ID = Expr               
              | ForStmt
              | IfStmt
  ForStmt     → for ID in ID { StmtList }
  IfStmt      → if Condition { StmtList }
  Condition   → ID CompOp Arg
  CompOp      → == | != | < | > | <= | >=
  Expr        → run ID . ID ( ArgList ) (RunExpr)
              | ArithExpr
  ArgList     → Arg ArgTail | ε
  ArgTail     → , Arg ArgTail | ε
  ArithExpr   → Term ArithTail
  ArithTail   → + Term ArithTail | - Term ArithTail | ε
  Term        → Factor TermTail
  TermTail    → * Factor TermTail | / Factor TermTail | ε
  Factor      → INT_LIT | STRING_LIT | true | false | ID
              | ( ArithExpr ) | ListLit
  ListLit     → [ ListItems ]
  ListItems   → Arg ListItemsTail | ε
  ListItemsTail → , Arg ListItemsTail | ε
  Arg         → STRING_LIT | INT_LIT | ID | true | false
  Type        → string | int | bool | list
"""

import sys
from dsl_lexer import tokenize, Token

# Helper sets (used in parse functions for LL(1) lookahead decisions)
TYPE_TOKENS    = {"STRING_TYPE", "INT_TYPE", "BOOL_TYPE", "LIST_TYPE"}
ARG_TOKENS     = {"STRING_LIT", "INT_LIT", "ID", "TRUE", "FALSE"}
FACTOR_TOKENS  = {"INT_LIT", "STRING_LIT", "TRUE", "FALSE", "ID", "LPAREN", "LBRACKET"}
STMT_FIRST     = TYPE_TOKENS | {"ID", "FOR", "IF"}
COMP_OPS       = {"EQEQ", "NEQ", "LT", "GT", "LEQ", "GEQ"}


class Parser:
    """
    LL(1) Recursive Descent Parser.

    Each public parse_X() method corresponds to non-terminal X in the grammar.
    The parser uses peek() for lookahead and expect() to consume expected tokens,
    exactly as described in our course notes.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        # index points to the next unconsumed token
        #  peek() definition
        self.index = 0


    def peek(self, how_far=1):
        """
        Return the token how_far positions ahead WITHOUT consuming it.
        peek(1) → next token to be consumed (does not advance index).
          "peek(1) returns token_array[index+1-1] = token_array[index]"
        """
        idx = self.index + how_far - 1
        if idx >= len(self.tokens):
            return Token("EOF", "", -1, -1)
        return self.tokens[idx]

    def get_token(self):
        """
        Consume and return the next token (advances index).
        getToken() definition from our class notes.
        """
        if self.index >= len(self.tokens):
            return Token("EOF", "", -1, -1)
        tok = self.tokens[self.index]
        self.index += 1
        return tok

    def expect(self, token_type):
        """
        Consume the next token; raise SyntaxError if its type differs from token_type.
        expect() definition from our class notes:
          "expect(ttype) : t = lexer.getToken(); if (t.token_type != ttype) syntax_error();"
        """
        tok = self.get_token()
        if tok.type != token_type:
            self._syntax_error(
                f"expected '{token_type}' but found '{tok.type}' ('{tok.value}')",
                tok
            )
        return tok

    def _syntax_error(self, msg, tok=None):
        """
        Report a syntax error and stop. As described also in our course notes.
        """
        if tok and tok.line >= 0:
            raise SyntaxError(f"Syntax error at line {tok.line}, col {tok.column}: {msg}")
        raise SyntaxError(f"Syntax error: {msg}")


    def parse_program(self):
        """Program → AgentList SystemBlock"""
        self.parse_agent_list()
        self.parse_system_block()
        # After the program there should be nothing left
        remaining = self.get_token()
        if remaining.type != "EOF":
            self._syntax_error(
                f"unexpected token '{remaining.value}' after system block",
                remaining
            )
        print("Parsing successful - DSL program is syntactically valid.")

    #Agent definitions

    def parse_agent_list(self):
        """
        AgentList → AgentDef AgentList | ε
        Decide using peek(1): if AGENT → parse AgentDef; else ε (do nothing).
        FIRST(AgentDef) = {AGENT}, FOLLOW(AgentList) = {SYSTEM}
        """
        while self.peek().type == "AGENT":
            self.parse_agent_def()

    def parse_agent_def(self):
        """AgentDef → agent ID { AgentBody }"""
        self.expect("AGENT")
        self.expect("ID")
        self.expect("LBRACE")
        self.parse_agent_body()
        self.expect("RBRACE")

    def parse_agent_body(self):
        """
        AgentBody → AgentItem AgentBody | ε
        FIRST(AgentItem) = {TOOL, TASK}, FOLLOW(AgentBody) = {RBRACE}
        """
        while self.peek().type in ("TOOL", "TASK"):
            self.parse_agent_item()

    def parse_agent_item(self):
        """
        AgentItem → ToolDecl | TaskDecl
        Distinguish by lookahead: TOOL → ToolDecl, TASK → TaskDecl
        """
        t = self.peek().type
        if t == "TOOL":
            self.parse_tool_decl()
        elif t == "TASK":
            self.parse_task_decl()
        else:
            self._syntax_error("expected 'tool' or 'task' declaration", self.peek())

    def parse_tool_decl(self):
        """ToolDecl → tool ID"""
        self.expect("TOOL")
        self.expect("ID")

    def parse_task_decl(self):
        """TaskDecl → task ID ( ParamList ) ReturnSpec { ActionList }"""
        self.expect("TASK")
        self.expect("ID")
        self.expect("LPAREN")
        self.parse_param_list()
        self.expect("RPAREN")
        self.parse_return_spec()
        self.expect("LBRACE")
        self.parse_action_list()
        self.expect("RBRACE")

    def parse_param_list(self):
        """
        ParamList → Param ParamListTail | ε
        FIRST(Param) = TYPE_TOKENS, FOLLOW(ParamList) = {RPAREN}
        """
        if self.peek().type in TYPE_TOKENS:
            self.parse_param()
            self.parse_param_list_tail()

    def parse_param_list_tail(self):
        """ParamListTail → , Param ParamListTail | ε"""
        while self.peek().type == "COMMA":
            self.expect("COMMA")
            self.parse_param()

    def parse_param(self):
        """Param → Type ID"""
        self.parse_type()
        self.expect("ID")

    def parse_return_spec(self):
        """
        ReturnSpec → -> Type ID | ε
        FIRST = {ARROW}, FOLLOW = {LBRACE}
        """
        if self.peek().type == "ARROW":
            self.expect("ARROW")
            self.parse_type()
            self.expect("ID")

    def parse_action_list(self):
        """
        ActionList → ActionStmt ActionList | ε
        FIRST(ActionStmt) = {ACTION}, FOLLOW(ActionList) = {RBRACE}
        """
        while self.peek().type == "ACTION":
            self.parse_action_stmt()

    def parse_action_stmt(self):
        """ActionStmt → action : ID ( ActionArgs )"""
        self.expect("ACTION")
        self.expect("COLON")
        self.expect("ID")
        self.expect("LPAREN")
        self.parse_action_args()
        self.expect("RPAREN")

    def parse_action_args(self):
        """
        ActionArgs → Arg ActionArgsTail | ε
        FIRST(Arg) = ARG_TOKENS, FOLLOW(ActionArgs) = {RPAREN}
        """
        if self.peek().type in ARG_TOKENS:
            self.parse_arg()
            while self.peek().type == "COMMA":
                self.expect("COMMA")
                self.parse_arg()

    #  System block 

    def parse_system_block(self):
        """SystemBlock → system { StmtList }"""
        self.expect("SYSTEM")
        self.expect("LBRACE")
        self.parse_stmt_list()
        self.expect("RBRACE")

    def parse_stmt_list(self):
        """
        StmtList → Stmt StmtList | ε
        FIRST(Stmt) = STMT_FIRST, FOLLOW(StmtList) = {RBRACE}
        """
        while self.peek().type in STMT_FIRST:
            self.parse_stmt()

    def parse_stmt(self):
        """
        Stmt → Type ID = Expr          (VarDecl)
             | ID = Expr               (Assignment)
             | ForStmt
             | IfStmt

        Lookahead one token is sufficient because each alternative starts with
        a distinct token (TYPE_TOKENS vs ID vs FOR vs IF) so no conflict.
        """
        t = self.peek().type
        if t in TYPE_TOKENS:
            # VarDecl: Type ID = Expr
            self.parse_type()
            self.expect("ID")
            self.expect("EQ")
            self.parse_expr()
        elif t == "ID":
            # Assignment: ID = Expr
            self.expect("ID")
            self.expect("EQ")
            self.parse_expr()
        elif t == "FOR":
            self.parse_for_stmt()
        elif t == "IF":
            self.parse_if_stmt()
        else:
            self._syntax_error("expected statement", self.peek())

    def parse_for_stmt(self):
        """ForStmt → for ID in ID { StmtList }"""
        self.expect("FOR")
        self.expect("ID")
        self.expect("IN")
        self.expect("ID")
        self.expect("LBRACE")
        self.parse_stmt_list()
        self.expect("RBRACE")

    def parse_if_stmt(self):
        """IfStmt → if Condition { StmtList }"""
        self.expect("IF")
        self.parse_condition()
        self.expect("LBRACE")
        self.parse_stmt_list()
        self.expect("RBRACE")

    def parse_condition(self):
        """Condition → ID CompOp Arg"""
        self.expect("ID")
        self.parse_comp_op()
        self.parse_arg()

    def parse_comp_op(self):
        """CompOp → == | != | < | > | <= | >="""
        if self.peek().type in COMP_OPS:
            self.get_token()
        else:
            self._syntax_error("expected comparison operator (==, !=, <, >, <=, >=)", self.peek())

    # Expressions 

    def parse_expr(self):
        """
        Expr → run ID . ID ( ArgList )   (RunExpr)
             | ArithExpr

        FIRST(RunExpr) = {RUN}
        FIRST(ArithExpr) = FACTOR_TOKENS
        The two sets are disjoint - no LL(1) conflict.
        """
        if self.peek().type == "RUN":
            # RunExpr : call to an agent task
            self.expect("RUN")
            self.expect("ID")
            self.expect("DOT")
            self.expect("ID")
            self.expect("LPAREN")
            self.parse_arg_list()
            self.expect("RPAREN")
        elif self.peek().type in FACTOR_TOKENS:
            self.parse_arith_expr()
        else:
            self._syntax_error("expected expression", self.peek())

    def parse_arg_list(self):
        """ArgList → Arg ArgTail | ε"""
        if self.peek().type in ARG_TOKENS:
            self.parse_arg()
            while self.peek().type == "COMMA":
                self.expect("COMMA")
                self.parse_arg()

    def parse_arith_expr(self):
        """ArithExpr → Term ArithTail"""
        self.parse_term()
        self.parse_arith_tail()

    def parse_arith_tail(self):
        """
        ArithTail → + Term ArithTail | - Term ArithTail | ε
        FIRST = {PLUS, MINUS}
        """
        while self.peek().type in ("PLUS", "MINUS"):
            self.get_token()
            self.parse_term()

    def parse_term(self):
        """Term → Factor TermTail"""
        self.parse_factor()
        self.parse_term_tail()

    def parse_term_tail(self):
        """
        TermTail → * Factor TermTail | / Factor TermTail | ε
        FIRST = {MULT, DIV}
        """
        while self.peek().type in ("MULT", "DIV"):
            self.get_token()
            self.parse_factor()

    def parse_factor(self):
        """
        Factor → INT_LIT | STRING_LIT | true | false | ID
               | ( ArithExpr )
               | ListLit

        Each alternative starts with a distinct token  no LL(1) conflict. 
        """
        t = self.peek().type
        if t == "INT_LIT":
            self.expect("INT_LIT")
        elif t == "STRING_LIT":
            self.expect("STRING_LIT")
        elif t == "TRUE":
            self.expect("TRUE")
        elif t == "FALSE":
            self.expect("FALSE")
        elif t == "ID":
            self.expect("ID")
        elif t == "LPAREN":
            self.expect("LPAREN")
            self.parse_arith_expr()
            self.expect("RPAREN")
        elif t == "LBRACKET":
            self.parse_list_lit()
        else:
            self._syntax_error("expected factor (literal, identifier, or sub-expression)", self.peek())

    def parse_list_lit(self):
        """ListLit → [ ListItems ]"""
        self.expect("LBRACKET")
        self.parse_list_items()
        self.expect("RBRACKET")

    def parse_list_items(self):
        """ListItems → Arg ListItemsTail | ε"""
        if self.peek().type in ARG_TOKENS:
            self.parse_arg()
            while self.peek().type == "COMMA":
                self.expect("COMMA")
                self.parse_arg()

    def parse_arg(self):
        """Arg → STRING_LIT | INT_LIT | ID | true | false"""
        t = self.peek().type
        if t in ARG_TOKENS:
            self.get_token()
        else:
            self._syntax_error(
                "expected argument (string literal, integer, identifier, or boolean)",
                self.peek()
            )

    def parse_type(self):
        """Type → string | int | bool | list"""
        if self.peek().type in TYPE_TOKENS:
            self.get_token()
        else:
            self._syntax_error("expected type keyword (string, int, bool, list)", self.peek())




#Here we used the help from chatgpt to learn how we can run our parser and lexer to test our code.
def main():
    if len(sys.argv) != 2:
        print("Usage: python dsl_parser.py <dsl_source_file>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    try:
        tokens = tokenize(source)
    except SyntaxError as e:
        print("Lexical error:", e)
        sys.exit(1)

    try:
        parser = Parser(tokens)
        parser.parse_program()
    except SyntaxError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
