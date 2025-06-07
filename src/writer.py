"""Changelog file writer for changit."""

import tomllib
from datetime import datetime
from pathlib import Path


def update_changelog(version, content):
    """Add changelog entry to target project's CHANGELOG.md."""
    # Get project name for backup file
    try:
        pyproject_path = Path.cwd() / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
            project_name = pyproject["project"]["name"]
        else:
            project_name = "unknown"
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError):
        project_name = "unknown"

    # Create backup in changeit
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CHANGELOG_{project_name}_{version}_{timestamp}.md"
    changit_root = Path(__file__).parent.parent
    backup_dir = changit_root / "changelog_generated"
    backup_dir.mkdir(exist_ok=True)

    # Target project's CHANGELOG.md
    target_changelog = Path.cwd() / "CHANGELOG.md"

    # Read existing changelog
    try:
        with open(target_changelog, "r", encoding="utf-8") as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = ""

    # Create new entry
    new_entry = f"## [{version}]\n\n{content}\n\n"

    # Add separator if existing content
    if existing_content.strip():
        new_entry += "----\n\n"

    # Combine new entry with existing content
    updated_content = new_entry + existing_content

    # Write updated changelog to target project
    with open(target_changelog, "w", encoding="utf-8") as f:
        f.write(updated_content)

    # Create backup in changeit
    backup_path = backup_dir / filename
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(new_entry)

    print(f"✅ Updated {target_changelog}")
    print(f"✅ Backup created: {backup_path}")
