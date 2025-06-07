"""GUI utilities for changit."""


class GUIUtils:
    """Utility functions for GUI operations."""

    def __init__(self, app):
        """Initialize GUI utilities."""
        self.app = app

    def set_status(self, message):
        """Update status label."""
        self.app.status_label.configure(text=message)
        self.app.root.update_idletasks()

    def show_error(self, title, message):
        """Show error message above the generate button."""
        error_text = f"{title}: {message}"
        self.app.error_label.configure(text=error_text)
        self.app.error_label.pack(pady=(10, 0), before=self.app.generate_btn)

    def hide_error(self):
        """Hide the error message."""
        self.app.error_label.pack_forget()
