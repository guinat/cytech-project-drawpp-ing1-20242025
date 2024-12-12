from enum import Enum, auto


class TokenType(Enum):
    # Identifiers and literals
    IDENTIFIER = auto()  # Variable names
    NUMBER = auto()  # Integers and floats
    STRING = auto()  # String literals
    BOOL_VALUE = auto()  # true/false

    # Types
    INT = auto()  # "int"
    FLOAT = auto()  # "float"
    BOOL = auto()  # "bool"
    STRING_TYPE = auto()  # "string"
    COLOR = auto()  # "color"

    # Declaration keywords
    VAR = auto()  # "var"
    CONST = auto()  # "const"

    # Control flow keywords
    IF = auto()  # "if"
    ELIF = auto()  # "elif"
    ELSE = auto()  # "else"
    FOR = auto()  # "for"
    WHILE = auto()  # "while"

    # Cursor-related keywords
    CURSOR = auto()  # "cursor"
    CREATE_CURSOR = auto()  # "create_cursor"
    MOVE = auto()  # "move"
    ROTATE = auto()  # "rotate"
    POSITION = auto()  # "position"
    THICKNESS = auto()  # "thickness"
    VISIBLE = auto()  # "visible"

    # Shape-related keywords
    DRAW_LINE = auto()  # "draw_line"
    DRAW_RECTANGLE = auto()  # "draw_rectangle"
    DRAW_CIRCLE = auto()  # "draw_circle"
    DRAW_TRIANGLE = auto()  # "draw_triangle"
    DRAW_ELLIPSE = auto()  # "draw_ellipse"

    # Window-related keywords
    WINDOW = auto()  # "window"
    CLEAR = auto()  # "clear"
    UPDATE = auto()  # "update"

    # Color values
    RGB = auto()  # "rgb"
    # Predefined colors
    BLACK = auto()
    WHITE = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    GRAY = auto()
    LIGHT_GRAY = auto()
    DARK_GRAY = auto()
    ORANGE = auto()
    BROWN = auto()
    PINK = auto()
    CORAL = auto()
    GOLD = auto()
    PURPLE = auto()
    INDIGO = auto()
    TURQUOISE = auto()
    NAVY = auto()
    TEAL = auto()
    FOREST_GREEN = auto()
    SKY_BLUE = auto()
    OLIVE = auto()
    SALMON = auto()
    BEIGE = auto()
    YELLOW = auto()

    # Operators
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    SLASH = "/"
    MODULO = "%"

    # Compound assignment operators
    PLUS_EQUAL = "+="
    MINUS_EQUAL = "-="
    STAR_EQUAL = "*="
    SLASH_EQUAL = "/="

    # Comparison operators
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="

    # Delimiters
    ASSIGN = "="  # Assignment operator
    SEMICOLON = ";"  # Statement terminator
    COMMA = ","  # Parameter separator
    DOT = "."  # Member access
    LPAREN = "("  # Left parenthesis
    RPAREN = ")"  # Right parenthesis
    LBRACE = "{"  # Left brace
    RBRACE = "}"  # Right brace

    # Comments
    COMMENT = auto()  # Single-line comment //
    MULTILINE_COMMENT = auto()  # Multi-line comment /* */

    # End of file
    EOF = auto()


class Token:
    def __init__(self, type, value=None, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"