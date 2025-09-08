// backend/src/scripts/finalDemo.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function finalDemo() {
  console.log('=== ДЕМОНСТРАЦИЯ ПОИСКА В БАЗЕ ДОКУМЕНТОВ ===\n');
  
  // 1. Text search for "идея"
  console.log('1. Текстовый поиск слова "идея":');
  const { data: textResults, error: textError } = await supabase
    .from('documents')
    .select('id, date, sender, text, origin')
    .ilike('text', '%идея%');
  
  if (textError) {
    console.error('Ошибка текстового поиска:', textError);
  } else {
    console.log(`Найдено ${textResults.length} документов:`);
    textResults.forEach((doc, index) => {
      console.log(`  ${index + 1}. "${doc.text}" (от ${doc.sender})`);
    });
  }
  
  console.log('\n' + '='.repeat(50) + '\n');
  
  // 2. Semantic search using the first document with "идея"
  console.log('2. Семантический поиск похожих документов:');
  
  const { data: queryDoc, error: queryError } = await supabase
    .from('documents')
    .select('id, text, embedding')
    .ilike('text', '%идея%')
    .limit(1)
    .single();
  
  if (queryError) {
    console.error('Ошибка получения документа для семантического поиска:', queryError);
    return;
  }
  
  // Parse the embedding
  let queryEmbedding;
  if (typeof queryDoc.embedding === 'string') {
    queryEmbedding = JSON.parse(queryDoc.embedding);
  } else {
    queryEmbedding = queryDoc.embedding;
  }
  
  console.log(`Документ-запрос: "${queryDoc.text}"\n`);
  
  // Perform semantic search
  const { data: semanticResults, error: semanticError } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.75, // Only show quite similar documents
    match_count: 5
  });
  
  if (semanticError) {
    console.error('Ошибка семантического поиска:', semanticError);
  } else {
    console.log('Похожие документы (по убыванию сходства):');
    semanticResults.forEach((doc: any, index: number) => {
      if (doc.id !== queryDoc.id) { // Skip the query document itself
        console.log(`  ${index}. "${doc.text}" (сходство: ${(doc.similarity * 100).toFixed(1)}%, от ${doc.sender})`);
      }
    });
  }
  
  console.log('\n' + '='.repeat(50) + '\n');
  
  // 3. Database statistics
  console.log('3. Статистика базы данных:');
  
  const { count, error: countError } = await supabase
    .from('documents')
    .select('*', { count: 'exact', head: true });
  
  if (countError) {
    console.error('Ошибка получения статистики:', countError);
  } else {
    console.log(`Всего документов в базе: ${count}`);
  }
  
  console.log('\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===');
}

finalDemo();