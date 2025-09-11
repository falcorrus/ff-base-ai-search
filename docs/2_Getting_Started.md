# Начало работы

## Установка и запуск

### Бэкенд

1. Установите зависимости:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Создайте файл `.env` в корне проекта, скопировав пример:
   ```bash
   cp .env.example .env
   ```
   Затем отредактируйте `.env` и укажите ваши реальные значения, как минимум `GOOGLE_API_KEY`.

3. Запустите сервер:
   ```bash
   cd backend
   ./start.sh
   # Или альтернативно:
   # uvicorn main:app --reload --port 8000
   ```

### Фронтенд

1. Откройте `frontend/index.html` в браузере или запустите локальный сервер:
   ```bash
   cd frontend
   python -m http.server 3000
   ```
