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
                notesCountDiv.textContent = data.count;
            } else {
                notesCountDiv.textContent = 'Не удалось загрузить';
            }
        } catch (error) {
            console.error('Error fetching notes count:', error);
            notesCountDiv.textContent = 'Ошибка загрузки';
        }
    }

    // Call fetchNotesCount on page load
    fetchNotesCount();

    // Функция для выполнения поиска
    async function performSearch(query) {
        if (!query.trim()) {
            resultsDiv.innerHTML = `
                <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm animate-fade-in">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <i class="fas fa-exclamation-circle text-red-500 text-xl"></i>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-red-700">
                                <span class="font-medium">Ошибка:</span> Пожалуйста, введите запрос для поиска.
                            </p>
                        </div>
                    </div>
                </div>
            `;
            return;
        }

        // Показываем индикатор загрузки с анимацией
        resultsDiv.innerHTML = `
            <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
                <div class="flex items-center justify-center">
                    <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mr-3"></div>
                    <p class="text-gray-600 text-lg">Ищем наиболее релевантные заметки...</p>
                </div>
                <div class="mt-4 w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full animate-pulse" style="width: 75%"></div>
                </div>
            </div>
        `;

        try {
            // Выполняем запрос к бэкенду
            const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Отображаем результаты
            if (data.error) {
                resultsDiv.innerHTML = `
                    <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm animate-fade-in">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <i class="fas fa-exclamation-circle text-red-500 text-xl"></i>
                            </div>
                            <div class="ml-3">
                                <p class="text-sm text-red-700">
                                    <span class="font-medium">Ошибка:</span> ${data.error}
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            } else if (data.answer) {
                // Display the AI-generated answer with enhanced styling
                let htmlContent = `
                    <div class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200 animate-fade-in">
                        <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-4">
                            <h2 class="text-xl font-bold text-white flex items-center">
                                <i class="fas fa-robot mr-2"></i> Интеллектуальный ответ
                            </h2>
                        </div>
                        <div class="p-6">
                            <div class="prose max-w-none">
                                <div class="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                                    <div class="flex items-start">
                                        <div class="flex-shrink-0">
                                            <i class="fas fa-lightbulb text-blue-500 text-lg mt-1"></i>
                                        </div>
                                        <div class="ml-3">
                                            <p class="text-gray-700">${data.answer}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                // Display relevant documents if they exist with enhanced styling
                if (data.relevant_documents && data.relevant_documents.length > 0) {
                    htmlContent += `
                        <div class="bg-white rounded-xl shadow-lg mt-6 overflow-hidden border border-gray-200 animate-fade-in-delay">
                            <div class="bg-gradient-to-r from-green-500 to-teal-600 p-4">
                                <h3 class="text-lg font-bold text-white flex items-center">
                                    <i class="fas fa-file-alt mr-2"></i> Найденные заметки (${data.relevant_documents.length})
                                </h3>
                            </div>
                            <div class="p-4">
                                <ul class="space-y-3">
                    `;
                    
                    data.relevant_documents.forEach((doc, index) => {
                        // Extract filename from file_path for display
                        const fileName = doc.file_path.split('/').pop().replace('.md', '');
                        const similarity = (doc.similarity * 100).toFixed(2);
                        
                        // Determine color based on similarity
                        let similarityColor = 'text-gray-500';
                        if (similarity > 80) similarityColor = 'text-green-600';
                        else if (similarity > 60) similarityColor = 'text-yellow-600';
                        else if (similarity > 40) similarityColor = 'text-orange-600';
                        
                        htmlContent += `
                            <li class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-300">
                                <div class="flex justify-between items-center">
                                    <div class="flex items-center">
                                        <div class="bg-gray-100 p-2 rounded-lg mr-3">
                                            <i class="fas fa-file-alt text-gray-600"></i>
                                        </div>
                                        <div>
                                            <span class="font-medium text-gray-800">${fileName}</span>
                                            <div class="text-xs text-gray-500 mt-1">
                                                <i class="fas fa-folder mr-1"></i> 
                                                ${doc.file_path.split('/').slice(-2, -1)[0] || 'Корневая папка'}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex items-center">
                                        <div class="mr-2">
                                            <div class="text-sm font-medium ${similarityColor}">${similarity}%</div>
                                            <div class="text-xs text-gray-500">релевантность</div>
                                        </div>
                                        <div class="w-12 h-12">
                                            <div class="relative">
                                                <svg class="w-12 h-12">
                                                    <circle cx="24" cy="24" r="20" fill="none" stroke="#e5e7eb" stroke-width="3"></circle>
                                                    <circle 
                                                        cx="24" cy="24" r="20" fill="none" 
                                                        stroke="${similarity > 80 ? '#10b981' : similarity > 60 ? '#f59e0b' : similarity > 40 ? '#f97316' : '#9ca3af'}" 
                                                        stroke-width="3" 
                                                        stroke-dasharray="125.6" 
                                                        stroke-dashoffset="${125.6 * (1 - doc.similarity)}" 
                                                        transform="rotate(-90 24 24)"
                                                    ></circle>
                                                </svg>
                                                <div class="absolute inset-0 flex items-center justify-center text-xs font-bold ${similarityColor}">
                                                    ${Math.round(similarity)}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3 ml-11">
                                    <div class="w-full bg-gray-200 rounded-full h-1.5">
                                        <div 
                                            class="h-1.5 rounded-full ${similarity > 80 ? 'bg-green-500' : similarity > 60 ? 'bg-yellow-500' : similarity > 40 ? 'bg-orange-500' : 'bg-gray-500'}" 
                                            style="width: ${similarity}%"
                                        ></div>
                                    </div>
                                </div>
                            </li>
                        `;
                    });
                    
                    htmlContent += `
                                </ul>
                            </div>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = htmlContent;
            } else {
                resultsDiv.innerHTML = `
                    <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-lg shadow-sm animate-fade-in">
                        <div class="flex">
                            <div class="flex-shrink-0">
                                <i class="fas fa-exclamation-triangle text-yellow-500 text-xl"></i>
                            </div>
                            <div class="ml-3">
                                <p class="text-sm text-yellow-700">
                                    <span class="font-medium">Внимание:</span> По вашему запросу заметки не найдены.
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            resultsDiv.innerHTML = `
                <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm animate-fade-in">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <i class="fas fa-exclamation-circle text-red-500 text-xl"></i>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-red-700">
                                <span class="font-medium">Ошибка:</span> Не удалось выполнить поиск. Пожалуйста, проверьте подключение к серверу.
                            </p>
                            <p class="text-xs text-red-600 mt-1">${error.message}</p>
                        </div>
                    </div>
                </div>
            `;
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