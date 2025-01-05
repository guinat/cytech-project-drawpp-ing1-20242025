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
    A terminal widget that interacts with a subprocess.
    """

    def __init__(self, parent, command, *args, **kwargs):
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
        Starts the subprocess and a thread to read its output.
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
        Terminates the subprocess if it's running.
        """
        if self.process and self.process.poll() is None:  # Check if process is running
            self.process.terminate()
            self.process.wait()

    def read_output(self):
        """
        Reads output from the subprocess and displays it in the terminal.
        """
        for line in self.process.stdout:
            self.insert(tk.END, line)
            self.see(tk.END)

    def send_input(self, event=None):
        """
        Sends input to the subprocess.
        """
        input_line = self.get("insert linestart", "insert lineend")
        self.process.stdin.write(input_line + "\n")
        self.process.stdin.flush()
        self.insert(tk.END, "\n")  # Move to the next line
        return "break"  # Prevent default behavior of the Enter key

class DrawTerminal(Cmd):
    """
    Terminal interactif pour Draw++ avec commandes intégrées.
    """
    intro = "Bienvenue dans le terminal Draw++ ! Tapez 'help' pour la liste des commandes."
    prompt = "draw++> "

    def __init__(self, terminal_widget=None):
        """
        Initialise le terminal interactif.

        Args:
            terminal_widget (tk.Text, optional): Widget pour rediriger la sortie du terminal.
        """
        super().__init__()
        self.terminal_widget = terminal_widget  # Widget pour rediriger les sorties
        self.source_code = None
        self.tokens = None
        self.ast = None
        self.check_imports()

    def print_to_terminal(self, message):
        """
        Affiche un message dans le widget terminal ou dans le shell si aucun widget n'est attaché.

        Args:
            message (str): Le message à afficher.
        """
        if self.terminal_widget:
            # Ajoute un saut de ligne avant et après chaque message
            self.terminal_widget.insert("end", "\n" + message + "\n")
            self.terminal_widget.see("end")
        else:
            print("\n" + message + "\n")

    def check_imports(self):
        """
        Vérifie que les classes nécessaires sont bien importées.
        """
        self.print_to_terminal("=== Vérification des importations ===")
        try:
            self.print_to_terminal(f"Classes vérifiées :\nProgram: {Program}, VarDecl: {VarDecl}")
        except NameError as e:
            self.print_to_terminal(f"Erreur d'importation : {e}")

    def do_help(self, arg):
        """
        Affiche l'aide des commandes disponibles.
        Syntaxe : help [commande]
        """
        if arg:
            # Affiche l'aide pour une commande spécifique
            func = getattr(self, f"do_{arg}", None)
            if func and func.__doc__:
                self.print_to_terminal(func.__doc__)
            else:
                self.print_to_terminal(f"Aucune aide trouvée pour '{arg}'.")
        else:
            # Affiche la liste des commandes disponibles
            commands = [attr[3:] for attr in dir(self) if attr.startswith('do_')]
            self.print_to_terminal("=== Commandes disponibles ===")
            for cmd in commands:
                self.print_to_terminal(f"{cmd} - {getattr(self, f'do_{cmd}').__doc__.strip().splitlines()[0]}")

    def do_lex(self, line):
        """
        Effectue l'analyse lexicale d'une ligne de code.
        Syntaxe : lex <code>
        """
        if not line.strip():
            self.print_to_terminal("Erreur : Fournissez une ligne de code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            self.print_to_terminal("=== Tokens générés ===")
            for token in self.tokens:
                self.print_to_terminal(str(token))
        except Exception as e:
            self.print_to_terminal(f"Erreur lexicale : {e}")

    def do_parse(self, line):
        """
        Effectue l'analyse syntaxique d'une ligne de code et génère un AST.
        Syntaxe : parse <code>
        """
        if not line.strip():
            self.print_to_terminal("Erreur : Fournissez une ligne ou un bloc de code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            self.print_to_terminal("=== AST généré ===")
            self.print_to_terminal(str(self.ast))
        except Exception as e:
            self.print_to_terminal(f"Erreur syntaxique : {e}")

    def do_run(self, line):
        """
        Exécute le code Draw++ fourni.
        Syntaxe : run <chemin_fichier> | run -c <code>
        """
        args = line.split(maxsplit=1)
        if not args:
            self.print_to_terminal("Erreur : Fournissez un chemin ou du code.")
            return

        try:
            if args[0] == "-c":
                source_code = args[1]
                self.run_code(source_code=source_code)
            else:
                source_file = args[0]
                self.run_code(source_file=source_file)
        except Exception as e:
            self.print_to_terminal(f"Erreur d'exécution : {e}")

    def run_code(self, source_code=None, source_file=None):
        """
        Compile et exécute du code Draw++.

        Args:
            source_code (str, optional): Code Draw++ à exécuter.
            source_file (str, optional): Chemin du fichier Draw++ à exécuter.
        """
        if not source_code and not source_file:
            self.print_to_terminal("Erreur : Fournissez une source de code.")
            return

        # Sauvegarde le code temporaire si nécessaire
        temp_file = "temp.dpp"
        if source_code:
            with open(temp_file, "w") as f:
                f.write(source_code)
            source_file = temp_file

        # Compile et exécute
        try:
            c_file = "temp.c"
            executable = "temp_program"
            compile_cmd = f"python -m compiler.compiler {source_file} -o {c_file}"
            gcc_cmd = f"gcc -I../lib/DPP/include -I../lib/SDL2/include -L../lib -o {executable} {c_file} -ldrawpp -lSDL2 -lm"
            run_cmd = f"./{executable}"

            # Compilation Draw++ vers C
            self.print_to_terminal(f"Compilation : {compile_cmd}")
            result = subprocess.run(compile_cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                self.print_to_terminal(f"Erreur de compilation Draw++ : {result.stderr}")
                return

            # Compilation C vers exécutable
            self.print_to_terminal(f"Compilation : {gcc_cmd}")
            result = subprocess.run(gcc_cmd.split(), capture_output=True, text=True)
            if result.returncode != 0:
                self.print_to_terminal(f"Erreur de compilation C : {result.stderr}")
                return

            # Exécution
            self.print_to_terminal("Exécution de l'exécutable...")
            result = subprocess.run(run_cmd.split(), capture_output=True, text=True)
            self.print_to_terminal(result.stdout)
            if result.returncode != 0:
                self.print_to_terminal(f"Erreur d'exécution : {result.stderr}")
        finally:
            self.cleanup_temp_files([temp_file, c_file, executable])

    def cleanup_temp_files(self, files):
        """
        Supprime les fichiers temporaires générés.

        Args:
            files (list): Liste des fichiers à supprimer.
        """
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def do_save(self, line):
        """
        Sauvegarde le code source, les tokens ou l'AST dans un fichier.
        Syntaxe : save <type> <nom_fichier>
        """
        args = line.split()
        if len(args) != 2:
            self.print_to_terminal("Erreur : Syntaxe incorrecte. Utilisation : save <type> <nom_fichier>")
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
                self.print_to_terminal("Erreur : Données inexistantes à sauvegarder.")
        except Exception as e:
            self.print_to_terminal(f"Erreur de sauvegarde : {e}")

    def do_clear(self, _):
        """
        Efface l'écran.
        """
        if self.terminal_widget:
            self.terminal_widget.delete("1.0", "end")
        else:
            os.system("clear")

    def do_exit(self, _):
        """
        Quitte le terminal.
        """
        self.print_to_terminal("Au revoir !")
        return True


if __name__ == "__main__":
    DrawTerminal().cmdloop()
