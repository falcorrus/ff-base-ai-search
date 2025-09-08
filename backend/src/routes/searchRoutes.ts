// src/routes/searchRoutes.ts
import { Router } from 'express';
import { SearchController } from '../controllers/searchController';
import { VectorDbService } from '../services/vectorDbService';

// Export a function that takes searchController as an argument
export default (searchController: SearchController) => {
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
  router.get('/semantic-search', (req, res) => {
    return searchController.semanticSearch(req, res);
  });

  return router;
};