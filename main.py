"""Main entry point for changit changelog generator."""

import os
from pathlib import Path

from dotenv import load_dotenv

from src.llm.base import get_available_llm
from src.manager import get_version
from src.operations import get_commits
from src.writer import update_changelog


def main():
    """Generate changelog for a git project using AI."""
    # Load environment variables from .env file
    load_dotenv()

    print("📄 Changit - Changelog Generator")
    print("=" * 35)

    # Get project path
    project_path = input(
        "Enter project path (or press Enter for current directory): "
    ).strip()

    if project_path:
        project_path = Path(project_path).expanduser().resolve()
        if not project_path.exists():
            print(f"❌ Path does not exist: {project_path}")
            return
        print(f"Switching to: {project_path}")
        os.chdir(project_path)
    else:
        project_path = Path.cwd()
        print(f"Using current directory: {project_path}")

    # Check if git repo
    if not (project_path / ".git").exists():
        print("❌ Not a git repository")
        return

    # Get commits
    commits = get_commits()
    if not commits:
        print("❌ No commits found")
        return

    print(f"Found {len(commits)} commits")

    # Show the commits
    print("\nCommits to process:")
    for i, commit in enumerate(commits, 1):
        print(f"  {i}. {commit}")
    print()  # Empty line

    # Get LLM
    llm = get_available_llm()
    if not llm:
        print("❌ No LLM available")
        return

    # Get version
    version = get_version()
    if not version:
        print("❌ Version required")
        return

    print(f"Using version: {version}")

    # Generate changelog
    print(f"🤖 Processing with {llm.name}...")
    content = llm.process_commits(commits)

    if not content:
        print("❌ Failed to generate changelog")
        return

    # Update file
    update_changelog(version, content)
    print("🎉 Changit complete! Check CHANGELOG.md")


if __name__ == "__main__":
    main()
