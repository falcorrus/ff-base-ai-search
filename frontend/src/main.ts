// main.ts
// Точка входа для пользовательского JavaScript/TypeScript кода

// Импортируем HTMX
import 'htmx.org';

// Обработчик для модального окна просмотра заметки
document.addEventListener('DOMContentLoaded', () => {
  // Получаем элементы модального окна
  const modal = document.getElementById('note-modal') as HTMLElement;
  const closeModalBtn = document.getElementById('close-modal') as HTMLElement;
  
  // Функция для закрытия модального окна
  const closeModal = () => {
    if (modal) {
      modal.classList.add('hidden');
    }
  };
  
  // Закрытие модального окна при клике на кнопку закрытия
  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
  }
  
  // Закрытие модального окна при клике вне его содержимого
  if (modal) {
    modal.addEventListener('click', (event) => {
      if (event.target === modal) {
        closeModal();
      }
    });
  }
  
  // Обработчик для открытия модального окна через HTMX
  document.body.addEventListener('openModal', (event: any) => {
    if (modal) {
      // Получаем данные из события
      const detail = event.detail;
      
      // Заполняем содержимое модального окна
      const modalTitle = document.getElementById('modal-title');
      const modalContent = document.getElementById('modal-content');
      const githubLink = document.getElementById('github-link') as HTMLAnchorElement;
      
      if (modalTitle) modalTitle.textContent = detail.title;
      if (modalContent) modalContent.innerHTML = detail.content;
      if (githubLink) {
        githubLink.href = detail.githubUrl;
        githubLink.textContent = `View ${detail.title} on GitHub`;
      }
      
      // Открываем модальное окно
      modal.classList.remove('hidden');
    }
  });
});

// Функция для создания карточки результата
async function createResultCard(result: any): Promise<string> {
  const response = await fetch('/src/search-result.html');
  const template = await response.text();
  
  return template
    .replace('{{title}}', result.title)
    .replace('{{excerpt}}', result.excerpt)
    .replace('{{path}}', result.path)
    .replace('{{githubUrl}}', result.githubUrl)
    .replace('{{id}}', result.id);
}

// Обработчик для отображения результатов поиска
document.body.addEventListener('htmx:afterOnLoad', async (event: any) => {
  console.log('htmx:afterOnLoad event fired.');
  console.log('Event detail XHR responseURL:', event.detail.xhr.responseURL);

  // Проверяем, что запрос был к /api/search
  if (event.detail.xhr.responseURL && event.detail.xhr.responseURL.includes('/api/search')) {
    console.log('Request path starts with /api/search.');
    try {
      // Парсим ответ
      const responseText = event.detail.xhr.responseText;
      console.log('Raw response text:', responseText);
      const response = JSON.parse(responseText);
      console.log('Parsed response object:', response);

      // Отображаем AI-ответ, если он есть
      const aiAnswer = document.getElementById('ai-answer');
      const answerContent = document.getElementById('answer-content');

      console.log('aiAnswer element:', aiAnswer);
      console.log('answerContent element:', answerContent);
      console.log('response.answer:', response.answer);

      if (aiAnswer && answerContent && response.answer) {
        answerContent.innerHTML = response.answer;
        aiAnswer.classList.remove('hidden');
        console.log('AI Answer displayed.');
      } else if (aiAnswer) {
        aiAnswer.classList.add('hidden');
        console.log('AI Answer hidden (no answer or elements not found).');
      }

      // Отображаем результаты поиска, если они есть
      const searchResults = document.getElementById('search-results');
      console.log('searchResults element:', searchResults);
      console.log('response.results:', response.results);

      if (searchResults && response.results && response.results.length > 0) {
        // Создаем HTML для карточек результатов
        const cards = await Promise.all(response.results.map(createResultCard));
        searchResults.innerHTML = cards.join('');
        console.log('Search results displayed.');
      } else if (searchResults) {
        searchResults.innerHTML = '<p class="text-center text-gray-500">No results found</p>';
        console.log('No search results found or displayed.');
      }
    } catch (e) {
      console.error('Error parsing search response or rendering:', e);
    }
  } else {
    console.log('Request path does not start with /api/search. Path:', event.detail.path);
  }
});