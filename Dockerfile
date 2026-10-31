# Production Dockerfile for Multi-Agent Delivery Fleet Coordination System
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and datasets
COPY . .

# Expose ports: 8000 for FastAPI / A2A API, 8001 for FastMCP server
EXPOSE 8000 8001

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src; print('Health: OK')" || exit 1

# Default command: run interactive demonstration and evaluation suite
CMD ["python", "demo.py"]
