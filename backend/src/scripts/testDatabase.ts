// testDatabase.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

async function testDatabase() {
  try {
    console.log('Testing Supabase database connection...');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
    
    console.log('Supabase URL exists:', !!supabaseUrl);
    console.log('Supabase Key exists:', !!supabaseKey);
    
    if (!supabaseUrl || !supabaseKey) {
      console.error('Supabase credentials are not set');
      return;
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Test database connection by querying a small amount of data
    const { data, error } = await supabase
      .from('documents')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('Database connection failed:', error);
      return;
    }
    
    console.log('Database connection successful');
    console.log('Found', data.length, 'documents');
    
    if (data.length > 0) {
      console.log('Sample document:', {
        id: data[0].id,
        text: data[0].text?.substring(0, 100) + '...'
      });
    }
    
  } catch (error) {
    console.error('Database test failed:', error);
  }
}

testDatabase();