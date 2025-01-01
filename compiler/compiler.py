import os
import argparse
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.semantic_analyzer import SemanticAnalyzer, SemanticError, analyze
from compiler.codegen.codegen import CodeGenerator


class CompilationError(Exception):
    """
    @brief Exception class for handling compilation errors.

    @param phase The phase of the compilation process where the error occurred.
    @param message A description of the error.
    """

    def __init__(self, phase, message):
        self.phase = phase
        self.message = message
        super().__init__(f"{phase}: {message}")


class Compiler:
    """
    @brief Main compiler class for processing Draw++ files and generating C code.

    This class performs lexical analysis, syntax analysis, semantic analysis,
    and code generation for Draw++ source files.
    """

    def __init__(self):
        """
        @brief Initializes the Compiler instance with placeholders for tokens and AST.
        """
        self.tokens = None
        self.ast = None

    def compile(self, input_file, output_file=None):
        """
        @brief Compiles a Draw++ source file into a C source file.

        @param input_file The path to the Draw++ source file (.dpp).
        @param output_file Optional path to the output C source file (.c).
        @return True if compilation succeeds, False otherwise.
        """
        try:
            # Verify file extension
            if not input_file.endswith('.dpp'):
                raise CompilationError(
                    "Input", "The source file must have a .dpp extension")

            # Read the source file
            print(f"\n[1/5] Reading source file: {input_file}")
            with open(input_file, 'r') as f:
                source_code = f.read()

            # Lexical analysis
            print("\n[2/5] Performing lexical analysis...")
            self.tokens = self._lexical_analysis(source_code)
            print("✓ Lexical analysis completed successfully")
            print(f"Number of tokens: {len(self.tokens)}")

            # Syntax analysis
            print("\n[3/5] Performing syntax analysis...")
            self.ast = self._syntax_analysis(self.tokens)
            print("✓ Syntax analysis completed successfully")
            print(f"Number of statements: {len(self.ast.statements)}")

            # Semantic analysis
            print("\n[4/5] Performing semantic analysis...")
            success, error = self._semantic_analysis(self.ast)
            if not success:
                raise CompilationError("Semantic", error)
            print("✓ Semantic analysis completed successfully")

            # Code generation
            print("\n[5/5] Generating code...")
            if output_file is None:
                output_file = os.path.splitext(input_file)[0] + '.c'

            self._generate_code(self.ast, output_file)
            print(f"✓ C code generated successfully: {output_file}")

            print("\n✨ Compilation completed successfully!")
            return True

        except FileNotFoundError:
            print(f"\n❌ Error: File not found: {input_file}")
            return False
        except CompilationError as e:
            print(f"\n❌ Compilation error ({e.phase}): {e.message}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def _lexical_analysis(self, source_code):
        """
        @brief Performs lexical analysis on the source code.

        @param source_code The source code to tokenize.
        @return A list of tokens generated from the source code.
        """
        lexer = Lexer(source_code)
        return lexer.tokenize()

    def _syntax_analysis(self, tokens):
        """
        @brief Performs syntax analysis on the tokens.

        @param tokens The tokens generated from lexical analysis.
        @return An Abstract Syntax Tree (AST) representing the program.
        """
        parser = Parser(tokens)
        return parser.parse()

    def _semantic_analysis(self, ast):
        """
        @brief Performs semantic analysis on the Abstract Syntax Tree.

        @param ast The Abstract Syntax Tree to analyze.
        @return A tuple (success, error), where success is a boolean indicating
        whether the analysis succeeded, and error is the error message (if any).
        """
        return analyze(ast)

    def _generate_code(self, ast, output_file):
        """
        @brief Generates C code from the Abstract Syntax Tree and writes it to a file.

        @param ast The Abstract Syntax Tree representing the program.
        @param output_file The path to the output C file.
        """
        generator = CodeGenerator()
        code = generator.generate(ast)  # Generate C code as a string
        os.makedirs(os.path.dirname(
            os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(code)


def main():
    """
    @brief Entry point for the Draw++ compiler.

    Parses command-line arguments and compiles the specified Draw++ source file.
    """
    parser = argparse.ArgumentParser(description="Draw++ Compiler")
    parser.add_argument('input', help='Draw++ source file (.dpp)')
    parser.add_argument('-o', '--output', help='Output C file (.c)')
    args = parser.parse_args()

    print(f"Working directory: {os.getcwd()}")
    input_file = os.path.abspath(args.input)
    print(f"Input file: {input_file}")

    compiler = Compiler()
    success = compiler.compile(input_file, args.output)
    exit(0 if success else 1)


if __name__ == "__main__":
    """
    @brief Executes the main function to start the compilation process.
    """
    main()
