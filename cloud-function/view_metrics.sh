#!/bin/bash
# Script to view Cloud Function metrics

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📊 Viewing Cloud Function metrics..."

# View execution count
echo "📈 Execution Count:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_count AND resource.type=cloud_function" \
  --limit=10

# View execution times
echo "⏱️ Execution Times:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_times AND resource.type=cloud_function" \
  --limit=10

# View errors
echo "❌ Errors:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_count AND resource.type=cloud_function AND metric.label.status=error" \
  --limit=10

# View active instances
echo "🏃 Active Instances:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/active_instances AND resource.type=cloud_function" \
  --limit=10

echo "📊 Metrics viewing completed!"