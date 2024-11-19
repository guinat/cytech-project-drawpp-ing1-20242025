from compiler.lexer.tokens import TokenType


class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, type_):
        self.symbols[name] = type_

    def lookup(self, name):
        return self.symbols.get(name)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise SemanticError(f'No visit method for {type(node)}')

    def visit_Program(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDecl(self, node):
        # Vérifier si la variable est déjà déclarée
        if self.symbol_table.lookup(node.name):
            raise SemanticError(f"Variable {node.name} already declared")

        # Définir la variable dans la table des symboles
        self.symbol_table.define(node.name, node.var_type)

        # Vérifier l'expression d'initialisation si elle existe
        if node.init_value:
            init_type = self.visit(node.init_value)
            if not self.check_types(init_type, node.var_type):
                raise SemanticError(f"Type mismatch in initialization of {node.name}")

    def visit_Assign(self, node):
        # Vérifier si la variable est déclarée
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")

        # Vérifier le type de l'expression
        expr_type = self.visit(node.value)
        if not self.check_types(expr_type, var_type):
            raise SemanticError(f"Type mismatch in assignment to {node.name}")

    def visit_BinOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        # Vérifier la compatibilité des types pour les opérations binaires
        if node.op in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE]:
            if left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]:
                # Si l'un des opérandes est FLOAT, le résultat est FLOAT
                return TokenType.FLOAT if TokenType.FLOAT in [left_type, right_type] else TokenType.INT
            raise SemanticError(f"Invalid operand types for arithmetic operation: {left_type} and {right_type}")

        elif node.op in [TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
            if left_type in [TokenType.INT, TokenType.FLOAT] and right_type in [TokenType.INT, TokenType.FLOAT]:
                return TokenType.BOOL
            raise SemanticError(f"Invalid operand types for comparison: {left_type} and {right_type}")

    def visit_Num(self, node):
        # Déterminer si le nombre est un int ou float
        return TokenType.FLOAT if isinstance(node.value, float) else TokenType.INT

    def visit_Var(self, node):
        var_type = self.symbol_table.lookup(node.name)
        if not var_type:
            raise SemanticError(f"Variable {node.name} not declared")
        return var_type

    def visit_If(self, node):
        # Vérifier que la condition est un booléen
        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL:
            raise SemanticError("Condition must be boolean")

        # Vérifier les blocs then et else
        for stmt in node.true_body:
            self.visit(stmt)
        if node.false_body:
            for stmt in node.false_body:
                self.visit(stmt)

    def visit_While(self, node):
        # Vérifier que la condition est un booléen
        condition_type = self.visit(node.condition)
        if condition_type != TokenType.BOOL:
            raise SemanticError("While condition must be boolean")

        # Vérifier le corps de la boucle
        for stmt in node.body:
            self.visit(stmt)

    def check_types(self, from_type, to_type):
        """Vérifie si une conversion de type est possible"""
        if from_type == to_type:
            return True

        # Conversions autorisées
        if from_type == TokenType.INT and to_type == TokenType.FLOAT:
            return True

        return False


def analyze(ast):
    analyzer = SemanticAnalyzer()
    try:
        analyzer.visit(ast)
        return True, None
    except SemanticError as e:
        return False, str(e)


def main():
    from compiler.lexer.lexer import Lexer
    from compiler.parser.parser import Parser

    # Code source de test plus complet
    source_code = """
    // Test des déclarations et initialisations
    int x = 10;
    float y = 20.5;
    int sum = 0;
    float average = 0.0;

    // Test des opérations arithmétiques
    sum = x + 5;
    average = (x + y) / 2;

    // Test des structures conditionnelles imbriquées
    if (x < y) {
        if (sum > 15) {
            x = x + 1;
        } else {
            x = x - 1;
        }
    } else {
        if (sum < 10) {
            y = y + 1.5;
        } else {
            y = y - 1.5;
        }
    }

    // Test de la boucle while avec conditions composées
    while (x < 20) {
        x = x + 1;
        if (x == 15) {
            y = y * 2;
        }
    }

    // Test des opérations de comparaison
    if (x <= y) {
        sum = sum + 1;
    }

    if (x >= 10) {
        sum = sum - 1;
    }

    if (x == y) {
        average = x;
    }

    if (x != y) {
        average = (x + y) / 2;
    }

    // Test des expressions arithmétiques complexes
    float result = (x * y + sum) / (average + 1.0);

    // Test des erreurs potentielles (commenter/décommenter pour tester)
    // int z = 2.5;        // Erreur de type
    // float w = z;        // Variable non déclarée
    // if (x + y) { }      // Condition non booléenne
    // while (1) { }       // Condition non booléenne
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
        for name, type_ in analyzer.symbol_table.symbols.items():
            print(f"Variable: {name:10} | Type: {type_}")

        print("\nVérifications effectuées avec succès:")
        print("✓ Toutes les variables sont correctement déclarées")
        print("✓ Tous les types sont compatibles")
        print("✓ Toutes les opérations sont valides")
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


if __name__ == "__main__":
    main()