# 📄Changit - Auto-Generate Changelogs Using AI

Changit is an AI-powered tool that auto-generates changelogs from git commits to save hours of manual work. Available as both CLI and GUI.

## ✨ Features

- 🤖 **AI-powered**: Uses Claude or GPT to categorize commits
- 🖥️ **Dual interfaces**: Modern GUI or CLI for automation
- 📝 **Smart formatting**: Organizes commits into Added/Changed/Fixed/Removed with emojis
- 🏷️ **Auto-versioning**: Reads version from `pyproject.toml`
- 🌍 **Universal Git support**: Works with GitHub, GitLab, Bitbucket, or any Git platform

## 📋 Pre-requisites

**Required:**
- **Python 3.11+** (requires-python = ">=3.11")
- **UV Package Manager** - [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Local git repository** with commit history
- **pyproject.toml** with project name and version
- Claude API key (`ANTHROPIC_API_KEY`) or OpenAI API key (`OPENAI_API_KEY`) in `.env`

**Optional:**
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop) (for containerized usage)
- **Make**
  - **Windows:** `winget install GnuWin32.Make`
  - **macOS:** `brew install make`
  - **Linux:** `sudo apt install make`

**Functional Requirements:**
- A local Git repository with commit history
- A `pyproject.toml` file containing the project name and version
- Commits must exist on the `main` branch (merge commits are ignored)
- Commit messages should ideally follow the conventional format (e.g., `feat:`, `fix:`)


## 🚀 Quick Start

### Clone and Configure
```bash
git clone https://github.com/lisekarimi/changit.git
cd changit
uv sync
```
Rename `.env.example` to `.env` and populate it with the required secrets.

You can either choose the GUI or CLI.

### GUI (Recommended)
```bash
uv run gui.py
```
1. Browse and select your git project
2. Choose Claude or OpenAI
3. Enter API key
4. Click "🚀 Generate Changelog"


### CLI
```bash
uv run main.py
```

## 🐳 Docker

```bash
make docker-build
# Update PATH_SCAN in Makefile with your project path
make docker-run
```

## 📦 Executable

Build standalone .exe:
```bash
make build-exe
make compile-exe
```
Find executable in `dist/` folder - create desktop shortcut for daily use.

👉 Or simply [download the executable here](https://lisekarimi.github.io/changit/)

## 📄 Output Format

```markdown
## [1.2.0]

### ✨ Added
- New user authentication system

### 🔄 Changed
- Improved performance

### 🐛 Fixed
- Memory leak resolved

### 🗑️ Removed
- Deprecated API endpoints

----

## [1.1.0]
...previous entries
```

## ⚙️ Configuration

### API Keys
- **CLI**: Set in `.env` file
  - If both keys present: Claude used first
  - Comment out one key to switch LLMs
- **GUI**: Enter directly (not saved between sessions)

### Git Settings
- Reads commits from **main branch only**
- Processes commits since last git tag
- Excludes merge commits automatically


## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Run `uv sync` |
| No commits found | Check main branch has commits since last tag |
| Invalid API key | Verify key in .env (CLI) or GUI input |
| No version found | Ensure `pyproject.toml` has `[project] version = "x.x.x"` |
| GUI button corruption | Restart app (known CustomTkinter multi-monitor issue) |

## 📄 License

MIT
