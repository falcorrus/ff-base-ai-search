// src/services/vectorDbService.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { Document } from '../models/Document';

export class VectorDbService {
  private supabase: SupabaseClient;

  constructor() {
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    if (!supabaseUrl || !supabaseServiceRoleKey) {
      throw new Error('Missing Supabase URL or Service Role Key in environment variables.');
    }

    this.supabase = createClient(
      supabaseUrl,
      supabaseServiceRoleKey,
      { auth: { persistSession: false } }
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

