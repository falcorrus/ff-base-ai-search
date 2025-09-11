#!/bin/bash
# Script to set up monitoring schedule

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📅 Setting up monitoring schedule..."

# Create Cloud Scheduler job for performance monitoring
gcloud scheduler jobs create http monitor-drive-to-gcs-performance \\
  --project=$PROJECT_ID \\
  --location=$REGION \\
  --schedule="0 */6 * * *" \\
  --uri="https://$REGION-$PROJECT_ID.cloudfunctions.net/monitor-drive-to-gcs" \\
  --http-method=GET \\
  --time-zone=Europe/Moscow \\
  --description="Performance monitoring for FF-BASE sync function every 6 hours"

echo "✅ Performance monitoring job created!"

# Create Cloud Scheduler job for daily reports
gcloud scheduler jobs create http daily-report-drive-to-gcs \\
  --project=$PROJECT_ID \\
  --location=$REGION \\
  --schedule="0 9 * * *" \\
  --uri="https://$REGION-$PROJECT_ID.cloudfunctions.net/daily-report-drive-to-gcs" \\
  --http-method=GET \\
  --time-zone=Europe/Moscow \\
  --description="Daily report for FF-BASE sync function at 9:00 AM MSK"

echo "✅ Daily report job created!"

echo "📅 Monitoring schedule setup completed!"