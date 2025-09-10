document.addEventListener('DOMContentLoaded', () => {
    console.log('Script loaded');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsDiv = document.getElementById('results');
    const notesCountDiv = document.getElementById('notes-count');

    // Function to fetch and display notes count
    async function fetchNotesCount() {
        try {
            console.log('Fetching notes count from backend');
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
            resultsDiv.innerHTML = '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">Пожалуйста, введите запрос для поиска.</div>';
            return;
        }

        // Показываем индикатор загрузки
        resultsDiv.innerHTML = '<div class="text-center text-gray-600">Идет поиск...</div>';

        try {
            // Выполняем запрос к бэкенду
            const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Отображаем результаты
            if (data.error) {
                resultsDiv.innerHTML = `<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">Ошибка: ${data.error}</div>`;
            } else if (data.answer) {
                // Display the AI-generated answer
                let htmlContent = `
                    <div class="mb-6">
                        <h2 class="text-xl font-bold text-gray-800 mb-3">Ответ:</h2>
                        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <p class="text-gray-700">${data.answer}</p>
                        </div>
                    </div>
                `;
                
                // Display relevant documents if they exist
                if (data.relevant_documents && data.relevant_documents.length > 0) {
                    htmlContent += `
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800 mb-3">Найденные заметки:</h3>
                            <ul class="space-y-2">
                    `;
                    
                    data.relevant_documents.forEach(doc => {
                        // Extract filename from file_path for display
                        const fileName = doc.file_path.split('/').pop().replace('.md', '');
                        htmlContent += `
                            <li class="flex justify-between items-center bg-gray-50 p-3 rounded hover:bg-gray-100">
                                <span class="font-medium text-gray-700">${fileName}</span>
                                <span class="text-sm text-gray-500">Релевантность: ${(doc.similarity * 100).toFixed(2)}%</span>
                            </li>
                        `;
                    });
                    
                    htmlContent += `
                            </ul>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = htmlContent;
            } else {
                resultsDiv.innerHTML = '<div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4">По вашему запросу заметки не найдены.</div>';
            }
        } catch (error) {
            resultsDiv.innerHTML = `<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">Ошибка при выполнении поиска: ${error.message}</div>`;
        }
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