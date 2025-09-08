// Тестирование сервиса LLM
async function testLlmService() {
  try {
    // Динамический импорт сервиса LLM
    const { llmService } = await import('./src/services/llmService');
    
    // Тестовая строка
    const testQuery = 'Как использовать API?';
    
    // Создание embedding'а
    const embedding = await llmService.createEmbedding(testQuery);
    
    console.log('Успешное создание embedding\'а');
    console.log('Длина embedding\'а:', embedding.length);
    console.log('Пример значений:', embedding.slice(0, 10));
    
    // Проверка RPC функции с реальным embedding'ом
    const { createClient } = await import('@supabase/supabase-js');
    
    // Конфигурация Supabase из вашего .env файла
    const supabaseUrl = 'https://olarimkwaftkourjzrfn.supabase.co';
    const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYXJpbWt3YWZ0a291cmp6cmZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njk0MDgwNCwiZXhwIjoyMDcyNTE2ODA0fQ.oas6_sSCh0eqCiC7oIKDy2u41vclGJSgpqXfYrI2TGs';
    
    // Создание клиента Supabase
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Вызов RPC функции
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: embedding,
      match_threshold: 0.7,
      match_count: 5,
    });
    
    if (error) {
      console.error('Ошибка при вызове RPC функции:', error);
      return;
    }
    
    console.log('Успешный вызов RPC функции с реальным embedding\'ом');
    console.log('Найдено совпадений:', data.length);
  } catch (err) {
    console.error('Ошибка при тестировании LLM сервиса:', err);
  }
}

testLlmService();