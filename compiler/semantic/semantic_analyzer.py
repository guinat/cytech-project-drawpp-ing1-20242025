from compiler.lexer.tokens import TokenType


class SemanticError(Exception):
    """
    @brief Custom exception for semantic errors during analysis.
    """
    pass


class SymbolTable:
    """
    @brief Represents a symbol table for storing variable and cursor declarations.
    """

    def __init__(self):
        """
        @brief Initializes the symbol table.
        """
        self.symbols = {}
        self.cursors = {}

    def define(self, name, type_):
        """
        @brief Adds a new variable to the symbol table.

        @param name Name of the variable.
        @param type_ Type of the variable.
        @throws SemanticError if the identifier is already declared.
        """
        if name in self.symbols or name in self.cursors:
            raise SemanticError(f"Identifier {name} already declared")
        self.symbols[name] = type_

    def define_cursor(self, name):
        """
        @brief Adds a new cursor to the symbol table.

        @param name Name of the cursor.
        @throws SemanticError if the identifier is already declared.
        """
        if name in self.symbols or name in self.cursors:
            raise SemanticError(f"Identifier {name} already declared")
        self.cursors[name] = True

    def lookup(self, name):
        """
        @brief Looks up a variable in the symbol table.

        @param name Name of the variable.
        @return The type of the variable, or None if not found.
        """
        return self.symbols.get(name)

    def is_cursor(self, name):
        """
        @brief Checks if a name refers to a cursor.

        @param name Name to check.
        @return True if the name is a cursor, False otherwise.
        """
        return name in self.cursors


class SemanticAnalyzer:
    """
    @brief Performs semantic analysis on an abstract syntax tree (AST).
    """

    def __init__(self):
        """
        @brief Initializes the semantic analyzer with an empty symbol table.
        """
        self.symbol_table = SymbolTable()

    def visit(self, node):
        """
        @brief Visits a node in the AST and delegates to the appropriate method.

        @param node The AST node to visit.
        @return The result of the visit method for the node.
        """
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        @brief Fallback method for visiting unsupported nodes.

        @param node The unsupported AST node.
        @throws SemanticError when no visit method is implemented for the node.
        """
        raise SemanticError(f'No visit method for {type(node)}')

    def check_types(self, from_type, to_type):
        """
        @brief Checks if a value of one type can be assigned to another type.

        @param from_type The type of the value.
        @param to_type The type to which the value is being assigned.
        @return True if the types are compatible, False otherwise.
        """
        if from_type == to_type:
            return True

        if to_type == TokenType.NUMBER and from_type in [TokenType.INT, TokenType.FLOAT]:
            return True

        if from_type == TokenType.INT and to_type == TokenType.FLOAT:
            return True

        if from_type == TokenType.STRING and to_type == TokenType.STRING_TYPE:
            return True

        if from_type == TokenType.BOOL_VALUE and to_type == TokenType.BOOL:
            return True

        return False

    def check_cursor_method(self, cursor_name, method_name):
        """
        @brief Validates a cursor method and retrieves its parameter types.

        @param cursor_name The name of the cursor.
        @param method_name The name of the method.
        @return A list of expected parameter types for the method.
        @throws SemanticError if the method is invalid or the cursor is undefined.
        """
        if not self.symbol_table.is_cursor(cursor_name):
            raise SemanticError(f"Identifier {cursor_name} is not a cursor")

        valid_methods = {
            'move': [TokenType.NUMBER],
            'rotate': [TokenType.NUMBER],
            'color': [TokenType.COLOR],
            'thickness': [TokenType.NUMBER],
            'visible': [TokenType.BOOL_VALUE],
            'draw_line': [TokenType.NUMBER],
            'draw_rectangle': [TokenType.NUMBER, TokenType.NUMBER, TokenType.BOOL_VALUE],
            'draw_circle': [TokenType.NUMBER, TokenType.BOOL_VALUE],
            'draw_triangle': [TokenType.NUMBER, TokenType.NUMBER, TokenType.BOOL_VALUE],
            'draw_ellipse': [TokenType.NUMBER, TokenType.NUMBER, TokenType.BOOL_VALUE]
        }

        if method_name not in valid_methods:
            raise SemanticError(f"Invalid cursor method: {method_name}")

        return valid_methods[method_name]

    def visit_Program(self, node):
        """
        @brief Visits a program node and analyzes all statements.

        @param node The program node.
        """
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDecl(self, node):
        """
        @brief Visits a variable declaration node.

        @param node The variable declaration node.
        @throws SemanticError if the variable is already declared or if there is a type mismatch.
        """
        if self.symbol_table.lookup(node.name):
            raise SemanticError(f"Variable {node.name} already declared")

        self.symbol_table.define(node.name, node.var_type)

        if node.init_value:
            init_type = self.visit(node.init_value)
            if not self.check_types(init_type, node.var_type):
                raise SemanticError(
                    f"Type mismatch in initialization of {node.name}")

    def visit_Assign(self, node):
        """
        @brief Visits an assignment node.

        @param node The assignment node.
        @throws SemanticError if the variable is not declared or if there is a type mismatch.
        """
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")

        expr_type = self.visit(node.value)
        if not self.check_types(expr_type, var_type):
            raise SemanticError(f"Type mismatch in assignment to {node.name}")

    def visit_CursorCreation(self, node):
        """
        @brief Visits a cursor creation node.

        @param node The cursor creation node.
        @throws SemanticError if the cursor coordinates are not numeric.
        """
        self.symbol_table.define_cursor(node.name)
        x_type = self.visit(node.x)
        y_type = self.visit(node.y)
        if not (x_type in [TokenType.INT, TokenType.FLOAT] and y_type in [TokenType.INT, TokenType.FLOAT]):
            raise SemanticError("Cursor coordinates must be numeric")

    def visit_CursorMethod(self, node):
        """
        @brief Visits a cursor method node.

        @param node The cursor method node.
        @throws SemanticError if the parameters do not match the expected types.
        """
        expected_param_types = self.check_cursor_method(
            node.cursor_name, node.method_name)
        if len(node.params) != len(expected_param_types):
            raise SemanticError(f"Method {node.method_name} expects {
                                len(expected_param_types)} parameters")

        for param, expected_type in zip(node.params, expected_param_types):
            param_type = self.visit(param)
            if not self.check_types(param_type, expected_type):
                raise SemanticError(f"Invalid parameter type for method {
                                    node.method_name}")

    def visit_DrawCommand(self, node):
        """
        @brief Visits a draw command node.

        @param node The draw command node.
        @throws SemanticError if the parameters do not match the expected types.
        """
        expected_param_types = self.check_cursor_method(
            node.cursor_name, node.shape_type)
        if len(node.params) != len(expected_param_types):
            raise SemanticError(f"Shape {node.shape_type} expects {
                                len(expected_param_types)} parameters")

        for param, expected_type in zip(node.params, expected_param_types):
            param_type = self.visit(param)
            if not self.check_types(param_type, expected_type):
                raise SemanticError(
                    f"Invalid parameter type for shape {node.shape_type}")

    def visit_BinOp(self, node):
        """
        @brief Visits a binary operation node.

        @param node The binary operation node.
        @return The resulting type of the operation.
        @throws SemanticError if the operand types are invalid.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.op in [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.SLASH, TokenType.MODULO]:
            if left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]:
                return TokenType.FLOAT if TokenType.FLOAT in [left_type, right_type] else TokenType.INT
            raise SemanticError(f"Invalid operand types for arithmetic operation: {
                                left_type} and {right_type}")

        elif node.op in [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL]:

            if (left_type == right_type) \
                    or (left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]) \
                    or ((left_type == TokenType.BOOL and right_type == TokenType.BOOL_VALUE) or
                        (left_type == TokenType.BOOL_VALUE and right_type == TokenType.BOOL)):
                return TokenType.BOOL_VALUE

            raise SemanticError(f"Invalid operand types for comparison: {
                                left_type} and {right_type}")

        raise SemanticError(f"Unknown binary operator {node.op}")

    def visit_If(self, node):
        """
        @brief Visits an if-statement node.

        @param node The if-statement node.
        @throws SemanticError if the condition is not boolean.
        """
        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL_VALUE:
            raise SemanticError("If condition must be boolean")

        for stmt in node.true_body:
            self.visit(stmt)

        if node.elif_bodies:
            for elif_condition, elif_body in node.elif_bodies:
                elif_condition_type = self.visit(elif_condition)
                if elif_condition_type != TokenType.BOOL_VALUE:
                    raise SemanticError("Elif condition must be boolean")
                for stmt in elif_body:
                    self.visit(stmt)

        if node.false_body:
            for stmt in node.false_body:
                self.visit(stmt)

    def visit_While(self, node):
        """
        @brief Visits a while-loop node.

        @param node The while-loop node.
        @throws SemanticError if the condition is not boolean.
        """
        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL_VALUE:
            raise SemanticError("While condition must be boolean")

        for stmt in node.body:
            self.visit(stmt)

    def visit_For(self, node):
        """
        @brief Visits a for-loop node.

        @param node The for-loop node.
        @throws SemanticError if the condition is not boolean.
        """
        self.visit(node.init)

        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL_VALUE:
            raise SemanticError("For condition must be boolean")

        self.visit(node.update)

        for stmt in node.body:
            self.visit(stmt)

    def visit_Num(self, node):
        """
        @brief Visits a numeric literal node.

        @param node The numeric literal node.
        @return TokenType.FLOAT if the value is a float, TokenType.INT otherwise.
        """
        return TokenType.FLOAT if isinstance(node.value, float) else TokenType.INT

    def visit_StringLiteral(self, node):
        """
        @brief Visits a string literal node.

        @param node The string literal node.
        @return TokenType.STRING.
        """
        return TokenType.STRING

    def visit_BooleanLiteral(self, node):
        """
        @brief Visits a boolean literal node.

        @param node The boolean literal node.
        @return TokenType.BOOL_VALUE.
        """
        return TokenType.BOOL_VALUE

    def visit_ColorValue(self, node):
        """
        @brief Visits a color value node.

        @param node The color value node.
        @return TokenType.COLOR.
        @throws SemanticError if RGB values are not numeric.
        """
        if node.color_name:
            return TokenType.COLOR
        if node.rgb_values:
            for value in node.rgb_values:
                value_type = self.visit(value)
                if value_type not in [TokenType.INT, TokenType.FLOAT]:
                    raise SemanticError("RGB values must be numeric")
        return TokenType.COLOR

    def visit_Var(self, node):
        """
        @brief Visits a variable reference node.

        @param node The variable reference node.
        @return The type of the variable.
        @throws SemanticError if the variable is not declared.
        """
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")
        return var_type


def analyze(ast):
    """
    @brief Performs semantic analysis on the provided AST.

    @param ast The abstract syntax tree to analyze.
    @return Tuple (bool, str): (True, None) if successful, (False, error message) if an error occurs.
    """
    analyzer = SemanticAnalyzer()
    try:
        analyzer.visit(ast)
        return True, None
    except SemanticError as e:
        return False, str(e)