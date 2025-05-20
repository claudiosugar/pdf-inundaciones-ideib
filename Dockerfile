FROM python:3.9.13 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

# Add playwright install in the builder stage as well (safer)
RUN .venv/bin/playwright install --with-deps chromium

# Use the same Python version slim image for the final stage
FROM python:3.9.13-slim

# Install system dependencies needed by Playwright/Chromium
# Need wget and ca-certificates for playwright install command itself
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libexpat1 \
    wget \
    ca-certificates \
    xvfb \
    xauth \
    # Clean up apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment with installed packages from the builder
COPY --from=builder /app/.venv .venv/

# Copy the application code
COPY . .

# Ensure the playwright browsers are installed in the final image
# Run this *after* copying .venv which contains the playwright executable
# Using --with-deps might be redundant now but is safe
RUN .venv/bin/playwright install --with-deps chromium

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080 \
    NODE_OPTIONS="--max-old-space-size=3072"

# Start app with Xvfb to provide virtual display
CMD xvfb-run --auto-servernum --server-args="-screen 0 1280x960x24" \
    /app/.venv/bin/gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 1 --threads 2 pdf-inundaciones-ideib:app
