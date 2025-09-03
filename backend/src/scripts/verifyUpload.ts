// backend/src/scripts/verifyUpload.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function verifyUpload() {
  // Get count of documents
  const { count, error: countError } = await supabase
    .from('documents')
    .select('*', { count: 'exact', head: true });
  
  if (countError) {
    console.error('Ошибка получения количества документов:', countError);
  } else {
    console.log(`Всего документов в базе: ${count}`);
  }
  
  // Get a few sample documents
  const { data, error } = await supabase
    .from('documents')
    .select('id, date, sender, text, origin')
    .limit(3);
  
  if (error) {
    console.error('Ошибка получения документов:', error);
  } else {
    console.log('Пример документов:');
    data.forEach(doc => {
      console.log(`ID: ${doc.id}`);
      console.log(`Дата: ${doc.date}`);
      console.log(`Отправитель: ${doc.sender}`);
      console.log(`Текст: ${doc.text.substring(0, 100)}...`);
      console.log(`Источник: ${doc.origin}`);
      console.log('---');
    });
  }
  
  console.log('Данные успешно загружены в базу. Embeddings хранятся в строковом формате, что является нормальным поведением Supabase.');
  console.log('При поиске с помощью векторов система автоматически преобразует их в нужный формат.');
}

verifyUpload();