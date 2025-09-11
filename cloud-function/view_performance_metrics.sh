#!/bin/bash
# Script to view Cloud Function performance metrics

# Set project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region (replace with your preferred region)
REGION="us-central1"

echo "📊 Viewing Cloud Function performance metrics..."

# View execution count metrics
echo "📈 Execution count metrics:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_count AND resource.type=cloud_function AND resource.labels.function_name=sync-drive-to-gcs" \
  --limit=10

# View execution time metrics
echo -e "\n⏱️ Execution time metrics:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_times AND resource.type=cloud_function AND resource.labels.function_name=sync-drive-to-gcs" \
  --limit=10

# View error metrics
echo -e "\n❌ Error metrics:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/execution_count AND resource.type=cloud_function AND resource.labels.function_name=sync-drive-to-gcs AND metric.labels.status=error" \
  --limit=10

# View active instances metrics
echo -e "\n🏃 Active instances metrics:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/active_instances AND resource.type=cloud_function AND resource.labels.function_name=sync-drive-to-gcs" \
  --limit=10

# View memory usage metrics
echo -e "\n🧠 Memory usage metrics:"
gcloud monitoring metrics list \
  --project=$PROJECT_ID \
  --filter="metric.type=cloudfunctions.googleapis.com/function/user_memory_bytes AND resource.type=cloud_function AND resource.labels.function_name=sync-drive-to-gcs" \
  --limit=10

echo "📊 Cloud Function performance metrics viewing completed!"