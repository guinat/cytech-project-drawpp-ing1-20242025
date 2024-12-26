import tkinter as tk
from tkinter import messagebox
from utils.file_manager import new_file, open_file, save_file, close_tab


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
    file_menu.add_command(label="New", command=lambda: new_file(notebook, add_tab_callback))
    file_menu.add_command(label="Open", command=lambda: open_file(notebook, add_tab_callback))
    file_menu.add_command(label="Save", command=lambda: save_file(notebook))
    file_menu.add_command(label="Close Tab", command=lambda: close_tab(notebook))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    # "Run" menu
    run_menu = tk.Menu(menubar, tearoff=0)
    run_menu.add_command(label="Run", command=lambda: print("Running the code..."))  # Simple example
    menubar.add_cascade(label="Run", menu=run_menu)

    # "Help" menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: show_about_dialog())
    menubar.add_cascade(label="Help", menu=help_menu)

    # Attach the menu bar to the root window
    root.config(menu=menubar)


def show_about_dialog():
    """
    @brief Displays an 'About' dialog box with information about the IDE.
    """
    messagebox.showinfo("About", "Draw++ IDE\nVersion 1.0")
