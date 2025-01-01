import os
from tkinter import filedialog, messagebox

# A dictionary to keep track of file paths associated with each tab
file_paths = {}


def open_file(notebook, add_tab_callback):
    """
    @brief Opens an existing file and loads its content into a new tab.

    @param notebook The ttk.Notebook widget where the tabs are managed.
    @param add_tab_callback A callback function to add a new tab to the notebook.
    """
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()

            # Add a new tab with the file content
            file_name = os.path.basename(file_path)
            editor, frame = add_tab_callback(notebook, title=file_name)
            editor.insert("1.0", content)  # Load content into the editor
            file_paths[frame] = file_path  # Associate the tab with the file path
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file:\n{e}")


def save_file(notebook):
    """
    @brief Saves the content of the currently active tab to a file.

    @param notebook The ttk.Notebook widget where the tabs are managed.
    """
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    editor = getattr(current_frame, "editor", None)
    file_path = file_paths.get(current_frame)

    if not editor:
        return

    if file_path is None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return

    try:
        with open(file_path, "w") as file:
            file.write(editor.get("1.0", "end-1c"))  # Save editor content
        file_paths[current_frame] = file_path
        file_name = os.path.basename(file_path)
        notebook.tab(current_frame, text=file_name)  # Update the tab's title
    except Exception as e:
        messagebox.showerror("Error", f"Unable to save file:\n{e}")


def new_file(notebook, add_tab_callback):
    """
    @brief Creates a new empty tab.

    @param notebook The ttk.Notebook widget where the tabs are managed.
    @param add_tab_callback A callback function to add a new tab to the notebook.
    """
    editor, frame = add_tab_callback(notebook, title="Untitled")
    file_paths[frame] = None


def close_tab(notebook):
    """
    @brief Closes the currently active tab.

    @param notebook The ttk.Notebook widget where the tabs are managed.
    """
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    editor = getattr(current_frame, "editor", None)

    if editor and editor.get("1.0", "end-1c").strip():
        result = messagebox.askyesnocancel("Close Tab", "Do you want to save changes before closing?")
        if result is None:  # Cancel
            return
        elif result:  # Yes
            save_file(notebook)

    notebook.forget(current_tab)
    file_paths.pop(current_frame, None)
