FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for pymysql compilation
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY arxiv_pulse/ arxiv_pulse/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "arxiv_pulse.main:app", "--host", "0.0.0.0", "--port", "8000"]

