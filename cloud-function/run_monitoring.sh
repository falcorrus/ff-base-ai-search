#!/bin/bash
# Script to run performance monitoring

# Change to the project directory
cd /Users/eugene/MyProjects/ff-base-ai-search/cloud-function

# Activate virtual environment
source ../backend/venv/bin/activate

# Run the performance monitoring script
echo "📊 Running performance monitoring..."
python monitor_performance.py

# Log the execution
echo "✅ Performance monitoring completed at $(date)" >> /Users/eugene/MyProjects/ff-base-ai-search/cloud-function/monitor.log