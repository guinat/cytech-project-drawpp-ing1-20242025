from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()

    IF = auto()
    ELSE = auto()
    WHILE = auto()

    IDENTIFIER = auto()
    NUMBER = auto()

    ASSIGN = auto()  # =
    PLUS = auto()  # +
    MINUS = auto()  # -
    MULTIPLY = auto()  # *
    DIVIDE = auto()  # /
    EQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    GT = auto()  # >
    LTE = auto()  # <=
    GTE = auto()  # >=

    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,

    EOF = auto()


class Token:
    def __init__(self, type, value=None, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, column={self.column})"
