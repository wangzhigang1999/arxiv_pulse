FROM python:3.12-bookworm

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set working directory
WORKDIR /app

COPY . .

# Install uv and sync dependencies in a single RUN layer
RUN pip install --no-cache-dir --upgrade pip uv \
    && uv sync --frozen

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "main.py"]
