// test-llm-real.ts
import { llmService } from './src/services/llmService';
import { Document } from './src/models/Document';

async function testLLM() {
  try {
    console.log('Testing LLM service...');
    
    // Создадим тестовый запрос
    const query = 'Как использовать API?';
    
    // Создадим embedding
    const embedding = await llmService.createEmbedding(query);
    
    console.log('Embedding length:', embedding.length);
    console.log('First 10 values:', embedding.slice(0, 10));
    
    // Проверим, что embedding не пустой
    if (embedding.length === 0) {
      console.log('Error: Embedding is empty');
      return;
    }
    
    // Создадим тестовые документы
    const testDocuments: Document[] = [
      {
        id: 1,
        date: '2025-01-01',
        sender: 'Test',
        text: 'Это тестовый документ о том, как использовать API',
        origin: 'test',
        embedding: new Array(1536).fill(0)
      }
    ];
    
    // Попробуем сгенерировать ответ
    const answer = await llmService.generateAnswer(query, testDocuments);
    
    console.log('Generated answer:', answer);
  } catch (err) {
    console.error('LLM Error:', err);
  }
}

testLLM();