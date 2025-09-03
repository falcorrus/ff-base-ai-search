// src/routes/searchRoutes.ts
import { Router } from 'express';
import { searchController } from '../controllers/searchController';
import { vectorDbService } from '../services/vectorDbService';

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

const router = Router();

// Маршрут для поиска
router.get('/search', (req, res) => {
  console.log('Search route hit');
  return searchController.search(req, res);
});

// Маршрут для получения содержимого документа
router.get('/note/:id', searchController.getDocumentContent);

// Text search endpoint
router.get('/text-search', async (req, res) => {
  try {
    const { query } = req.query;
    
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'Query parameter is required' });
    }
    
    // Create a new Supabase client for direct access
    const { createClient } = await import('@supabase/supabase-js');
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL || '',
      process.env.SUPABASE_SERVICE_ROLE_KEY || ''
    );
    
    const { data, error } = await supabase
      .from('documents')
      .select('id, date, sender, text, origin')
      .ilike('text', `%${query}%`)
      .limit(20);
    
    if (error) {
      console.error('Text search error:', error);
      return res.status(500).json({ error: 'Text search failed' });
    }
    
    return res.json(data);
  } catch (err) {
    console.error('Unexpected error in text search:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Simple semantic search endpoint
router.get('/semantic-search', async (req, res) => {
  try {
    const { query } = req.query;
    
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'Query parameter is required' });
    }
    
    // Import the LLM service dynamically to avoid circular dependencies
    const { llmService } = await import('../services/llmService');
    
    // Create embedding for the query
    const queryEmbedding = await llmService.createEmbedding(query);
    
    // Convert embedding to 1536-dimensional if needed
    const convertedEmbedding = convertEmbedding(queryEmbedding);
    
    // Find similar documents
    const similarDocuments = await vectorDbService.findSimilarDocuments(convertedEmbedding, 10);
    
    return res.json(similarDocuments);
  } catch (err) {
    console.error('Unexpected error in semantic search:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;