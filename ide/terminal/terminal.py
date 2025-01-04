import sys
import os
# Ajoute la racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import cmd
import subprocess
from compiler.lexer.lexer import Lexer
from compiler.lexer.tokens import Token, TokenType
from compiler.parser.parser import Parser
from compiler.parser.syntax_tree import *

class DrawTerminal(cmd.Cmd):
    # Message d'introduction affiché lorsque le terminal démarre
    intro = "Bienvenue dans le terminal Draw++ ! Tapez 'help' pour la liste des commandes."
    prompt = "draw++> "

    def do_help(self, line):
        """Affiche l'aide pour les commandes."""
        print("Liste des commandes disponibles :")
        print(" - lex       : Analyse lexicale d'une ligne de code")
        print(" - parse     : Analyse syntaxique d'un code complet")
        print(" - see       : Affiche les fichiers à charger")
        print(" - load      : Charge un fichier Draw++ et l'analyse")
        print(" - save      : Sauvegarde du code source, des tokens ou de l'AST dans un fichier")
        print(" - run       : Exécute le code et affiche le résultat")
        print(" - debug     : Débogue le programme étape par étape")
        print(" - compile   : Vérification sémantique et compilation")
        print(" - history   : Affiche l'historique des commandes")
        print(" - clear     : Efface l'écran du terminal")
        print(" - exit      : Quitte le terminal")


    def __init__(self):
        super().__init__()
        self.source_code = None
        self.tokens = None
        self.ast = None
        self.check_imports()

    def check_imports(self):
        print("=== Vérification des importations ===")
        try:
            print("Program class:", Program)
            print("VarDecl class:", VarDecl)
            print("Assign class:", Assign)
            print("Num class:", Num)
            print("StringLiteral class:", StringLiteral)
            print("BooleanLiteral class:", BooleanLiteral)
            print("BinOp class:", BinOp)
            print("Var class:", Var)
            print("Toutes les classes sont correctement importées.")
        except NameError as e:
            print("Erreur d'importation :", e)

    def do_lex(self, line):
        """Analyse lexicale d'une ligne de code."""
        if not line.strip():
            print("Erreur : Veuillez fournir une ligne de code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            print("Tokens générés :")
            for token in self.tokens:
                print(token)
        except ValueError as e:
            print(f"Erreur lexicale : {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

    def do_parse(self, line):
        """
        Analyse syntaxique d'une ligne ou d'un bloc de code et affiche l'AST généré.
        """
        if not line.strip():
            print("Erreur : Veuillez fournir une ligne ou un bloc de code.")
            return

        try:
            lexer = Lexer(line)
            self.tokens = lexer.tokenize()
            print("=== Tokens générés ===")
            for token in self.tokens:
                print(token)

            parser = Parser(self.tokens)
            self.ast = parser.parse()

            if isinstance(self.ast, Program):
                print("\n=== Analyse syntaxique réussie ===")
                print("AST généré :")
                print(self.ast)
            else:
                print("Erreur : Aucun AST n'a été généré ou le format est incorrect.")

            self.source_code = line
        except Exception as e:
            print(f"\nErreur lors de l'analyse syntaxique : {e}")

    def run_code(self, source_code=None, source_file=None):
        """
        Compile et exécute le code Draw++ fourni, ou le contenu d'un fichier.

        Args:
            source_code (str, optional): Le code Draw++ à exécuter.
            source_file (str, optional): Le chemin d'un fichier Draw++ à exécuter.
        """
        try:
            # Vérifie que l'une des sources est fournie
            if source_code is None and source_file is None:
                print("[ERROR] Aucune source de code fournie.")
                return

            # Si le code est fourni directement, sauvegarde dans un fichier temporaire
            if source_code is not None:
                source_file = "temp.dpp"
                with open(source_file, "w") as file:
                    file.write(source_code)

            # Temporary output C file and executable name
            output_file = "temp.c"
            executable = "temp_program"

            # Commands to compile Draw++ and C code
            compile_drawpp_command = f"python -m compiler.compiler {source_file} -o {output_file}"
            compile_c_command = f"gcc -I../lib/DPP/include -I../lib/SDL2/include -L../lib -o {executable} {output_file} -ldrawpp -lSDL2 -lm"
            run_command = f"./{executable}"

            # Compile Draw++ to C
            print(f"[INFO] Compiling Draw++ file: {source_file}")
            if os.system(compile_drawpp_command) != 0:
                print("[ERROR] Compilation Draw++ to C failed.")
                return

            # Compile the C code to an executable
            print(f"[INFO] Compiling C file: {output_file}")
            if os.system(compile_c_command) != 0:
                print("[ERROR] Compilation C to executable failed.")
                return

            # Set the DISPLAY environment variable and execute the program
            print("[INFO] Running the executable...")
            os.environ["DISPLAY"] = ":0"
            os.system(run_command)

            print("[INFO] Execution completed successfully.")

        except Exception as e:
            print(f"[ERROR] Exception during execution: {e}")

        finally:
            # Cleanup temporary files
            self.cleanup_temp_files([source_file, output_file, executable])

    def cleanup_temp_files(self, files):
        """
        Supprime les fichiers temporaires générés.

        Args:
            files (list): Liste des fichiers à supprimer.
        """
        for file in files:
            try:
                if file and os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(f"[WARNING] Failed to remove {file}: {e}")


    def do_run(self, line):
        """
        Exécute un fichier ou une ligne de code Draw++.

        Syntaxe :
            run <nom_fichier>     - Exécute un fichier Draw++.
            run -c <code>         - Exécute directement une ligne de code.
        """
        args = line.split(maxsplit=1)
        if not args:
            print("[ERROR] Commande invalide. Utilisez 'run <nom_fichier>' ou 'run -c <code>'.")
            return

        try:
            if args[0] == "-c" and len(args) > 1:
                # Exécute le code directement
                self.run_code(source_code=args[1])
            else:
                # Exécute un fichier Draw++
                source_file = args[0]
                if not source_file.endswith(".dpp"):
                    source_file += ".dpp"

                if not os.path.exists(source_file):
                    print(f"[ERROR] Fichier '{source_file}' introuvable.")
                    return

                self.run_code(source_file=source_file)

        except Exception as e:
            print(f"[ERROR] Exception during execution: {e}")

    def do_see(self, line):
        """
        Liste les fichiers disponibles dans le répertoire pour chargement.
        """
        directory = "examples"
        try:
            if not os.path.exists(directory):
                print(f"Répertoire '{directory}' introuvable.")
                return

            files = os.listdir(directory)
            if not files:
                print(f"Aucun fichier trouvé dans '{directory}'.")
                return

            print(f"Fichiers disponibles dans '{directory}' :")
            for file in files:
                print(f" - {file}")
        except Exception as e:
            print(f"Erreur lors de la lecture du répertoire : {e}")

    def do_save(self, line):
        """
        Sauvegarde le code source, les tokens ou l'AST dans un fichier.
        Syntaxe : save [source|tokens|ast] <nom_fichier>
        """
        args = line.split()
        if len(args) != 2:
            print("Erreur : Syntaxe incorrecte. Utilisation : save [source|tokens|ast] <nom_fichier>")
            return

        save_type, filename = args
        directory = "saves"

        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)

        try:
            if save_type == "source":
                if self.source_code is None:
                    print("Erreur : Aucun code source à sauvegarder.")
                    return
                with open(filepath, "w") as file:
                    file.write(self.source_code)
                print(f"Code source sauvegardé dans {filepath}.")

            elif save_type == "tokens":
                if self.tokens is None:
                    print("Erreur : Aucun token à sauvegarder.")
                    return
                with open(filepath, "w") as file:
                    for token in self.tokens:
                        file.write(str(token) + "\n")
                print(f"Tokens sauvegardés dans {filepath}.")

            elif save_type == "ast":
                if self.ast is None:
                    print("Erreur : Aucun AST à sauvegarder.")
                    return
                with open(filepath, "w") as file:
                    file.write(str(self.ast))
                print(f"AST sauvegardé dans {filepath}.")

            else:
                print("Erreur : Type de sauvegarde inconnu. Utilisation : save [source|tokens|ast] <nom_fichier>")

        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def do_load(self, filepath):
        """
        @brief Charge un fichier Draw++ (.dpp) et l'analyse.

        @param filepath Chemin du fichier à charger.
        """
        directory = "saves"
        if not filepath.strip():
            print("Erreur : Veuillez fournir le nom d'un fichier.")
            return

        filepath = os.path.join(directory, filepath)
        if not filepath.endswith(".dpp"):
            filepath += ".dpp"

        try:
            with open(filepath, 'r') as file:
                content = file.read()

            print(f"\n=== Contenu du fichier {filepath} ===")
            print(content)

            lexer = Lexer(content)
            self.tokens = lexer.tokenize()

            print("\n=== Tokens générés ===")
            for token in self.tokens:
                print(token)

            parser = Parser(self.tokens)
            self.ast = parser.parse()

            print("\n=== Analyse syntaxique réussie ===")
            print("AST généré :")
            print(self.ast)

            self.source_code = content
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{filepath}' est introuvable.")
        except ValueError as e:
            print(f"Erreur lors de l'analyse lexicale : {e}")
        except Exception as e:
            print(f"Erreur lors de l'analyse syntaxique : {e}")



    def do_exit(self, _):
        """Quitte le terminal."""
        print("Au revoir !")
        return True

# Démarre le terminal
if __name__ == "__main__":
    DrawTerminal().cmdloop()

