// src/services/vectorDbService.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { Document } from '../models/Document';
import { config } from '../config';

export class VectorDbService {
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(
      config.SUPABASE.URL,
      config.SUPABASE.SERVICE_ROLE_KEY,
      { auth: { persistSession: false } } // Use service role key, do not persist session
    );
  }

  // Найти похожие документы в Supabase
  async findSimilarDocuments(queryEmbedding: number[], limit: number = 5): Promise<Document[]> {
    try {
      const { data, error } = await this.supabase.rpc('match_documents', {
        query_embedding: queryEmbedding,
        match_threshold: 0.7, // Adjust as needed
        match_count: limit,
      });

      if (error) {
        console.error('Error calling match_documents RPC:', error);
        return [];
      }

      // Map the RPC response to Document interface
      return data.map((item: any) => ({
        id: item.id,
        date: item.date,
        sender: item.sender,
        text: item.text,
        origin: item.origin,
        embedding: item.embedding, // Assuming embedding is returned by RPC
      }));

    } catch (error) {
      console.error('Error finding similar documents in Supabase:', error);
      return [];
    }
  }

  // Получить документ по ID из Supabase
  async getDocumentById(id: string | number): Promise<Document | null> {
    try {
      const { data, error } = await this.supabase
        .from('documents') // Assuming your table name is 'documents'
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        console.error('Error getting document by ID from Supabase:', error);
        return null;
      }

      return data as Document;

    } catch (error) {
      console.error('Error getting document by ID from Supabase:', error);
      return null;
    }
  }
}

// Экспортируем экземпляр сервиса
export const vectorDbService = new VectorDbService();