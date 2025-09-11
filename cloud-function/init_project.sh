#!/bin/bash
# Script to initialize the Google Cloud project for the sync function

# Set your project ID (replace with your actual project ID)
PROJECT_ID="ff-base"

# Set region
REGION="us-central1"

echo "🔧 Initializing Google Cloud project for FF-BASE sync..."

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable storage-api.googleapis.com
gcloud services enable drive.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Create service account if it doesn't exist
echo "👤 Creating service account..."
gcloud iam service-accounts create ff-base-backend \
  --display-name="FF-BASE Backend Service Account"

# Assign roles to the service account
echo "🔐 Assigning roles to service account..."

# Storage Object Admin role for the specific bucket
gsutil iam ch serviceAccount:ff-base-backend@$PROJECT_ID.iam.gserviceaccount.com:roles/storage.objectAdmin gs://ff-base-knowledge-base

# Create Secret Manager secret for service account key
echo "🔑 Creating Secret Manager secret..."
gcloud secrets create ff-base-service-account-key \
  --replication-policy="automatic"

# Add the service account key to Secret Manager
gcloud secrets versions add ff-base-service-account-key \
  --data-file="../backend/service-account-key.json"

# Grant the service account access to the secret
gcloud secrets add-iam-policy-binding ff-base-service-account-key \
  --member="serviceAccount:ff-base-backend@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

echo "✅ Project initialization completed!"

echo "
📝 Next steps:
1. Deploy the Cloud Function:
   cd cloud-function
   ./deploy.sh

2. Set up Cloud Scheduler:
   ./setup_scheduler.sh

3. Monitor the function:
   gcloud functions logs read sync-drive-to-gcs --limit 50
"