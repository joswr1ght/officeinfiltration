#!/bin/bash
set -e

# Create directory for certificates
mkdir -p certs

# Generate self-signed certificate
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout certs/server.key -out certs/server.crt \
  -subj "/C=US/ST=Rhode Island/L=Providence/O=SEC504/CN=prompt.sec504.org"

# Set appropriate permissions
chmod 400 certs/server.key
chmod 444 certs/server.crt

echo "Self-signed certificate created successfully in certs/ directory"
