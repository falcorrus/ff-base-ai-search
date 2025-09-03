// src/models/Document.ts

export interface Document {
  id: string | number;
  date?: string;
  sender?: string;
  text: string;
  origin?: string;
  embedding: number[];
}

export interface SearchResult {
  document: Document;
  similarity: number;
}