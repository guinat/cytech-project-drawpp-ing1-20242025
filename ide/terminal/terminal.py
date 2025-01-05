import sys
import os
import subprocess
import threading
import tkinter as tk
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.parser.syntax_tree import *
from cmd import Cmd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class InteractiveTerminal(tk.Text):
    """
    @brief A terminal widget that interacts with a subprocess.
    """

    def __init__(self, parent, command, *args, **kwargs):
        """
        @brief Constructor for the InteractiveTerminal class.
        @param parent The parent widget/container.
        @param command The command to be executed in the subprocess.
        @param args Additional positional arguments for tk.Text.
        @param kwargs Additional keyword arguments for tk.Text.
        """
        super().__init__(parent, *args, **kwargs)
        self.command = command
        self.process = None
        self.thread = None

        # Start the subprocess
        self.start_subprocess()

        # Bind Enter key to send input
        self.bind("<Return>", self.send_input)

    def start_subprocess(self):
        """
        @brief Start the subprocess and a thread to read its output.
        """
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Start a thread to read subprocess output
        self.thread = threading.Thread(target=self.read_output, daemon=True)
        self.thread.start()

    def close_subprocess(self):
        """
        @brief Terminate the subprocess if it's running.
        """
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

    def read_output(self):
        """
        @brief Read output from the subprocess and display it in the terminal.
        """
        for line in self.process.stdout:
            self.insert(tk.END, line)
            self.see(tk.END)

    def send_input(self, event=None):
        """
        @brief Send input to the subprocess.
        @param event The tkinter event object (optional).
        @return "break" to prevent the default behavior of the Enter key.
        """
        input_line = self.get("insert linestart", "insert lineend")
        self.process.stdin.write(input_line + "\n")
        self.process.stdin.flush()
        self.insert(tk.END, "\n")  # Move to the next line
        self.see(tk.END)
        return "break"  # Prevent default Enter key behavior


class DrawTerminal(Cmd):
    """
    Interactive terminal for Draw++ with integrated commands.
    """
    intro = "Welcome to the Draw++ terminal! Type 'help' for the list of commands."
    prompt = "draw++> "

    def __init__(self, terminal_widget=None):
        """
        @brief Initializes the interactive terminal.

        @param terminal_widget Optional. A widget to redirect terminal output.
        """
        super().__init__()
        self.terminal_widget = terminal_widget  # Widget for output redirection
        self.source_code = None
        self.tokens = None
        self.ast = None
        self.history = []
        self.check_imports()

    def print_to_terminal(self, message):
        """
        @brief Displays a message in the terminal widget or shell.

        @param message The message to display.
        """
        if self.terminal_widget:
            # Add a newline before and after each message
            self.terminal_widget.insert("end", "\n" + message + "\n")
            self.terminal_widget.see("end")
        else:
            print("\n" + message + "\n")

    def check_imports(self):
        """
        @brief Checks if the required classes are properly imported.
        """
        self.print_to_terminal("=== Checking imports ===")
        try:
            self.print_to_terminal(f"Checked classes:\nProgram: {Program}, VarDecl: {VarDecl}")
        except NameError as e:
            self.print_to_terminal(f"Import error: {e}")

    def precmd(self, line):
        """
        Called before executing a command, adds to command history.
        """
        if line.strip():  # Ignore empty commands
            self.history.append(line)
        return line

    def onecmd(self, line):
        """
        Override onecmd to ensure precmd is called before executing commands.
        """
        line = self.precmd(line)  # Call precmd to add the command to history
        return super().onecmd(line)

    def do_history(self, _):
        """
        Displays the history of executed commands.
        """
        if not self.history:
            self.print_to_terminal("No commands in history.")
            return

        self.print_to_terminal("\n=== Command History ===")
        for idx, command in enumerate(self.history, start=1):
            self.print_to_terminal(f"{idx}. {command}")

    def do_see(self, line):
        """
        Lists available files in the examples directory.
        """
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../examples"))

        try:
            if not os.path.exists(directory):
                self.print_to_terminal(f"Directory '{directory}' not found.")
                return

            files = os.listdir(directory)
            if not files:
                self.print_to_terminal(f"No files found in '{directory}'.")
                return

            self.print_to_terminal(f"Files in '{directory}':")
            for file in files:
                self.print_to_terminal(f" - {file}")
        except Exception as e:
            self.print_to_terminal(f"Error listing files: {e}")

    def do_debug(self, line):
        """
        Debugs a line of code or a Draw++ file and displays errors.
        Syntax:
            debug -c <code>
            debug <file.dpp>
        """
        args = line.split(maxsplit=1)
        if not args:
            self.print_to_terminal("Error: Invalid syntax. Use 'debug -c <code>' or 'debug <file.dpp>'.")
            return

        try:
            if args[0] == "-c":
                code = args[1]
                self._debug_line(code)
            else:
                file_path = args[0]
                if not file_path.endswith(".dpp"):
                    file_path += ".dpp"
                if not os.path.exists(file_path):
                    self.print_to_terminal(f"Error: File '{file_path}' not found.")
                    return
                with open(file_path, "r") as file:
                    code = file.read()
                self._debug_line(code)
        except Exception as e:
            self.print_to_terminal(f"Debug error: {e}")

    def _debug_line(self, code):
        """
        Debugs a line of code and displays errors.
        """
        try:
            self.print_to_terminal("[INFO] Lexical Analysis...")
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            self.print_to_terminal("[INFO] Lexical Analysis Passed.")

            self.print_to_terminal("[INFO] Syntax Analysis...")
            parser = Parser(tokens)
            ast = parser.parse()
            self.print_to_terminal("[INFO] Syntax Analysis Passed.")
            self.print_to_terminal("[INFO] No errors detected.")
        except Exception as e:
            self.print_to_terminal(f"[ERROR] {e}")

    def do_help(self, arg):
        """
        @brief Displays help for available commands.

        @param arg Optional. The specific command to display help for.
        """
        if arg:
            func = getattr(self, f"do_{arg}", None)
            if func and func.__doc__:
                self.print_to_terminal(func.__doc__)
            else:
                self.print_to_terminal(f"No help found for '{arg}'.")
        else:
            commands = [attr[3:] for attr in dir(self) if attr.startswith('do_')]
            self.print_to_terminal("=== Available Commands ===")
            for cmd in commands:
                self.print_to_terminal(f"{cmd} - {getattr(self, f'do_{cmd}').__doc__.strip().splitlines()[0]}")

    def do_lex(self, line):
        """
        @brief Performs lexical analysis on a line of code.

        @param line The code to analyze.
        """
        if not line.strip():
            self.print_to_terminal("Error: Provide a line of code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            self.print_to_terminal("=== Generated Tokens ===")
            for token in self.tokens:
                self.print_to_terminal(str(token))
        except Exception as e:
            self.print_to_terminal(f"Lexical error: {e}")

    def do_parse(self, line):
        """
        @brief Performs syntax analysis on a line of code and generates an AST.

        @param line The code to parse.
        """
        if not line.strip():
            self.print_to_terminal("Error: Provide a line or block of code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            self.print_to_terminal("=== Generated AST ===")
            self.print_to_terminal(str(self.ast))
        except Exception as e:
            self.print_to_terminal(f"Syntax error: {e}")

    def do_run(self, line):
        """
        @brief Executes the provided Draw++ code.

        @param line Syntax: run <file_path> | run -c <code>
        """
        args = line.split(maxsplit=1)
        if not args:
            self.print_to_terminal("Error: Provide a file path or code.")
            return

        try:
            if args[0] == "-c":
                source_code = args[1]
                self.run_code(source_code=source_code)
            else:
                source_file = args[0]
                self.run_code(source_file=source_file)
        except Exception as e:
            self.print_to_terminal(f"Execution error: {e}")

    def run_code(self, source_code=None, source_file=None):
        """
        @brief Compiles and executes Draw++ code.

        @param source_code Optional. The Draw++ code to execute.
        @param source_file Optional. The file path of the Draw++ code to execute.
        """
        if not source_code and not source_file:
            self.print_to_terminal("Error: Provide a source of code.")
            return

        temp_file = "temp.dpp"
        if source_code:
            with open(temp_file, "w") as f:
                f.write(source_code)
            source_file = temp_file

        try:
            c_file = "temp.c"
            executable = "temp_program"
            compile_cmd = f"python -m compiler.compiler {source_file} -o {c_file}"
            gcc_cmd = f"gcc -I../lib/DPP/include -I../lib/SDL2/include -L../lib -o {executable} {c_file} -ldrawpp -lSDL2 -lm"
            run_cmd = f"./{executable}"

            self.print_to_terminal(f"Compiling: {compile_cmd}")
            result = subprocess.run(compile_cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                self.print_to_terminal(f"Draw++ compilation error: {result.stderr}")
                return

            self.print_to_terminal(f"Compiling: {gcc_cmd}")
            result = subprocess.run(gcc_cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                self.print_to_terminal(f"C compilation error: {result.stderr}")
                return

            self.print_to_terminal("Running executable...")
            result = subprocess.run(run_cmd.split(), capture_output=True, text=True)
            self.print_to_terminal(result.stdout)
            if result.returncode != 0:
                self.print_to_terminal(f"Execution error: {result.stderr}")
        finally:
            self.cleanup_temp_files([temp_file, c_file, executable])

    def cleanup_temp_files(self, files):
        """
        @brief Removes generated temporary files.

        @param files List of files to delete.
        """
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def do_save(self, line):
        """
        @brief Saves source code, tokens, or AST to a file.

        @param line Syntax: save <type> <filename>
        """
        args = line.split()
        if len(args) != 2:
            self.print_to_terminal("Error: Incorrect syntax. Usage: save <type> <filename>")
            return

        save_type, filename = args
        try:
            if save_type == "source" and self.source_code:
                with open(filename, "w") as f:
                    f.write(self.source_code)
            elif save_type == "tokens" and self.tokens:
                with open(filename, "w") as f:
                    for token in self.tokens:
                        f.write(str(token) + "\n")
            elif save_type == "ast" and self.ast:
                with open(filename, "w") as f:
                    f.write(str(self.ast))
            else:
                self.print_to_terminal("Error: No data to save.")
        except Exception as e:
            self.print_to_terminal(f"Save error: {e}")

    def do_clear(self, _):
        """
        @brief Clears the terminal screen.
        """
        if self.terminal_widget:
            self.terminal_widget.delete("1.0", "end")
        else:
            os.system("clear")

    def do_exit(self, _):
        """
        @brief Exits the terminal.
        @return True to signal termination.
        """
        self.print_to_terminal("Goodbye!")
        return True

if __name__ == "__main__":
    DrawTerminal().cmdloop()
