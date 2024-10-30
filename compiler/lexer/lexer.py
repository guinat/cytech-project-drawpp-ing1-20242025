from tokens import Token, TokenType

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 0

    def advance(self):
        if self.position < len(self.source_code):
            char = self.source_code[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 0
            else:
                self.column += 1
            return char
        return None

    def peek(self):
        if self.position < len(self.source_code):
            return self.source_code[self.position]
        return None

    def skip_whitespace(self):
        while self.peek() is not None and self.peek() in ' \t\n\r':
            self.advance()

    def get_identifier_or_keyword(self):
        start_pos = self.position - 1
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            self.advance()
        identifier = self.source_code[start_pos:self.position]
        keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'bool': TokenType.BOOL,
            'string': TokenType.STRING
        }
        return keywords.get(identifier, TokenType.IDENTIFIER), identifier

    def get_number(self):
        start_pos = self.position - 1
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            self.advance()
        number = self.source_code[start_pos:self.position]
        return TokenType.NUMBER, float(number) if '.' in number else int(number)

    def tokenize(self):
        tokens = []
        current_char = self.advance()

        while current_char is not None:
            if current_char in ' \t\n\r':
                self.skip_whitespace()
                current_char = self.advance()
                continue

            if current_char.isalpha() or current_char == '_':
                token_type, value = self.get_identifier_or_keyword()
                tokens.append(Token(token_type, value, self.line, self.column))

            elif current_char.isdigit():
                token_type, value = self.get_number()
                tokens.append(Token(token_type, value, self.line, self.column))

            elif current_char == '+':
                tokens.append(Token(TokenType.PLUS, current_char, self.line, self.column))
            elif current_char == '-':
                tokens.append(Token(TokenType.MINUS, current_char, self.line, self.column))
            elif current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.EQ, '==', self.line, self.column))
                else:
                    tokens.append(Token(TokenType.ASSIGN, current_char, self.line, self.column))

            elif current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.LTE, '<=', self.line, self.column))
                else:
                    tokens.append(Token(TokenType.LT, current_char, self.line, self.column))
            elif current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.GTE, '>=', self.line, self.column))
                else:
                    tokens.append(Token(TokenType.GT, current_char, self.line, self.column))
            elif current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    tokens.append(Token(TokenType.NEQ, '!=', self.line, self.column))
                else:
                    raise ValueError(f"Unexpected character '{current_char}' at line {self.line}, column {self.column}")

            elif current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON, current_char, self.line, self.column))
            elif current_char == '(':
                tokens.append(Token(TokenType.LPAREN, current_char, self.line, self.column))
            elif current_char == ')':
                tokens.append(Token(TokenType.RPAREN, current_char, self.line, self.column))
            elif current_char == '{':
                tokens.append(Token(TokenType.LBRACE, current_char, self.line, self.column))
            elif current_char == '}':
                tokens.append(Token(TokenType.RBRACE, current_char, self.line, self.column))

            else:
                raise ValueError(f"Unexpected character '{current_char}' at line {self.line}, column {self.column}")

            current_char = self.advance()

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens


def main():
    source_code = """
    int x = 10;
    float y = 20.5;
    if (x < y) {
        x = x + 1;
    }
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
