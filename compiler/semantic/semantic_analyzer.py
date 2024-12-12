from compiler.lexer.tokens import TokenType

class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.cursors = {}

    def define(self, name, type_):
        if name in self.symbols or name in self.cursors:
            raise SemanticError(f"Identifier {name} already declared")
        self.symbols[name] = type_

    def define_cursor(self, name):
        if name in self.symbols or name in self.cursors:
            raise SemanticError(f"Identifier {name} already declared")
        self.cursors[name] = True

    def lookup(self, name):
        return self.symbols.get(name)

    def is_cursor(self, name):
        return name in self.cursors


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise SemanticError(f'No visit method for {type(node)}')

    def check_types(self, from_type, to_type):
        if from_type == to_type:
            return True

        # Accepter INT ou FLOAT si on attend NUMBER
        if to_type == TokenType.NUMBER and from_type in [TokenType.INT, TokenType.FLOAT]:
            return True

        # Convertir INT en FLOAT
        if from_type == TokenType.INT and to_type == TokenType.FLOAT:
            return True

        # Accepter STRING pour STRING_TYPE
        if from_type == TokenType.STRING and to_type == TokenType.STRING_TYPE:
            return True

        # Accepter BOOL_VALUE pour BOOL
        if from_type == TokenType.BOOL_VALUE and to_type == TokenType.BOOL:
            return True

        return False

    def check_cursor_method(self, cursor_name, method_name):
        """Vérifie si une méthode de curseur est valide et retourne ses types de paramètres attendus"""
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
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDecl(self, node):
        if self.symbol_table.lookup(node.name):
            raise SemanticError(f"Variable {node.name} already declared")

        self.symbol_table.define(node.name, node.var_type)

        if node.init_value:
            init_type = self.visit(node.init_value)
            if not self.check_types(init_type, node.var_type):
                raise SemanticError(f"Type mismatch in initialization of {node.name}")

    def visit_Assign(self, node):
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")

        expr_type = self.visit(node.value)
        if not self.check_types(expr_type, var_type):
            raise SemanticError(f"Type mismatch in assignment to {node.name}")

    def visit_CursorCreation(self, node):
        self.symbol_table.define_cursor(node.name)
        x_type = self.visit(node.x)
        y_type = self.visit(node.y)
        if not (x_type in [TokenType.INT, TokenType.FLOAT] and
                y_type in [TokenType.INT, TokenType.FLOAT]):
            raise SemanticError("Cursor coordinates must be numeric")

    def visit_CursorMethod(self, node):
        expected_param_types = self.check_cursor_method(node.cursor_name, node.method_name)
        if len(node.params) != len(expected_param_types):
            raise SemanticError(f"Method {node.method_name} expects {len(expected_param_types)} parameters")

        for param, expected_type in zip(node.params, expected_param_types):
            param_type = self.visit(param)
            if not self.check_types(param_type, expected_type):
                raise SemanticError(f"Invalid parameter type for method {node.method_name}")

    def visit_DrawCommand(self, node):
        expected_param_types = self.check_cursor_method(node.cursor_name, node.shape_type)
        if len(node.params) != len(expected_param_types):
            raise SemanticError(f"Shape {node.shape_type} expects {len(expected_param_types)} parameters")

        for param, expected_type in zip(node.params, expected_param_types):
            param_type = self.visit(param)
            if not self.check_types(param_type, expected_type):
                raise SemanticError(f"Invalid parameter type for shape {node.shape_type}")

    def visit_WindowCommand(self, node):
        valid_commands = ['clear', 'update']
        if node.command not in valid_commands:
            raise SemanticError(f"Invalid window command: {node.command}")

    def visit_BinOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        # Opérations arithmétiques
        if node.op in [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.SLASH, TokenType.MODULO]:
            if left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]:
                # Si l'un des deux est FLOAT, le résultat est FLOAT, sinon INT
                return TokenType.FLOAT if TokenType.FLOAT in [left_type, right_type] else TokenType.INT
            raise SemanticError(f"Invalid operand types for arithmetic operation: {left_type} and {right_type}")

        # Opérations de comparaison
        elif node.op in [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL,
                         TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL]:

            # Conditions pour autoriser la comparaison :
            # 1. Les deux opérandes sont du même type.
            # 2. Les deux opérandes sont numériques (INT/FLOAT), conversions permises.
            # 3. Une combinaison de BOOL et BOOL_VALUE, qu'on autorise à se comparer.
            if (left_type == right_type) \
                    or (
                    left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]) \
                    or ((left_type == TokenType.BOOL and right_type == TokenType.BOOL_VALUE) or
                        (left_type == TokenType.BOOL_VALUE and right_type == TokenType.BOOL)):
                return TokenType.BOOL_VALUE

            raise SemanticError(f"Invalid operand types for comparison: {left_type} and {right_type}")

        # Si l'opérateur n'est ni arithmétique ni de comparaison, cas non géré
        raise SemanticError(f"Unknown binary operator {node.op}")

    def visit_If(self, node):
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
        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL_VALUE:
            raise SemanticError("While condition must be boolean")

        for stmt in node.body:
            self.visit(stmt)

    def visit_For(self, node):
        self.visit(node.init)

        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL_VALUE:
            raise SemanticError("For condition must be boolean")

        self.visit(node.update)

        for stmt in node.body:
            self.visit(stmt)

    def visit_Num(self, node):
        return TokenType.FLOAT if isinstance(node.value, float) else TokenType.INT

    def visit_StringLiteral(self, node):
        return TokenType.STRING

    def visit_BooleanLiteral(self, node):
        return TokenType.BOOL_VALUE

    def visit_ColorValue(self, node):
        if node.color_name:
            return TokenType.COLOR
        if node.rgb_values:
            for value in node.rgb_values:
                value_type = self.visit(value)
                if value_type not in [TokenType.INT, TokenType.FLOAT]:
                    raise SemanticError("RGB values must be numeric")
        return TokenType.COLOR

    def visit_Var(self, node):
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")
        return var_type


def analyze(ast):
    analyzer = SemanticAnalyzer()
    try:
        analyzer.visit(ast)
        return True, None
    except SemanticError as e:
        return False, str(e)


if __name__ == "__main__":
    from compiler.lexer.lexer import Lexer
    from compiler.parser.parser import Parser

    source_code = """
    // Test des déclarations et initialisations
    var int width = 800;
    var float angle = 45.0;
    var string message = "Hello Draw++";
    var bool isDrawing = true;

    // Test de la création et configuration du curseur
    cursor main = create_cursor(400, 300);
    main.color(RED);
    main.thickness(2);

    // Test des structures conditionnelles
    if (isDrawing == true) {
        main.visible(true);
        main.draw_rectangle(60, 40, true);
    } elif (width > 500) {
        main.draw_circle(30, false);
    } else {
        window.clear();
    };

    // Test de la boucle for avec dessin
    for (var int i = 0; i < 4; i += 1) {
        main.rotate(90);
        main.move(100);
    };

    // Test des expressions arithmétiques et des méthodes de dessin
    var float radius = (width + angle) / 4;
    main.draw_circle(radius, true);

    // Test des couleurs RGB
    main.color(rgb(255, 0, 0));
    main.draw_triangle(50, 40, true);
    """

    try:
        # Analyse lexicale
        print("-" * 50)
        print("ANALYSE LEXICALE")
        print("-" * 50)
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("Tokens générés avec succès")
        print("\nPremiers tokens:")
        for i, token in enumerate(tokens[:10]):
            print(f"{i + 1}. {token}")
        print("...")

        # Analyse syntaxique
        print("\n" + "-" * 50)
        print("ANALYSE SYNTAXIQUE")
        print("-" * 50)
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST généré avec succès")
        print("\nStructure du programme:")
        print(f"Nombre de déclarations au niveau racine: {len(ast.statements)}")

        # Analyse sémantique
        print("\n" + "-" * 50)
        print("ANALYSE SÉMANTIQUE")
        print("-" * 50)
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)

        print("\nContenu de la table des symboles:")
        print("\nVariables:")
        for name, type_ in analyzer.symbol_table.symbols.items():
            print(f"  {name:10} | Type: {type_}")

        print("\nCurseurs:")
        for cursor in analyzer.symbol_table.cursors:
            print(f"  {cursor}")

        print("\nVérifications effectuées avec succès:")
        print("✓ Toutes les variables sont correctement déclarées")
        print("✓ Tous les types sont compatibles")
        print("✓ Toutes les opérations sont valides")
        print("✓ Toutes les méthodes de curseur sont valides")
        print("✓ Toutes les formes ont des paramètres valides")
        print("✓ Toutes les conditions sont booléennes")
        print("✓ Pas de variables non déclarées utilisées")

        print("\n" + "-" * 50)
        print("COMPILATION TERMINÉE AVEC SUCCÈS")
        print("-" * 50)

    except Exception as e:
        print("\n" + "!" * 50)
        print("ERREUR DE COMPILATION")
        print("!" * 50)
        print(f"\nType d'erreur: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\nStacktrace:")
        import traceback

        traceback.print_exc()