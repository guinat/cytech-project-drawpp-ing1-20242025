from tkinter import Menu
import tkinter as tk

def setup_menu(menubar, root, notebook):
    from file_manager import new_file, close_tab, open_file, save_file

    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: new_file(notebook))
    file_menu.add_command(label="Open", command=lambda: open_file(notebook))
    file_menu.add_command(label="Save", command=lambda: save_file(notebook))
    file_menu.add_command(label="Close Tab", command=lambda: close_tab(notebook))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

def create_console(parent):
    console = tk.Text(parent, height=5, bg="gray", fg="white")
    console.pack(fill=tk.BOTH)
    return console
