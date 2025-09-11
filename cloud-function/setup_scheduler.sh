#!/bin/bash
# Script to set up Cloud Scheduler for daily sync at 23:00 MSK

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

# Set timezone to Moscow (MSK)
TIMEZONE="Europe/Moscow"

# Calculate UTC time for 23:00 MSK
# 23:00 MSK = 20:00 UTC (during standard time)
# 23:00 MSK = 20:00 UTC (during daylight saving time in Russia - no DST)

echo "📅 Setting up Cloud Scheduler for daily sync at 23:00 MSK..."

# Create Cloud Scheduler job
gcloud scheduler jobs create http sync-drive-to-gcs-daily \
  --project=$PROJECT_ID \
  --location=$REGION \
  --schedule="0 20 * * *" \
  --uri="https://$REGION-$PROJECT_ID.cloudfunctions.net/sync-drive-to-gcs" \
  --http-method=GET \
  --time-zone=$TIMEZONE \
  --description="Daily sync from Google Drive to GCS at 23:00 MSK"

echo "✅ Cloud Scheduler job created!"

echo "📋 To list scheduled jobs:"
echo "gcloud scheduler jobs list --project=$PROJECT_ID --location=$REGION"

echo "⏯️ To manually run the job:"
echo "gcloud scheduler jobs run sync-drive-to-gcs-daily --project=$PROJECT_ID --location=$REGION"