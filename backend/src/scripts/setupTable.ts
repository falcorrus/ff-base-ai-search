// backend/src/scripts/setupTable.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function setupTable() {
  try {
    // First, drop the existing table
    const { error: dropError } = await supabase.rpc('execute_sql', {
      sql: 'DROP TABLE IF EXISTS documents;'
    });
    
    if (dropError) {
      console.error('Ошибка удаления таблицы:', dropError);
      return;
    }
    
    console.log('Старая таблица удалена');
    
    // Enable vector extension if not already enabled
    const { error: extensionError } = await supabase.rpc('execute_sql', {
      sql: 'CREATE EXTENSION IF NOT EXISTS vector;'
    });
    
    if (extensionError) {
      console.error('Ошибка включения расширения vector:', extensionError);
      return;
    }
    
    console.log('Расширение vector включено');
    
    // Create the new table with proper vector column
    const { error: createError } = await supabase.rpc('execute_sql', {
      sql: `
        CREATE TABLE documents (
          id BIGINT PRIMARY KEY,
          date TEXT,
          sender TEXT,
          text TEXT,
          origin TEXT,
          embedding VECTOR(1536)
        );
      `
    });
    
    if (createError) {
      console.error('Ошибка создания таблицы:', createError);
      return;
    }
    
    console.log('Новая таблица documents успешно создана с правильным типом vector');
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

setupTable();