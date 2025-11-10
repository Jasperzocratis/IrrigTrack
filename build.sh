#!/bin/bash
set -e

# Build script for DigitalOcean
# This script builds only the components that are detected

# If package.json exists, build Node.js frontend
if [ -f "package.json" ] && [ -d "frontend-vue" ]; then
    echo "Building Vue.js frontend..."
    cd frontend-vue
    npm install
    npm run build
    cd ..
fi

# If requirements.txt exists, install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Don't try to run composer if PHP buildpack isn't detected
# Composer should only run if deploying from backend-laravel directory

echo "Build completed successfully!"

