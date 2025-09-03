// testSearchFunctionality.ts
import { GoogleGenerativeAI } from '@google/generative-ai';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

// Initialize services
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
const supabase = createClient(supabaseUrl, supabaseKey);
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

async function testSearchFunctionality() {
  try {
    console.log('Testing search functionality...');
    
    // Test 1: Check if LLM service is working
    console.log('Testing LLM service...');
    const testQuery = 'мысль';
    const model = genAI.getGenerativeModel({ model: 'embedding-001' });
    const result = await model.embedContent(testQuery);
    const embedding = result.embedding.values;
    console.log('Embedding generated successfully, length:', embedding.length);
    
    // Test 2: Check if vector database service is working
    console.log('Testing vector database service...');
    // Convert 768-dimensional embedding to 1536-dimensional if needed
    let queryEmbedding = embedding;
    if (embedding.length === 768) {
      queryEmbedding = [...embedding, ...Array(768).fill(0)];
    }
    
    const { data, error } = await supabase.rpc('match_documents', {
      query_embedding: queryEmbedding,
      match_threshold: 0.7,
      match_count: 5
    });
    
    if (error) {
      console.error('Database error:', error);
      return;
    }
    
    console.log('Found', data.length, 'similar documents');
    
    if (data.length > 0) {
      console.log('First result:', {
        id: data[0].id,
        text: data[0].text?.substring(0, 100) + '...'
      });
    }
    
    console.log('All tests passed!');
  } catch (error) {
    console.error('Test failed:', error);
  }
}

testSearchFunctionality();