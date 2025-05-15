FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py static/ createcert.sh templates/ .

# Make the certificate generation script executable
RUN chmod +x createcert.sh

# Create SSL certificate directory
RUN mkdir -p /app/certs

# Create a non-root user for security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app

# Generate self-signed certificates
RUN ./createcert.sh

# Expose ports for HTTP and HTTPS
EXPOSE 80 443

# Set up command to run with Gunicorn
USER appuser

# Create a startup script to run Gunicorn with dual HTTP/HTTPS support
RUN echo '#!/bin/bash\n\
gunicorn --bind=0.0.0.0:80 app:app &\n\
gunicorn --bind=0.0.0.0:443 --certfile=/app/certs/server.crt --keyfile=/app/certs/server.key app:app\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run with dual HTTP/HTTPS support
CMD ["/app/start.sh"]
# CMD ["/bin/sh"]
