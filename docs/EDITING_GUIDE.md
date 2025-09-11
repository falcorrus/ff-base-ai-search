# Руководство по редактированию элементов интерфейса

Это руководство поможет вам понять структуру интерфейса и научит вас редактировать различные элементы.

## 1. Структура HTML-файла

Файл `index.html` содержит основную структуру интерфейса и разделен на несколько секций:

### Header (Заголовок)
```html
<header class="text-center mb-12 mt-6">
    <div class="flex justify-center mb-4">
        <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-full shadow-lg">
            <i class="fas fa-brain text-white text-2xl"></i>
        </div>
    </div>
    <h1 class="text-4xl font-bold text-gray-800 mb-3">Интеллектуальный поиск по заметкам</h1>
    <p class="text-gray-600 max-w-2xl mx-auto">Используйте силу искусственного интеллекта для поиска и анализа ваших заметок</p>
</header>
```

### Stats Panel (Панель статистики)
```html
<div class="bg-white rounded-xl shadow-lg p-6 mb-8 border border-gray-200">
    <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="flex items-center mb-4 md:mb-0">
            <div class="bg-blue-100 p-3 rounded-lg mr-4">
                <i class="fas fa-file-alt text-blue-600 text-xl"></i>
            </div>
            <div>
                <p class="text-gray-500 text-sm">Загружено заметок</p>
                <p id="notes-count" class="text-2xl font-bold text-gray-800">Загрузка...</p>
            </div>
        </div>
        <div class="flex items-center">
            <div class="bg-green-100 p-3 rounded-lg mr-4">
                <i class="fas fa-bolt text-green-600 text-xl"></i>
            </div>
            <div>
                <p class="text-gray-500 text-sm">Технология</p>
                <p class="text-2xl font-bold text-gray-800">Google Gemini</p>
            </div>
        </div>
    </div>
</div>
```

### Search Section (Секция поиска)
```html
<div class="bg-white rounded-xl shadow-lg p-6 mb-8 border border-gray-200">
    <div class="mb-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-2">Поиск по заметкам</h2>
        <p class="text-gray-600">Введите запрос, и система интеллектуального поиска найдет наиболее релевантные заметки</p>
    </div>
    
    <div class="search-container">
        <div class="flex rounded-lg overflow-hidden shadow-md focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
            <input 
                type="text" 
                id="search-input" 
                placeholder="Например: Как настроить синхронизацию Google Drive?" 
                class="flex-grow px-5 py-4 text-gray-700 focus:outline-none border-0"
            >
            <button 
                id="search-button" 
                class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-4 font-medium transition-all duration-300 transform hover:scale-105"
            >
                <i class="fas fa-search mr-2"></i>Искать
            </button>
        </div>
        <div class="mt-3 text-sm text-gray-500 flex items-center">
            <i class="fas fa-lightbulb mr-2 text-yellow-500"></i>
            Попробуйте: "Как использовать API Google Drive" или "Настройка Cloud Functions"
        </div>
    </div>
</div>
```

### Results Section (Секция результатов)
```html
<div id="results" class="space-y-6"></div>
```

### Footer (Нижний колонтитул)
```html
<footer class="text-center py-6 text-gray-600 text-sm">
    <p>© 2025 Интеллектуальный поиск по заметкам. Используется технология Google Gemini.</p>
</footer>
```

## 2. Работа с CSS

CSS стили определяются в файле `styles/globals.css`. Мы используем Tailwind CSS с дополнительными кастомными стилями.

### Цветовая палитра
Основные цвета определены в переменных CSS:
- `--primary`: Основной цвет
- `--secondary`: Второстепенный цвет
- `--accent`: Акцентный цвет
- `--background`: Цвет фона
- `--foreground`: Цвет текста

### Кастомные анимации
В файле определены следующие анимации:
- `animate-fade-in`: Плавное появление
- `animate-fade-in-delay`: Плавное появление с задержкой
- `animate-pulse-slow`: Медленный пульс

## 3. Работа с JavaScript

JavaScript в файле `script.js` отвечает за интерактивность интерфейса.

### Основные функции:
1. `fetchNotesCount()` - Получает и отображает количество заметок
2. `performSearch(query)` - Выполняет поиск и отображает результаты
3. Обработчики событий для кнопки поиска и нажатия Enter

## 4. Как редактировать элементы

### Изменение текста
Чтобы изменить текст, просто отредактируйте соответствующий текст в HTML-тегах:
```html
<!-- Было -->
<h1 class="text-4xl font-bold text-gray-800 mb-3">Интеллектуальный поиск по заметкам</h1>

<!-- Стало -->
<h1 class="text-4xl font-bold text-gray-800 mb-3">Мой крутой поиск по заметкам</h1>
```

### Изменение стилей
Для изменения стилей можно использовать классы Tailwind CSS:
```html
<!-- Было -->
<div class="bg-white rounded-xl shadow-lg p-6 mb-8 border border-gray-200">

<!-- Стало (изменили фон и добавили отступ) -->
<div class="bg-blue-50 rounded-2xl shadow-xl p-8 mb-10 border-2 border-blue-200">
```

### Изменение цветов
Цвета можно изменить двумя способами:
1. Используя классы Tailwind:
```html
<!-- Было -->
<div class="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-full shadow-lg">

<!-- Стало (изменили градиент) -->
<div class="bg-gradient-to-r from-green-500 to-teal-600 p-3 rounded-full shadow-lg">
```

2. Или изменив переменные CSS в `styles/globals.css`:
```css
/* Было */
--primary: 222.2 47.4% 11.2%;

/* Стало */
--primary: 160 80% 40%;
```

### Добавление новых элементов
Чтобы добавить новый элемент, просто вставьте HTML в нужное место:
```html
<!-- Добавим информационную панель после header -->
<header>...</header>

<!-- Новая информационная панель -->
<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded">
    <div class="flex">
        <div class="flex-shrink-0">
            <i class="fas fa-info-circle text-yellow-400 text-xl"></i>
        </div>
        <div class="ml-3">
            <p class="text-sm text-yellow-700">
                <span class="font-medium">Совет:</span> Используйте точные фразы для более точного поиска.
            </p>
        </div>
    </div>
</div>

<div class="bg-white rounded-xl shadow-lg p-6 mb-8 border border-gray-200">
```

## 5. Работа с иконками

Мы используем Font Awesome для иконок. Чтобы изменить иконку:
1. Найдите нужную иконку на https://fontawesome.com/icons
2. Замените класс `fas fa-...` на нужный:
```html
<!-- Было -->
<i class="fas fa-brain text-white text-2xl"></i>

<!-- Стало -->
<i class="fas fa-robot text-white text-2xl"></i>
```

## 6. После внесения изменений

После внесения изменений в HTML или CSS, необходимо:
1. Пересобрать CSS (если меняли styles/globals.css):
```bash
cd frontend
npm run build:css
```

2. Перезапустить сервер:
```bash
# Остановить текущий сервер
pkill -f "node server.js"

# Запустить заново
npm start
```

Или используйте скрипт:
```bash
./scripts/stop-dev.sh
./scripts/start-dev.sh
```

## 7. Полезные классы Tailwind

### Цвета
- `bg-*` - Цвет фона (bg-red-500, bg-blue-100)
- `text-*` - Цвет текста (text-white, text-gray-800)
- `border-*` - Цвет границы (border-red-300)

### Отступы
- `p-*` - Padding (p-4, px-2, py-3)
- `m-*` - Margin (m-4, mx-2, my-3)
- `space-y-*` - Вертикальное расстояние между элементами

### Размеры
- `w-*` - Ширина (w-full, w-1/2)
- `h-*` - Высота (h-10, h-screen)
- `text-*` - Размер текста (text-sm, text-xl)

### Другие полезные классы
- `rounded-*` - Скругление углов (rounded, rounded-lg)
- `shadow-*` - Тени (shadow, shadow-lg)
- `flex` - Flexbox (flex, flex-col, items-center)
- `grid` - Grid (grid, grid-cols-2)