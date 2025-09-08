// testLLM.ts
import { llmService } from '../services/llmService';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

async function testLLM() {
  try {
    console.log('Testing LLM service...');
    
    // Test embedding creation
    const testText = "This is a test query";
    console.log('Creating embedding for:', testText);
    
    const embedding = await llmService.createEmbedding(testText);
    console.log('Embedding length:', embedding.length);
    console.log('First 5 values:', embedding.slice(0, 5));
    
    // Test answer generation
    console.log('Testing answer generation...');
    const answer = await llmService.generateAnswer("What is this?", []);
    console.log('Generated answer:', answer);
    
  } catch (err) {
    console.error('Error testing LLM service:', err);
  }
}

testLLM();