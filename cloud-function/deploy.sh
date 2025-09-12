#!/bin/bash
# Script to deploy the optimized Cloud Function

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

# Set service account (optional, but recommended)
SERVICE_ACCOUNT="ff-base-backend@ff-base.iam.gserviceaccount.com"

echo "🚀 Deploying optimized Cloud Function..."

# Deploy the function with optimized code
gcloud functions deploy sync-drive-to-gcs \
  --project=$PROJECT_ID \
  --region=$REGION \
  --runtime=python39 \
  --trigger-http \
  --entry-point=sync_drive_to_gcs_http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=540s \
  --service-account=$SERVICE_ACCOUNT \
  --source=. \
  --update-labels=environment=production,version=optimized

echo "✅ Optimized deployment completed!"