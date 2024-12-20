from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.semantic_analyzer import SemanticAnalyzer, SemanticError, analyze
from compiler.lexer.tokens import TokenType


class ErrorAnalyzer:
    """
    @brief Analyzes code for errors using the full compiler pipeline.
    """

    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()

    def analyze_code(self, code):
        """
        @brief Analyzes the code using the full compiler pipeline.

        @param code The source code to analyze.
        @return tuple (bool, str, dict) Success flag, error message, and suggestions.
        """
        try:
            # Si le code est vide
            if not code.strip():
                return True, None, {}

            # Analyse lexicale
            lexer = Lexer(code)
            try:
                tokens = list(lexer.tokenize())
            except Exception as e:
                error_msg = str(e)
                line_num = self._extract_line_number(error_msg, code)

                # Suggestions spécifiques si la cause est un point-virgule manquant
                if ("TokenType.VAR" in error_msg and "got TokenType.VAR" in error_msg) or \
                        ("Expected TokenType.SEMICOLON" in error_msg):

                    lines = code.split('\n')
                    actual_line = line_num
                    while actual_line > 0 and not lines[actual_line - 1].strip():
                        actual_line -= 1

                    if actual_line > 0:
                        previous_line = lines[actual_line - 1].strip()
                        return False, "Missing semicolon", {
                            actual_line: [
                                "Add semicolon (;) at the end of the line",
                                f"{previous_line};"
                            ]
                        }

                return False, error_msg, {line_num: self._get_lexer_suggestions(error_msg)}

            # Analyse syntaxique
            try:
                parser = Parser(tokens)
                ast = parser.parse()
            except Exception as e:
                error_msg = str(e)
                line_num = self._extract_line_number(error_msg, code)
                return False, error_msg, {line_num: self._get_parser_suggestions(error_msg)}

            # Analyse sémantique
            success, error = analyze(ast)
            if not success:
                line_num = self._extract_line_number(error, code)
                return False, error, {line_num: self._get_semantic_suggestions(error)}

            return True, None, {}

        except Exception as e:
            return False, str(e), {1: [str(e)]}

    def _extract_line_number(self, error_msg, code):
        """
        @brief Extrait le numéro de ligne du message d'erreur.

        @param error_msg Le message d'erreur.
        @param code Le code source complet (pour éventuellement ajuster si nécessaire).
        @return int Le numéro de ligne ou 1 si non trouvé.
        """
        line_num = 1
        try:
            error_msg = str(error_msg)
            # Format: "at line X, column Y"
            if "at line" in error_msg:
                line_part = error_msg.split("at line")[1].split(",")[0]
                line_num = int(line_part.strip())
            # Format: "line=X"
            elif "line=" in error_msg:
                line_num = int(error_msg.split("line=")[1].split(",")[0])
            # Format: "line X"
            elif "line" in error_msg:
                parts = error_msg.split("line")[1].split()
                for part in parts:
                    if part.isdigit():
                        line_num = int(part)
                        break
        except:
            pass

        # Ajustement pour les erreurs de point-virgule manquant
        # On détecte soit le message "Missing semicolon" soit "Expected TokenType.SEMICOLON"
        if ("Missing semicolon" in error_msg or "Expected TokenType.SEMICOLON" in error_msg) and line_num > 1:
            # Vérification supplémentaire : si la ligne précédente se termine sans point-virgule
            lines = code.split('\n')
            if line_num <= len(lines):
                # On regarde la ligne précédente
                prev_line_index = line_num - 2
                if prev_line_index >= 0:
                    prev_line = lines[prev_line_index].strip()
                    # Si la ligne précédente ne se termine pas par un point-virgule et n'est pas vide,
                    # on ajuste le numéro de ligne à la précédente
                    if prev_line and not prev_line.endswith(';'):
                        line_num -= 1

        return line_num

    def _get_semantic_suggestions(self, error_msg):
        """
        @brief Génère des suggestions basées sur les erreurs sémantiques.
        """
        error_msg = str(error_msg).lower()
        suggestions = []

        if "not declared" in error_msg:
            var_name = error_msg.split("'")[1] if "'" in error_msg else error_msg.split()[1]
            suggestions.extend([
                f"var int {var_name} = 0;",
                f"var float {var_name} = 0.0;",
                f"var string {var_name} = \"\";",
                f"cursor {var_name} = create_cursor(0, 0);"
            ])
        elif "already declared" in error_msg:
            suggestions.extend([
                "Use a different variable name",
                "Remove the duplicate declaration"
            ])
        elif "type mismatch" in error_msg:
            suggestions.extend([
                "Check variable types",
                "Make sure types are compatible"
            ])
        elif "is not a cursor" in error_msg:
            cursor_name = error_msg.split(" ")[1]
            suggestions.extend([
                f"Declare the cursor first:",
                f"cursor {cursor_name} = create_cursor(x, y);"
            ])
        elif "invalid cursor method" in error_msg:
            suggestions.extend([
                "Available methods:",
                "move(distance)",
                "rotate(angle)",
                "color(COLOR)",
                "thickness(value)",
                "visible(bool)"
            ])

        return suggestions

    def _get_parser_suggestions(self, error_msg):
        """
        @brief Génère des suggestions basées sur les erreurs syntaxiques.
        """
        error_msg = str(error_msg).lower()
        suggestions = []

        if "unexpected token" in error_msg:
            suggestions.extend([
                "Check syntax",
                "Ensure all statements end with semicolon (;)",
                "Verify parentheses and braces"
            ])
        elif "expected type" in error_msg:
            suggestions.extend([
                "Use a valid type: int, float, string, bool, or color",
                "Example: var int myVariable = 0;"
            ])

        return suggestions

    def _get_lexer_suggestions(self, error_msg):
        """
        @brief Génère des suggestions basées sur les erreurs lexicales.
        """
        error_msg = str(error_msg).lower()
        suggestions = []

        if "invalid character" in error_msg:
            suggestions.extend([
                "Remove or replace invalid character",
                "Use only allowed characters"
            ])
        elif "unterminated string" in error_msg:
            suggestions.append("Add closing quotation mark (\")")
        else:
            suggestions.append("Check syntax and ensure all statements end with semicolon (;)")

        return suggestions
