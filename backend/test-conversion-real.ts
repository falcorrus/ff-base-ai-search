// test-conversion-real.ts
import { GoogleGenerativeAI } from '@google/generative-ai';
import { config } from './src/config';

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

async function testConversion() {
  try {
    console.log('Testing embedding conversion...');
    
    // Создаем клиент Google Generative AI
    const genAI = new GoogleGenerativeAI(config.GEMINI.API_KEY);
    const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });
    
    // Создаем тестовый запрос
    const query = 'Как использовать API?';
    
    // Создаем embedding
    const result = await embeddingModel.embedContent(query);
    const embedding = result.embedding.values;
    
    console.log('Original embedding length:', embedding.length);
    
    // Конвертируем embedding
    const convertedEmbedding = convertEmbedding(embedding);
    
    console.log('Converted embedding length:', convertedEmbedding.length);
    console.log('First 10 values:', convertedEmbedding.slice(0, 10));
    console.log('Last 10 values:', convertedEmbedding.slice(-10));
  } catch (err) {
    console.error('Embedding conversion error:', err);
  }
}

testConversion();