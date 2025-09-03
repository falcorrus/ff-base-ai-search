// backend/src/scripts/checkFunctions.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkFunctions() {
  try {
    // Try to get information about available RPC functions
    const { data, error } = await supabase.rpc('execute_sql', {
      sql: `
        SELECT proname, proargnames, proargtypes
        FROM pg_proc
        WHERE proname LIKE '%match%'
        LIMIT 10;
      `
    });
    
    if (error) {
      console.error('Ошибка получения списка функций:', error);
    } else {
      console.log('Найденные функции с "match" в названии:');
      console.log(data);
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

checkFunctions();