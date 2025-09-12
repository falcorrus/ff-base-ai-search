# Деплой фронтенда на Firebase Hosting

Фронтенд проекта успешно развернут на Firebase Hosting и доступен по адресу: https://ff-base-4d8ee.web.app/



  Если ты хочешь обновить базу знаний из локальной директории, указанной в переменной окружения `FF_BASE_DIR` (по умолчанию `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`), можешь
  выполнить запрос:

   1 curl http://localhost:8000/update-knowledge-base-local





## Предварительные требования

1. Убедитесь, что у вас установлен Node.js и npm
2. Установите Firebase CLI (если еще не установлен):
   ```
   npm install -g firebase-tools
   ```

## Шаги для развертывания

1. Авторизуйтесь в Firebase:
   ```
   firebase login
   ```

2. Создайте новый проект в Firebase Console:
   - Перейдите на сайт https://console.firebase.google.com/
   - Нажмите "Создать проект"
   - Введите имя проекта (например, "ff-base-ai-search")
   - Следуйте инструкциям для создания проекта

3. В директории frontend-react выполните инициализацию Firebase:
   ```
   cd frontend-react
   firebase use --add
   ```
   
   При инициализации:
   - Выберите ваш созданный проект из списка
   - Выберите псевдоним "default" для проекта

4. Инициализируйте Firebase Hosting:
   ```
   firebase init hosting
   ```
   
   При инициализации:
   - Выберите ваш проект Firebase
   - Укажите public директорию как "."
   - Настройте перезапись всех URL на index.html (для SPA)
   - Ответьте "No" на вопрос о перезаписи существующих файлов

5. Выполните развертывание:
   ```
   firebase deploy --only hosting
   ```

## Альтернативный способ развертывания через CI/CD

Если вы хотите настроить автоматический деплой, вы можете использовать Firebase CLI token:

1. Создайте токен:
   ```
   firebase login:ci
   ```

2. Используйте этот токен в вашем CI/CD pipeline.

## Настройка кастомного домена (опционально)

1. Перейдите в Firebase Console
2. Выберите ваш проект
3. Перейдите в раздел Hosting
4. В настройках домена добавьте ваш кастомный домен
5. Следуйте инструкциям по настройке DNS записей

## Проверка развертывания

После успешного развертывания вы получите URL вида:
`https://your-project-id.web.app` или `https://your-project-id.firebaseapp.com`

Вы можете открыть этот URL в браузере для проверки работы фронтенда.

Фронт развернут на https://ff-base-4d8ee.web.app