// backend/src/scripts/clearTable.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function clearTable() {
  const { error } = await supabase
    .from('documents')
    .delete()
    .neq('id', -1); // This will delete all rows (since no row has id = -1)
  
  if (error) {
    console.error('Ошибка очистки таблицы:', error);
  } else {
    console.log('Таблица documents успешно очищена');
  }
}

clearTable();