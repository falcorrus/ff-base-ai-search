// test-embedding-real.ts
import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from './src/config';

async function testEmbedding() {
  try {
    console.log('Testing embedding creation...');
    
    // Создаем клиент Google Generative AI
    const genAI = new GoogleGenerativeAI(config.GEMINI.API_KEY);
    const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });
    
    // Создаем тестовый запрос
    const query = 'Как использовать API?';
    
    // Создаем embedding
    const result = await embeddingModel.embedContent(query);
    const embedding = result.embedding.values;
    
    console.log('Embedding creation successful');
    console.log('Embedding length:', embedding.length);
    console.log('First 10 values:', embedding.slice(0, 10));
    
    // Проверим, что embedding не пустой
    if (embedding.length === 0) {
      console.log('Error: Embedding is empty');
      return;
    }
  } catch (err) {
    console.error('Embedding creation error:', err);
  }
}

testEmbedding();