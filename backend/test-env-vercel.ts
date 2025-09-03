// test-env-vercel.ts
console.log('NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log('SUPABASE_SERVICE_ROLE_KEY exists:', !!process.env.SUPABASE_SERVICE_ROLE_KEY);
console.log('GEMINI_API_KEY exists:', !!process.env.GEMINI_API_KEY);
console.log('PORT:', process.env.PORT);