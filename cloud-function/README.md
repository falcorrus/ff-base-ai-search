# Cloud Function для синхронизации заметок из Google Drive в Google Cloud Storage

Эта облачная функция автоматически синхронизирует заметки из папки Google Drive `FF-BASE` в бакет Google Cloud Storage `ff-base-knowledge-base`.

https://console.cloud.google.com/functions/details/us-central1/sync-drive-to-gcs?project=ff-base

## Особенности

- **Оптимизированная синхронизация**: Сначала сравнивает хэш папки в Google Drive с сохраненным хэшем в GCS
- **Инкрементальная синхронизация**: Синхронизирует только измененные файлы
- **Параллельная обработка**: Ускоренная обработка множества файлов
- **Автономная работа**: Работает независимо от состояния локального компьютера
- **Расписание**: Ежедневный запуск в 23:00 по московскому времени

## Архитектура

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Cloud Scheduler │───▶│ Google Cloud     │───▶│ Google Drive     │
│ (ежедневно 23:00 │    │   Functions      │    │ (источник)       │
│  по Москве)     │    │ sync-drive-to-gcs│    └──────────────────┘
└─────────────────┘    └──────────────────┘    ┌──────────────────┐
                                                │ Google Cloud     │
                                                │ Storage          │
                                                │ (назначение)     │
                                                └──────────────────┘
```

## Установка и настройка

### 1. Предварительные требования

1. Установленный `gcloud` CLI
2. Аутентификация в Google Cloud:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. Включенные API:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudscheduler.googleapis.com
   gcloud services enable storage-api.googleapis.com
   gcloud services enable drive.googleapis.com
   ```

### 2. Развертывание облачной функции

```bash
cd cloud-function
./deploy.sh
```

### 3. Настройка расписания

```bash
./setup_scheduler.sh
```

## Конфигурация

### Переменные окружения

- `GOOGLE_SERVICE_ACCOUNT_KEY`: JSON-ключ сервисного аккаунта
- `BUCKET_NAME`: Имя бакета GCS (по умолчанию `ff-base-knowledge-base`)

### Файлы конфигурации

- `drive_folder_hash.txt`: Хэш папки Google Drive (хранится в GCS)
- `metadata_cache.json`: Кэш метаданных файлов (хранится в GCS)
- `last_sync_token.json`: Токен последней синхронизации (хранится в GCS)

## Мониторинг

### Просмотр логов

```bash
gcloud functions logs read sync-drive-to-gcs --project=YOUR_PROJECT_ID
```

### Просмотр запланированных задач

```bash
gcloud scheduler jobs list --project=YOUR_PROJECT_ID --location=us-central1
```

## Безопасность

### Сервисный аккаунт

Функция использует сервисный аккаунт с минимальными необходимыми правами:

- `roles/storage.objectAdmin` для бакета `ff-base-knowledge-base`
- Доступ на чтение к папке Google Drive `FF-BASE`

### Ключи и секреты

- Ключи хранятся в Secret Manager
- Переменные окружения передаются безопасно
- Никакие секреты не хранятся в коде

## Стоимость

При ежедневной синхронизации:

- **Cloud Functions**: Бесплатно (в пределах бесплатного лимита)
- **Cloud Storage**: ~$0.0013/месяц за хранение метаданных
- **Cloud Scheduler**: Бесплатно (в пределах бесплатного лимита)

Итого: **$0.0013/месяц** (~$0.02/год)

## Устранение неполадок

### Ошибка аутентификации

1. Проверьте, что сервисный аккаунт имеет необходимые права
2. Убедитесь, что ключ сервисного аккаунта действителен
3. Проверьте переменные окружения

### Ошибка доступа к Google Drive

1. Убедитесь, что папка `FF-BASE` существует в Google Drive
2. Проверьте права доступа к папке для сервисного аккаунта
3. Убедитесь, что API Google Drive включен

### Ошибка доступа к GCS

1. Проверьте, что бакет `ff-base-knowledge-base` существует
2. Убедитесь, что сервисный аккаунт имеет права на запись в бакет
3. Проверьте квоты использования GCS

## Разработка

### Локальная разработка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите функцию локально:
   ```bash
   functions-framework --target=sync_drive_to_gcs_http
   ```

### Тестирование

```bash
python -m pytest tests/
```

## Лицензия

MIT License