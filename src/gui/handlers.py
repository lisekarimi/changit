"""Event handlers for changit GUI."""

import os
import threading
from pathlib import Path
from tkinter import filedialog

from src.llm.base import get_available_llm
from src.manager import get_version
from src.operations import get_commits
from src.writer import update_changelog


class EventHandlers:
    """Handle all GUI events and user interactions."""

    def __init__(self, app):
        """Initialize event handlers."""
        self.app = app

    def browse_project(self):
        """Open file browser to select project directory."""
        folder = filedialog.askdirectory(title="Select Git Project Folder")
        if folder:
            self.app.project_path.set(folder)

    def generate_changelog_thread(self):
        """Run changelog generation in separate thread."""
        # Disable button during processing
        self.app.generate_btn.configure(text="⏳ Generating...")

        # Start generation in thread
        thread = threading.Thread(target=self.generate_changelog)
        thread.daemon = True
        thread.start()

    def generate_changelog(self):
        """Generate changelog with selected options."""
        try:
            self.app.utils.set_status("Validating inputs...")

            # Validate inputs
            if not self._validate_inputs():
                return

            # Set API keys in environment
            if not self._setup_api_keys():
                return

            # Change to project directory
            original_dir = os.getcwd()
            project_dir = Path(self.app.project_path.get())
            os.chdir(project_dir)

            try:
                # Generate changelog
                if not self._process_changelog():
                    return

            finally:
                # Restore original directory
                os.chdir(original_dir)

        except Exception as e:
            self.app.utils.show_error("❌ Error", f"An error occurred: {str(e)}")
            self.app.utils.set_status("❌ Error occurred")

        finally:
            # Re-enable button
            self.app.generate_btn.configure(text="🚀 Generate Changelog")

    def _validate_inputs(self):
        """Validate user inputs."""
        if not self.app.project_path.get():
            self.app.utils.show_error(
                "📂 Error", "Please select a project folder first"
            )
            return False

        project_dir = Path(self.app.project_path.get())
        if not project_dir.exists():
            self.app.utils.show_error("📂 Error", "Selected folder does not exist")
            return False

        if not (project_dir / ".git").exists():
            self.app.utils.show_error(
                "📂 Error", "Selected folder is not a git repository"
            )
            return False

        # Clear any previous errors when validation passes
        self.app.utils.hide_error()
        return True

    def _setup_api_keys(self):
        """Set up API keys in environment."""
        llm_type = self.app.llm_choice.get()
        if llm_type == "claude":
            if not self.app.api_key_claude.get():
                self.app.utils.show_error("🔑 Error", "Please enter Claude API key")
                return False
            os.environ["ANTHROPIC_API_KEY"] = self.app.api_key_claude.get()
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            if not self.app.api_key_openai.get():
                self.app.utils.show_error("🔑 Error", "Please enter OpenAI API key")
                return False
            os.environ["OPENAI_API_KEY"] = self.app.api_key_openai.get()
            os.environ.pop("ANTHROPIC_API_KEY", None)

        # Clear any previous errors when setup passes
        self.app.utils.hide_error()
        return True

    def _process_changelog(self):
        """Process the changelog generation."""
        self.app.utils.set_status("Reading git commits...")

        # Get commits
        commits = get_commits()
        if not commits:
            self.app.utils.show_error("⚠️ Warning", "No commits found in repository")
            return False

        self.app.utils.set_status(f"Found {len(commits)} commits")
        # Show the commits
        print("\nCommits to process:")
        for i, commit in enumerate(commits, 1):
            print(f"  {i}. {commit}")
        print()  # Empty line

        # Get version
        self.app.utils.set_status("Reading project version...")
        version = get_version()
        if not version:
            self.app.utils.show_error(
                "📄 Error", "Could not find version in pyproject.toml"
            )
            return False

        # Get LLM
        self.app.utils.set_status("Initializing AI model...")
        llm = get_available_llm()
        if not llm:
            self.app.utils.show_error("🤖 Error", "Could not initialize AI model")
            return False

        # Generate changelog
        self.app.utils.set_status(f"Processing with {llm.name}...")
        content = llm.process_commits(commits)

        if content == "INVALID_API_KEY":
            self.app.utils.show_error(
                "🔑 Invalid API Key", f"{llm.name} API key is invalid or expired"
            )
            return False
        elif not content:
            self.app.utils.show_error(
                "⚠️ Generation Failed", "Failed to generate changelog"
            )
            return False

        # Update changelog file
        self.app.utils.set_status("Saving changelog...")
        update_changelog(version, content)

        changelog_path = os.path.join(os.getcwd(), "CHANGELOG.md")
        self.app.utils.set_status(
            f"✅ Changes added at the top of changelog\n {changelog_path}"
        )

        return True
