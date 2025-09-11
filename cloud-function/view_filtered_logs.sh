#!/bin/bash
# Script to view filtered Cloud Function logs

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📋 Viewing filtered Cloud Function logs..."

# View recent logs with timestamps
echo "🕒 Recent logs with timestamps:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --limit=100 \\
  --format="table(timestamp,severity,textPayload)"

# View error logs
echo -e "\n❌ Error logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --level=ERROR \\
  --limit=50 \\
  --format="table(timestamp,severity,textPayload)"

# View warning logs
echo -e "\n⚠️ Warning logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --level=WARNING \\
  --limit=50 \\
  --format="table(timestamp,severity,textPayload)"

# View info logs
echo -e "\nℹ️ Info logs:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --level=INFO \\
  --limit=50 \\
  --format="table(timestamp,severity,textPayload)"

# View logs with specific keywords
echo -e "\n🔍 Logs with 'Sync' keyword:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --limit=50 \\
  --filter="textPayload:*Sync*" \\
  --format="table(timestamp,severity,textPayload)"

echo -e "\n🔍 Logs with 'File' keyword:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --limit=50 \\
  --filter="textPayload:*File*" \\
  --format="table(timestamp,severity,textPayload)"

echo -e "\n🔍 Logs with 'Hash' keyword:"
gcloud functions logs read sync-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --region=$REGION \\
  --limit=50 \\
  --filter="textPayload:*Hash*" \\
  --format="table(timestamp,severity,textPayload)"

echo "📋 Filtered Cloud Function logs viewing completed!"