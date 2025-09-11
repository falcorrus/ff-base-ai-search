#!/bin/bash
# Script to view status of all scheduled jobs

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📋 Viewing status of all scheduled jobs..."

# List all scheduled jobs
echo "📅 Scheduled Jobs:"
gcloud scheduler jobs list \
  --project=$PROJECT_ID \
  --location=$REGION

# Describe each job
echo -e "\n📄 Job Details:"
for job in $(gcloud scheduler jobs list --project=$PROJECT_ID --location=$REGION --format="value(ID)" | grep -E "(sync-drive-to-gcs|monitor-drive-to-gcs|daily-report-drive-to-gcs)"); do
  echo -e "\n🔍 Details for job: $job"
  gcloud scheduler jobs describe $job \
    --project=$PROJECT_ID \
    --location=$REGION
done

echo "📋 Job status viewing completed!"