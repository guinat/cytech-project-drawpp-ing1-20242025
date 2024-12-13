import tkinter as tk
from tkinter import ttk
from ide.components.editor_tab import add_tab
from ide.components.menu_bar import create_menu_bar
from ide.utils.shortcuts import configure_keyboard_shortcuts
from ide.config.settings import APP_TITLE, APP_DIMENSIONS
from ide.config.styles import apply_styles


def main():
    """
    @brief Main function to initialize and run the Draw++ IDE.
    """
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(APP_DIMENSIONS)
    root.wm_minsize(800, 600)  # Minimum window size

    # Apply custom styles
    apply_styles()

    # Notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create the menu bar
    create_menu_bar(root, notebook, add_tab)

    # Configure keyboard shortcuts
    configure_keyboard_shortcuts(root, notebook, add_tab)

    # Add a default tab
    add_tab(notebook, title="Untitled")

    # Start the main application loop
    root.mainloop()


if __name__ == "__main__":
    main()
