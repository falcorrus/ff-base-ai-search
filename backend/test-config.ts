// test-config.ts
import { config } from './src/config';

console.log('Configuration:');
console.log('PORT:', config.PORT);
console.log('SUPABASE URL:', config.SUPABASE.URL);
console.log('SUPABASE SERVICE_ROLE_KEY:', config.SUPABASE.SERVICE_ROLE_KEY ? 'SET' : 'NOT SET');
console.log('GEMINI API KEY:', config.GEMINI.API_KEY ? 'SET' : 'NOT SET');