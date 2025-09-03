// testLLM.ts
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../.env') });

async function testLLM() {
  try {
    console.log('Testing LLM service...');
    
    const apiKey = process.env.GEMINI_API_KEY;
    console.log('API Key exists:', !!apiKey);
    
    if (!apiKey) {
      console.error('GEMINI_API_KEY is not set');
      return;
    }
    
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: 'embedding-001' });
    
    // Test embedding creation
    const testText = "This is a test query";
    console.log('Creating embedding for:', testText);
    
    const result = await model.embedContent(testText);
    const embedding = result.embedding.values;
    console.log('Embedding length:', embedding.length);
    console.log('First 5 values:', embedding.slice(0, 5));
    
    console.log('LLM service is working correctly');
    
  } catch (err) {
    console.error('Error testing LLM service:', err);
  }
}

testLLM();