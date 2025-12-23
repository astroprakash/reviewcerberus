# Build stage
FROM python:3.11-slim AS builder

# Install poetry
RUN pip install poetry==1.8.3

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (without dev dependencies)
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi

# Runtime stage
FROM python:3.11-slim

# Install git (required for repository operations)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src ./src

# Add virtualenv to PATH and app to PYTHONPATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Set working directory for mounted repositories
WORKDIR /repo

# Run reviewcerberus
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--help"]
