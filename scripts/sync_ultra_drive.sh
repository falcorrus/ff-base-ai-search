#!/bin/bash
# Ultra-optimized script to sync notes from Google Drive to GCS
# Compares Google Drive folder hash with saved hash in GCS first

# Change to the project directory
cd "$(dirname "$0")/.."

# Activate virtual environment
source backend/venv/bin/activate

# Run the ultra-optimized sync script
echo "🔄 Starting ultra-optimized sync (Drive hash comparison)..."
python python/sync_drive_to_gcs_ultra.py

# Log the execution
echo "✅ Ultra-optimized sync completed at $(date)" >> sync_ultra.log