// backend/src/scripts/searchMyshi.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function searchMyshi() {
  const searchText = "мысли";
  
  console.log(`Поиск документов, содержащих слово: "${searchText}"`);
  
  // Search for documents containing the text
  const { data, error } = await supabase
    .from('documents')
    .select('id, date, sender, text, origin')
    .ilike('text', `%${searchText}%`);
  
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
    
    // If we found documents, let's also do a semantic search using the first one
    if (data.length > 0) {
      console.log('\n' + '='.repeat(50));
      console.log('Семантический поиск похожих документов:');
      
      // Get the embedding for the first document
      const { data: queryDoc, error: queryError } = await supabase
        .from('documents')
        .select('id, text, embedding')
        .eq('id', data[0].id)
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
        match_threshold: 0.7,
        match_count: 5
      });
      
      if (semanticError) {
        console.error('Ошибка семантического поиска:', semanticError);
      } else {
        console.log('Похожие документы (по убыванию сходства):');
        semanticResults.forEach((doc: any, index: number) => {
          if (doc.id !== queryDoc.id) { // Skip the query document itself
            console.log(`  ${index}. "${doc.text.substring(0, 100)}${doc.text.length > 100 ? '...' : ''}" (сходство: ${(doc.similarity * 100).toFixed(1)}%, от ${doc.sender})`);
          }
        });
      }
    }
  } else {
    console.log('Документы не найдены');
  }
}

searchMyshi();