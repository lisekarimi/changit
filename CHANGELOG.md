
## 🏷️ [0.1.1]

### 🗑️ Removed
- Frontend/website components moved to separate [`changit-web`](https://github.com/lisekarimi/changit-web) repository
- Landing page and web interface separated from core tool functionality
- Web-related dependencies and assets removed from main repository

### 🔄 Changed
- Repository structure simplified to focus on core CLI/GUI functionality
- Product separation: core tool vs. website/landing page now in distinct repositories

## [0.1.0]

### ✨ Added
- AI-powered changelog generation using LLMs (Claude and GPT-4o)
- Modern GUI application for Windows (.exe) - macOS and Linux not supported yet
- CLI interface for automation
- Git commit processing with automatic merge commit filtering
- Support for any Git platform (GitHub, GitLab, Bitbucket) - only Git required
- Local-only operation except for LLM API calls
