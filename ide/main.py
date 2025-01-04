import tkinter as tk
from tkinter import ttk
from ide.components.editor_tab import add_tab
from ide.components.menu_bar import create_menu_bar
from ide.utils.shortcuts import configure_keyboard_shortcuts
from ide.config.settings import APP_TITLE, APP_DIMENSIONS
from ide.config.styles import apply_styles
import subprocess
import threading
from queue import Queue, Empty


class TerminalFrame(tk.Frame):
    """
    A frame containing a simple terminal with an input field and an output display.
    """
    def __init__(self, parent):
        super().__init__(parent)

        # Terminal output widget (read-only)
        self.output_widget = tk.Text(self, wrap="word", state="disabled", bg="black", fg="white")
        self.output_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Terminal input field
        self.input_widget = tk.Entry(self, bg="black", fg="white", insertbackground="white")
        self.input_widget.pack(side=tk.BOTTOM, fill=tk.X)
        self.input_widget.bind("<Return>", self.process_command)

        # Start the subprocess for terminal.py
        self.process = subprocess.Popen(
            ["python", "ide/terminal/terminal.py"],  # Update the path to your terminal.py
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Queue for asynchronous output
        self.output_queue = Queue()
        threading.Thread(target=self.read_output, daemon=True).start()

        # Update the output widget periodically
        self.update_output()

    def read_output(self):
        """
        Reads subprocess stdout and stderr, and enqueues the output.
        """
        for line in self.process.stdout:
            self.output_queue.put(line)
        for line in self.process.stderr:
            self.output_queue.put(line)

    def update_output(self):
        """
        Periodically fetch output from the subprocess and display it.
        """
        try:
            while True:
                line = self.output_queue.get_nowait()
                self.output_widget.config(state="normal")
                self.output_widget.insert("end", line)
                self.output_widget.see("end")
                self.output_widget.config(state="disabled")
        except Empty:
            pass
        self.after(100, self.update_output)

    def process_command(self, event):
        """
        Sends user input to the subprocess and displays it in the terminal output.
        """
        command = self.input_widget.get() + "\n"
        self.input_widget.delete(0, tk.END)

        # Write the command to the subprocess stdin
        self.process.stdin.write(command)
        self.process.stdin.flush()

        # Display the command in the terminal output
        self.output_widget.config(state="normal")
        self.output_widget.insert("end", f"> {command}")
        self.output_widget.see("end")
        self.output_widget.config(state="disabled")


def main():
    """
    Main function to initialize and run the Draw++ IDE.
    """
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(APP_DIMENSIONS)
    root.wm_minsize(800, 600)  # Minimum window size

    # Apply custom styles
    apply_styles()

    # Paned window for resizable layout
    paned_window = ttk.PanedWindow(root, orient=tk.VERTICAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Notebook for tabs (top pane)
    notebook = ttk.Notebook(paned_window)
    paned_window.add(notebook, weight=4)

    # Add a default editor tab
    add_tab(notebook, title="Untitled")

    # Create the menu bar
    create_menu_bar(root, notebook, add_tab)

    # Configure keyboard shortcuts
    configure_keyboard_shortcuts(root, notebook, add_tab)

    # Terminal at the bottom pane
    terminal_frame = TerminalFrame(paned_window)
    paned_window.add(terminal_frame, weight=1)

    # Start the main application loop
    root.mainloop()


if __name__ == "__main__":
    main()
