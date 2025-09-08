// backend/src/scripts/testSingleUpload.ts
import { createClient } from '@supabase/supabase-js';
import * as fs from 'fs';
import * as path from 'path';

const supabaseUrl = process.env.SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

// Read the JSON file synchronously
const basePath = path.resolve(__dirname, '../../../base.json');
const rawData = fs.readFileSync(basePath, 'utf-8');
const data = JSON.parse(rawData);

// Function to convert 768-dimensional embedding to 1536-dimensional embedding
function convertEmbedding(embedding: number[]): number[] {
  // If already 1536-dimensional, return as is
  if (embedding.length === 1536) {
    return embedding;
  }
  
  // If 768-dimensional, pad with zeros to make it 1536-dimensional
  if (embedding.length === 768) {
    return [...embedding, ...Array(768).fill(0)];
  }
  
  // For any other size, pad or truncate to 1536
  const result = new Array(1536).fill(0);
  const copyLength = Math.min(embedding.length, 1536);
  for (let i = 0; i < copyLength; i++) {
    result[i] = embedding[i];
  }
  return result;
}

async function testSingleUpload() {
  // Take the first document
  const firstDoc = data[0];
  const docWithConvertedEmbedding = {
    ...firstDoc,
    embedding: convertEmbedding(firstDoc.embedding)
  };
  
  console.log(`Converted embedding length: ${docWithConvertedEmbedding.embedding.length}`);
  
  // Insert just this one document
  const { error } = await supabase.from('documents').insert(docWithConvertedEmbedding);
  
  if (error) {
    console.error('Ошибка загрузки документа:', error);
  } else {
    console.log('Документ успешно загружен');
    
    // Now retrieve it to check the embedding size
    const { data: retrievedData, error: retrieveError } = await supabase
      .from('documents')
      .select('embedding')
      .eq('id', firstDoc.id)
      .single();
      
    if (retrieveError) {
      console.error('Ошибка получения документа:', retrieveError);
    } else {
      console.log(`Retrieved embedding length: ${retrievedData.embedding.length}`);
    }
    
    // Delete the document
    const { error: deleteError } = await supabase
      .from('documents')
      .delete()
      .eq('id', firstDoc.id);
      
    if (deleteError) {
      console.error('Ошибка удаления документа:', deleteError);
    } else {
      console.log('Документ успешно удален');
    }
  }
}

testSingleUpload();