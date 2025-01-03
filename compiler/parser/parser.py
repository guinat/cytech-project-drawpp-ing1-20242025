from compiler.lexer.tokens import TokenType
from compiler.parser.syntax_tree import *


class Parser:
    """
    @brief A class responsible for parsing tokens into an abstract syntax tree (AST).
    """

    def __init__(self, tokens):
        """
        @brief Initializes the parser with a list of tokens.

        @param tokens List of tokens to be parsed.
        """
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]

    def error(self, message=""):
        """
        @brief Raises a parsing error with a message.

        @param message A custom error message.
        @throws Exception with details about the parsing error.
        """
        raise Exception(f'Parser error at token {
                        self.current_token}: {message}')

    def eat(self, token_type):
        """
        @brief Consumes the current token if it matches the expected type.

        @param token_type The expected token type.
        @throws Exception if the current token does not match the expected type.
        """
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(f'Expected {token_type}, got {self.current_token.type}')

    def peek(self):
        """
        @brief Peeks at the next token without consuming it.

        @return The next token or None if at the end of the token list.
        """
        peek_pos = self.pos + 1
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def is_cursor_method_type(self, ttype):
        """
        @brief Checks if a token type corresponds to a cursor method.

        @param ttype The token type to check.
        @return True if the token type is a cursor method, False otherwise.
        """
        cursor_method_types = [
            TokenType.COLOR,
            TokenType.THICKNESS,
            TokenType.MOVE,
            TokenType.ROTATE,
            TokenType.VISIBLE,
            TokenType.DRAW_LINE,
            TokenType.DRAW_RECTANGLE,
            TokenType.DRAW_CIRCLE,
            TokenType.DRAW_TRIANGLE,
            TokenType.DRAW_ELLIPSE
        ]
        return ttype in cursor_method_types

    def program(self):
        """
        @brief Parses a program consisting of multiple statements.

        @return A Program node containing a list of statements.
        """
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        """
        @brief Parses a single statement.

        @return A statement node.
        @throws Exception if an unexpected token is encountered.
        """
        token = self.current_token

        if token.type == TokenType.VAR:
            return self.var_declaration()

        elif token.type == TokenType.CURSOR:
            return self.cursor_statement()

        elif token.type == TokenType.IF:
            return self.if_statement()

        elif token.type == TokenType.FOR:
            return self.for_statement()

        elif token.type == TokenType.WHILE:
            return self.while_statement()

        elif token.type == TokenType.IDENTIFIER:
            return self.identifier_statement()

        else:
            self.error(f"Unexpected token {token.type} in statement")

    def identifier_statement(self):
        """
        @brief Parses a statement starting with an identifier.

        @return A node representing an assignment, method call, or error.
        """
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        if self.current_token.type == TokenType.DOT:
            self.eat(TokenType.DOT)
            method_token = self.current_token
            if self.is_cursor_method_type(method_token.type):
                method_name = method_token.value
                self.eat(method_token.type)
                return self.cursor_method_statement(name, method_name)
            else:
                self.error("Expected a known method after '.'")

        elif self.current_token.type in [TokenType.ASSIGN, TokenType.PLUS_EQUAL,
                                         TokenType.MINUS_EQUAL, TokenType.STAR_EQUAL,
                                         TokenType.SLASH_EQUAL]:
            return self.assignment_statement(name)
        else:
            self.error("Expected '.' or assignment operator after identifier")

    def cursor_statement(self):
        """
        @brief Parses a cursor creation statement.

        @return A CursorCreation node.
        """
        self.eat(TokenType.CURSOR)
        cursor_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ASSIGN)
        self.eat(TokenType.CREATE_CURSOR)
        self.eat(TokenType.LPAREN)

        x = self.expr()
        self.eat(TokenType.COMMA)
        y = self.expr()

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)

        return CursorCreation(cursor_name, x, y)

    def cursor_method_statement(self, cursor_name, method_name):
        """
        @brief Parses a cursor method statement.

        @param cursor_name The name of the cursor.
        @param method_name The name of the method to call.
        @return A CursorMethod or DrawCommand node.
        """
        self.eat(TokenType.LPAREN)

        params = []
        if self.current_token.type != TokenType.RPAREN:
            params.append(self.expr())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.expr())

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)

        if method_name.startswith('draw_'):
            return DrawCommand(cursor_name, method_name, params)
        else:
            return CursorMethod(cursor_name, method_name, params)

    def assignment_statement(self, name, eat_semicolon=True):
        """
        @brief Parses an assignment statement.

        @param name The name of the variable being assigned.
        @param eat_semicolon Whether to consume the semicolon at the end.
        @return An Assign node.
        """
        if self.current_token.type in [TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL,
                                       TokenType.STAR_EQUAL, TokenType.SLASH_EQUAL]:
            op = self.current_token.type
            self.eat(op)
            expr = self.expr()
            binary_op = {
                TokenType.PLUS_EQUAL: TokenType.PLUS,
                TokenType.MINUS_EQUAL: TokenType.MINUS,
                TokenType.STAR_EQUAL: TokenType.MULT,
                TokenType.SLASH_EQUAL: TokenType.SLASH
            }[op]
            value = BinOp(Var(name), binary_op, expr)
        else:
            self.eat(TokenType.ASSIGN)
            value = self.expr()

        if eat_semicolon:
            self.eat(TokenType.SEMICOLON)

        return Assign(name, value)

    def if_statement(self):
        """
        @brief Parses an if-statement.

        @return An If node.
        """
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.bool_expr()
        self.eat(TokenType.RPAREN)

        self.eat(TokenType.LBRACE)
        true_body = []
        while self.current_token.type != TokenType.RBRACE:
            true_body.append(self.statement())
        self.eat(TokenType.RBRACE)

        elif_bodies = []
        while self.current_token.type == TokenType.ELIF:
            self.eat(TokenType.ELIF)
            self.eat(TokenType.LPAREN)
            elif_condition = self.bool_expr()
            self.eat(TokenType.RPAREN)

            self.eat(TokenType.LBRACE)
            elif_body = []
            while self.current_token.type != TokenType.RBRACE:
                elif_body.append(self.statement())
            self.eat(TokenType.RBRACE)

            elif_bodies.append((elif_condition, elif_body))

        false_body = None
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            false_body = []
            while self.current_token.type != TokenType.RBRACE:
                false_body.append(self.statement())
            self.eat(TokenType.RBRACE)

        self.eat(TokenType.SEMICOLON)
        return If(condition, true_body, elif_bodies, false_body)

    def for_statement(self):
        """
        @brief Parses a for-loop statement.

        @return A For node.
        """
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)

        if self.current_token.type == TokenType.VAR:
            init = self.var_declaration()
        else:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            init = self.assignment_statement(var_name)

        condition = self.bool_expr()
        self.eat(TokenType.SEMICOLON)

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        update = self.assignment_statement(var_name, eat_semicolon=False)

        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)

        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        self.eat(TokenType.RBRACE)

        self.eat(TokenType.SEMICOLON)
        return For(init, condition, update, body)

    def while_statement(self):
        """
        @brief Parses a while-loop statement.

        @return A While node.
        """
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.bool_expr()
        self.eat(TokenType.RPAREN)

        self.eat(TokenType.LBRACE)
        body = []
        while self.current_token.type != TokenType.RBRACE:
            body.append(self.statement())
        self.eat(TokenType.RBRACE)

        self.eat(TokenType.SEMICOLON)
        return While(condition, body)

    def bool_expr(self):
        """
        @brief Parses a boolean expression.

        @return A BinOp or expression node.
        """
        left = self.expr()

        if self.current_token.type in [TokenType.LESS, TokenType.LESS_EQUAL,
                                       TokenType.GREATER, TokenType.GREATER_EQUAL,
                                       TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL]:
            op = self.current_token.type
            self.eat(op)
            right = self.expr()
            return BinOp(left, op, right)

        return left

    def expr(self):
        """
        @brief Parses an expression.

        @return A BinOp or term node.
        """
        node = self.term()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.term())

        return node

    def term(self):
        """
        @brief Parses a term.

        @return A BinOp or factor node.
        """
        node = self.factor()

        while self.current_token.type in [TokenType.MULT, TokenType.SLASH, TokenType.MODULO]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.factor())

        return node

    def factor(self):
        """
        @brief Parses a factor.

        @return A node representing a number, string, boolean, or other basic value.
        @throws Exception if the factor is invalid.
        """
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token.value)

        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return StringLiteral(token.value)

        elif token.type == TokenType.BOOL_VALUE:
            self.eat(TokenType.BOOL_VALUE)
            return BooleanLiteral(token.value)


        elif token.type in [TokenType.RED, TokenType.GREEN, TokenType.BLUE,
                            TokenType.BLACK, TokenType.WHITE, TokenType.GRAY,
                            TokenType.LIGHT_GRAY, TokenType.DARK_GRAY,
                            TokenType.ORANGE, TokenType.BROWN, TokenType.PINK,
                            TokenType.CORAL, TokenType.GOLD, TokenType.PURPLE,
                            TokenType.INDIGO, TokenType.TURQUOISE, TokenType.NAVY,
                            TokenType.TEAL, TokenType.FOREST_GREEN, TokenType.SKY_BLUE,
                            TokenType.OLIVE, TokenType.SALMON, TokenType.BEIGE]:
            color_name = token.value
            self.eat(token.type)
            return ColorValue(color_name=color_name)

        elif token.type == TokenType.RGB:
            self.eat(TokenType.RGB)
            self.eat(TokenType.LPAREN)
            r = self.expr()
            self.eat(TokenType.COMMA)
            g = self.expr()
            self.eat(TokenType.COMMA)
            b = self.expr()
            self.eat(TokenType.RPAREN)
            return ColorValue(rgb_values=(r, g, b))

        elif token.type == TokenType.IDENTIFIER:
            var_name = token.value
            self.eat(TokenType.IDENTIFIER)
            return Var(var_name)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        self.error("Invalid factor")

    def var_declaration(self):
        """
        @brief Parses a variable declaration.

        @return A VarDecl node.
        @throws Exception if the type specifier is missing or invalid.
        """
        self.eat(TokenType.VAR)

        valid_types = [
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.BOOL,
            TokenType.STRING_TYPE,
            TokenType.COLOR
        ]

        if self.current_token.type not in valid_types:
            self.error(f"Expected type specifier (int, float, bool, string, color), got {
                       self.current_token.type}")

        var_type = self.current_token.type
        self.eat(var_type)

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ASSIGN)
        init_value = self.expr()
        self.eat(TokenType.SEMICOLON)

        return VarDecl(var_type, var_name, init_value)

    def parse(self):
        """
        @brief Parses the entire token stream into an abstract syntax tree.

        @return A Program node representing the parsed AST.
        """
        return self.program()
