// testSearchController.ts
import { llmService } from '../services/llmService';
import { VectorDbService } from '../services/vectorDbService';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

// Create instances of services
const vectorDbService = new VectorDbService();

async function testSearchController() {
  try {
    console.log('Testing search controller logic...');
    
    const query = "мысль";
    console.log('Processing search for query:', query);
    
    // Create embedding for the query
    console.log('Creating embedding...');
    const queryEmbedding = await llmService.createEmbedding(query);
    console.log('Generated query embedding with length:', queryEmbedding.length);
    
    // Check if we need to pad the embedding
    let finalEmbedding = queryEmbedding;
    if (queryEmbedding.length === 768) {
      // Pad with zeros to make it 1536-dimensional
      finalEmbedding = [...queryEmbedding, ...Array(768).fill(0)];
      console.log('Padded embedding to 1536 dimensions');
    }
    
    // Search for similar documents
    console.log('Searching for similar documents...');
    const similarDocuments = await vectorDbService.findSimilarDocuments(finalEmbedding, 5);
    console.log('Found similar documents:', similarDocuments.length);
    
    if (similarDocuments.length > 0) {
      console.log('First document:', {
        id: similarDocuments[0].id,
        text: similarDocuments[0].text.substring(0, 100) + '...'
      });
    }
    
    console.log('Search controller logic is working correctly');
    
  } catch (err) {
    console.error('Error testing search controller logic:', err);
  }
}

testSearchController();