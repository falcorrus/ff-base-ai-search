#!/bin/bash
# Script to start both backend and frontend for local development

echo "Starting FF-BASE AI Search development environment..."

# Start backend in background
echo "Starting backend server..."
cd backend
./start.sh > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start frontend in background
echo "Starting frontend server..."
cd frontend-react
npm start > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend logs: backend.log"
echo "Frontend logs: frontend.log"
echo ""
echo "Servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID