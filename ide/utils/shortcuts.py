from ide.utils.file_manager import new_file, open_file, save_file, close_tab
from ide.config.settings import SHORTCUTS


def configure_keyboard_shortcuts(root, notebook, add_tab_callback):
    """
    @brief Configures keyboard shortcuts for the IDE.

    @param root The root Tkinter window.
    @param notebook The ttk.Notebook widget managing the tabs.
    @param add_tab_callback A callback function to add a new tab to the notebook.
    """
    root.bind(SHORTCUTS["new_file"], lambda event: new_file(
        notebook, add_tab_callback))  # Ctrl+N
    root.bind(SHORTCUTS["open_file"], lambda event: open_file(
        notebook, add_tab_callback))  # Ctrl+O
    root.bind(SHORTCUTS["save_file"],
              lambda event: save_file(notebook))  # Ctrl+S
    root.bind(SHORTCUTS["close_tab"],
              lambda event: close_tab(notebook))  # Ctrl+W
    root.bind(SHORTCUTS["select_all"],
              lambda event: select_all(notebook))  # Ctrl+A


def select_all(notebook):
    """
    @brief Selects all text in the active editor.

    @param notebook The ttk.Notebook widget managing the tabs.
    """
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    editor = getattr(current_frame, "editor", None)
    if editor:
        editor.tag_add("sel", "1.0", "end")
