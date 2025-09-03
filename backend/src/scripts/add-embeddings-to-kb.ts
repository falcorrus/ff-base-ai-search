
import * as fs from 'fs';
import * as path from 'path';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const API_KEY = process.env.GEMINI_API_KEY;
if (!API_KEY) {
  throw new Error('GEMINI_API_KEY is not defined in the .env file');
}

const KNOWLEDGE_BASE_PATH = path.resolve(__dirname, '../../knowledge_base.json');

if (!KNOWLEDGE_BASE_PATH) {
  throw new Error('KNOWLEDGE_BASE_PATH is not defined');
}

// Define a robust interface
interface Message {
  id: number;
  date: string;
  sender: string;
  text?: string; // Text is optional
  origin: string;
  embedding?: number[];
}

const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

async function addEmbeddingsToKB() {
  console.log('Starting to add embeddings to Knowledge Base...');

  try {
    if (!KNOWLEDGE_BASE_PATH) {
      throw new Error('KNOWLEDGE_BASE_PATH is not defined');
    }
    
    const fileContent = fs.readFileSync(KNOWLEDGE_BASE_PATH, 'utf-8');
    const messages: Message[] = JSON.parse(fileContent);

    const genAI = new GoogleGenerativeAI(API_KEY!);
    const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });

    let updatedCount = 0;

    for (const message of messages) {
      // Skip if embedding already exists
      if (message.embedding && message.embedding.length > 0) {
        continue;
      }

      // Robustly check if text is a non-empty string
      if (typeof message.text === 'string' && message.text.trim() !== '') {
        console.log(`Processing message ID: ${message.id}`);
        try {
          const result = await embeddingModel.embedContent(message.text);
          message.embedding = result.embedding.values;
          updatedCount++;
          await sleep(200); // Adhere to rate limits
        } catch (error) {
          console.error(`Failed to generate embedding for message ID: ${message.id}. Error:`, error);
        }
      } else {
        console.log(`Skipping message ID: ${message.id} due to missing or empty text.`);
      }
    }

    fs.writeFileSync(KNOWLEDGE_BASE_PATH, JSON.stringify(messages, null, 2));

    console.log('\nEmbedding generation complete.');
    console.log(`Updated ${updatedCount} messages with new embeddings.`);
    console.log(`Knowledge base saved to ${KNOWLEDGE_BASE_PATH}`);

  } catch (error) {
    console.error('An error occurred:', error);
  }
}

addEmbeddingsToKB();
