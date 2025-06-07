# =====================================
# 🌱 Project & Environment Configuration
# =====================================

# Read from pyproject.toml using grep (works on all platforms)
PROJECT_NAME = $(shell python -c "import re; print(re.search('name = \"(.*)\"', open('pyproject.toml').read()).group(1))")
VERSION = $(shell python -c "import re; print(re.search('version = \"(.*)\"', open('pyproject.toml').read()).group(1))")

-include .env
export DOCKER_USERNAME
export PATH_SCAN

DOCKER_IMAGE = $(DOCKER_USERNAME)/$(PROJECT_NAME)
TAG = $(VERSION)
CONTAINER_NAME = $(PROJECT_NAME)-container


# =====================================
# 🛠️  Environment Setup (using UV)
# =====================================
# uv add package-name - Add a new dependency
# uv add --dev package-name - Add a development dependency
# uv sync - Install/sync all dependencies
# uv remove package-name - Remove a dependency
# uv remove --dev package-name - Remove a development dependency
# uv cache clean - Clear the cache

# Activate the virtual environment:
# .\.venv\Scripts\activate (Windows)
# source .venv/bin/activate (Mac/Linux)

# =======================
# 🪝 Hooks
# =======================

install-hooks:	## Install pre-commit hooks
	uvx pre-commit install
	uvx pre-commit install --hook-type commit-msg


# =====================================
# ✨ Code Quality
# =====================================

lint:	## Run code linting and formatting
	uvx ruff check .
	uvx ruff format .

fix:	## Fix code issues and format
	uvx ruff check --fix .
	uvx ruff format .


# =====================================
# 🚀 Run App Locally
# =====================================

# Note: uv run automatically creates venv and installs dependencies if needed

run:	## Run the app locally
	uv run main.py

gui:	## Run the GUI script
	uv run gui.py


# =======================
# 🐳 Docker Commands
# =======================

docker-build: ## Build the Docker image for development
	docker build -t $(DOCKER_IMAGE):$(TAG) .

docker-ls: ## List files in Docker image
	docker run --rm $(DOCKER_IMAGE):$(TAG) ls -la /app

docker-run:	## Run the Docker container
# Change PATH_SCAN in .env
# Press Enter when prompted for path - project is already mounted at /workspace
	docker run -it --rm --name $(CONTAINER_NAME) \
		-v $(PATH_SCAN):/workspace \
		--env-file .env \
		-w /workspace \
		$(DOCKER_IMAGE):$(TAG)


# =======================
# 🔍 Security Scanning
# =======================

# Install gitleaks first: https://github.com/gitleaks/gitleaks

check-secrets:		## Debug: Check secrets manually
	gitleaks detect --source . --verbose

audit:	## Audit dependencies for vulnerabilities
	uv run --with pip-audit pip-audit


# =====================================
# 📦 Build & Distribution - Only for Windows
# =====================================
build-exe: ## Build the executable using PyInstaller
	uv run pyi-makespec --onefile --windowed \
		--icon=assets/img/changit.ico \
		--name="changit" \
		--hidden-import=pkg_resources \
		--hidden-import=packaging \
		--hidden-import=packaging.version \
		--hidden-import=packaging.specifiers \
		--hidden-import=packaging.requirements \
		gui.py

compile-exe: ## Compile the executable from spec file
	uv run pyinstaller "changit.spec"
	@echo "Executable compiled successfully. You can find it in the dist/ folder."


# =====================================
# 📚 Documentation & Help
# =====================================

help: ## Show this help message
	@echo Available commands:
	@echo.
	@python -c "import re; lines=open('Makefile', encoding='utf-8').readlines(); targets=[re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$',l) for l in lines]; [print(f'  make {m.group(1):<20} {m.group(2)}') for m in targets if m]"


# =======================
# 🎯 PHONY Targets
# =======================

# Auto-generate PHONY targets (cross-platform)
.PHONY: $(shell python -c "import re; print(' '.join(re.findall(r'^([a-zA-Z_-]+):\s*.*?##', open('Makefile', encoding='utf-8').read(), re.MULTILINE)))")

# Test the PHONY generation
# test-phony:
# 	@echo "$(shell python -c "import re; print(' '.join(sorted(set(re.findall(r'^([a-zA-Z0-9_-]+):', open('Makefile', encoding='utf-8').read(), re.MULTILINE)))))")"
