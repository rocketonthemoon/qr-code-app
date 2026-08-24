FROM python:3.12-slim

# Prevent Python from writing bytecode (.pyc) and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Copy requirements first for Docker layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy application code
COPY . /app/

# 3. Create non-root system user and set permissions
RUN useradd -r -s /bin/false pythonuser && \
    chown -R pythonuser:pythonuser /app

USER pythonuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

# 4. Bind to 0.0.0.0 to accept container traffic
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]