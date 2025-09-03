// backend/src/scripts/createTable.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function createTable() {
  try {
    // Enable vector extension
    const { error: extensionError } = await supabase.rpc('execute_sql', {
      sql: 'CREATE EXTENSION IF NOT EXISTS vector;'
    });
    
    if (extensionError) {
      console.error('Ошибка включения расширения vector:', extensionError);
    } else {
      console.log('Расширение vector включено');
    }
    
    // Create the documents table using raw SQL
    const { error } = await supabase.rpc('execute_sql', {
      sql: `
        CREATE TABLE IF NOT EXISTS documents (
          id BIGINT PRIMARY KEY,
          date TEXT,
          sender TEXT,
          text TEXT,
          origin TEXT,
          embedding VECTOR(1536)
        );
      `
    });
    
    if (error) {
      console.error('Ошибка создания таблицы:', error);
    } else {
      console.log('Таблица documents успешно создана');
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

createTable();