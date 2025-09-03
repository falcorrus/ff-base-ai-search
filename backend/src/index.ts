// src/index.ts
import express, { Request, Response } from 'express';
import cors from 'cors';
import searchRoutes from './routes/searchRoutes';
import { config } from './config/index';

const app = express();
const port = config.PORT;

// Middleware
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://your-app-domain.vercel.app', 'https://your-app-domain-git-main.your-vercel-account.vercel.app'] 
    : 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());

// Маршруты
app.use('/api', searchRoutes);

// Тестовый маршрут
app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Intelligent Search API is running!' });
});

// Запуск сервера
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

module.exports = app;