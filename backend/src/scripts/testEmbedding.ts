// backend/src/scripts/testEmbedding.ts
import * as fs from 'fs';
import * as path from 'path';

// Read the JSON file synchronously
const basePath = path.resolve(__dirname, '../../../base.json');
const rawData = fs.readFileSync(basePath, 'utf-8');
const data = JSON.parse(rawData);

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

// Test with first document
const firstDoc = data[0];
console.log(`Original embedding length: ${firstDoc.embedding.length}`);
const convertedEmbedding = convertEmbedding(firstDoc.embedding);
console.log(`Converted embedding length: ${convertedEmbedding.length}`);

// Check if they're the same
console.log(`First 5 values of original: ${firstDoc.embedding.slice(0, 5)}`);
console.log(`First 5 values of converted: ${convertedEmbedding.slice(0, 5)}`);
console.log(`Last 5 values of converted: ${convertedEmbedding.slice(-5)}`);