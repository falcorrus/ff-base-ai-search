// test-llm.ts
import { llmService } from './src/services/llmService';
import { createClient } from '@supabase/supabase-js';

// Function to convert 768-dimensional embedding to 1536-dimensional embedding
function convertEmbedding(embedding: number[]): number[] {
  // If already 1536-dimensional, return as is
  if (embedding.length === 1536) {
    return embedding;
  }
  
  // If 768-dimensional, pad with zeros to make it 1536-dimensional
  if (embedding.length === 768) {
    return [...embedding, ...Array(768).fill(0)];
  }
  
  // For any other size, pad or truncate to 1536
  const result = new Array(1536).fill(0);
  const copyLength = Math.min(embedding.length, 1536);
  for (let i = 0; i < copyLength; i++) {
    result[i] = embedding[i];
  }
  return result;
}

async function testLlmService() {
  try {
    console.log('Начало тестирования LLM сервиса');
    
    // Тестовая строка
    const testQuery = 'Как использовать API?';
    console.log('Тестовый запрос:', testQuery);
    
    // Создание embedding'а
    const embedding = await llmService.createEmbedding(testQuery);
    
    console.log('Успешное создание embedding\'а');
    console.log('Длина embedding\'а:', embedding.length);
    console.log('Пример значений:', embedding.slice(0, 10));
    
    // Проверяем, что embedding не пустой
    if (embedding.length === 0) {
      console.log('Ошибка: embedding пустой');
      return;
    }
    
    // Конвертируем embedding в нужную размерность
    const convertedEmbedding = convertEmbedding(embedding);
    console.log('Конвертированный embedding, длина:', convertedEmbedding.length);
    
    // Конфигурация Supabase из вашего .env файла
    const supabaseUrl = 'https://olarimkwaftkourjzrfn.supabase.co';
    const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYXJpbWt3YWZ0a291cmp6cmZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njk0MDgwNCwiZXhwIjoyMDcyNTE2ODA0fQ.oas6_sSCh0eqCiC7oIKDy2u41vclGJSgpqXfYrI2TGs';
    
    // Создание клиента Supabase
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Вызов RPC функции
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: convertedEmbedding,
      match_threshold: 0.7,
      match_count: 5,
    });
    
    if (error) {
      console.error('Ошибка при вызове RPC функции:', error);
      return;
    }
    
    console.log('Успешный вызов RPC функции с реальным embedding\'ом');
    console.log('Найдено совпадений:', data.length);
    if (data.length > 0) {
      console.log('Пример данных:', data[0]);
    }
  } catch (err) {
    console.error('Ошибка при тестировании LLM сервиса:', err);
  }
}

testLlmService().then(() => {
  console.log('Тестирование завершено');
});