from compiler.lexer.tokens import Token, TokenType

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 0
        self.current_char = None
        self.advance()

    def advance(self):
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
            self.position += 1
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            else:
                self.column += 1
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # Commentaire sur une ligne
        if self.current_char == '/' and self.peek() == '/':
            self.advance()  # Passer le premier /
            self.advance()  # Passer le deuxième /
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.advance()
            return True
        # Commentaire multi-lignes
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()  # Passer le /
            self.advance()  # Passer le *
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # Passer le *
                    self.advance()  # Passer le /
                    return True
                self.advance()
            return True
        return False

    def peek(self):
        peek_pos = self.position
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def get_number(self):
        result = ''
        decimal_point_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break
            result += self.current_char
            self.advance()

        if decimal_point_count == 0:
            return Token(TokenType.NUMBER, int(result), self.line, self.column)
        else:
            return Token(TokenType.NUMBER, float(result), self.line, self.column)

    def get_identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'bool': TokenType.BOOL,
            'string': TokenType.STRING,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE
        }

        token_type = keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result, self.line, self.column)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/':
                if self.skip_comment():
                    continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, '==', self.line, self.column)
                return Token(TokenType.ASSIGN, '=', self.line, self.column)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, '<=', self.line, self.column)
                return Token(TokenType.LT, '<', self.line, self.column)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, '>=', self.line, self.column)
                return Token(TokenType.GT, '>', self.line, self.column)

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NEQ, '!=', self.line, self.column)
                raise ValueError(f"Unexpected '!' at line {self.line}, column {self.column}")

            # Single-character tokens
            char_to_token = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA
            }

            if self.current_char in char_to_token:
                char = self.current_char
                self.advance()
                return Token(char_to_token[char], char, self.line, self.column)

            raise ValueError(f"Invalid character '{self.current_char}' at line {self.line}, column {self.column}")

        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens