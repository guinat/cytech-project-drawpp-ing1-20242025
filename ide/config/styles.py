from tkinter import ttk
from ide.config.settings import THEME_COLORS


def apply_styles():
    """
    @brief Configures custom styles for the application.

    @note Relies on THEME_COLORS defined in the application's configuration.
    """
    style = ttk.Style()
    style.theme_use("clam")

    # Configure tab styles for TNotebook
    style.configure(
        "TNotebook.Tab",
        background=THEME_COLORS["button"],
        foreground=THEME_COLORS["fg"],
        padding=[5, 2],
        font=("Consolas", 10)
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", THEME_COLORS["accent"])],
        foreground=[("selected", "#ffffff")]
    )
