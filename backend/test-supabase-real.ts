// test-supabase-real.ts
import { createClient } from '@supabase/supabase-js';
import { config } from './src/config';

async function testSupabase() {
  try {
    console.log('Testing Supabase connection...');
    
    // Создаем клиент Supabase
    const supabase = createClient(
      config.SUPABASE.URL,
      config.SUPABASE.SERVICE_ROLE_KEY
    );
    
    // Попробуем выполнить простой запрос
    const { data, error } = await supabase
      .from('documents')
      .select('id, text')
      .limit(1);
    
    if (error) {
      console.error('Supabase error:', error);
      return;
    }
    
    console.log('Supabase connection successful');
    console.log('Found documents:', data.length);
    console.log('First document:', data[0]);
  } catch (err) {
    console.error('Supabase connection error:', err);
  }
}

testSupabase();