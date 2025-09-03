// backend/src/scripts/checkTable.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkTable() {
  // Query to get table column information using raw SQL
  const { data, error } = await supabase.rpc('execute_sql', {
    sql: `
      SELECT column_name, data_type, is_nullable, column_default
      FROM information_schema.columns
      WHERE table_name = 'documents'
      ORDER BY ordinal_position;
    `
  });
  
  if (error) {
    console.error('Ошибка получения схемы:', error);
  } else {
    console.log('Схема таблицы documents:');
    console.log(data);
  }
  
  // Check vector dimension
  const { data: vectorData, error: vectorError } = await supabase.rpc('execute_sql', {
    sql: `
      SELECT atttypmod as dimensions
      FROM pg_attribute
      WHERE attrelid = 'documents'::regclass
      AND attname = 'embedding';
    `
  });
  
  if (vectorError) {
    console.error('Ошибка получения информации о векторе:', vectorError);
  } else {
    console.log('Информация о векторе:');
    console.log(vectorData);
  }
}

checkTable();