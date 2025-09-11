#!/bin/bash
# Script to monitor Cloud Function execution

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📊 Monitoring Cloud Function execution..."

# View recent logs
echo "📋 Recent logs:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --limit=50

# View error logs (corrected syntax)
echo -e "\n❌ Error logs:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --min-log-level=ERROR \
  --limit=20

# View warning logs (corrected syntax)
echo -e "\n⚠️ Warning logs:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --min-log-level=WARNING \
  --limit=20

# View info logs (corrected syntax)
echo -e "\nℹ️ Info logs:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --min-log-level=INFO \
  --limit=20

# View logs with specific keywords (corrected syntax)
echo -e "\n🔍 Logs with 'Sync' keyword:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --limit=20 \
  --filter="textPayload:Sync"

echo -e "\n🔍 Logs with 'File' keyword:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --limit=20 \
  --filter="textPayload:File"

echo -e "\n🔍 Logs with 'Hash' keyword:"
gcloud functions logs read sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --limit=20 \
  --filter="textPayload:Hash"

echo "📊 Cloud Function monitoring completed!"