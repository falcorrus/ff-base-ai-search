// src/controllers/searchController.ts
import { Request, Response } from 'express';
import { VectorDbService } from '../services/vectorDbService';
import { llmService } from '../services/llmService';
import { Document } from '../models/Document';

export class SearchController {
  private vectorDbService: VectorDbService;

  constructor(vectorDbService: VectorDbService) {
    this.vectorDbService = vectorDbService;
  }

  // Function to convert 768-dimensional embedding to 1536-dimensional embedding
  private convertEmbedding(embedding: number[]): number[] {
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

  // Обработчик поискового запроса
  async search(req: Request, res: Response) {
    try {
      console.log('Received search request with query params:', req.query);
      const { q: query } = req.query;
      console.log('Extracted query:', query);
      
      // Проверяем, что запрос не пустой
      if (!query || typeof query !== 'string') {
        console.log('Query parameter is missing or invalid');
        return res.status(400).json({ error: 'Query parameter is required' });
      }
      
      console.log('Processing search for query:', query);
      
      // Создаем векторное представление для запроса
      const queryEmbedding = await llmService.createEmbedding(query);
      console.log('Generated query embedding with length:', queryEmbedding.length);
      
      // Convert embedding to 1536-dimensional if needed
      const convertedEmbedding = this.convertEmbedding(queryEmbedding);
      console.log('Converted query embedding to length:', convertedEmbedding.length);
      
      // Ищем похожие документы
      const similarDocuments = await this.vectorDbService.findSimilarDocuments(convertedEmbedding, 5);
      console.log('Found similar documents:', similarDocuments.length);
      console.log('Similar documents:', similarDocuments);
      
      // Генерируем ответ с помощью LLM
      const answer = await llmService.generateAnswer(query, similarDocuments);
      console.log('Generated answer:', answer.substring(0, 100) + '...');
      
      // Возвращаем результат
      return res.json({
        answer,
        results: similarDocuments.map((doc: Document) => ({
          id: doc.id,
          title: doc.id.toString(), // Using ID as title for now
          path: doc.origin || '',
          excerpt: doc.text.substring(0, 200) + '...',
          githubUrl: doc.origin || '#' // Use origin directly as it's a URL
        }))
      });
    } catch (error) {
      console.error('Search error:', error);
      return res.status(500).json({ error: 'Internal server error' });
    }
  }
  
  // Получить содержимое документа
  async getDocumentContent(req: Request, res: Response) {
    try {
      const { id } = req.params;
      
      if (!id) {
        return res.status(400).json({ error: 'Document ID is required' });
      }
      
      const document = await this.vectorDbService.getDocumentById(id);
      
      if (!document) {
        return res.status(404).json({ error: 'Document not found' });
      }
      
      return res.json({
        title: document.id.toString(), // Using ID as title for now
        content: document.text,
        path: document.origin || '',
        githubUrl: document.origin || '#' // Use origin directly as it's a URL
      });
    } catch (error) {
      console.error('Error fetching document content:', error);
      return res.status(500).json({ error: 'Internal server error' });
    }
  }

  // Обработчик семантического поиска
  async semanticSearch(req: Request, res: Response) {
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
      const convertedEmbedding = this.convertEmbedding(queryEmbedding);
      
      // Find similar documents
      const similarDocuments = await this.vectorDbService.findSimilarDocuments(convertedEmbedding, 10);
      
      return res.json(similarDocuments);
    } catch (err) {
      console.error('Unexpected error in semantic search:', err);
      return res.status(500).json({ error: 'Internal server error' });
    }
  }
}