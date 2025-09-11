#!/bin/bash
# Ultra-optimized script to sync notes from Google Drive to GCS
# Uses folder hash comparison first, then incremental sync with pageToken

# Change to the project directory
cd "$(dirname "$0")/.."

# Activate virtual environment
source backend/venv/bin/activate

# Run the ultra-optimized sync script
echo "🔄 Starting ultra-optimized sync..."
python python/sync_drive_to_gcs_ultra.py

# Log the execution
echo "✅ Ultra-optimized sync completed at $(date)" >> sync_ultra.log