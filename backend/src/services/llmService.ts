// src/services/llmService.ts
import { GoogleGenerativeAI, GenerativeModel } from '@google/generative-ai';
import { config } from '../config';
import { Document } from '../models/Document';

export class LLMService {
  private generativeModel: GenerativeModel;
  private embeddingModel: GenerativeModel;

  constructor() {
    const genAI = new GoogleGenerativeAI(config.GEMINI.API_KEY);
    this.generativeModel = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    this.embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });
  }

  // Создать векторное представление текста (embedding)
  async createEmbedding(text: string): Promise<number[]> {
    try {
      const result = await this.embeddingModel.embedContent(text);
      const embedding = result.embedding.values;
      
      return embedding;
    } catch (error) {
      console.error('Error creating embedding:', error);
      // Возвращаем пустой массив в случае ошибки
      return [];
    }
  }

  // Сгенерировать ответ на основе контекста
  async generateAnswer(query: string, context: Document[]): Promise<string> {
    try {
      // Формируем контекст для LLM
      const contextText = context.map(doc => 
        `Document ID: ${doc.id}
Content: ${doc.text.substring(0, 500)}...`
      ).join(`

`);
      
      const prompt = `You are an AI assistant that answers questions based on provided context. 
      Use the following documents to answer the question at the end. 
      If you don't know the answer, just say that you don't know, don't try to make up an answer.
      
      Context:
      ${contextText}
      
      Question: ${query}
      
      Answer:`;
      
      const result = await this.generativeModel.generateContent(prompt);
      const response = await result.response;
      
      return response.text() || 'Sorry, I could not generate an answer.';
    } catch (error) {
      console.error('Error generating answer:', error);
      return 'Sorry, I encountered an error while generating the answer.';
    }
  }
}

// Экспортируем экземпляр сервиса
export const llmService = new LLMService();