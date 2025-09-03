// testSupabase.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function testSupabase() {
  try {
    // Try to get table info using the Supabase client
    const { data, error } = await supabase
      .from('documents')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('Ошибка подключения к Supabase:', error);
    } else {
      console.log('Успешное подключение к Supabase');
      console.log('Данные:', data);
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

testSupabase();