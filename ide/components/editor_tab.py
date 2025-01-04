import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Pour afficher l'image générée
from ide.config.settings import THEME_COLORS, FONT_FAMILY, FONT_SIZE
from ide.utils.error_analyzer import ErrorAnalyzer
from ide.utils.file_manager import save_file, file_paths

# when you open a new tab, this is the default code
initial_content = 'var int windowHeight = 500;\nvar int windowWidth = 500;'

class ErrorHighlighter:
    """
    @brief Manages error highlighting and suggestions in the text editor.
    """

    def __init__(self, text_widget):
        """
        @brief Initializes the error highlighter.
        @param text_widget The text widget to associate with this highlighter.
        """
        self.text_widget = text_widget
        self.error_tags = {}
        self.suggestion_tags = {}

    def clear_highlights(self):
        """
        @brief Clears all error and suggestion highlights.
        """
        for tag in self.text_widget.tag_names():
            if tag.startswith("error_") or tag.startswith("suggestion_"):
                self.text_widget.tag_delete(tag)
        self.error_tags = {}
        self.suggestion_tags = {}

    def highlight_error(self, start_index, end_index, error_message):
        """
        @brief Highlights an error region and stores its message.
        @param start_index The start index of the error.
        @param end_index The end index of the error.
        @param error_message The error message to associate with the error.
        """
        line_num = str(start_index).split('.')[0]
        tag_name = f"error_{line_num}"

        if tag_name in self.error_tags:
            self.text_widget.tag_delete(tag_name)

        self.text_widget.tag_configure(tag_name,
                                       underline=True,
                                       foreground="red",
                                       underlinefg="red")

        line_start = f"{line_num}.0"
        line_end = f"{line_num}.end"
        self.text_widget.tag_add(tag_name, line_start, line_end)
        self.error_tags[tag_name] = error_message

    def add_suggestion(self, index, suggestion):
        """
        @brief Adds a suggestion for the specified line.
        @param index The index where the suggestion is applied.
        @param suggestion The suggestion text to display.
        """
        line_num = str(index).split('.')[0]
        tag_name = f"suggestion_{line_num}"

        if tag_name in self.suggestion_tags:
            self.text_widget.tag_delete(tag_name)

        self.text_widget.tag_configure(tag_name, foreground="green")

        if isinstance(suggestion, list):
            self.suggestion_tags[tag_name] = suggestion
        else:
            self.suggestion_tags[tag_name] = [suggestion]


class LineNumbers(tk.Canvas):
    """
    @brief Widget for displaying line numbers.
    """

    def __init__(self, master, *args, **kwargs):
        """
        @brief Initializes the LineNumbers widget.
        @param master The parent widget.
        @param args Additional positional arguments.
        @param kwargs Additional keyword arguments.
        """
        super().__init__(master, *args, **kwargs)
        self.text_widget = None
        self.configure(bg=THEME_COLORS["bg"], highlightthickness=0)

    def attach(self, text_widget):
        """
        @brief Attaches a text widget to the LineNumbers widget.
        @param text_widget The text widget to associate.
        """
        self.text_widget = text_widget
        self.text_widget.bind('<<Modified>>', self.update_line_numbers)
        self.text_widget.bind('<Configure>', self.update_line_numbers)
        self.text_widget.bind('<FocusIn>', self.update_line_numbers)
        self.text_widget.bind('<MouseWheel>', self.update_line_numbers)

    def update_line_numbers(self, event=None):
        """
        @brief Updates the displayed line numbers.
        @param event Optional event that triggered the update.
        """
        self.delete("all")

        if not self.text_widget:
            return

        temp = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(temp)
            if dline is None:
                break

            y = dline[1]
            line_num = str(temp).split('.')[0]
            self.create_text(
                35, y,
                anchor="ne",
                text=line_num,
                font=(FONT_FAMILY, FONT_SIZE),
                fill=THEME_COLORS["fg"]
            )
            temp = self.text_widget.index(f"{temp}+1line")


class EnhancedText(tk.Text):
    """
    @brief Enhanced text widget with error highlighting and suggestions.
    """

    def __init__(self, *args, **kwargs):
        """
        @brief Initializes the enhanced text widget.
        @param args Positional arguments for the text widget.
        @param kwargs Keyword arguments for the text widget.
        """
        super().__init__(*args, **kwargs)
        self.highlighter = ErrorHighlighter(self)
        self.error_analyzer = ErrorAnalyzer()

        self.bind('<KeyRelease>', self._on_text_change)
        self.bind('<Button-3>', self._show_suggestion_menu)
        self.bind('<Motion>', self._show_error_tooltip)

        self.after_id = None
        self.tooltip = None

    def _on_text_change(self, event=None):
        """
        @brief Handles text change events and schedules code analysis.
        @param event Optional event that triggered the change.
        """
        if self.after_id:
            self.after_cancel(self.after_id)
        self.after_id = self.after(1000, self._check_code)

    def _check_code(self):
        """
        @brief Performs code analysis and applies highlights or suggestions.
        """
        self.highlighter.clear_highlights()
        code = self.get("1.0", "end-1c")

        if not code.strip():
            return

        success, error_msg, suggestions = self.error_analyzer.analyze_code(
            code)

        if not success:
            line_num = self.error_analyzer._extract_line_number(
                error_msg, code)
            self.highlighter.highlight_error(
                f"{line_num}.0", f"{line_num}.end", error_msg)

            if suggestions and line_num in suggestions:
                for suggestion in suggestions[line_num]:
                    self.highlighter.add_suggestion(
                        f"{line_num}.0", suggestion)

    def _show_suggestion_menu(self, event):
        """
        @brief Displays a context menu with error details and suggestions.
        @param event The event triggering the menu display.
        """
        index = self.index(f"@{event.x},{event.y}")
        line_num = int(index.split('.')[0])
        tags = self.tag_names(index)
        error_tags = [tag for tag in tags if tag.startswith('error_')]

        if error_tags:
            menu = tk.Menu(self, tearoff=0)

            error_msg = None
            for tag in error_tags:
                if tag in self.highlighter.error_tags:
                    error_msg = self.highlighter.error_tags[tag]
                    break

            if error_msg:
                error_item = tk.Menu(menu, tearoff=0)
                error_item.add_command(
                    label=error_msg,
                    state="disabled",
                    background="#ffeeee",
                    foreground="red"
                )
                menu.add_cascade(label="Error Details", menu=error_item)

                menu.add_separator()

                fix_menu = tk.Menu(menu, tearoff=0)
                suggestions = self.highlighter.suggestion_tags.get(
                    f"suggestion_{line_num}.0", [])
                if isinstance(suggestions, str):
                    suggestions = [suggestions]

                for suggestion in suggestions:
                    fix_menu.add_command(
                        label=suggestion,
                        command=lambda s=suggestion: self._apply_suggestion(
                            line_num, s),
                        foreground="green",
                        background="#eeffee"
                    )

                menu.add_cascade(label="Suggested Fixes", menu=fix_menu)
                menu.add_separator()
                menu.add_command(
                    label="Ignore Error",
                    command=lambda: self.highlighter.clear_highlights()
                )

            menu.post(event.x_root, event.y_root)

    def _apply_suggestion(self, line_num, suggestion):
        """
        @brief Applies a suggestion to the specified line.
        @param line_num The line number to apply the suggestion.
        @param suggestion The suggestion text.
        """
        self.delete(f"{line_num}.0", f"{line_num}.end")
        self.insert(f"{line_num}.0", suggestion)
        self._check_code()

    def _show_error_tooltip(self, event):
        """
        @brief Displays an error tooltip on mouse hover.
        @param event The event triggering the tooltip display.
        """
        index = self.index(f"@{event.x},{event.y}")
        line_num = int(index.split('.')[0])

        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

        for tag in self.tag_names():
            if tag.startswith('error_'):
                try:
                    start_index = self.tag_ranges(tag)[0]
                    error_line = int(str(start_index).split('.')[0])

                    if error_line == line_num:
                        error_msg = self.highlighter.error_tags.get(
                            tag, "Syntax error")

                        self.tooltip = tk.Toplevel(self)
                        self.tooltip.wm_overrideredirect(True)
                        self.tooltip.wm_geometry(
                            f"+{event.x_root + 10}+{event.y_root + 10}")

                        label = tk.Label(
                            self.tooltip,
                            text=error_msg,
                            justify=tk.LEFT,
                            background="#ffece6",
                            relief=tk.SOLID,
                            borderwidth=1,
                            font=(FONT_FAMILY, FONT_SIZE - 1),
                            padx=5,
                            pady=3
                        )
                        label.pack()

                        self.tooltip.bind(
                            '<Leave>', lambda e: self.tooltip.destroy())
                        self.bind(
                            '<Leave>', lambda e: self.tooltip.destroy() if self.tooltip else None)
                        break
                except (IndexError, ValueError):
                    continue


def add_tab(notebook, title="Untitled"):
    """
    @brief Adds a new tab with an enhanced editor and preview area to a Notebook widget.

    @param notebook The ttk.Notebook widget to add the tab to.
    @param title The title of the new tab. Defaults to "Untitled".
    @return A tuple containing the Text widget for the editor and the tab's frame.
    """
    frame = ttk.Frame(notebook)
    frame.configure(style="TFrame")

    paned_window = tk.PanedWindow(
        frame,
        orient=tk.HORIZONTAL,
        bg=THEME_COLORS["border"],
        sashwidth=5
    )
    paned_window.pack(fill=tk.BOTH, expand=True)

    editor_frame = tk.Frame(paned_window, bg=THEME_COLORS["bg"])

    line_numbers = LineNumbers(editor_frame, width=40)
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    editor = EnhancedText(
        editor_frame,
        wrap=tk.NONE,
        bg=THEME_COLORS["bg"],
        fg=THEME_COLORS["fg"],
        font=(FONT_FAMILY, FONT_SIZE),
        relief=tk.FLAT,
        borderwidth=2,
        padx=5,
        pady=2,
        undo=True,
        maxundo=-1
    )
    
    if initial_content:
        editor.insert("1.0", initial_content)
    
    editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(5, 5))

    line_numbers.attach(editor)

    editor_frame.pack(fill=tk.BOTH, expand=True)
    paned_window.add(editor_frame)

    preview_frame = tk.Frame(paned_window, bg=THEME_COLORS["button"])
    preview_label = tk.Label(
        preview_frame,
        text="Preview Area",
        bg=THEME_COLORS["button"],
        fg=THEME_COLORS["fg"]
    )
    preview_label.pack(fill=tk.BOTH, expand=True)

    paned_window.add(preview_frame)

    paned_window.paneconfigure(editor_frame, minsize=300)
    paned_window.paneconfigure(preview_frame, minsize=200)

    frame.paned_window = paned_window
    frame.editor = editor
    frame.preview_frame = preview_frame
    frame.preview_label = preview_label

    notebook.add(frame, text=title)
    notebook.select(frame)

    line_numbers.update_line_numbers()

    return editor, frame

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

def update_preview(frame, image_path="output.bmp"):
    """
    @brief Updates the preview area with the generated image.
    @param frame The frame containing the preview area.
    @param image_path The path to the generated image.
    """
    try:
        image = Image.open(image_path)
        orig_width, orig_height = image.size # PIL lib
        aspect_ratio = orig_width / orig_height
        
        MAX_WIDTH = 500
        MAX_HEIGHT = 500
        
        # respects aspect ratio
        if orig_width > MAX_WIDTH or orig_height > MAX_HEIGHT:
            if aspect_ratio > 1:  # wider than tall
                new_width = MAX_WIDTH
                new_height = int(MAX_WIDTH / aspect_ratio)
            else:  # taller than wide
                new_height = MAX_HEIGHT
                new_width = int(MAX_HEIGHT * aspect_ratio)
        else:
            new_width = orig_width
            new_height = orig_height

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        frame.preview_label.configure(image=photo, text="")
        frame.preview_label.image = photo

        
    except Exception as e:
        print(f"Error updating preview: {e}")