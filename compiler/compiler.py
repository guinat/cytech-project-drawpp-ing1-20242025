import os
import argparse
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.semantic_analyzer import SemanticAnalyzer, SemanticError, analyze
from compiler.codegen.codegen import CodeGenerator


class CompilationError(Exception):
    def __init__(self, phase, message):
        self.phase = phase
        self.message = message
        super().__init__(f"{phase}: {message}")


class Compiler:
    def __init__(self):
        self.tokens = None
        self.ast = None

    def compile(self, input_file, output_file=None):
        try:
            # Vérification de l'extension
            if not input_file.endswith('.dpp'):
                raise CompilationError("Input", "Le fichier source doit avoir l'extension .dpp")

            # Lecture du fichier source
            print(f"\n[1/5] Lecture du fichier source: {input_file}")
            with open(input_file, 'r') as f:
                source_code = f.read()

            # Analyse lexicale
            print("\n[2/5] Analyse lexicale...")
            self.tokens = self._lexical_analysis(source_code)
            print("✓ Analyse lexicale réussie")
            print(f"Nombre de tokens: {len(self.tokens)}")

            # Analyse syntaxique
            print("\n[3/5] Analyse syntaxique...")
            self.ast = self._syntax_analysis(self.tokens)
            print("✓ Analyse syntaxique réussie")
            print(f"Nombre de déclarations: {len(self.ast.statements)}")

            # Analyse sémantique
            print("\n[4/5] Analyse sémantique...")
            success, error = self._semantic_analysis(self.ast)
            if not success:
                raise CompilationError("Semantic", error)
            print("✓ Analyse sémantique réussie")

            # Génération de code
            print("\n[5/5] Génération de code...")
            if output_file is None:
                output_file = os.path.splitext(input_file)[0] + '.c'

            self._generate_code(self.ast, output_file)
            print(f"✓ Code C généré avec succès: {output_file}")

            print("\n✨ Compilation terminée avec succès!")
            return True

        except FileNotFoundError:
            print(f"\n❌ Erreur: Fichier non trouvé: {input_file}")
            return False
        except CompilationError as e:
            print(f"\n❌ Erreur de compilation ({e.phase}): {e.message}")
            return False
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def _lexical_analysis(self, source_code):
        lexer = Lexer(source_code)
        return lexer.tokenize()

    def _syntax_analysis(self, tokens):
        parser = Parser(tokens)
        return parser.parse()

    def _semantic_analysis(self, ast):
        return analyze(ast)

    def _generate_code(self, ast, output_file):
        generator = CodeGenerator()
        code = generator.generate(ast)  # Utilisation de la méthode generate(ast) qui renvoie une chaîne de caractères
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(code)


def main():
    parser = argparse.ArgumentParser(description="Compilateur Draw++")
    parser.add_argument('input', help='Fichier source Draw++ (.dpp)')
    parser.add_argument('-o', '--output', help='Fichier de sortie C (.c)')
    args = parser.parse_args()

    print(f"Répertoire de travail : {os.getcwd()}")
    input_file = os.path.abspath(args.input)
    print(f"Fichier d'entrée : {input_file}")

    compiler = Compiler()
    success = compiler.compile(input_file, args.output)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
