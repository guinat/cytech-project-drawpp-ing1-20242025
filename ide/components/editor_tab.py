import tkinter as tk
from tkinter import ttk
from ide.config.settings import THEME_COLORS, FONT_FAMILY, FONT_SIZE


class LineNumbers(tk.Canvas):
    """
    @brief Widget for displaying line numbers alongside a text editor.
    """

    def __init__(self, master, *args, **kwargs):
        """
        @brief Initializes the LineNumbers widget.

        @param master The parent widget.
        @param args Additional positional arguments for the Canvas.
        @param kwargs Additional keyword arguments for the Canvas.
        """
        super().__init__(master, *args, **kwargs)
        self.text_widget = None
        self.configure(bg="#f0f0f0", highlightthickness=0)

    def attach(self, text_widget):
        """
        @brief Attaches a Text widget to the LineNumbers widget.

        @param text_widget The Text widget to attach.
        """
        self.text_widget = text_widget
        self.text_widget.bind("<KeyRelease>", self.update_line_numbers)
        self.text_widget.bind("<MouseWheel>", self.update_line_numbers)
        self.text_widget.bind("<ButtonRelease>", self.update_line_numbers)
        self.text_widget.bind("<Configure>", self.update_line_numbers)

    def update_line_numbers(self, event=None):
        """
        @brief Updates the line numbers based on the attached Text widget.

        @param event The triggering event (optional).
        """
        if not self.text_widget:
            return

        # Clear existing line numbers
        self.delete("all")

        # Loop through all visible lines
        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break

            # Get the vertical position
            y = dline[1] + 6  # Add vertical offset for alignment
            line_number = str(i).split(".")[0]  # Extract the line number
            self.create_text(5, y, anchor="nw", text=line_number, fill="#333333", font=("Consolas", 10))
            i = self.text_widget.index(f"{i}+1line")


def add_tab(notebook, title="Untitled"):
    """
    @brief Adds a new tab with an editor and preview area to a Notebook widget.

    @param notebook The ttk.Notebook widget to add the tab to.
    @param title The title of the new tab. Defaults to "Untitled".

    @return A tuple containing the Text widget for the editor and the tab's frame.
    """
    # Create a new frame for the tab
    frame = ttk.Frame(notebook)
    frame.configure(style="TFrame")

    # Create a PanedWindow for splitting the editor and preview
    paned_window = tk.PanedWindow(frame, orient=tk.HORIZONTAL, bg=THEME_COLORS["border"], sashwidth=5)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Editor area (with line numbers)
    editor_frame = tk.Frame(paned_window, bg=THEME_COLORS["bg"])

    # Line numbers widget
    line_numbers = LineNumbers(editor_frame, width=40)
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    # Text editor widget
    editor = tk.Text(
        editor_frame,
        wrap=tk.NONE,
        bg=THEME_COLORS["bg"],
        fg=THEME_COLORS["fg"],
        font=(FONT_FAMILY, FONT_SIZE),
        relief=tk.FLAT,
        borderwidth=2,
        padx=5,
        pady=2,
        undo=True  # Enable undo/redo functionality
    )
    editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(5, 5))

    # Attach the editor to the line numbers widget
    line_numbers.attach(editor)

    # Add the editor and line numbers to the editor frame
    editor_frame.pack(fill=tk.BOTH, expand=True)
    paned_window.add(editor_frame)

    # Preview area
    preview_frame = tk.Frame(paned_window, bg=THEME_COLORS["button"])
    preview_label = tk.Label(preview_frame, text="Preview Area", bg=THEME_COLORS["button"], fg=THEME_COLORS["fg"])
    preview_label.pack(fill=tk.BOTH, expand=True)

    paned_window.add(preview_frame)

    # Configure PanedWindow responsiveness
    paned_window.paneconfigure(editor_frame, minsize=300)
    paned_window.paneconfigure(preview_frame, minsize=200)

    # Store the PanedWindow in the frame attribute
    frame.paned_window = paned_window

    # Store the editor in the frame attribute for later access
    frame.editor = editor

    # Add the frame to the notebook
    notebook.add(frame, text=title)
    notebook.select(frame)

    # Update line numbers for the new tab
    line_numbers.update_line_numbers()

    return editor, frame
