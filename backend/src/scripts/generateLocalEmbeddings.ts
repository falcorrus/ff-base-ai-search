// generateLocalEmbeddings.ts
import * as fs from 'fs';
import * as path from 'path';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

// Configuration
const GEMINI_API_KEY = process.env.GOOGLE_API_KEY;
const SOURCE_DIR = path.resolve(__dirname, '../../../FF-BASE');
const OUTPUT_FILE = path.resolve(__dirname, '../../../knowledge_base/embeddings.json');

if (!GEMINI_API_KEY) {
  console.error('GOOGLE_API_KEY is not set in environment variables');
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
const embeddingModel = genAI.getGenerativeModel({ model: 'embedding-001' });

interface EmbeddingData {
  file_path: string;
  content: string;
  embedding: number[];
}

/**
 * Get all .md files from directory recursively
 */
function getAllMdFiles(dir: string, fileList: string[] = []): string[] {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    // Skip hidden directories
    if (stat.isDirectory() && !file.startsWith('.')) {
      getAllMdFiles(filePath, fileList);
    } else if (stat.isFile() && file.endsWith('.md')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

/**
 * Read file content
 */
function readFileContent(filePath: string): string {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error);
    return '';
  }
}

/**
 * Generate embedding for text
 */
async function generateEmbedding(text: string): Promise<number[]> {
  try {
    // Limit text size for API
    if (text.length > 10000) {
      text = text.substring(0, 10000);
    }
    
    const result = await embeddingModel.embedContent(text);
    return result.embedding.values;
  } catch (error) {
    console.error('Error generating embedding:', error);
    return [];
  }
}

/**
 * Generate embeddings for all .md files in directory
 */
async function generateEmbeddingsForDirectory(): Promise<void> {
  console.log(`Searching for .md files in directory: ${SOURCE_DIR}`);
  
  // Get all .md files
  const files = getAllMdFiles(SOURCE_DIR);
  console.log(`Found ${files.length} .md files`);
  
  const embeddingsData: EmbeddingData[] = [];
  
  // Process each file
  for (let i = 0; i < files.length; i++) {
    const filePath = files[i];
    const relativePath = path.relative(SOURCE_DIR, filePath);
    
    console.log(`Processing file ${i + 1}/${files.length}: ${relativePath}`);
    
    // Read file content
    const content = readFileContent(filePath);
    if (!content) {
      continue;
    }
    
    // Generate embedding
    const embedding = await generateEmbedding(content);
    if (embedding.length > 0) {
      embeddingsData.push({
        file_path: relativePath,
        content: content,
        embedding: embedding
      });
    } else {
      console.log(`Failed to generate embedding for ${relativePath}`);
    }
    
    // Show progress every 10 files
    if ((i + 1) % 10 === 0) {
      console.log(`Processed ${i + 1} files...`);
    }
  }
  
  // Save embeddings to file
  console.log(`Saving ${embeddingsData.length} embeddings to ${OUTPUT_FILE}`);
  
  // Ensure directory exists
  const dir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(embeddingsData, null, 2), 'utf-8');
  console.log('Embeddings saved successfully!');
}

// Run the script
async function main() {
  try {
    console.log('Starting embeddings generation for local files...');
    await generateEmbeddingsForDirectory();
    console.log('Process completed successfully!');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();