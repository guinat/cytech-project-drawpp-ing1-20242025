import tkinter as tk
from tkinter import messagebox
from ide.components.editor_tab import update_preview
from ide.utils.file_manager import new_file, open_file, save_file, close_tab
import os

def create_menu_bar(root, notebook, add_tab_callback):
    """
    @brief Creates a menu bar for managing IDE tools.

    @param root The root Tkinter window.
    @param notebook The ttk.Notebook widget where tabs are managed.
    @param add_tab_callback The callback function to add new tabs to the notebook.
    """
    # Create the menu bar
    menubar = tk.Menu(root)

    # "File" menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(
        label="New", command=lambda: new_file(notebook, add_tab_callback))
    file_menu.add_command(
        label="Open", command=lambda: open_file(notebook, add_tab_callback))
    file_menu.add_command(label="Save", command=lambda: save_file(notebook))
    file_menu.add_command(
        label="Close Tab", command=lambda: close_tab(notebook))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # "Run" menu
    run_menu = tk.Menu(menubar, tearoff=0)
    run_menu.add_command(label="Run", command=lambda: run_code(notebook))
    menubar.add_cascade(label="Run", menu=run_menu)

    # "Help" menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: show_about_dialog())
    menubar.add_cascade(label="Help", menu=help_menu)

    # Attach the menu bar to the root window
    root.config(menu=menubar)

def run_code(notebook):
    """
    @brief Compiles and executes the code in the editor, then updates the preview with the generated image.

    @param notebook The ttk.Notebook widget containing the editor and preview.
    """
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    editor = getattr(current_frame, "editor", None)

    if editor:
        try:
            # Extract the code from the editor
            code = editor.get("1.0", "end-1c")

            # Save the code to a temporary Draw++ source file
            source_file = "temp.dpp"
            with open(source_file, "w") as file:
                file.write(code)

            # Temporary output C file and executable name
            output_file = "temp.c"
            executable = "temp_program"

            # Commands to compile Draw++ and C code
            compile_drawpp_command = f"python -m compiler.compiler {source_file} -o {output_file}"
            compile_c_command = f"gcc -I../lib/DPP/include -I../lib/SDL2/include -L../lib -o {executable} {output_file} -ldrawpp -lSDL2 -lm"
            run_command = f"./{executable}"

            # Compile Draw++ to C
            if os.system(compile_drawpp_command) != 0:
                return

            # Compile the C code to an executable
            if os.system(compile_c_command) == 0:
                # Set the DISPLAY environment variable and execute the program
                os.environ["DISPLAY"] = ":0"
                os.system(run_command)

                # Update the preview with the generated image
                update_preview(current_frame, "output.bmp")

        except Exception as e:
            print(f"[ERROR] Exception during execution: {e}")


def show_about_dialog():
    """
    @brief Displays an 'About' dialog box with information about the IDE.
    """
    messagebox.showinfo("About", "Draw++ IDE\nVersion 1.0")
