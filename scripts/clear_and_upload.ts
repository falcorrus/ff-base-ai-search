// scripts/clear_and_upload.ts
import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';

// Read the JSON file synchronously
const rawData = fs.readFileSync('../knowledge_base.json', 'utf-8');
const data = JSON.parse(rawData);

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function clearAndUpload() {
  // Очистка таблицы documents
  const { error: deleteError } = await supabase
    .from('documents')
    .delete()
    .neq('id', -1); // Условие, которое всегда истинно, чтобы удалить все записи

  if (deleteError) {
    console.error('Ошибка очистки таблицы:', deleteError);
    return;
  }

  console.log('Таблица documents очищена.');

  // Загрузка новых данных
  const batchSize = 1000;
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);
    // Преобразуем поля, если необходимо (например, 'text' в 'content')
    const transformedBatch = batch.map((item: any) => ({
      id: item.id,
      date: item.date,
      sender: item.sender,
      content: item.text || item.content, // Поддержка обоих полей
      origin: item.origin,
      embedding: item.embedding
    }));

    const { error: insertError } = await supabase
      .from('documents')
      .insert(transformedBatch);

    if (insertError) {
      console.error('Ошибка загрузки:', insertError);
    } else {
      console.log(`Загружено ${Math.min(i + batchSize, data.length)} из ${data.length}`);
    }
  }
}

clearAndUpload();