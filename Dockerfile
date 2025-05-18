FROM python:3.13-slim

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
COPY ./ ./

# Make the certificate generation script executable
RUN chmod +x createcert.sh

# Create SSL certificate directory
RUN mkdir -p /app/certs

# Generate self-signed certificates
RUN ./createcert.sh

# Expose ports for HTTP and HTTPS
EXPOSE 80 443

# Create a startup script to run Gunicorn with dual HTTP/HTTPS support
RUN echo '#!/bin/bash\n\
gunicorn --bind=0.0.0.0:80 --timeout 120 app:app &\n\
gunicorn --bind=0.0.0.0:443 --timeout 120 --certfile=/app/certs/server.crt --keyfile=/app/certs/server.key app:app\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run with dual HTTP/HTTPS support
CMD ["/app/start.sh"]
