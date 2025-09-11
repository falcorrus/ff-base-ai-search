#!/bin/bash
# Script to rebuild CSS for the frontend

echo "Rebuilding CSS..."

cd /Users/eugene/MyProjects/ff-base-ai-search/frontend
npm run build:css

if [ $? -eq 0 ]; then
    echo "CSS rebuilt successfully!"
else
    echo "Error rebuilding CSS!"
    exit 1
fi