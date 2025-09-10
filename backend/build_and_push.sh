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

# Сборка Docker-образа для amd64 архитектуры
echo "Сборка Docker-образа..."
docker build --platform linux/amd64 -t gcr.io/$PROJECT_ID/$IMAGE_NAME .

# Загрузка образа в Google Container Registry
echo "Загрузка образа в Google Container Registry..."
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

echo "Образ успешно загружен в GCR."