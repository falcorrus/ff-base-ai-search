#!/bin/bash

# Проверка наличия PROJECT_ID
if [ -z "$PROJECT_ID" ]; then
  echo "PROJECT_ID не установлен. Пожалуйста, установите переменную окружения PROJECT_ID."
  exit 1
fi

# Проверка наличия IMAGE_NAME
if [ -z "$IMAGE_NAME" ]; then
  IMAGE_NAME="ff-base-ai-search-backend"
fi

# Проверка наличия REGION
if [ -z "$REGION" ]; then
  REGION="us-central1"
fi



# Деплой в Google Cloud Run
echo "Деплой в Google Cloud Run..."
gcloud run deploy $IMAGE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,LOG_LEVEL=$LOG_LEVEL,GCS_BUCKET_NAME=$GCS_BUCKET_NAME

echo "Деплой завершен."