// backend/src/routes/search.ts
import { Router } from 'express';
import { searchController } from '../controllers/searchController';

const router = Router();

// Text search endpoint
router.get('/text', async (req, res) => {
  try {
    const { query } = req.query;
    
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'Query parameter is required' });
    }
    
    // For text search, we'll use Supabase directly
    const { createClient } = await import('@supabase/supabase-js');
    const { config } = await import('../config');
    
    const supabase = createClient(
      config.SUPABASE.URL,
      config.SUPABASE.SERVICE_ROLE_KEY
    );
    
    try {
      const { data, error } = await supabase
        .from('documents')
        .select('id, date, sender, text, origin')
        .ilike('text', `%${query}%`)
        .limit(20);
      
      if (error) {
        console.error('Search error:', error);
        return res.status(500).json({ error: 'Search failed' });
      }
      
      return res.json(data);
    } catch (dbError) {
      console.error('Database error:', dbError);
      return res.status(500).json({ error: 'Database error' });
    }
  } catch (err) {
    console.error('Unexpected error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
});

// Semantic search endpoint (using the existing search controller)
router.get('/semantic', searchController.search);

export default router;