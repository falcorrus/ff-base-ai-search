// backend/src/scripts/testSearch.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function testSearch() {
  // Create a query vector (768-dimensional, then convert to 1536)
  const queryVector = Array(768).fill(0.1);
  // Pad with zeros to make it 1536-dimensional
  const paddedQueryVector = [...queryVector, ...Array(768).fill(0)];
  
  console.log(`Размер вектора запроса: ${paddedQueryVector.length}`);
  
  try {
    // Perform a similarity search
    const { data, error } = await supabase.rpc('execute_sql', {
      sql: `
        SELECT id, text, (embedding <=> '${JSON.stringify(paddedQueryVector)}') as similarity
        FROM documents
        ORDER BY embedding <=> '${JSON.stringify(paddedQueryVector)}'
        LIMIT 5;
      `
    });
    
    if (error) {
      console.error('Ошибка поиска:', error);
      // Let's try a simpler approach using the match_documents function if it exists
      console.log('Попробуем использовать функцию match_documents...');
      
      const { data: matchData, error: matchError } = await supabase.rpc('match_documents', {
        query_embedding: paddedQueryVector,
        match_threshold: 0.5,
        match_count: 5
      });
      
      if (matchError) {
        console.error('Ошибка при использовании match_documents:', matchError);
      } else {
        console.log('Результаты поиска с использованием match_documents:');
        console.log(matchData);
      }
    } else {
      console.log('Результаты поиска:');
      console.log(data);
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

testSearch();