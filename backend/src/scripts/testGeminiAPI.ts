// testGeminiAPI.ts
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

async function testGeminiAPI() {
  try {
    console.log('Testing Gemini API connection...');
    
    const apiKey = process.env.GEMINI_API_KEY;
    console.log('API Key exists:', !!apiKey);
    
    if (!apiKey) {
      console.error('GEMINI_API_KEY is not set');
      return;
    }
    
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: 'embedding-001' });
    
    // Simple test
    const result = await model.embedContent('test');
    console.log('Gemini API is working correctly');
    console.log('Embedding length:', result.embedding.values.length);
    
  } catch (error) {
    console.error('Gemini API test failed:', error);
  }
}

testGeminiAPI();