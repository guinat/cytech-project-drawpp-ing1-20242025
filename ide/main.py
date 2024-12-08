import tkinter as tk
from tkinter import Menu, ttk
from ui import setup_menu, create_console
from file_manager import new_file

def main():
    root = tk.Tk()
    root.title("Draw++")
    root.geometry("800x600")  

    # Create the main frames
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Notebook for multi-file support
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Add a default editor tab
    new_file(notebook)

    # Menu bar
    menubar = Menu(root)
    setup_menu(menubar, root, notebook)
    root.config(menu=menubar)

    # Bottom console
    console = create_console(bottom_frame)

    run_button = tk.Button(bottom_frame, text="Run", command=lambda: console.insert(tk.END, "Running code...\n"))
    run_button.pack(side=tk.RIGHT, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
