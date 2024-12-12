from compiler.lexer.tokens import TokenType
import json
import os


class CodeGenError(Exception):
    pass


class CodeGenerator:
    def __init__(self, config_file=None):
        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, "codegen_config.json")

        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.indent_level = 0
        self.output = []

    def indent(self):
        return "    " * self.indent_level

    def write_line(self, line=""):
        self.output.append(f"{self.indent()}{line}")
        return line

    def visit(self, node):
        if node is None:
            return ""

        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        result = visitor(node)
        return result if result is not None else ""

    def generic_visit(self, node):
        raise CodeGenError(f'No visit method for {type(node)}')

    def visit_Program(self, node):
        # En-têtes
        for header in self.config["headers"]:
            self.write_line(header)
        self.write_line()

        # Fonction main
        self.write_line("int main(int argc, char* argv[]) {")
        self.indent_level += 1

        # Initialisation SDL
        self.write_line("if (!initialize_SDL()) {")
        self.write_line("    printf(\"Failed to initialize SDL\\n\");")
        self.write_line("    return 1;")
        self.write_line("}")
        self.write_line()

        # Corps du programme
        for statement in node.statements:
            self.visit(statement)
            self.write_line()

        # Nettoyage et retour
        self.write_line("SDL_RenderPresent(renderer);")
        self.write_line("SDL_Delay(5000);")
        self.write_line("cleanup_SDL();")
        self.write_line("return 0;")

        self.indent_level -= 1
        self.write_line("}")

        return "\n".join(self.output)

    def visit_VarDecl(self, node):
        c_type = self.config["type_mappings"][str(node.var_type)]
        init_value = self.visit(node.init_value) if node.init_value else "0"
        return self.write_line(f"{c_type} {node.name} = {init_value};")

    def visit_Assign(self, node):
        value = self.visit(node.value)
        return self.write_line(f"{node.name} = {value};")

    def visit_CursorCreation(self, node):
        # Obtenir les coordonnées x et y
        x = self.visit(node.x)
        y = self.visit(node.y)
        # Générer le code de création du curseur
        return self.write_line(f"Cursor* {node.name} = create_cursor({x}, {y});")

    def visit_CursorMethod(self, node):
        params = [self.visit(p) for p in node.params]
        method_map = {
            'move': 'move_cursor',
            'rotate': 'rotate_cursor',
            'color': 'set_cursor_color',
            'thickness': lambda n, p: f"{n}->thickness = {p[0]}",
            'visible': 'set_cursor_visibility'
        }

        if node.method_name in method_map:
            if callable(method_map[node.method_name]):
                code = method_map[node.method_name](node.cursor_name, params)
            else:
                code = f"{method_map[node.method_name]}({node.cursor_name}, {', '.join(params)})"
            return self.write_line(f"{code};")
        return ""

    def visit_DrawCommand(self, node):
        params = [self.visit(p) for p in node.params]
        draw_map = {
            'draw_line': 'cursor_draw_line',
            'draw_rectangle': 'cursor_draw_rectangle',
            'draw_circle': 'cursor_draw_circle',
            'draw_triangle': 'cursor_draw_triangle',
            'draw_ellipse': 'cursor_draw_ellipse'
        }
        method = draw_map.get(node.shape_type)
        if method:
            return self.write_line(f"{method}({node.cursor_name}, {', '.join(params)});")
        return ""

    def visit_WindowCommand(self, node):
        if node.command == 'clear':
            self.write_line("SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);")
            return self.write_line("SDL_RenderClear(renderer);")
        elif node.command == 'update':
            return self.write_line("SDL_RenderPresent(renderer);")
        return ""

    def visit_If(self, node):
        condition = self.visit(node.condition)
        self.write_line(f"if ({condition}) {{")

        self.indent_level += 1
        for stmt in node.true_body:
            self.visit(stmt)
        self.indent_level -= 1

        if node.elif_bodies:
            for elif_condition, elif_body in node.elif_bodies:
                self.write_line(f"}} else if ({self.visit(elif_condition)}) {{")
                self.indent_level += 1
                for stmt in elif_body:
                    self.visit(stmt)
                self.indent_level -= 1

        if node.false_body:
            self.write_line("} else {")
            self.indent_level += 1
            for stmt in node.false_body:
                self.visit(stmt)
            self.indent_level -= 1

        return self.write_line("}")

    def visit_For(self, node):
        init = self.visit(node.init) or ""
        condition = self.visit(node.condition) or ""
        update = self.visit(node.update) or ""

        if update.endswith(';'):
            update = update[:-1]

        self.write_line(f"for ({init} {condition}; {update}) {{")

        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

        return self.write_line("}")

    def visit_While(self, node):
        condition = self.visit(node.condition)
        self.write_line(f"while ({condition}) {{")

        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1

        return self.write_line("}")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.config["operators"][str(node.op)]
        return f"({left} {op} {right})"

    def visit_Num(self, node):
        return str(node.value)

    def visit_StringLiteral(self, node):
        return f'"{node.value}"'

    def visit_BooleanLiteral(self, node):
        return "true" if node.value.lower() == "true" else "false"

    def visit_ColorValue(self, node):
        if node.color_name:
            return self.config["colors"].get(node.color_name, "black")
        if node.rgb_values:
            r, g, b = [self.visit(v) for v in node.rgb_values]
            return f"custom_color({r}, {g}, {b}, 255)"
        return "black"

    def visit_Var(self, node):
        return node.name

    def to_file(self, filename):
        with open(filename, 'w') as f:
            f.write("\n".join(self.output))