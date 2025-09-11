#!/bin/bash
# Script to stop the development environment

echo "Stopping FF-BASE AI Search development environment..."

# Kill backend processes
echo "Stopping backend server..."
pkill -f "uvicorn main:app" || echo "No backend processes found"

# Kill frontend processes
echo "Stopping frontend server..."
pkill -f "node server.js" || echo "No frontend processes found"

echo "Development environment stopped."