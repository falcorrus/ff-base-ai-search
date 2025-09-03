// generate-chat-embeddings.js
const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

// Загружаем конфигурацию
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const config = {
  GEMINI: {
    API_KEY: process.env.GEMINI_API_KEY || '',
  },
  VECTOR_DB_PATH: './data/vector-db.json'
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

// Функция для обработки файла порционно
async function processVectorDbInChunks() {
  console.log('Начинаем генерацию эмбеддингов для чата Telegram...');
  
  try {
    // Читаем файл как поток
    const data = fs.readFileSync(config.VECTOR_DB_PATH, 'utf8');
    
    // Пытаемся спарсить JSON
    let documents = [];
    try {
      documents = JSON.parse(data);
      console.log(`Загружено ${documents.length} документов`);
    } catch (parseError) {
      console.error('Ошибка парсинга всего файла. Попробуем восстановить данные...');
      
      // Если файл поврежден, попробуем извлечь часть данных
      const partialData = data.substring(0, 1000000); // Берем первый 1MB
      try {
        // Попробуем найти завершенные записи
        const arrayStart = partialData.indexOf('[');
        const lastObjectEnd = partialData.lastIndexOf('}');
        if (arrayStart !== -1 && lastObjectEnd !== -1) {
          const trimmedData = partialData.substring(0, lastObjectEnd + 1) + ']';
          documents = JSON.parse(trimmedData);
          console.log(`Восстановлено ${documents.length} документов из поврежденного файла`);
        }
      } catch (recoveryError) {
        console.error('Не удалось восстановить данные:', recoveryError.message);
        process.exit(1);
      }
    }
    
    // Обрабатываем документы порциями
    const batchSize = 10; // Размер порции
    let processedCount = 0;
    
    for (let i = 0; i < documents.length; i += batchSize) {
      const batch = documents.slice(i, i + batchSize);
      console.log(`\nОбрабатываем порцию ${Math.floor(i/batchSize) + 1}/${Math.ceil(documents.length/batchSize)}`);
      
      // Обрабатываем каждый документ в порции
      for (const doc of batch) {
        // Пропускаем документы, у которых уже есть эмбеддинги
        if (doc.embedding && doc.embedding.length > 0) {
          continue;
        }
        
        try {
          console.log(`  Создаем эмбеддинг для документа ID: ${doc.id}`);
          const embedding = await createEmbedding(doc.content);
          doc.embedding = embedding;
          processedCount++;
        } catch (error) {
          console.error(`  Ошибка обработки документа ID ${doc.id}:`, error.message);
        }
      }
      
      // Сохраняем промежуточные результаты
      fs.writeFileSync(config.VECTOR_DB_PATH + '.backup', JSON.stringify(documents, null, 2));
      console.log(`  Промежуточные результаты сохранены (${processedCount} документов обработано)`);
    }
    
    // Сохраняем финальные результаты
    fs.writeFileSync(config.VECTOR_DB_PATH, JSON.stringify(documents, null, 2));
    console.log(`\nГенерация эмбеддингов завершена!`);
    console.log(`Обработано документов: ${processedCount}`);
    console.log(`Всего документов в базе: ${documents.length}`);
    
  } catch (error) {
    console.error('Ошибка обработки векторной базы данных:', error.message);
  }
}

// Запускаем обработку
processVectorDbInChunks();