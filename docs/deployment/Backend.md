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

## Настройка переменных окружения в Cloud Run

При деплое в Google Cloud Run **не используется** локальный `.env` файл. Вместо этого, переменные окружения необходимо настроить напрямую в сервисе Cloud Run. Это более безопасно и является рекомендуемой практикой.

При создании или обновлении сервиса Cloud Run (через консоль или gcloud CLI), перейдите в раздел "Переменные и секреты" ("Variables & Secrets") и добавьте следующие переменные:

- `GOOGLE_API_KEY`: Ваш API-ключ для Google Gemini.
- `GCS_BUCKET_NAME`: Имя вашего бакета в Google Cloud Storage.
- `FF_BASE_DIR`: Путь к базе знаний (если отличается от значения по умолчанию).
- `LOG_LEVEL`: Уровень логирования (например, `INFO`).
- `GOOGLE_APPLICATION_CREDENTIALS`: Путь к ключу сервисного аккаунта (обычно `./service-account-key.json`, если он включен в Docker-образ).

Вы можете использовать Secret Manager для безопасного хранения `GOOGLE_API_KEY`, а затем подключить его как секрет в Cloud Run.

## Подготовка базы знаний

Перед деплоем необходимо подготовить базу знаний (эмбеддинги) и загрузить их в Google Cloud Storage:

1. Обновите локальную базу знаний из директории, указанной в переменной окружения `FF_BASE_DIR` (по умолчанию `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`):
   ```bash
   cd ..
   scripts/sync.sh
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

После деплоя приложения в Google Cloud Run вы можете обновлять базу знаний следующим способом:

### Локальное обновление и синхронизация

1. Обновите локальную базу знаний:
   ```bash
   cd ..
   scripts/sync.sh
   ```

2. Это обновит эмбеддинги в Google Cloud Storage, откуда их будет использовать запущенное приложение.

## Дополнительные настройки

- Убедитесь, что у вашего сервиса в Cloud Run есть права доступа к Google Cloud Storage, если вы используете его.
- Если вы используете Google Cloud Storage, убедитесь, что бакет создан и настроен.