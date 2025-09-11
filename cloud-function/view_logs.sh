#!/bin/bash
# Script to view Cloud Function logs

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📋 Viewing Cloud Function logs..."

# View recent logs
echo "Recent logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --limit=50

# View error logs
echo "Error logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --level=ERROR \\
  --limit=20

# View warning logs
echo "Warning logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --level=WARNING \\
  --limit=20

echo "📋 Logs viewing completed!"