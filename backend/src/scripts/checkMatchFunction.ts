// backend/src/scripts/checkMatchFunction.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function checkMatchFunction() {
  // Get the document with "идея" in the text
  const { data: queryDoc, error: queryError } = await supabase
    .from('documents')
    .select('id, text, embedding')
    .ilike('text', '%идея%')
    .limit(1)
    .single();
  
  if (queryError) {
    console.error('Ошибка поиска документа с "идея":', queryError);
    return;
  }
  
  console.log(`Найден документ с ID: ${queryDoc.id}`);
  
  // Parse the embedding if it's a string
  let queryEmbedding;
  if (typeof queryDoc.embedding === 'string') {
    queryEmbedding = JSON.parse(queryDoc.embedding);
  } else {
    queryEmbedding = queryDoc.embedding;
  }
  
  console.log(`Размер вектора: ${queryEmbedding.length}`);
  
  // Try to use the match_documents function
  try {
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: queryEmbedding,
      match_threshold: 0.7,
      match_count: 5
    });
    
    if (error) {
      console.error('Ошибка при вызове match_documents:', error);
      console.log('Функция match_documents недоступна или не существует');
    } else {
      console.log('Результаты поиска через match_documents:');
      console.log(data);
    }
  } catch (err) {
    console.error('Ошибка при вызове match_documents:', err);
    console.log('Функция match_documents недоступна');
  }
  
  // Try to list available RPC functions
  try {
    // This is a workaround to see what RPC functions are available
    const { data, error } = await supabase.rpc('nonexistent_function');
    
    // We expect this to fail, but the error message might tell us what functions are available
    if (error) {
      console.log('Информация об ошибке может содержать подсказки о доступных функциях:');
      console.log(error.message);
    }
  } catch (err) {
    console.log('Ошибка при попытке получить список функций:', err);
  }
}

checkMatchFunction();