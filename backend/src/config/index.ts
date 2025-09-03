// src/config/index.ts
import dotenv from 'dotenv';
import path from 'path';

// Загружаем переменные окружения из .env файла
const envPath = path.resolve(__dirname, '../../.env');
dotenv.config({ path: envPath });

// Проверяем обязательные переменные окружения
const requiredEnvVars = [
  'GITHUB_TOKEN',
  'GOOGLE_API_KEY', // Changed this to match .env
  'SUPABASE_SERVICE_ROLE_KEY',
];

// Проверка наличия обязательных переменных окружения
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    console.warn(`Warning: Missing required environment variable ${envVar}`);
  }
}

export const config = {
  // Порт сервера
  PORT: process.env.PORT || 3001,
  
  // GitHub конфигурация
  GITHUB: {
    TOKEN: process.env.GITHUB_TOKEN || '',
  },
  
  // Gemini конфигурация
  GEMINI: {
    API_KEY: process.env.GOOGLE_API_KEY || '',
  },

  // Supabase конфигурация
  SUPABASE: {
    URL: process.env.SUPABASE_URL || '',
    ANON_KEY: process.env.SUPABASE_ANON_KEY || '',
    SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY || '',
  },
  
  // Путь к файлу векторной базы данных (для прототипа)
  VECTOR_DB_PATH: process.env.VECTOR_DB_PATH || '../knowledge_base.json',
  
  // Другие конфигурации...
};