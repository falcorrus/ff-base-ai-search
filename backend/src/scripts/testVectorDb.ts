// testVectorDb.ts
import { VectorDbService } from '../services/vectorDbService';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

// Create instance of the service
const vectorDbService = new VectorDbService();

async function testVectorDb() {
  try {
    console.log('Testing Vector DB service...');
    
    // Test finding similar documents
    // The database expects 1536-dimensional embeddings
    const testEmbedding = Array(1536).fill(0.1);
    console.log('Searching for similar documents...');
    
    const documents = await vectorDbService.findSimilarDocuments(testEmbedding, 5);
    console.log('Found documents:', documents.length);
    
    if (documents.length > 0) {
      console.log('First document ID:', documents[0].id);
    }
    
    console.log('Vector DB service is working correctly');
    
  } catch (err) {
    console.error('Error testing Vector DB service:', err);
  }
}

testVectorDb();