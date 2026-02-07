# Multi-stage build for optimized backend image
# Builder stage
FROM python:3.11.6-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
        build-base \
        gcc

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies to a temporary directory
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-cache-dir --upgrade -r requirements.txt

# Production stage
FROM python:3.11.6-alpine AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN adduser -D -s /bin/sh worker

# Set working directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder --chown=worker:worker /root/.local /home/worker/.local

# Copy application code
COPY --chown=worker:worker . .

# Switch to non-root user
USER worker

# Make sure scripts in .local are usable
ENV PATH=/home/worker/.local/bin:$PATH

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]