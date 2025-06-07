FROM python:3.11-slim

# Install git (required for git operations)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY pyproject.toml ./
RUN pip install requests python-dotenv

# Copy source code
COPY . .

# Create volume mount point for target projects
VOLUME ["/workspace"]

# Set default working directory for git operations
WORKDIR /workspace

# Default command
CMD ["python", "/app/main.py"]
