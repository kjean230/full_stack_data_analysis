# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies for MySQL client + compilation
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    tzdata \
    curl \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Install runtime dependencies first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r /app/requirements.txt

# Copy application code
COPY app /app/app

# -------------------------
# Dev image (adds dev deps)
# -------------------------
FROM base AS dev
COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install -r /app/requirements-dev.txt

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# -------------------------
# Prod image (no dev deps)
# -------------------------
FROM base AS prod

# Run as non-root in production
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]