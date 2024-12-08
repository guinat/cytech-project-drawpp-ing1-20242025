import json
import os
from compiler.parser.syntax_tree import *


class CodeGenerator:
    def __init__(self, config_file=None):
        self.indent_level = 0
        self.output = []

        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, "codegen_config.json")

        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.indentation = "    "  # indentation fixe de 4 espaces

    def indent(self):
        return self.indentation * self.indent_level

    def write_line(self, line):
        self.output.append(f"{self.indent()}{line}")

    def generate(self, node):
        if node is None:
            return ""

        # Affichage de débogage pour voir le type exact du nœud
        print(f"Generating code for node type: {type(node).__name__}")

        method_name = f'generate_{type(node).__name__.lower()}'
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            raise Exception(f"Unsupported node type: {type(node).__name__} (looking for method {method_name})")

    def generate_program(self, node):
        # Headers
        for header in self.config["headers"]:
            self.write_line(header)
        self.write_line("")

        # Main function
        self.write_line("int main() {")
        self.indent_level += 1

        for statement in node.statements:
            self.generate(statement)

        self.indent_level -= 1
        self.write_line("    return 0;")
        self.write_line("}")

        return "\n".join(self.output)

    def generate_vardecl(self, node):
        c_type = self.config["types"][str(node.var_type)]
        value = self.generate(node.init_value) if node.init_value else "0"
        self.write_line(f"{c_type} {node.name} = {value};")

    def generate_assign(self, node):
        value = self.generate(node.value)
        self.write_line(f"{node.name} = {value};")

    def generate_binop(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)
        operator = self.config["operators"][str(node.op)]
        return f"({left} {operator} {right})"

    def generate_num(self, node):
        return str(node.value)

    def generate_var(self, node):
        return node.name

    def generate_if(self, node):
        condition = self.generate(node.condition)

        self.write_line(f"if ({condition}) {{")

        self.indent_level += 1
        for stmt in node.true_body:
            self.generate(stmt)
        self.indent_level -= 1

        self.write_line("}")

        if node.false_body:
            self.write_line("else {")
            self.indent_level += 1
            for stmt in node.false_body:
                self.generate(stmt)
            self.indent_level -= 1
            self.write_line("}")

    def generate_while(self, node):
        condition = self.generate(node.condition)

        self.write_line(f"while ({condition}) {{")

        self.indent_level += 1
        for stmt in node.body:
            self.generate(stmt)
        self.indent_level -= 1

        self.write_line("}")

    # Ajout des méthodes pour tous les types de nœuds possibles
    def generate_number(self, node):
        return str(node.value)

    def generate_identifier(self, node):
        return node.name

    def generate_numbernode(self, node):
        return str(node.value)

    def generate_varnode(self, node):
        return node.name

    def generate_variablenode(self, node):
        return node.name

    def to_c_file(self, filename):
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'w') as f:
            f.write("\n".join(self.output))


def create_default_config(config_file):
    config = {
        "headers": [
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <stdbool.h>"
        ],
        "types": {
            "TokenType.INT": "int",
            "TokenType.FLOAT": "float",
            "TokenType.BOOL": "bool",
            "TokenType.STRING": "char*"
        },
        "operators": {
            "TokenType.PLUS": "+",
            "TokenType.MINUS": "-",
            "TokenType.MULTIPLY": "*",
            "TokenType.DIVIDE": "/",
            "TokenType.LT": "<",
            "TokenType.GT": ">",
            "TokenType.LTE": "<=",
            "TokenType.GTE": ">=",
            "TokenType.EQ": "==",
            "TokenType.NEQ": "!="
        }
    }

    os.makedirs(os.path.dirname(config_file), exist_ok=True)

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)