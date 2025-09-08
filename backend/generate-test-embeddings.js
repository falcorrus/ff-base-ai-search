// generate-test-embeddings.js
const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Загружаем конфигурацию
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const config = {
  GEMINI: {
    API_KEY: process.env.GEMINI_API_KEY || '',
  },
  VECTOR_DB_PATH: './data/test-vector-db.json'
};

// Проверяем наличие API ключа
if (!config.GEMINI.API_KEY) {
  console.error('Не найден API ключ для Gemini. Проверьте файл .env');
  process.exit(1);
}

// Инициализируем Google Generative AI
const genAI = new GoogleGenerativeAI(config.GEMINI.API_KEY);
const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });

// Функция для создания эмбеддинга
async function createEmbedding(text) {
  try {
    const result = await embeddingModel.embedContent(text);
    return result.embedding.values;
  } catch (error) {
    console.error('Ошибка создания эмбеддинга:', error.message);
    return [];
  }
}

// Основная функция генерации эмбеддингов
async function generateEmbeddings() {
  console.log('Начинаем генерацию эмбеддингов для тестовой базы данных...');
  
  try {
    // Загружаем данные из файла
    const data = fs.readFileSync(config.VECTOR_DB_PATH, 'utf8');
    const documents = JSON.parse(data);
    console.log(`Загружено ${documents.length} документов`);
    
    // Обрабатываем каждый документ
    let processedCount = 0;
    for (const doc of documents) {
      try {
        console.log(`Создаем эмбеддинг для документа ID: ${doc.id}`);
        const embedding = await createEmbedding(doc.content);
        doc.embedding = embedding;
        processedCount++;
        console.log(`  Эмбеддинг создан, размер: ${embedding.length}`);
      } catch (error) {
        console.error(`Ошибка обработки документа ID ${doc.id}:`, error.message);
      }
    }
    
    // Сохраняем результаты
    fs.writeFileSync(config.VECTOR_DB_PATH, JSON.stringify(documents, null, 2));
    console.log(`\nГенерация эмбеддингов завершена!`);
    console.log(`Обработано документов: ${processedCount}`);
    console.log(`Всего документов в базе: ${documents.length}`);
    
  } catch (error) {
    console.error('Ошибка обработки векторной базы данных:', error.message);
  }
}

// Запускаем генерацию
generateEmbeddings();