# =============================================================================
# algo-trading — Dockerfile
# =============================================================================
# Multi-stage build:
#   builder  — installs dependencies using uv
#   runtime  — minimal image with only the app and installed packages
#
# Build:
#   docker build -f docker/Dockerfile -t algo-trading:latest .
#
# Run:
#   docker run --env-file .env algo-trading:latest
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: builder — install Python dependencies via uv
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /build

# Copy only dependency specification first (layer-cache friendly)
COPY pyproject.toml ./

# Install dependencies into an isolated virtual environment
RUN uv sync --no-dev --no-editable

# ---------------------------------------------------------------------------
# Stage 2: runtime — lean production image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Security: run as non-root user
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /build/.venv /app/.venv

# Copy application source
COPY app/ ./app/

# Ensure the venv is on PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ---------------------------------------------------------------------------
# Safety defaults — override via docker-compose.yml or --env-file
# ---------------------------------------------------------------------------
ENV APP_ENV=production
ENV LOG_FORMAT=json
ENV LOG_LEVEL=INFO
ENV LIVE_TRADING=false
ENV PAPER_TRADING=false

# Non-root
USER appuser

# Health check (extended in M9 when FastAPI is added)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from app.main import health_check; h = health_check(); exit(0 if h.status == 'ok' else 1)"

# Default command: start the application
CMD ["python", "-m", "app.main"]
