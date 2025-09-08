// test-rpc-real.ts
import { createClient } from '@supabase/supabase-js';
import { config } from './src/config';

async function testRpc() {
  try {
    console.log('Testing RPC function...');
    
    // Создаем клиент Supabase
    const supabase = createClient(
      config.SUPABASE.URL,
      config.SUPABASE.SERVICE_ROLE_KEY
    );
    
    // Создаем тестовый embedding (1536 нулей)
    const testEmbedding = new Array(1536).fill(0);
    
    // Вызываем RPC функцию
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: testEmbedding,
      match_threshold: 0.7,
      match_count: 5,
    });
    
    if (error) {
      console.error('RPC error:', error);
      return;
    }
    
    console.log('RPC function successful');
    console.log('Found matches:', data.length);
    console.log('First match:', data[0]);
  } catch (err) {
    console.error('RPC error:', err);
  }
}

testRpc();