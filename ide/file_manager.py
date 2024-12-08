import os
from tkinter import filedialog, messagebox, ttk
import tkinter as tk

file_paths = {}  

def open_file(notebook):
    file_path = filedialog.askopenfilename(filetypes=[("Draw++ Files", "*.dpp"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()

            # Add a new tab for the opened file
            file_name = os.path.basename(file_path)
            editor, frame = add_tab(notebook, title=file_name)
            editor.insert("1.0", content)  # Load file content into the editor
            file_paths[frame] = file_path  # Store the file path
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

def save_file(notebook):
    current_frame = notebook.nametowidget(notebook.select())
    editor = current_frame.editor  # Access the editor widget for the current tab
    file_path = file_paths.get(current_frame)

    if file_path is None:
        file_path = filedialog.asksaveasfilename(defaultextension=".dpp", filetypes=[("Draw++ Files", "*.dpp"), ("All Files", "*.*")])
        if not file_path:  # If user cancels, return
            return

    try:
        with open(file_path, "w") as file:
            file.write(editor.get("1.0", "end-1c"))  # Save editor content
        file_paths[current_frame] = file_path  # Update the file path
        file_name = os.path.basename(file_path)
        notebook.tab(current_frame, text=file_name)  # Update tab title
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")

def add_tab(notebook, title="Untitled"):
    frame = ttk.Frame(notebook)

    # PanedWindow to divide editor and preview
    paned_window = tk.PanedWindow(frame, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Text editor
    editor_frame = tk.Frame(paned_window)
    editor = tk.Text(editor_frame, wrap=tk.NONE)
    editor.pack(fill=tk.BOTH, expand=True)
    paned_window.add(editor_frame)  

    # Assign the editor to the frame for later access
    frame.editor = editor

    # Preview area
    preview_frame = tk.Frame(paned_window, bg="lightgray")
    preview_label = tk.Label(preview_frame, text="Preview Area", bg="lightgray")
    preview_label.pack(fill=tk.BOTH, expand=True)
    paned_window.add(preview_frame)  

    # Add the PanedWindow to the tab
    notebook.add(frame, text=title)
    notebook.select(frame)

    # Place the dividing line in the middle after layout
    def place_sash():
        paned_window.sash_place(0, notebook.winfo_width() // 2, 0)

    frame.after(100, place_sash)  

    return editor, frame

def new_file(notebook):
    editor, frame = add_tab(notebook, title="Untitled")
    file_paths[frame] = None  

def close_tab(notebook):
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    editor = current_frame.editor

    
    if editor.get("1.0", "end-1c").strip():
        if tk.messagebox.askyesnocancel("Close Tab", "Do you want to save changes before closing?"):
            save_file(notebook)

    notebook.forget(current_tab)  
    file_paths.pop(current_frame, None)  