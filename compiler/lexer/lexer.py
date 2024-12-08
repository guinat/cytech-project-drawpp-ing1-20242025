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

    def peek(self):
        peek_pos = self.position
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        # Single-line comments
        if self.current_char == '/' and self.peek() == '/':
            self.advance()  # Skip first '/'
            self.advance()  # Skip second '/'
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.advance()
            return True
        # Multi-line comments
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()  # Skip '/'
            self.advance()  # Skip '*'
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # Skip '*'
                    self.advance()  # Skip '/'
                    return True
                self.advance()
            return True
        return False

    def get_number(self):
        start_pos = self.position - 1
        decimal_point_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break
            self.advance()

        number = self.source_code[start_pos:self.position]
        if '.' in number:
            return Token(TokenType.NUMBER, float(number), self.line, self.column)
        else:
            return Token(TokenType.NUMBER, int(number), self.line, self.column)

    def get_identifier_or_keyword(self):
        start_pos = self.position - 1
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        identifier = self.source_code[start_pos:self.position]

        keywords_with_dots = {
            'cursor.',
            'styles.',
            'background.',
            'preset.',
        }

        if identifier in keywords_with_dots:
            identifier += self.source_code[self.position]
            self.advance()

        keywords = {
            'const': TokenType.CONST,
            'var': TokenType.VAR,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'elif': TokenType.ELIF,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING_TYPE,
            'bool': TokenType.BOOL,
            'cursor.': TokenType.CURSOR,
            'styles.': TokenType.STYLES,
            'background.': TokenType.BACKGROUND,
            'preset.': TokenType.PRESET,
        }

        if identifier in keywords:
            return Token(keywords[identifier], identifier, self.line, self.column)
        return Token(TokenType.IDENTIFIER, identifier, self.line, self.column)

    def tokenize(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/':
                if self.skip_comment():
                    continue

            if self.current_char.isdigit():
                tokens.append(self.get_number())
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                tokens.append(self.get_identifier_or_keyword())
                continue

            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }

            if self.current_char in single_char_tokens:
                tokens.append(Token(single_char_tokens[self.current_char], self.current_char, self.line, self.column))
                self.advance()
                continue

            raise ValueError(f"Unexpected character '{self.current_char}' at line {self.line}, column {self.column}")

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
