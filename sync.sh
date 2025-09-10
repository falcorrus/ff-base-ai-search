#!/bin/bash
# Sync script for updating embeddings from FF-BASE and syncing to GCS

echo "🔄 Updating embeddings from FF-BASE and syncing to GCS..."

# Set the Google service account key from .env file
if [ -f "backend/.env" ]; then
    export $(grep -v '^#' backend/.env | xargs)
    echo "✅ Environment variables loaded"
fi

# Activate virtual environment if it exists
if [ -f "backend/venv/bin/activate" ]; then
    source backend/venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the full sync
python sync_embeddings.py full-sync

if [ $? -eq 0 ]; then
    echo "✅ Knowledge base sync completed successfully!"
    echo "📊 Current note count:"
    if [ -f "knowledge_base/embeddings.json" ]; then
        count=$(python -c "import json; print(len(json.load(open('knowledge_base/embeddings.json'))))")
        echo "   $count notes in knowledge base"
    fi
else
    echo "❌ Knowledge base sync failed!"
    echo "💡 Troubleshooting tips:"
    echo "   1. Check if your GCS bucket exists: $GCS_BUCKET_NAME"
    echo "   2. Verify your service account has proper permissions"
    echo "   3. For now, your local embeddings are updated and ready for deployment"
    exit 1
fi