#!/bin/bash

echo "========================================"
echo "Starting Python ML API Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "ml_api_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv ml_api_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ml_api_env/bin/activate

# Install/upgrade requirements
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements_ml_api.txt

# Start the server
echo ""
echo "Starting ML API server..."
echo ""
python ml_api_server.py

