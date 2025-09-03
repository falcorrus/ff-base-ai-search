// test-vector-db.ts
import { vectorDbService } from './src/services/vectorDbService';

async function testVectorDb() {
  try {
    console.log('Testing vector DB service...');
    
    // Создадим тестовый embedding (1536 нулей)
    const testEmbedding = new Array(1536).fill(0);
    
    // Попробуем найти похожие документы
    const results = await vectorDbService.findSimilarDocuments(testEmbedding, 5);
    
    console.log('Found documents:', results.length);
    console.log('First result:', results[0]);
  } catch (err) {
    console.error('Vector DB Error:', err);
  }
}

testVectorDb();