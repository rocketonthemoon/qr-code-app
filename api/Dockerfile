# ---------------------------------------------------
# Stage 1: Build & Dependency Installation
# ---------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip/setuptools and install dependencies into a standalone prefix
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------------------------------------------------
# Stage 2: Distroless Runtime
# ---------------------------------------------------
FROM gcr.io/distroless/python3-debian12:nonroot AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/local/lib/python3.12/site-packages:/app

WORKDIR /app

# Copy installed dependencies and binaries
COPY --from=builder /install /usr/local

# Copy application source
COPY . /app

# Copy a dedicated healthcheck script
COPY healthcheck.py /app/healthcheck.py

EXPOSE 8000

# Exec format healthcheck (distroless has no shell /bin/sh)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/bin/python3", "/app/healthcheck.py"]

# Run uvicorn as a module using exec form
ENTRYPOINT ["/usr/bin/python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]