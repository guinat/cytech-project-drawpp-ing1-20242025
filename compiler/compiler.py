#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path

# Imports locaux avec chemins relatifs
from .lexer.lexer import Lexer
from .lexer.tokens import TokenType
from .parser.parser import Parser
from .semantic.semantic_analyzer import SemanticAnalyzer
from .codegen.codegen import CodeGenerator


class Compiler:
    def __init__(self, debug=False):
        self.debug = debug

    def compile(self, source_file, output_file):
        try:
            # Lecture du fichier source
            with open(source_file, 'r') as f:
                source_code = f.read()

            # 1. Analyse lexicale
            if self.debug:
                print("Starting lexical analysis...")
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            if self.debug:
                print("Lexical analysis completed.")

            # 2. Analyse syntaxique
            if self.debug:
                print("Starting parsing...")
            parser = Parser(tokens)
            ast = parser.parse()
            if self.debug:
                print("Parsing completed.")

            # 3. Analyse sémantique
            if self.debug:
                print("Starting semantic analysis...")
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.visit(ast)
            if self.debug:
                print("Semantic analysis completed.")

            # 4. Génération de code
            if self.debug:
                print("Starting code generation...")
            code_generator = CodeGenerator()
            code_generator.generate(ast)
            code_generator.to_c_file(output_file)
            if self.debug:
                print(f"Code generation completed. Output written to {output_file}")

            return True

        except Exception as e:
            print(f"Compilation error: {str(e)}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return False


def main():
    parser = argparse.ArgumentParser(description="Draw++ Compiler")
    parser.add_argument('input', help='Input source file')
    parser.add_argument('-o', '--output', help='Output C file', default='output.c')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')

    args = parser.parse_args()

    compiler = Compiler(debug=args.debug)
    success = compiler.compile(args.input, args.output)

    if success:
        print(f"Compilation successful. Output written to {args.output}")
    else:
        print("Compilation failed.")
        exit(1)


if __name__ == "__main__":
    main()