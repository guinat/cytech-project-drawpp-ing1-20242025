class ASTNode:
    def __init__(self):
        pass

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def __str__(self):
        return f"Program({self.statements})"

# Declarations et assignations
class VarDecl(ASTNode):
    def __init__(self, var_type, name, init_value=None):
        super().__init__()
        self.var_type = var_type
        self.name = name
        self.init_value = init_value

    def __str__(self):
        return f"VarDecl({self.var_type}, {self.name}, {self.init_value})"

class Assign(ASTNode):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f"Assign({self.name}, {self.value})"

# Curseur et méthodes
class CursorCreation(ASTNode):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return f"CursorCreation({self.name}, {self.x}, {self.y})"

class CursorMethod(ASTNode):
    def __init__(self, cursor_name, method_name, params):
        super().__init__()
        self.cursor_name = cursor_name
        self.method_name = method_name
        self.params = params

    def __str__(self):
        return f"CursorMethod({self.cursor_name}, {self.method_name}, {self.params})"

class DrawCommand(ASTNode):
    def __init__(self, cursor_name, shape_type, params):
        super().__init__()
        self.cursor_name = cursor_name
        self.shape_type = shape_type
        self.params = params

    def __str__(self):
        return f"DrawCommand({self.cursor_name}, {self.shape_type}, {self.params})"

# Window commands
class WindowCommand(ASTNode):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def __str__(self):
        return f"WindowCommand({self.command})"

# Structures de contrôle
class If(ASTNode):
    def __init__(self, condition, true_body, elif_bodies=None, false_body=None):
        super().__init__()
        self.condition = condition
        self.true_body = true_body
        self.elif_bodies = elif_bodies or []  # Liste de tuples (condition, body)
        self.false_body = false_body

    def __str__(self):
        return f"If({self.condition}, {self.true_body}, elif={self.elif_bodies}, else={self.false_body})"

class While(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition}, {self.body})"

class For(ASTNode):
    def __init__(self, init, condition, update, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __str__(self):
        return f"For({self.init}, {self.condition}, {self.update}, {self.body})"

# Expressions et opérations
class BinOp(ASTNode):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

# Valeurs et littéraux
class Num(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Num({self.value})"

class StringLiteral(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"String({self.value})"

class BooleanLiteral(ASTNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Boolean({self.value})"

class ColorValue(ASTNode):
    def __init__(self, color_name=None, rgb_values=None):
        super().__init__()
        self.color_name = color_name
        self.rgb_values = rgb_values

    def __str__(self):
        if self.color_name:
            return f"Color({self.color_name})"
        return f"Color(rgb{self.rgb_values})"

class Var(ASTNode):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Var({self.name})"