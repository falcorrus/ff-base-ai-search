#!/bin/bash
# Script to view Cloud Scheduler logs

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📋 Viewing Cloud Scheduler logs..."

# View recent logs for all jobs
echo "📅 Recent logs for all scheduled jobs:"
gcloud logging read "resource.type=\"cloud_scheduler_job\"" \
  --project=$PROJECT_ID \
  --limit=50 \
  --format="table(timestamp, resource.labels.job_id, severity, textPayload)"

# View logs for specific sync job
echo -e "\n🔄 Logs for sync-drive-to-gcs-daily job:"
gcloud logging read "resource.type=\"cloud_scheduler_job\" AND resource.labels.job_id=\"sync-drive-to-gcs-daily\"" \
  --project=$PROJECT_ID \
  --limit=20 \
  --format="table(timestamp, severity, textPayload)"

# View logs for monitoring jobs
echo -e "\n📊 Logs for monitoring jobs:"
gcloud logging read "resource.type=\"cloud_scheduler_job\" AND resource.labels.job_id=~\"monitor|report\"" \
  --project=$PROJECT_ID \
  --limit=20 \
  --format="table(timestamp, resource.labels.job_id, severity, textPayload)"

echo "📋 Cloud Scheduler logs viewing completed!"