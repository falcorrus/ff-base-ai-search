const { createClient } = require('@supabase/supabase-js');

// Конфигурация Supabase из вашего .env файла
const supabaseUrl = 'https://olarimkwaftkourjzrfn.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYXJpbWt3YWZ0a291cmp6cmZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njk0MDgwNCwiZXhwIjoyMDcyNTE2ODA0fQ.oas6_sSCh0eqCiC7oIKDy2u41vclGJSgpqXfYrI2TGs';

// Создание клиента Supabase
const supabase = createClient(supabaseUrl, supabaseKey);

// Тестирование RPC функции match_documents
async function testRpc() {
  try {
    // Создаем простой embedding для теста (1536 нулей)
    const testEmbedding = new Array(1536).fill(0);
    
    // Вызов RPC функции
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: testEmbedding,
      match_threshold: 0.7,
      match_count: 5,
    });

    if (error) {
      console.error('Ошибка при вызове RPC функции:', error);
      return;
    }

    console.log('Успешный вызов RPC функции match_documents');
    console.log('Найдено совпадений:', data.length);
    console.log('Пример данных:', data);
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

testRpc();