# Деплой бэкенда в Google Cloud Run

## Подготовка

1. Убедитесь, что у вас установлены:
   - Docker
   - Google Cloud SDK
   - Аккаунт Google Cloud с активированным биллингом

2. Авторизуйтесь в Google Cloud:
   ```bash
   gcloud auth login
   ```

3. Установите проект:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

## Настройка переменных окружения

1. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Отредактируйте файл `.env`, добавив ваши значения:
   - `GOOGLE_API_KEY` - API-ключ для Google Generative AI
   - `GITHUB_PAT` - Personal Access Token для GitHub (опционально)
   - `GCS_BUCKET_NAME` - Имя бакета Google Cloud Storage (опционально)

   Подробные инструкции по получению этих значений находятся в комментариях к файлу `.env`.

## Подготовка базы знаний

Перед деплоем необходимо подготовить базу знаний (эмбеддинги) и загрузить их в Google Cloud Storage:

1. Обновите локальную базу знаний из директории FF-BASE:
   ```bash
   cd ..
   ./sync.sh
   ```

2. Убедитесь, что файл `knowledge_base/embeddings.json` создан и содержит эмбеддинги для всех заметок.

## Сборка и загрузка Docker-образа

1. Перейдите в директорию `backend`:
   ```bash
   cd backend
   ```

2. Сделайте скрипты исполняемыми:
   ```bash
   chmod +x build_and_push.sh
   chmod +x deploy_to_cloud_run.sh
   ```

3. Установите переменные окружения:
   ```bash
   export PROJECT_ID="your-google-cloud-project-id"
   export REGION="your-google-cloud-region"  # По умолчанию us-central1
   ```

4. Запустите скрипт сборки и загрузки:
   ```bash
   ./build_and_push.sh
   ```

## Деплой в Google Cloud Run

1. Убедитесь, что все переменные окружения установлены.

2. Запустите скрипт деплоя:
   ```bash
   ./deploy_to_cloud_run.sh
   ```

## Обновление базы знаний после деплоя

После деплоя приложения в Google Cloud Run вы можете обновлять базу знаний двумя способами:

### 1. Локальное обновление и синхронизация

1. Обновите локальную базу знаний:
   ```bash
   cd ..
   ./sync.sh
   ```

2. Это обновит эмбеддинги в Google Cloud Storage, откуда их будет использовать запущенное приложение.

### 2. Обновление через GitHub (если настроено)

Если вы настроили GitHub интеграцию, можете обновить базу знаний через API:
```bash
curl https://YOUR_CLOUD_RUN_URL/update-knowledge-base
```

## Дополнительные настройки

- Убедитесь, что у вашего сервиса в Cloud Run есть права доступа к Google Cloud Storage, если вы используете его.
- Если вы используете Google Cloud Storage, убедитесь, что бакет создан и настроен.