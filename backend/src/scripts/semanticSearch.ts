// backend/src/scripts/semanticSearch.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function semanticSearch() {
  console.log('Поиск документа с текстом, содержащим слово "идея"...');
  
  // First, find a document containing "идея"
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
  console.log(`Текст: ${queryDoc.text}`);
  console.log(`Размер вектора: ${typeof queryDoc.embedding === 'string' ? queryDoc.embedding.length : queryDoc.embedding.length}`);
  
  // Parse the embedding if it's a string
  let queryEmbedding;
  if (typeof queryDoc.embedding === 'string') {
    // Remove brackets and split by comma
    queryEmbedding = JSON.parse(queryDoc.embedding);
  } else {
    queryEmbedding = queryDoc.embedding;
  }
  
  console.log(`Размер разобранного вектора: ${queryEmbedding.length}`);
  
  try {
    // Perform semantic search using cosine similarity
    // Note: This is a simplified approach. In practice, you might want to create a dedicated RPC function in Supabase
    const { data: similarDocs, error: searchError } = await supabase.rpc('execute_sql', {
      sql: `
        SELECT id, text, origin,
               (embedding <=> '${JSON.stringify(queryEmbedding)}') as similarity
        FROM documents
        WHERE id != ${queryDoc.id}
        ORDER BY embedding <=> '${JSON.stringify(queryEmbedding)}'
        LIMIT 3;
      `
    });
    
    if (searchError) {
      console.error('Ошибка семантического поиска:', searchError);
      console.log('Попробуем альтернативный подход...');
      
      // Alternative approach: Get a few documents and calculate similarity manually would be complex
      // Let's just get a few random documents for comparison
      const { data: randomDocs, error: randomError } = await supabase
        .from('documents')
        .select('id, date, sender, text, origin')
        .neq('id', queryDoc.id)
        .limit(3);
      
      if (randomError) {
        console.error('Ошибка получения случайных документов:', randomError);
      } else {
        console.log('\nДля сравнения, несколько случайных документов из базы:');
        randomDocs.forEach((doc, index) => {
          console.log(`\n${index + 1}. ID: ${doc.id}`);
          console.log(`   Дата: ${doc.date}`);
          console.log(`   Отправитель: ${doc.sender}`);
          console.log(`   Текст: ${doc.text.substring(0, 150)}${doc.text.length > 150 ? '...' : ''}`);
          console.log(`   Источник: ${doc.origin}`);
        });
      }
    } else {
      console.log('\nРезультаты семантического поиска (похожие документы):');
      similarDocs.forEach((doc: any, index: number) => {
        console.log(`\n${index + 1}. ID: ${doc.id}`);
        console.log(`   Сходство: ${doc.similarity}`);
        console.log(`   Текст: ${doc.text.substring(0, 150)}${doc.text.length > 150 ? '...' : ''}`);
        console.log(`   Источник: ${doc.origin}`);
      });
    }
  } catch (err) {
    console.error('Неожиданная ошибка:', err);
  }
}

semanticSearch();