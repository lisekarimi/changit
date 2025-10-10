"""Main GUI application class."""

import customtkinter as ctk

from src.gui.components import UIComponents
from src.gui.handlers import EventHandlers
from src.gui.utils import GUIUtils

# Set appearance with purple theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # Green theme has purple-ish colors


class ChangitGUI:
    """Main GUI application for changit."""

    def __init__(self):
        """Initialize the GUI application."""
        self.root = ctk.CTk()
        self.root.title("Changit 0.1.1 - Changelog Generator")
        self.root.geometry("900x700")

        # Fix multi-monitor scaling issues
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        # Initialize utilities and handlers
        self.utils = GUIUtils(self)
        self.handlers = EventHandlers(self)
        self.components = UIComponents(self)

        # Initialize variables
        self.project_path = ctk.StringVar()
        self.api_key_claude = ctk.StringVar()
        self.api_key_openai = ctk.StringVar()
        self.llm_choice = ctk.StringVar(value="claude")

        # Setup UI and load environment
        self.components.setup_ui()

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
