# FF-BASE AI Search System

Система интеллектуального поиска по заметкам из Google Drive с использованием Google Cloud Platform.

## Обзор

Этот проект предоставляет интеллектуальный поиск по вашим заметкам из Google Drive, используя векторные эмбеддинги и Large Language Models (LLM) от Google Gemini. Заметки автоматически синхронизируются из папки `FF-BASE` в Google Drive в бакет Google Cloud Storage, а затем обрабатываются для создания векторных представлений.

## Компоненты системы

### 1. Синхронизация
- **Источник**: Папка `FF-BASE` в Google Drive
- **Назначение**: Бакет `ff-base-knowledge-base` в Google Cloud Storage
- **Метод**: Инкрементальная синхронизация с проверкой хэшей
- **Расписание**: Ежедневно в 23:00 по Московскому времени

### 2. Обработка заметок
- **Создание эмбеддингов**: Использование модели `models/embedding-001` от Google Gemini
- **Хранение**: JSON-файл с эмбеддингами в GCS
- **Обновление**: Автоматическое обновление при изменении заметок

### 3. Поиск
- **Векторный поиск**: Сравнение запроса с эмбеддингами заметок
- **LLM**: Использование Google Gemini для генерации ответов
- **API**: RESTful API для интеграции с внешними приложениями

### 4. Мониторинг
- **Логирование**: Подробные логи всех операций
- **Метрики**: Отслеживание производительности и ошибок
- **Уведомления**: Уведомления в Telegram о результатах синхронизации
- **Расписание**: Автоматическое выполнение задач по расписанию

## Структура проекта

```
ff-base-ai-search/
├── backend/                    # Backend приложение (FastAPI)
│   ├── main.py                # Основной код API
│   ├── requirements.txt       # Зависимости backend
│   ├── service-account-key.json # Ключи сервисного аккаунта
│   └── venv/                  # Виртуальное окружение
├── cloud-function/            # Облачные функции
│   ├── main.py               # Основной код облачной функции
│   ├── enhanced_sync.py      # Улучшенная версия синхронизации
│   ├── requirements.txt      # Зависимости Cloud Functions
│   ├── deploy.sh            # Скрипт развертывания
│   ├── setup_scheduler.sh   # Скрипт настройки Cloud Scheduler
│   └── monitor/             # Скрипты мониторинга
│       ├── manage_monitoring.sh
│       ├── view_logs.sh
│       ├── view_metrics.sh
│       └── ...
├── FF-BASE/                  # Локальная копия заметок (если используется)
├── knowledge_base/           # Локальная база знаний (эмбеддинги, логи)
├── frontend/                 # Frontend приложение (если используется)
└── tests/                    # Тесты
```

## Установка и настройка

### 1. Предварительные требования
- Google Cloud Platform аккаунт
- Google Drive с папкой `FF-BASE`
- Python 3.9+
- Google Cloud SDK

### 2. Настройка backend
```bash
# Переход в директорию backend
cd backend

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл с вашими данными
```

### 3. Настройка Cloud Functions
```bash
# Переход в директорию cloud-function
cd cloud-function

# Установка зависимостей
pip install -r requirements.txt

# Развертывание функции
./deploy.sh

# Настройка расписания
./setup_scheduler.sh
```

### 4. Настройка мониторинга
```bash
# Переход в директорию мониторинга
cd cloud-function/monitor

# Запуск менеджера мониторинга
./manage_monitoring.sh
```

### 5. Настройка frontend (shadcn/ui)
```bash
# Переход в директорию frontend
cd frontend

# Установка зависимостей shadcn/ui
npm install class-variance-authority clsx tailwind-merge lucide-react tw-animate-css

# Добавление компонентов
npx shadcn@latest add button
```

Более подробную информацию о настройке и использовании shadcn/ui можно найти в файле `frontend/SHADCN_UI.md`.
Подробный отчет о проделанной работе находится в файле `frontend/SHADCN_UI_SETUP_SUMMARY.md`.

## Использование

### Запуск backend сервера
```bash
# Активация виртуального окружения
source backend/venv/bin/activate

# Запуск сервера
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Или используйте скрипт запуска:
```bash
cd backend
./start.sh
```

### Запуск frontend сервера
```bash
# Переход в директорию frontend
cd frontend

# Запуск сервера
npm start
```

### Запуск всего окружения для разработки
```bash
# Запуск обоих серверов
./scripts/start-dev.sh

# Остановка серверов
./scripts/stop-dev.sh
```

После запуска:
- Backend будет доступен по адресу: http://localhost:8000
- Frontend будет доступен по адресу: http://localhost:3000

### Ручной запуск синхронизации
```bash
# Активация виртуального окружения
source backend/venv/bin/activate

# Запуск синхронизации
cd cloud-function
python enhanced_sync.py
```

### Просмотр документации API
Откройте в браузере: `http://localhost:8000/docs`

## Эндпоинты API

- `GET /` - Проверка состояния системы
- `GET /update-knowledge-base` - Обновление базы знаний из GitHub
- `GET /update-knowledge-base-local` - Обновление базы знаний из локальной папки
- `GET /search?query={query}` - Поиск по заметкам
- `GET /notes-count` - Получение количества заметок в базе

## Мониторинг и уведомления

### Просмотр логов
```bash
# Просмотр логов Cloud Functions
gcloud functions logs read sync-drive-to-gcs --limit 50

# Просмотр логов Cloud Scheduler
gcloud scheduler jobs logs read sync-drive-to-gcs-daily --limit 50
```

### Уведомления в Telegram
Система отправляет уведомления в Telegram о результатах синхронизации:
- ✅ Успешное завершение синхронизации
- ❌ Ошибки синхронизации
- ⏱️ Время выполнения операций

## Безопасность

- Все ключи и токены хранятся в Secret Manager
- Используются сервисные аккаунты с минимальными необходимыми правами
- HTTPS для всех API эндпоинтов
- Аутентификация через Google OAuth 2.0

## Стоимость

Все компоненты системы находятся в пределах бесплатных лимитов Google Cloud:
- Cloud Functions: Бесплатно (в пределах лимита)
- Cloud Storage: Бесплатно (в пределах лимита)
- Cloud Scheduler: Бесплатно (3 задачи в месяц)
- Google Drive API: Бесплатно (чтение)
- Google Gemini API: Бесплатно (в пределах лимита)

Общая стоимость: **$0.00 в месяц**

## Разработка

### Запуск тестов
```bash
# Активация виртуального окружения
source backend/venv/bin/activate

# Запуск тестов
cd tests
python -m pytest
```

### Добавление новых функций
1. Создайте новую ветку для разработки
2. Реализуйте функциональность
3. Напишите тесты
4. Проверьте работоспособность
5. Слейте изменения в основную ветку

## Поддержка

Если у вас возникли вопросы или проблемы с системой, пожалуйста:
1. Проверьте логи системы
2. Обратитесь к документации
3. Создайте issue в репозитории
4. Свяжитесь с разработчиком через Telegram

## Лицензия

MIT License