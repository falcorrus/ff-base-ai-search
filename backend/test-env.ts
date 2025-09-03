// test-env.ts
import { config } from './src/config';

console.log('SUPABASE URL:', config.SUPABASE.URL);
console.log('SUPABASE SERVICE_ROLE_KEY exists:', !!config.SUPABASE.SERVICE_ROLE_KEY);
console.log('GEMINI API KEY exists:', !!config.GEMINI.API_KEY);