"""GUI entry point for changit."""

from src.gui.app import ChangitGUI


def main():
    """Start the GUI application."""
    app = ChangitGUI()
    app.run()


if __name__ == "__main__":
    main()
