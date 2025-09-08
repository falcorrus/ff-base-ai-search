# ff-base-ai-search

Интеллектуальная система поиска по базе знаний пользователя, хранящейся в виде Markdown-файлов в репозитории GitHub.

## Описание проекта

Этот проект представляет собой веб-приложение для интеллектуального поиска и генерации комплексных ответов на основе личной базы знаний, состоящей из Markdown заметок, хранящихся в репозитории GitHub [falcorrus/ff-base](https://github.com/falcorrus/ff-base).

Проект использует векторный поиск и большие языковые модели (LLM) для предоставления быстрых и точных ответов на основе базы знаний пользователя.

## Ключевые технологии

* **Бэкенд:** Python 3.9+, FastAPI
* **ИИ:** Google Gemini API (для генерации embeddings и ответов)
* **Хранилище данных:** GitHub API (для получения Markdown файлов), локальное JSON хранилище (для embeddings)
* **Фронтенд:** Vanilla JavaScript (в процессе разработки)
* **Деплой:** Google Cloud Run (бэкенд), Firebase Hosting (фронтенд)

## Архитектура

1. **Синхронизация:** Получение Markdown заметок из репозитория GitHub `falcorrus/ff-base`
2. **Генерация embeddings:** Создание и хранение векторных представлений для каждой заметки с использованием Google Gemini API
3. **Поиск:** Преобразование пользовательского запроса в embedding и поиск релевантных заметок через векторное сходство
4. **Генерация ответа:** Формирование контекста из релевантных заметок и отправка его в Google Gemini LLM для генерации комплексного ответа
5. **Логирование:** Все запросы логируются в JSON файл

## Структура проекта

```
ff-base-ai-search/
├── backend/                 # Бэкенд приложение на FastAPI
│   ├── main.py             # Основной файл приложения
│   ├── requirements.txt    # Зависимости Python
│   └── .env                # Переменные окружения
├── frontend/               # Фронтенд приложение (в разработке)
│   ├── index.html          # Главная страница
│   ├── style.css           # Стили
│   └── script.js           # JavaScript код
├── knowledge_base/         # Локальное хранилище embeddings
│   └── embeddings.json     # Векторные представления заметок
└── ...
```

## Установка и запуск

### Бэкенд

1. Установите зависимости:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Создайте файл `.env` с необходимыми переменными окружения:
   ```
   GITHUB_PAT=ваш_github_personal_access_token
   GEMINI_API_KEY=ваш_google_gemini_api_key
   GITHUB_REPO_OWNER=falcorrus
   GITHUB_REPO_NAME=ff-base
   ```

3. Запустите сервер:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

### Фронтенд

1. Откройте `frontend/index.html` в браузере или запустите локальный сервер:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

## API эндпоинты

* `GET /` - Проверка работы сервера
* `GET /update-knowledge-base` - Обновление базы знаний из GitHub репозитория
* `GET /search?query={запрос}` - Поиск по заметкам и генерация ответа

## Деплой

* **Бэкенд:** Google Cloud Run
* **Фронтенд:** Firebase Hosting

## Лицензия

MIT