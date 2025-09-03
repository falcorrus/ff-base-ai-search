# Intelligent Search Backend

Backend для приложения "Intelligent Search", реализованный на Node.js с TypeScript и Express.js.

## Технологии

- **Node.js**: Среда выполнения JavaScript
- **TypeScript**: Язык программирования для типобезопасной разработки
- **Express.js**: Веб-фреймворк для Node.js
- **Google Gemini API**: Для создания векторных представлений и генерации ответов
- **Octokit**: Для работы с GitHub API
- **JSON-файл**: Векторная база данных (для прототипа)

## Структура проекта

```
backend/
├── src/
│   ├── config/          # Конфигурация приложения
│   ├── controllers/     # Контроллеры для обработки запросов
│   ├── middleware/      # Промежуточное ПО
│   ├── models/          # Модели данных
│   ├── routes/          # Маршруты API
│   ├── services/        # Сервисы для бизнес-логики
│   ├── utils/           # Вспомогательные функции
│   └── index.ts         # Точка входа приложения
├── dist/                # Скомпилированный JavaScript код
├── data/                # Данные приложения (векторная база)
├── package.json         # Зависимости и скрипты
├── tsconfig.json        # Конфигурация TypeScript
└── .env.example         # Пример файла переменных окружения
```

## Доступные скрипты

- `npm run dev` - Запуск приложения в режиме разработки с hot-reload
- `npm run build` - Компиляция TypeScript в JavaScript
- `npm start` - Запуск скомпилированного приложения

## API Endpoints

### Поиск

- `GET /api/search?q={query}` - Поиск документов по запросу
- `GET /api/note/:id` - Получение содержимого документа по ID

## Переменные окружения

Для работы приложения необходимо создать файл `.env` в корне проекта со следующими переменными:

```
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key_here
PORT=3001
VECTOR_DB_PATH=./data/vector-db.json
```

Пример файла можно найти в `.env.example`.

## Разработка

1. Установите зависимости: `npm install`
2. Создайте файл `.env` с вашими переменными окружения
3. Запустите приложение в режиме разработки: `npm run dev`
4. Сервер будет доступен по адресу: `http://localhost:3001`