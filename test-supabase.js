const { createClient } = require('@supabase/supabase-js');

// Конфигурация Supabase из вашего .env файла
const supabaseUrl = 'https://olarimkwaftkourjzrfn.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sYXJpbWt3YWZ0a291cmp6cmZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Njk0MDgwNCwiZXhwIjoyMDcyNTE2ODA0fQ.oas6_sSCh0eqCiC7oIKDy2u41vclGJSgpqXfYrI2TGs';

// Создание клиента Supabase
const supabase = createClient(supabaseUrl, supabaseKey);

// Тестирование подключения
async function testConnection() {
  try {
    // Попытка получить данные из таблицы documents
    const { data, error } = await supabase
      .from('documents')
      .select('id, text')
      .limit(5);

    if (error) {
      console.error('Ошибка при подключении к Supabase:', error);
      return;
    }

    console.log('Успешное подключение к Supabase');
    console.log('Найдено записей:', data.length);
    console.log('Пример данных:', data);
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

testConnection();