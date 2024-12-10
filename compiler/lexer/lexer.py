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

    def skip_comment(self):
        while self.peek() not in ('\n', None):
            self.advance()

    def get_identifier_or_keyword(self):
        start_pos = self.position - 1
        while self.peek() and (self.peek().isalnum() or self.peek() in ['_']):
            self.advance()
        identifier = self.source_code[start_pos:self.position]

        keywordsWithDots = {
            'cursor',
            'styles',
            'background',
            'presets',
        }
        if identifier in keywordsWithDots:  # fixing issue where special keyword was returned without any dot
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

            # special keywords
            'cursor.': TokenType.CURSOR,
            'status': TokenType.STATUS,  # cursor.status
            'orientation': TokenType.ORIENTATION,
            'move': TokenType.MOVE,
            'position': TokenType.POSITION,
            'styles.': TokenType.STYLES,
            'thickness': TokenType.THICKNESS,  # cursor.styles.thickness
            'color': TokenType.COLOR,  # cursor.color, background.color
            'background.': TokenType.BACKGROUND,
            'path': TokenType.PATH,
            'preset.': TokenType.PRESET,
            'square': TokenType.SQUARE,  # preset.square
            'rectangle': TokenType.RECTANGLE,
            'star': TokenType.STAR,
            'circle': TokenType.CIRCLE,
            'triangle': TokenType.TRIANGLE,
        }

        if identifier in keywords:
            return keywords[identifier], identifier

        return TokenType.IDENTIFIER, identifier

    def get_number(self):  # handling numbers, finds out if it's an int or a float
        start_pos = self.position - 1
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            self.advance()
        number = self.source_code[start_pos:self.position]
        if '.' in number:
            return TokenType.NUMBER, float(number)
        else:
            return TokenType.NUMBER, int(number)

    def tokenize(self):
        tokens = []
        current_char = self.advance()

        while current_char is not None:
            if current_char in ' \t\n\r':  # ignore spaces
                self.skip_whitespace()
                current_char = self.advance()
                continue

            if current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON, current_char, self.line, self.column))
                self.skip_comment()

            elif current_char.isalpha() or current_char == '_':
                token_type, value = self.get_identifier_or_keyword()
                tokens.append(Token(token_type, value, self.line, self.column))

            elif current_char.isdigit():
                token_type, value = self.get_number()
                tokens.append(Token(token_type, value, self.line, self.column))

            elif current_char in ["+", "-", "*", "/", "%", "<", ">", "=", "!"]:
                next_char = self.peek()
                self.advance()
                if next_char == ' ':  # handle single char case
                    tokens.append(Token(TokenType(current_char), current_char, self.line, self.column))

                elif next_char == "=":
                    tokens.append(
                        Token(TokenType(current_char + next_char), current_char + next_char, self.line, self.column))
                else:
                    raise ValueError(
                        f"Unexpected operator '{current_char, next_char}' at line {self.line}, column {self.column}")

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
    const int x = 10 * 2;
    if (1){
        cursor.styles.thickness(10);
    };
    ; this comment will be ignored
    x += 5.5;
    """
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()