// backend/src/scripts/checkVectorDimension.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkVectorDimension() {
  try {
    // Use raw SQL to check the vector dimension
    const { data, error } = await supabase.rpc('execute_sql', {
      sql: `
        SELECT 
          col.column_name,
          col.data_type,
          attr.atttypmod as vector_dimension
        FROM 
          information_schema.columns col
        LEFT JOIN 
          pg_attribute attr ON attr.attrelid = col.table_name::regclass AND attr.attname = col.column_name
        WHERE 
          col.table_name = 'documents' 
          AND col.column_name = 'embedding';
      `
    });
    
    if (error) {
      console.error('Ошибка выполнения запроса:', error);
      // Let's try a simpler approach
      const { data: simpleData, error: simpleError } = await supabase
        .from('documents')
        .select('embedding')
        .limit(1);
        
      if (simpleError) {
        console.error('Ошибка получения данных:', simpleError);
      } else if (simpleData && simpleData.length > 0) {
        console.log(`Размер вектора в возвращенных данных: ${simpleData[0].embedding.length}`);
        console.log(`Тип данных первого элемента: ${typeof simpleData[0].embedding[0]}`);
        console.log(`Первые 5 элементов: ${simpleData[0].embedding.slice(0, 5)}`);
      }
    } else {
      console.log('Результат запроса:', data);
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

checkVectorDimension();