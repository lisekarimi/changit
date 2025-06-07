"""UI components for changit GUI."""

import customtkinter as ctk


class UIComponents:
    """Handle all UI component creation and layout."""

    def __init__(self, app):
        """Initialize UI components manager."""
        self.app = app
        self.root = app.root

    def setup_ui(self):
        """Set up the complete user interface."""
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self._create_title()
        self._create_project_section()
        self._create_llm_section()
        self._create_generate_section()

    def _create_title(self):
        """Create title section."""
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="📄 Changit - Changelog Generator",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=(20, 30))

    def _create_project_section(self):
        """Create project selection section."""
        # Project Selection Frame
        project_frame = ctk.CTkFrame(self.main_frame)
        project_frame.pack(fill="x", padx=20, pady=(0, 20))

        project_label = ctk.CTkLabel(project_frame, text="Select Git Project:")
        project_label.pack(anchor="w", padx=20, pady=(20, 5))

        project_path_frame = ctk.CTkFrame(project_frame)
        project_path_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.app.project_entry = ctk.CTkEntry(
            project_path_frame,
            textvariable=self.app.project_path,
            placeholder_text="Select project folder...",
        )
        self.app.project_entry.pack(
            side="left", fill="x", expand=True, padx=(10, 5), pady=10
        )

        browse_btn = ctk.CTkButton(
            project_path_frame,
            text="Browse",
            command=self.app.handlers.browse_project,
            width=80,
        )
        browse_btn.pack(side="right", padx=(5, 10), pady=10)

    def _create_llm_section(self):
        """Create LLM selection section."""
        # LLM Selection Frame
        llm_frame = ctk.CTkFrame(self.main_frame)
        llm_frame.pack(fill="x", padx=20, pady=(0, 20))

        llm_label = ctk.CTkLabel(llm_frame, text="Select AI Model:")
        llm_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Radio buttons for LLM selection
        radio_frame = ctk.CTkFrame(llm_frame)
        radio_frame.pack(fill="x", padx=20, pady=(0, 10))

        claude_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Claude 3.5 Sonnet",
            variable=self.app.llm_choice,
            value="claude",
            command=self._toggle_api_keys,
        )
        claude_radio.pack(side="left", padx=20, pady=10)

        openai_radio = ctk.CTkRadioButton(
            radio_frame,
            text="OpenAI GPT-4o",
            variable=self.app.llm_choice,
            value="openai",
            command=self._toggle_api_keys,
        )
        openai_radio.pack(side="left", padx=20, pady=10)

        # API Keys Frame
        self._create_api_keys_section(llm_frame)

        # Initial toggle to show correct fields
        self._toggle_api_keys()

    def _create_api_keys_section(self, parent):
        """Create API keys input section."""
        self.api_frame = ctk.CTkFrame(parent)
        self.api_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Claude API Key Frame
        self.claude_frame = ctk.CTkFrame(self.api_frame)

        self.claude_label = ctk.CTkLabel(self.claude_frame, text="Claude API Key:")
        self.claude_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.app.claude_entry = ctk.CTkEntry(
            self.claude_frame,
            textvariable=self.app.api_key_claude,
            placeholder_text="sk-ant-...",
            show="*",
        )
        self.app.claude_entry.pack(fill="x", padx=20, pady=(0, 10))

        # OpenAI API Key Frame
        self.openai_frame = ctk.CTkFrame(self.api_frame)

        self.openai_label = ctk.CTkLabel(self.openai_frame, text="OpenAI API Key:")
        self.openai_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.app.openai_entry = ctk.CTkEntry(
            self.openai_frame,
            textvariable=self.app.api_key_openai,
            placeholder_text="sk-proj-...",
            show="*",
        )
        self.app.openai_entry.pack(fill="x", padx=20, pady=(0, 10))

    def _toggle_api_keys(self):
        """Show/hide API key fields based on selected LLM."""
        if self.app.llm_choice.get() == "claude":
            self.claude_frame.pack(fill="x", padx=20, pady=(0, 10))
            self.openai_frame.pack_forget()
        else:
            self.openai_frame.pack(fill="x", padx=20, pady=(0, 10))
            self.claude_frame.pack_forget()

    def _create_generate_section(self):
        """Create generate button and status section."""
        # Add error label above generate button (initially hidden)
        self.app.error_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color="red",
            width=600,  # Fixed width
            height=30,  # Fixed height
            wraplength=580,  # Wrap text within width
        )

        # Generate Button
        self.app.generate_btn = ctk.CTkButton(
            self.main_frame,
            text="📄 Generate Changelog",
            command=self.app.handlers.generate_changelog_thread,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8,
            border_width=0,
        )
        self.app.generate_btn.pack(pady=20)

        # Status Label
        self.app.status_label = ctk.CTkLabel(
            self.main_frame, text="Ready to generate changelog"
        )
        self.app.status_label.pack(pady=(0, 10))
