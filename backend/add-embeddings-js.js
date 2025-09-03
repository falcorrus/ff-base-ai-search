const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const API_KEY = process.env.GEMINI_API_KEY;
if (!API_KEY) {
  throw new Error('GEMINI_API_KEY is not defined in the .env file');
}

const KNOWLEDGE_BASE_PATH = '/Users/eugene/MyProjects/ff-base-ai-search/knowledge_base.json';

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function addEmbeddings() {
  console.log('Starting to add embeddings using JavaScript script...');

  try {
    const fileContent = fs.readFileSync(KNOWLEDGE_BASE_PATH, 'utf-8');
    const messages = JSON.parse(fileContent);

    const genAI = new GoogleGenerativeAI(API_KEY);
    const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });

    let updatedCount = 0;

    for (const message of messages) {
      if (message.embedding && message.embedding.length > 0) {
        continue;
      }

      if (typeof message.text === 'string' && message.text.trim() !== '') {
        console.log(`Processing message ID: ${message.id}`);
        try {
          const result = await embeddingModel.embedContent(message.text);
          message.embedding = result.embedding.values;
          updatedCount++;
          await sleep(200);
        } catch (error) {
          console.error(`Failed to generate embedding for message ID: ${message.id}. Error:`, error.message);
        }
      } else {
        console.log(`Skipping message ID: ${message.id} due to missing or empty text.`);
      }
    }

    fs.writeFileSync(KNOWLEDGE_BASE_PATH, JSON.stringify(messages, null, 2));

    console.log('\nEmbedding generation complete.');
    console.log(`Updated ${updatedCount} messages.`);
    console.log(`Knowledge base saved to ${KNOWLEDGE_BASE_PATH}`);

  } catch (error) {
    console.error('An error occurred:', error.message);
  }
}

addEmbeddings();
