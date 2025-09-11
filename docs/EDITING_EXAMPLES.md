# Примеры редактирования интерфейса

## 1. Изменение цветовой схемы

### Изменение градиента в заголовке

Было:
```html
<div class="bg-gradient-to-r from-blue-500 to-purple-600 p-3 rounded-full shadow-lg">
    <i class="fas fa-brain text-white text-2xl"></i>
</div>
```

Стало (теплые цвета):
```html
<div class="bg-gradient-to-r from-orange-500 to-red-600 p-3 rounded-full shadow-lg">
    <i class="fas fa-brain text-white text-2xl"></i>
</div>
```

### Изменение цвета фона страницы

Было:
```html
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
```

Стало:
```html
<body class="bg-gradient-to-br from-gray-100 to-gray-300 min-h-screen">
```

## 2. Добавление нового элемента

Добавим панель приветствия после заголовка:

```html
<!-- После закрывающего тега </header> добавьте: -->
<div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white mb-8">
    <div class="flex items-center">
        <div class="mr-4">
            <i class="fas fa-hand-wave text-2xl"></i>
        </div>
        <div>
            <h2 class="text-xl font-bold mb-1">Добро пожаловать!</h2>
            <p class="opacity-90">Исследуйте ваши заметки с помощью интеллектуального поиска</p>
        </div>
    </div>
</div>
```

## 3. Изменение стиля кнопки поиска

Было:
```html
<button 
    id="search-button" 
    class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-4 font-medium transition-all duration-300 transform hover:scale-105"
>
    <i class="fas fa-search mr-2"></i>Искать
</button>
```

Стало (более плоский дизайн):
```html
<button 
    id="search-button" 
    class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 font-medium transition-colors duration-300 rounded-r-lg"
>
    <i class="fas fa-search mr-2"></i>Искать
</button>
```

## 4. Изменение анимаций

В файле `styles/globals.css` можно изменить анимации:

Было:
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

Стало (более плавное появление):
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}
```

## 5. Изменение шрифтов

В HTML можно добавить Google Fonts:

В `<head>` добавьте:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

И в стилях:
```css
body {
    @apply bg-background text-foreground;
    font-family: 'Inter', sans-serif;
    font-feature-settings: "rlig" 1, "calt" 1;
}
```

## 6. Добавление темной темы

Добавьте переключатель темы в HTML:
```html
<!-- В header добавьте: -->
<div class="absolute top-4 right-4">
    <button id="theme-toggle" class="bg-gray-200 p-2 rounded-full">
        <i class="fas fa-moon"></i>
    </button>
</div>
```

И соответствующий JavaScript:
```javascript
// Добавьте в конец script.js:
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        const icon = themeToggle.querySelector('i');
        if (document.body.classList.contains('dark')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });
});
```

## Как применить изменения:

1. Внесите изменения в `index.html`
2. Если меняли CSS, пересоберите стили:
   ```bash
   cd frontend
   npm run build:css
   ```
3. Перезапустите сервер:
   ```bash
   pkill -f "node server.js" && npm start
   ```