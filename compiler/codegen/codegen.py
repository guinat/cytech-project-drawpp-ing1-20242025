from lexer.tokens import TokenType
import os
import json

class CodeGenError(Exception):
    """
    @brief Custom exception class for code generation errors.
    """
    pass

class CodeGenerator:
    """
    @brief A class responsible for generating C code from an abstract syntax tree (AST).
    """

    def __init__(self, config_file=None):
        """
        @brief Initializes the CodeGenerator with configuration settings.

        @param config_file Optional path to a configuration file. If not provided, a default file named `codegen_config.json` is used.
        """
        self.indent_level = 0
        self.output = []

        if config_file is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, "codegen_config.json")

        with open(config_file, 'r') as f:
            self.config = json.load(f)

        # Convert keys "TokenType.X" to str(TokenType.X) if needed
        self.type_mappings = {}
        for k, v in self.config["type_mappings"].items():
            enum_name = getattr(TokenType, k.split('.')[-1], None)
            if enum_name:
                self.type_mappings[str(enum_name)] = v

        self.operator_map = {}
        for k, v in self.config["operators"].items():
            enum_name = getattr(TokenType, k.split('.')[-1], None)
            if enum_name:
                self.operator_map[str(enum_name)] = v

        self.color_map = self.config["colors"]

    def indent(self):
        """
        @brief Generates the current indentation level as a string.

        @return A string representing the current indentation level.
        """
        return "    " * self.indent_level

    def write_line(self, line=""):
        """
        @brief Appends a line of code to the output, respecting the current indentation level.

        @param line The line of code to write. Defaults to an empty line.
        """
        self.output.append(f"{self.indent()}{line}")

    def visit(self, node):
        """
        @brief Visits a node in the AST and delegates to the appropriate visit method.

        @param node The AST node to visit.
        @return The generated code for the node.
        """
        if node is None:
            return ""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        @brief A generic fallback for unsupported nodes.

        @param node The unsupported AST node.
        @throws CodeGenError if no specific visit method exists for the node.
        """
        raise CodeGenError(f'No visit method for {type(node)}')

    def generate(self, ast):
        """
        @brief Generates the C code for the given AST.

        @param ast The abstract syntax tree representing the program.
        @return The generated C code as a string.
        """
        # Include headers from the configuration
        for header in self.config["headers"]:
            self.write_line(header)
        self.write_line()

        self.write_line("int main(int argc, char* argv[]) {")
        self.indent_level += 1
        self.write_line("if (!initialize_SDL()) {")
        self.indent_level += 1
        self.write_line('printf("Failed to initialize SDL\\n");')
        self.write_line("return 1;")
        self.indent_level -= 1
        self.write_line("}")
        self.write_line()

        for stmt in ast.statements:
            self.visit(stmt)

        self.write_line()
        self.write_line("// Event loop waiting for window closure")
        self.write_line("bool running = true;")
        self.write_line("SDL_Event event;")
        self.write_line("while (running) {")
        self.indent_level += 1
        self.write_line("while (SDL_PollEvent(&event)) {")
        self.indent_level += 1
        self.write_line("if (event.type == SDL_QUIT) {")
        self.indent_level += 1
        self.write_line("running = false;")
        self.indent_level -= 1
        self.write_line("}")
        self.indent_level -= 1
        self.write_line("}")
        self.indent_level -= 1
        self.write_line("}")
        self.write_line("cleanup_SDL();")
        self.write_line("return 0;")
        self.indent_level -= 1
        self.write_line("}")

        return "\n".join(self.output)

    def visit_Program(self, node):
        """
        @brief Visits a program node and generates code for its statements.

        @param node The program node.
        """
        pass

    def visit_VarDecl(self, node):
        """
        @brief Generates code for a variable declaration.

        @param node The variable declaration node.
        """
        c_type = self.type_mappings.get(str(node.var_type), "int")
        init_value = self.visit(node.init_value) if node.init_value else "0"
        self.write_line(f"{c_type} {node.name} = {init_value};")

    def visit_Assign(self, node):
        """
        @brief Generates code for a variable assignment.

        @param node The assignment node.
        """
        value = self.visit(node.value)
        self.write_line(f"{node.name} = {value};")

    def visit_CursorCreation(self, node):
        """
        @brief Generates code for cursor creation.

        @param node The cursor creation node.
        """
        x = self.visit(node.x)
        y = self.visit(node.y)
        self.write_line(f"Cursor* {node.name} = create_cursor({x}, {y});")

    def visit_CursorMethod(self, node):
        """
        @brief Generates code for a cursor method call.

        @param node The cursor method node.
        """
        params = [self.visit(p) for p in node.params]
        method = node.method_name

        if method == "move":
            self.write_line(f"move_cursor({node.cursor_name}, {params[0]});")

        elif method == "rotate":
            self.write_line(f"rotate_cursor({node.cursor_name}, {params[0]});")

        elif method == "color":
            self.write_line(f"set_cursor_color({node.cursor_name}, {params[0]});")

        elif method == "thickness":
            self.write_line(f"{node.cursor_name}->thickness = (int){params[0]};")

        elif method == "visible":
            self.write_line(f"set_cursor_visibility({node.cursor_name}, {params[0]});")

    def visit_DrawCommand(self, node):
        """
        @brief Generates code for a draw command.

        @param node The draw command node specifying the shape type and parameters.
        """
        params = [self.visit(p) for p in node.params]
        shape = node.shape_type

        if shape == "draw_line":
            self.write_line(f"cursor_draw_line({node.cursor_name}, {params[0]});")

        elif shape == "draw_rectangle":
            self.write_line(f"cursor_draw_rectangle({node.cursor_name}, {params[0]}, {params[1]}, {params[2]});")

        elif shape == "draw_circle":
            self.write_line(f"cursor_draw_circle({node.cursor_name}, {params[0]}, {params[1]});")

        elif shape == "draw_triangle":
            self.write_line(f"cursor_draw_triangle({node.cursor_name}, {params[0]}, {params[1]}, {params[2]});")

        elif shape == "draw_ellipse":
            self.write_line(f"cursor_draw_ellipse({node.cursor_name}, {params[0]}, {params[1]}, {params[2]});")

        self.write_line("SDL_RenderPresent(renderer);")
        self.write_line("SDL_Delay(1000);")

    def visit_WindowCommand(self, node):
        """
        @brief Generates code for window-related commands (e.g., clear or update).

        @param node The window command node specifying the action to perform.
        """
        if node.command == "clear":
            self.write_line("SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);")
            self.write_line("SDL_RenderClear(renderer);")
        elif node.command == "update":
            self.write_line("SDL_RenderPresent(renderer);")

    def visit_If(self, node):
        """
        @brief Generates code for an if statement.

        @param node The if statement node containing condition, true body, and optional elif/else blocks.
        """
        condition = self.visit(node.condition)
        self.write_line(f"if ({condition}) {{")
        self.indent_level += 1
        for stmt in node.true_body:
            self.visit(stmt)
        self.indent_level -= 1
        if node.elif_bodies:
            for elif_condition, elif_body in node.elif_bodies:
                cond = self.visit(elif_condition)
                self.write_line(f"}} else if ({cond}) {{")
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
        self.write_line("}")

    def visit_For(self, node):
        """
        @brief Generates code for a for loop.

        @param node The for loop node containing initialization, condition, update, and body statements.
        """
        old_output = self.output
        self.output = []
        self.indent_level_tmp = self.indent_level

        self.visit(node.init)
        init_code = "".join(self.output).strip()
        self.output = []
        self.indent_level = self.indent_level_tmp

        cond_code = self.visit(node.condition)
        if cond_code.endswith(";"):
            cond_code = cond_code[:-1]

        self.visit(node.update)
        update_code = "".join(self.output).strip()
        if update_code.endswith(";"):
            update_code = update_code[:-1]

        self.output = old_output

        self.write_line(f"for ({init_code} {cond_code}; {update_code}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.write_line("}")

    def visit_While(self, node):
        """
        @brief Generates code for a while loop.

        @param node The while loop node containing the condition and body statements.
        """
        condition = self.visit(node.condition)
        self.write_line(f"while ({condition}) {{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.write_line("}")

    def visit_BinOp(self, node):
        """
        @brief Generates code for a binary operation.

        @param node The binary operation node containing left operand, operator, and right operand.
        @return The generated C code for the binary operation.
        """
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.operator_map.get(str(node.op), "+")
        return f"({left} {op} {right})"

    def visit_Num(self, node):
        """
        @brief Generates code for a numeric literal.

        @param node The numeric literal node.
        @return The numeric value as a string.
        """
        return str(node.value)

    def visit_StringLiteral(self, node):
        """
        @brief Generates code for a string literal.

        @param node The string literal node.
        @return The string value enclosed in double quotes.
        """
        return f"\"{node.value}\""

    def visit_BooleanLiteral(self, node):
        """
        @brief Generates code for a boolean literal.

        @param node The boolean literal node.
        @return The boolean value as 'true' or 'false'.
        """
        val = node.value.lower()
        return "true" if val == "true" else "false"

    def visit_ColorValue(self, node):
        """
        @brief Generates code for a color value, either predefined or custom RGB.

        @param node The color value node specifying color name or RGB components.
        @return The generated C code for the color.
        """
        if node.color_name:
            return self.color_map.get(node.color_name, "black")
        if node.rgb_values:
            r = self.visit(node.rgb_values[0])
            g = self.visit(node.rgb_values[1])
            b = self.visit(node.rgb_values[2])
            return f"custom_color((Uint8){r}, (Uint8){g}, (Uint8){b}, 255)"
        return "black"

    def visit_Var(self, node):
        """
        @brief Generates code for a variable reference.

        @param node The variable reference node.
        @return The variable name.
        """
        return node.name

    def to_file(self, filename):
        """
        @brief Writes the generated code to a file.

        @param filename The path to the output file.
        """
        with open(filename, 'w') as f:
            f.write("\n".join(self.output))
