from compiler.lexer.tokens import TokenType
from compiler.parser.syntax_tree import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]

    def error(self, message=""):
        raise Exception(f'Parser error at token {self.current_token}: {message}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(f'Expected {token_type}, got {self.current_token.type}')

    def program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.statement()
            statements.append(stmt)
        return Program(statements)

    def statement(self):
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.STRING]:
            return self.var_declaration()
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment()
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        else:
            self.error("Invalid statement")

    def var_declaration(self):
        var_type = self.current_token.type
        self.eat(var_type)

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ASSIGN)
        init_value = self.expr()
        self.eat(TokenType.SEMICOLON)

        return VarDecl(var_type, var_name, init_value)

    def assignment(self):
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        value = self.expr()
        self.eat(TokenType.SEMICOLON)
        return Assign(name, value)

    def if_statement(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.bool_expr()  # Utilise bool_expr au lieu de expr
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)

        true_body = []
        while self.current_token.type != TokenType.RBRACE:
            true_body.append(self.statement())
        self.eat(TokenType.RBRACE)

        false_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            false_body = []
            while self.current_token.type != TokenType.RBRACE:
                false_body.append(self.statement())
            self.eat(TokenType.RBRACE)

        return If(condition, true_body, false_body)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.bool_expr()  # Utilise bool_expr au lieu de expr
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)

        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        self.eat(TokenType.RBRACE)

        return While(condition, body)

    def bool_expr(self):
        left = self.expr()

        if self.current_token.type in [TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
                                       TokenType.EQ, TokenType.NEQ]:
            op = self.current_token.type
            self.eat(op)
            right = self.expr()
            return BinOp(left, op, right)

        return left

    def expr(self):
        node = self.term()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.factor())

        return node

    def factor(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Var(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            self.error("Invalid factor")

    def parse(self):
        return self.program()