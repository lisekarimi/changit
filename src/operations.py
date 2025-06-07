"""Git operations for changit."""

import subprocess

from src.constants import GIT_BRANCH, GIT_LOG_FORMAT


def run_command(cmd):
    """Run shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def get_last_tag():
    """Get the last git tag."""
    return run_command("git describe --tags --abbrev=0")


def get_commits():
    """Get commits since last tag from main branch."""
    last_tag = get_last_tag()

    if last_tag:
        print(f"Last tag: {last_tag}")
        cmd = f"git log {last_tag}..{GIT_BRANCH} {GIT_LOG_FORMAT}"
    else:
        print("No tags found, getting recent commits")
        cmd = f"git log {GIT_BRANCH} {GIT_LOG_FORMAT}"

    commits = run_command(cmd)
    if not commits:
        return []

    # print(f"Raw git output: {repr(commits)}")

    # Split commits by double newlines
    return commits.split("\n")
