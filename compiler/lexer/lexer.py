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
        return self.current_char

    def peek(self):
        peek_pos = self.position
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()
            self.advance()
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()

    def get_identifier(self):
        # Lis un identificateur simple (sans point)
        identifier = ''
        start_column = self.column

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()

        return identifier

    def get_number(self):
        number = ''
        decimal_points = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                decimal_points += 1
                if decimal_points > 1:
                    raise ValueError(f"Invalid number format at line {self.line}, column {self.column}")
            number += self.current_char
            self.advance()

        if decimal_points == 0:
            return TokenType.NUMBER, int(number)
        return TokenType.NUMBER, float(number)

    def get_string(self):
        string = ''
        self.advance()

        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()

        if self.current_char != '"':
            raise ValueError(f"Unterminated string at line {self.line}, column {self.column}")

        self.advance()
        return TokenType.STRING, string

    def get_operator(self):
        current_char = self.current_char
        column = self.column
        self.advance()

        if self.current_char == '=':
            operator = current_char + '='
            operators = {
                '+=': TokenType.PLUS_EQUAL,
                '-=': TokenType.MINUS_EQUAL,
                '*=': TokenType.STAR_EQUAL,
                '/=': TokenType.SLASH_EQUAL,
                '==': TokenType.EQUAL_EQUAL,
                '!=': TokenType.NOT_EQUAL,
                '<=': TokenType.LESS_EQUAL,
                '>=': TokenType.GREATER_EQUAL
            }
            self.advance()
            return operators.get(operator), operator

        operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '/': TokenType.SLASH,
            '%': TokenType.MODULO,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '=': TokenType.ASSIGN
        }
        return operators.get(current_char), current_char

    def tokenize(self):
        tokens = []

        # Mots-clés sans point
        keywords = {
            # Types de base
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'string': TokenType.STRING_TYPE,
            'bool': TokenType.BOOL,

            # Déclaration
            'var': TokenType.VAR,
            'const': TokenType.CONST,

            # Structures
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,

            # Valeurs de BOOL
            'true': TokenType.BOOL_VALUE,
            'false': TokenType.BOOL_VALUE,

            # Curseur et fenêtre
            'cursor': TokenType.CURSOR,
            'create_cursor': TokenType.CREATE_CURSOR,
            'window': TokenType.WINDOW,
            'clear': TokenType.CLEAR,
            'update': TokenType.UPDATE,

            # Méthodes de curseur color.(..) (sans le point)
            'color': TokenType.COLOR,
            'thickness': TokenType.THICKNESS,
            'move': TokenType.MOVE,
            'rotate': TokenType.ROTATE,
            'visible': TokenType.VISIBLE,
            'draw_line': TokenType.DRAW_LINE,
            'draw_rectangle': TokenType.DRAW_RECTANGLE,
            'draw_circle': TokenType.DRAW_CIRCLE,
            'draw_triangle': TokenType.DRAW_TRIANGLE,
            'draw_ellipse': TokenType.DRAW_ELLIPSE,

            'rgb': TokenType.RGB,

            # Couleurs
            'RED': TokenType.RED,
            'GREEN': TokenType.GREEN,
            'BLUE': TokenType.BLUE,
            'BLACK': TokenType.BLACK,
            'WHITE': TokenType.WHITE,
            'GRAY': TokenType.GRAY,
            'ORANGE': TokenType.ORANGE,
            'PURPLE': TokenType.PURPLE
            #TODO : Ajouter les autres couleurs


        }

        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue

            if self.current_char == '/':
                next_char = self.peek()
                if next_char in ['/', '*']:
                    self.skip_comment()
                    continue

            if self.current_char.isalpha() or self.current_char == '_':
                # Lis un identificateur simple
                start_line = self.line
                start_column = self.column
                ident = self.get_identifier()

                # Vérifie si c'est un mot-clé
                token_type = keywords.get(ident, TokenType.IDENTIFIER)
                tokens.append(Token(token_type, ident, start_line, start_column))

                # Si le prochain char est un point, on l'émet en token séparé
                while self.current_char == '.':
                    dot_line = self.line
                    dot_col = self.column
                    self.advance()
                    tokens.append(Token(TokenType.DOT, '.', dot_line, dot_col))

                    # Lit le nouvel identificateur après le point
                    if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
                        method_line = self.line
                        method_col = self.column
                        method_ident = self.get_identifier()
                        method_token_type = keywords.get(method_ident, TokenType.IDENTIFIER)
                        tokens.append(Token(method_token_type, method_ident, method_line, method_col))
                    else:
                        raise ValueError(f"Unexpected character after '.' at line {self.line}, column {self.column}")
                continue

            if self.current_char.isdigit():
                start_line = self.line
                start_column = self.column
                token_type, value = self.get_number()
                tokens.append(Token(token_type, value, start_line, start_column))
                continue

            if self.current_char == '"':
                start_line = self.line
                start_column = self.column
                token_type, value = self.get_string()
                tokens.append(Token(token_type, value, start_line, start_column))
                continue

            if self.current_char in '+-*/<>=!':
                start_line = self.line
                start_column = self.column
                token_type, value = self.get_operator()
                if token_type:
                    tokens.append(Token(token_type, value, start_line, start_column))
                    continue

            delimiters = {
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE
            }

            if self.current_char in delimiters:
                start_line = self.line
                start_column = self.column
                token_type = delimiters[self.current_char]
                tokens.append(Token(token_type, self.current_char, start_line, start_column))
                self.advance()
                continue

            raise ValueError(f"Unexpected character '{self.current_char}' at line {self.line}, column {self.column}")

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens

def main():
    source_code = """
    var int width = 800;
    var float angle = 45.0;
    var string message = "Hello Draw++";
    var bool isDrawing = true;

    cursor main = create_cursor(400, 300);
    main.color(RED);
    main.thickness(2);

    if (isDrawing == true) {
        main.visible(true);
        main.draw_rectangle(60, 40, true);
    } elif (width > 500) {
        main.draw_circle(30, false);
    } else {
        window.clear();
    };

    for (var int i = 0; i < 4; i += 1) {
        main.rotate(90);
        main.move(100);
    };
    """

    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print("=== Tokens générés ===")
        for token in tokens:
            print(token)

    except ValueError as e:
        print(f"Erreur lors de l'analyse lexicale : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
