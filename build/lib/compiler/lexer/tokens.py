from enum import Enum, auto

class TokenType(Enum):
    """
    @brief Enum representing different types of tokens in draw++.
    """

    # Identifiers and literals
    IDENTIFIER = auto()  # Variable names
    NUMBER = auto()  # Integers and floats
    STRING = auto()  # String literals
    BOOL_VALUE = auto()  # true/false

    # Types
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING_TYPE = auto()
    COLOR = auto()

    # Declaration keywords
    VAR = auto()
    CONST = auto()

    # Control flow keywords
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()

    # Cursor-related keywords
    CURSOR = auto()
    CREATE_CURSOR = auto()
    MOVE = auto()
    ROTATE = auto()
    POSITION = auto()
    THICKNESS = auto()
    VISIBLE = auto()

    # Shape-related keywords
    DRAW_LINE = auto()
    DRAW_RECTANGLE = auto()
    DRAW_CIRCLE = auto()
    DRAW_TRIANGLE = auto()
    DRAW_ELLIPSE = auto()

    # Window-related keywords
    WINDOW = auto()
    CLEAR = auto()
    UPDATE = auto()

    # Color values
    RGB = auto()

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
    ASSIGN = "="
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Comments
    COMMENT = auto()  # Single-line comment //
    MULTILINE_COMMENT = auto()  # Multi-line comment /* */

    # End of file
    EOF = auto()

class Token:
    """
    @brief Class representing a token in the source code.
    """
    def __init__(self, type, value=None, line=0, column=0):
        """
        @brief Initializes a Token instance.

        @param type The type of the token (from TokenType).
        @param value The value of the token (optional).
        @param line The line number where the token is located (default: 0).
        @param column The column number where the token is located (default: 0).
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        """
        @brief Returns a string representation of the token.

        @return A string in the format "Token(type, value, line, column)".
        """
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"
