#!/bin/bash

# Run locally (for dev purposes)

# Create and activate virtual environment
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

echo "Activating virtual environment..."
source env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the Flask application
echo "Starting application..."
echo "Visit http://localhost:3000 in your browser"
export FLASK_APP=app.py
export FLASK_DEBUG=1
export OPENAI_API_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL="phi4-mini:latest"
export OPENAI_TIMEOUT="60"
export OPENAI_SEED="42"
# flask run -p 3000 --host 0.0.0.0
flask run -p 3000
