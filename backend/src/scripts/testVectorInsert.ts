// backend/src/scripts/testVectorInsert.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function testVectorInsert() {
  // Create a simple test document with a small vector
  const testDocument = {
    id: 999999,
    date: "03.09.2025 10:00:00 UTC-03:00",
    sender: "Test User",
    text: "This is a test document",
    origin: "https://test.com",
    embedding: Array(1536).fill(0.1) // Create array with 1536 elements
  };
  
  // First, clear any existing test document
  await supabase.from('documents').delete().eq('id', 999999);
  
  // Insert the test document
  const { error } = await supabase.from('documents').insert(testDocument);
  
  if (error) {
    console.error('Ошибка вставки тестового документа:', error);
    return;
  }
  
  console.log('Тестовый документ успешно вставлен');
  
  // Retrieve the document to check the embedding
  const { data, error: fetchError } = await supabase
    .from('documents')
    .select('embedding')
    .eq('id', 999999)
    .single();
  
  if (fetchError) {
    console.error('Ошибка получения тестового документа:', fetchError);
    return;
  }
  
  console.log(`Тип данных embedding: ${typeof data.embedding}`);
  console.log(`Длина embedding: ${data.embedding.length}`);
  
  if (Array.isArray(data.embedding)) {
    console.log(`Первые 5 элементов: ${data.embedding.slice(0, 5)}`);
  } else {
    console.log(`Содержимое embedding (первые 100 символов): ${data.embedding.substring(0, 100)}`);
  }
  
  // Clean up
  await supabase.from('documents').delete().eq('id', 999999);
  console.log('Тестовый документ удален');
}

testVectorInsert();