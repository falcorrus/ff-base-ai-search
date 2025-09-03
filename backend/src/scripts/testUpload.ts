// backend/src/scripts/testUpload.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function testUpload() {
  // Create a test document with 1536-dimensional embedding
  const testDocument = {
    id: 999999,
    date: "03.09.2025 10:00:00 UTC-03:00",
    sender: "Test User",
    text: "This is a test document",
    origin: "https://test.com",
    embedding: Array(1536).fill(0.1) // Create array with 1536 elements
  };
  
  const { error } = await supabase.from('documents').insert(testDocument);
  
  if (error) {
    console.error('Ошибка загрузки тестового документа:', error);
  } else {
    console.log('Тестовый документ успешно загружен');
    
    // Delete the test document
    const { error: deleteError } = await supabase
      .from('documents')
      .delete()
      .eq('id', 999999);
      
    if (deleteError) {
      console.error('Ошибка удаления тестового документа:', deleteError);
    } else {
      console.log('Тестовый документ успешно удален');
    }
  }
}

testUpload();