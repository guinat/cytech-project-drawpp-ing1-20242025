import tkinter as tk
from tkinter import ttk
from ide.components.editor_tab import add_tab
from ide.components.menu_bar import create_menu_bar
from ide.utils.shortcuts import configure_keyboard_shortcuts
from ide.config.settings import APP_TITLE, APP_DIMENSIONS
from ide.config.styles import apply_styles


def main():
    """
    Main function to initialize and run the Draw++ IDE.
    """
    # Initialize the root window
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(APP_DIMENSIONS)
    root.wm_minsize(width=800, height=600)  # Minimum window size

    # Apply custom styles
    apply_styles()

    # Create a Notebook widget to manage tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create the menu bar
    create_menu_bar(root, notebook, add_tab)

    # Configure keyboard shortcuts
    configure_keyboard_shortcuts(root, notebook, add_tab)

    # Add an initial tab
    add_tab(notebook, title="Untitled")

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
