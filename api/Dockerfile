FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Patch OS packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip/setuptools, install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip "setuptools>=84.0.0" "msgpack>=1.2.1" && \
    pip install --no-cache-dir -r requirements.txt

# 3. Final cleanup: Remove pip, setuptools, ensurepip, and all caches
RUN pip uninstall -y pip setuptools wheel && \
    rm -rf /usr/local/lib/python3.12/ensurepip \
    /root/.cache \
    /tmp/* \
    /var/tmp/* \
    /usr/local/lib/python3.12/site-packages/pip* \
    /usr/local/lib/python3.12/site-packages/setuptools* \
    /usr/local/bin/pip*

# 4. Copy application source
COPY . .

# 5. Non-root user setup
RUN useradd -r -s /bin/false appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "/app/healthcheck.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]