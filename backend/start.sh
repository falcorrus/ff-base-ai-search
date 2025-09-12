#!/bin/bash
# Script to start the FastAPI backend

echo "Starting FF-BASE AI Search System..."
echo "-----------------------------------"

# Navigate to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found."
    echo "Please create it first with: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "Checking dependencies..."
if ! python -c "import fastapi, uvicorn, google.generativeai" &> /dev/null; then
    echo "Error: Required dependencies not found."
    echo "Please install them with: pip install -r requirements.txt"
    exit 1
fi

echo "Dependencies check passed."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found."
    echo "Please create it from .env.example and configure your API keys."
fi

echo ""
echo "Note: If you experience connection issues, try using the direct start script:"
echo "  ./start_direct.sh"
echo ""

echo "Starting server..."
echo "Server will be available at http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000