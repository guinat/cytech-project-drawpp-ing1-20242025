class ASTNode:
    """
    @brief Base class for all nodes in the abstract syntax tree (AST).
    """
    def __init__(self):
        pass

class Program(ASTNode):
    """
    @brief Represents the root node of a program in the AST.

    @param statements List of statements in the program.
    """
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def __str__(self):
        return f"Program({self.statements})"

class VarDecl(ASTNode):
    """
    @brief Represents a variable declaration in the AST.

    @param var_type Type of the variable.
    @param name Name of the variable.
    @param init_value Initial value assigned to the variable (optional).
    """
    def __init__(self, var_type, name, init_value=None):
        super().__init__()
        self.var_type = var_type
        self.name = name
        self.init_value = init_value

    def __str__(self):
        return f"VarDecl({self.var_type}, {self.name}, {self.init_value})"

class Assign(ASTNode):
    """
    @brief Represents an assignment operation in the AST.

    @param name Name of the variable being assigned.
    @param value Value being assigned to the variable.
    """
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return f"Assign({self.name}, {self.value})"

class CursorCreation(ASTNode):
    """
    @brief Represents the creation of a cursor in the AST.

    @param name Name of the cursor.
    @param x X-coordinate of the cursor.
    @param y Y-coordinate of the cursor.
    """
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return f"CursorCreation({self.name}, {self.x}, {self.y})"

class CursorMethod(ASTNode):
    """
    @brief Represents a method call on a cursor in the AST.

    @param cursor_name Name of the cursor.
    @param method_name Name of the method being called.
    @param params List of parameters passed to the method.
    """
    def __init__(self, cursor_name, method_name, params):
        super().__init__()
        self.cursor_name = cursor_name
        self.method_name = method_name
        self.params = params

    def __str__(self):
        return f"CursorMethod({self.cursor_name}, {self.method_name}, {self.params})"

class DrawCommand(ASTNode):
    """
    @brief Represents a draw command in the AST.

    @param cursor_name Name of the cursor used for drawing.
    @param shape_type Type of shape to draw.
    @param params List of parameters for the draw command.
    """
    def __init__(self, cursor_name, shape_type, params):
        super().__init__()
        self.cursor_name = cursor_name
        self.shape_type = shape_type
        self.params = params

    def __str__(self):
        return f"DrawCommand({self.cursor_name}, {self.shape_type}, {self.params})"

class WindowCommand(ASTNode):
    """
    @brief Represents a window-related command in the AST.

    @param command Command to execute (e.g., clear or update).
    """
    def __init__(self, command):
        super().__init__()
        self.command = command

    def __str__(self):
        return f"WindowCommand({self.command})"

class If(ASTNode):
    """
    @brief Represents an if-statement in the AST.

    @param condition The condition to evaluate.
    @param true_body List of statements to execute if the condition is true.
    @param elif_bodies Optional list of elif conditions and their bodies.
    @param false_body Optional list of statements to execute if all conditions are false.
    """
    def __init__(self, condition, true_body, elif_bodies=None, false_body=None):
        super().__init__()
        self.condition = condition
        self.true_body = true_body
        self.elif_bodies = elif_bodies or []
        self.false_body = false_body

    def __str__(self):
        return f"If({self.condition}, {self.true_body}, elif={self.elif_bodies}, else={self.false_body})"

class While(ASTNode):
    """
    @brief Represents a while-loop in the AST.

    @param condition The condition to evaluate.
    @param body List of statements to execute in the loop.
    """
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        return f"While({self.condition}, {self.body})"

class For(ASTNode):
    """
    @brief Represents a for-loop in the AST.

    @param init Initialization statement.
    @param condition The condition to evaluate.
    @param update Update statement after each iteration.
    @param body List of statements to execute in the loop.
    """
    def __init__(self, init, condition, update, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __str__(self):
        return f"For({self.init}, {self.condition}, {self.update}, {self.body})"

class BinOp(ASTNode):
    """
    @brief Represents a binary operation in the AST.

    @param left Left operand.
    @param op Operator.
    @param right Right operand.
    """
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Num(ASTNode):
    """
    @brief Represents a numeric literal in the AST.

    @param value The numeric value.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Num({self.value})"

class StringLiteral(ASTNode):
    """
    @brief Represents a string literal in the AST.

    @param value The string value.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"String({self.value})"

class BooleanLiteral(ASTNode):
    """
    @brief Represents a boolean literal in the AST.

    @param value The boolean value.
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"Boolean({self.value})"

class ColorValue(ASTNode):
    """
    @brief Represents a color value in the AST.

    @param color_name Optional name of the color.
    @param rgb_values Optional tuple of RGB values.
    """
    def __init__(self, color_name=None, rgb_values=None):
        super().__init__()
        self.color_name = color_name
        self.rgb_values = rgb_values

    def __str__(self):
        if self.color_name:
            return f"Color({self.color_name})"
        return f"Color(rgb{self.rgb_values})"

class Var(ASTNode):
    """
    @brief Represents a variable reference in the AST.

    @param name Name of the variable.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Var({self.name})"
