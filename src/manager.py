"""Version management for changit."""

import tomllib
from pathlib import Path


def get_version():
    """Get version from current project's pyproject.toml."""
    try:
        pyproject_path = Path.cwd() / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
            return pyproject["project"]["version"]
    except Exception:
        pass
    return None
