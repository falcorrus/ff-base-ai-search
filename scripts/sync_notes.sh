#!/bin/bash
# Script to sync notes from Google Drive to GCS (incremental sync)

# Change to the project directory
cd "$(dirname "$0")/.."

# Activate virtual environment
source backend/venv/bin/activate

# Run the sync script
python python/sync_drive_to_gcs.py

# Log the execution
echo "Incremental sync completed at $(date)" >> scripts/sync.log