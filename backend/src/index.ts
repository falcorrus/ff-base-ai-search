// src/index.ts
import dotenv from 'dotenv';
import path from 'path';

const envPath = path.resolve(__dirname, '../../.env');
console.log('Attempting to load .env from:', envPath);
dotenv.config({ path: envPath });

console.log('Environment check:');
console.log('SUPABASE_URL exists:', !!process.env.SUPABASE_URL);
console.log('SUPABASE_SERVICE_ROLE_KEY exists:', !!process.env.SUPABASE_SERVICE_ROLE_KEY);
console.log('GOOGLE_API_KEY exists:', !!process.env.GOOGLE_API_KEY);
console.log('Full process.env:', process.env);

import express, { Request, Response } from 'express';
import cors from 'cors';
import searchRoutes from './routes/searchRoutes';
import { config } from './config/index';
import { VectorDbService } from './services/vectorDbService';
import { SearchController } from './controllers/searchController';

const app = express();
const port = config.PORT;

// Instantiate VectorDbService after dotenv.config() has run
const vectorDbService = new VectorDbService();
const searchController = new SearchController(vectorDbService);

// Middleware
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://your-app-domain.vercel.app', 'https://your-app-domain-git-main.your-vercel-account.vercel.app'] 
    : 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

// Маршруты
app.use('/api', searchRoutes(searchController));

// Тестовый маршрут
app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Intelligent Search API is running!' });
});

// Запуск сервера
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});