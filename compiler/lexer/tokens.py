from enum import Enum, auto

class TokenType(Enum):
    # auto() is assigning an id to each token.type

    IDENTIFIER = auto() # variables names
    NUMBER = auto() # ints and floats

    # keywords
    CONST = auto() # "const"
    VAR = auto() # "var"
    IF = auto() # "if"
    ELSE = auto() # "else"
    ELIF = auto() # "elif"
    FOR = auto() # "for"
    WHILE = auto() # "while"
    INT = auto() # "int"
    FLOAT = auto() # "float"
    STRING_TYPE = auto() # "string"
    BOOL = auto() # "bool"

    # special keywords
    CURSOR = auto() # "cursor."
    STATUS = auto() # "cursor.status()"
    ORIENTATION = auto() # "cursor.orientation()"
    MOVE = auto() # "cursor.move()"
    POSITION = auto() # "cursor.position(x, y)"
    STYLES = auto() # "styles."
    THICKNESS = auto() # "cursor.styles.thickness()"
    COLOR = auto() # "cursor.styles.color() or background.color()"
    BACKGROUND = auto() # "background."
    PATH = auto() # "background.path"
    PRESET = auto() # "preset."
    SQUARE = auto() # "preset.square(,)"
    RECTANGLE = auto()
    STAR = auto()
    CIRCLE = auto()
    TRIANGLE = auto()

    # comparing operators
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="

    # math operators
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    SLASH = "/"
    MODULO = "%"
    PLUS_EQUAL = "+="
    MINUS_EQUAL = "-="
    STAR_EQUAL = "*="
    SLASH_EQUAL = "/="

    # signs
    ASSIGN = "="
    SEMICOLON = ";"
    COMMA = ","
    DOT = "." 
    LPAREN = "(" 
    RPAREN = ")"
    LBRACE = "{" 
    RBRACE = "}"

    EOF = auto()


class Token:
    def __init__(self, type, value=None, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"
