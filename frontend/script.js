document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsDiv = document.getElementById('results');

    // Функция для выполнения поиска
    async function performSearch(query) {
        if (!query.trim()) {
            resultsDiv.innerHTML = '<div class="error">Пожалуйста, введите запрос для поиска.</div>';
            return;
        }

        // Показываем индикатор загрузки
        resultsDiv.innerHTML = '<div class="loading">Идет поиск и генерация ответа...</div>';
        resultsDiv.className = 'loading';

        try {
            // Выполняем запрос к бэкенду
            const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Отображаем результаты
            if (data.error) {
                resultsDiv.innerHTML = `<div class="error">Ошибка: ${data.error}</div>`;
            } else if (data.result) {
                resultsDiv.innerHTML = `
                    <div class="success">
                        <h2>Ответ:</h2>
                        <p>${data.result}</p>
                        ${data.source ? `<p><strong>Источник:</strong> ${data.source}</p>` : ''}
                        ${data.similarity ? `<p><strong>Релевантность:</strong> ${(data.similarity * 100).toFixed(2)}%</p>` : ''}
                        <p><strong>Время запроса:</strong> ${data.timestamp}</p>
                    </div>
                `;
            } else {
                resultsDiv.innerHTML = '<div class="error">Не удалось получить результаты поиска.</div>';
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