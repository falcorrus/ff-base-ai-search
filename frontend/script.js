document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsDiv = document.getElementById('results');
    const notesCountDiv = document.getElementById('notes-count'); // New element

    // Function to fetch and display notes count
    async function fetchNotesCount() {
        try {
            const response = await fetch('http://localhost:8000/notes-count');
            const data = await response.json();
            if (data.count !== undefined) {
                notesCountDiv.textContent = `Загружено заметок: ${data.count}`;
            } else {
                notesCountDiv.textContent = 'Не удалось загрузить количество заметок.';
            }
        } catch (error) {
            console.error('Error fetching notes count:', error);
            notesCountDiv.textContent = 'Ошибка загрузки количества заметок.';
        }
    }

    // Call fetchNotesCount on page load
    fetchNotesCount();

    // Функция для выполнения поиска
    async function performSearch(query) {
        if (!query.trim()) {
            resultsDiv.innerHTML = '<div class="error">Пожалуйста, введите запрос для поиска.</div>';
            return;
        }

        // Показываем индикатор загрузки
        resultsDiv.innerHTML = '<div class="loading">Идет поиск...</div>';
        resultsDiv.className = 'loading';

        try {
            // Выполняем запрос к бэкенду
            const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Отображаем результаты
            if (data.error) {
                resultsDiv.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
            } else if (data.relevant_documents && data.relevant_documents.length > 0) {
                // Display the AI-generated answer
                let htmlContent = `<h2>Ответ:</h2><p>${data.answer}</p>`;
                
                // Display relevant documents
                htmlContent += '<h3>Найденные заметки:</h3><ul>';
                data.relevant_documents.forEach(doc => {
                    // Extract filename from file_path for display
                    const fileName = doc.file_path.split('/').pop().replace('.md', '');
                    htmlContent += `<li><a href="#" target="_blank">${fileName}</a> (Релевантность: ${(doc.similarity * 100).toFixed(2)}%)</li>`;
                });
                htmlContent += '</ul>';
                
                resultsDiv.innerHTML = `<div class="success">${htmlContent}</div>`;
            } else {
                resultsDiv.innerHTML = '<div class="info">По вашему запросу заметки не найдены.</div>';
            }
        } catch (error) {
            resultsDiv.innerHTML = `<div class="error">Ошибка при выполнении поиска: ${error.message}</div>`;
        }

        resultsDiv.className = '';
    }

    // Обработчик клика по кнопке поиска
    searchButton.addEventListener('click', () => {
        const query = searchInput.value;
        performSearch(query);
    });

    // Обработчик нажатия Enter в поле ввода
    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            const query = searchInput.value;
            performSearch(query);
        }
    });
});