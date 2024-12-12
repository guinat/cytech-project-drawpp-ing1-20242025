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

    def peek(self):
        peek_pos = self.pos + 1
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None

    def is_cursor_method_type(self, ttype):
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
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
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

        elif token.type == TokenType.WINDOW:
            # window statement (window.clear(), window.update())
            return self.window_statement()

        # Méthodes sans "window" au début, ex : "clear()", "update()" seuls
        elif token.type in [TokenType.CLEAR, TokenType.UPDATE]:
            return self.window_statement()

        elif token.type == TokenType.IDENTIFIER:
            return self.identifier_statement()

        else:
            self.error(f"Unexpected token {token.type} in statement")

    def identifier_statement(self):
        # On a lu un IDENTIFIER, plusieurs cas :
        # 1. IDENTIFIER '=' ... => assignation
        # 2. IDENTIFIER '+=' etc. => assignation
        # 3. IDENTIFIER '.' IDENTIFIER(...) => appel méthode curseur ou fenêtre
        # Sinon erreur
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        # Vérifie si on a un "." -> appel de méthode
        if self.current_token.type == TokenType.DOT:
            self.eat(TokenType.DOT)
            # Après le ".", on doit avoir un token de type méthode ou commande
            method_token = self.current_token
            if method_token.type in [TokenType.CLEAR, TokenType.UPDATE]:
                # window.clear() ou window.update() style
                # mais on est dans identifier_statement donc name != 'window'
                # On le gére comme un window_statement si name = "window"
                if name == 'window':
                    return self.window_call(method_token)
                else:
                    self.error("Invalid window method call on non-window identifier")
            elif self.is_cursor_method_type(method_token.type):
                # Appel méthode curseur
                method_name = method_token.value
                self.eat(method_token.type)
                return self.cursor_method_statement(name, method_name)
            else:
                self.error("Expected a known method after '.'")

        # Sinon c'est une assignation
        elif self.current_token.type in [TokenType.ASSIGN, TokenType.PLUS_EQUAL,
                                         TokenType.MINUS_EQUAL, TokenType.STAR_EQUAL,
                                         TokenType.SLASH_EQUAL]:
            return self.assignment_statement(name)
        else:
            self.error("Expected '.' or assignment operator after identifier")

    def cursor_statement(self):
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

    def window_call(self, method_token):
        # Appel de méthode sur 'window'
        self.eat(method_token.type)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return WindowCommand(method_token.value)

    def assignment_statement(self, name, eat_semicolon=True):
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

    def window_statement(self):
        # window CLEAR ou UPDATE (window.clear(), window.update())
        token = self.current_token
        if token.type == TokenType.WINDOW:
            self.eat(TokenType.WINDOW)
            self.eat(TokenType.DOT)
            method_token = self.current_token
            if method_token.type not in [TokenType.CLEAR, TokenType.UPDATE]:
                self.error("Expected 'clear' or 'update' after 'window.'")
            self.eat(method_token.type)
        else:
            # clear() ou update() seuls (même sémantique ?)
            method_token = self.current_token
            self.eat(method_token.type)
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return WindowCommand(method_token.value)

    def if_statement(self):
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
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)

        # Initialisation
        if self.current_token.type == TokenType.VAR:
            init = self.var_declaration()
        else:
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            init = self.assignment_statement(var_name)

        # Condition
        condition = self.bool_expr()
        self.eat(TokenType.SEMICOLON)

        # Update sans point-virgule
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
        node = self.term()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.term())

        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in [TokenType.MULT, TokenType.SLASH, TokenType.MODULO]:
            op = self.current_token.type
            self.eat(op)
            node = BinOp(node, op, self.factor())

        return node

    def factor(self):
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
                            TokenType.ORANGE, TokenType.PURPLE]:
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
        self.eat(TokenType.VAR)

        valid_types = [
            TokenType.INT,
            TokenType.FLOAT,
            TokenType.BOOL,
            TokenType.STRING_TYPE,
            TokenType.COLOR
        ]

        if self.current_token.type not in valid_types:
            self.error(f"Expected type specifier (int, float, bool, string, color), got {self.current_token.type}")

        var_type = self.current_token.type
        self.eat(var_type)

        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.ASSIGN)
        init_value = self.expr()
        self.eat(TokenType.SEMICOLON)

        return VarDecl(var_type, var_name, init_value)

    def parse(self):
        return self.program()
