// backend/src/scripts/searchByText.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function searchByText() {
  const searchText = "идея";
  
  console.log(`Поиск документов, содержащих слово: "${searchText}"`);
  
  // Search for documents containing the text
  const { data, error } = await supabase
    .from('documents')
    .select('id, date, sender, text, origin')
    .ilike('text', `%${searchText}%`)
    .limit(5);
  
  if (error) {
    console.error('Ошибка поиска:', error);
    return;
  }
  
  console.log(`Найдено ${data.length} документов:`);
  
  if (data.length > 0) {
    data.forEach((doc, index) => {
      console.log(`\n${index + 1}. ID: ${doc.id}`);
      console.log(`   Дата: ${doc.date}`);
      console.log(`   Отправитель: ${doc.sender}`);
      console.log(`   Текст: ${doc.text.substring(0, 200)}${doc.text.length > 200 ? '...' : ''}`);
      console.log(`   Источник: ${doc.origin}`);
    });
  } else {
    console.log('Документы не найдены');
  }
}

searchByText();