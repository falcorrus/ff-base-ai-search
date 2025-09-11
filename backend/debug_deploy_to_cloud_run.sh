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

# Загрузка переменных окружения из .env файла (только непустые строки без комментариев)
if [ -f .env ]; then
  export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

# Проверка наличия GOOGLE_API_KEY
if [ -z "$GOOGLE_API_KEY" ]; then
  echo "GOOGLE_API_KEY не установлен. Пожалуйста, установите переменную окружения GOOGLE_API_KEY в файле .env."
  exit 1
fi

# Вывод значений переменных окружения для отладки
echo "PROJECT_ID: $PROJECT_ID"
echo "IMAGE_NAME: $IMAGE_NAME"
echo "REGION: $REGION"
echo "GOOGLE_API_KEY: $GOOGLE_API_KEY"
echo "LOG_LEVEL: $LOG_LEVEL"
echo "GCS_BUCKET_NAME: $GCS_BUCKET_NAME"

# Деплой в Google Cloud Run
echo "Деплой в Google Cloud Run..."
gcloud run deploy $IMAGE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY,LOG_LEVEL=$LOG_LEVEL,GCS_BUCKET_NAME=$GCS_BUCKET_NAME

echo "Деплой завершен."
