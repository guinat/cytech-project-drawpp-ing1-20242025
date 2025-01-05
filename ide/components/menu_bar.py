import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
from ide.components.editor_tab import update_preview
from ide.utils.file_manager import new_file, open_file, save_file
from ide.components.editor_tab import close_tab
import os

# Variable globale pour stocker le chemin de l'image générée
generated_image_path = None


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
    file_menu.add_command(label="Download Image", command=download_image)  # New option
    file_menu.add_command(label="Close Tab", command=lambda: close_tab(notebook))
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
    global generated_image_path
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
                messagebox.showerror("Error", "Compilation of Draw++ to C failed.")
                return

            # Compile the C code to an executable
            if os.system(compile_c_command) == 0:
                # Set the DISPLAY environment variable and execute the program
                os.environ["DISPLAY"] = ":0"
                os.system(run_command)

                # Update the preview with the generated image
                image_path = "output.bmp"
                update_preview(current_frame, image_path)

                # Store the path of the generated image
                generated_image_path = image_path

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during execution: {e}")


def download_image():
    """
    @brief Downloads the generated output image as a PNG file.
    """
    global generated_image_path

    # Vérifie si l'image a été générée
    if not generated_image_path or not os.path.exists(generated_image_path):
        messagebox.showerror("Error", "No image found to download.")
        return

    try:
        # Ouvre l'image BMP
        image = Image.open(generated_image_path)

        # Demande à l'utilisateur où sauvegarder l'image
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save Image As"
        )

        if save_path:  # Si l'utilisateur a spécifié un chemin
            # Sauvegarde l'image au format PNG
            image.save(save_path, "PNG")
            messagebox.showinfo("Success", f"Image saved successfully as {save_path}")
        else:
            messagebox.showinfo("Cancelled", "Image download cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download image: {e}")


def show_about_dialog():
    """
    @brief Displays an 'About' dialog box with information about the IDE.
    """
    messagebox.showinfo("About", "Draw++ IDE\nVersion 1.0")
