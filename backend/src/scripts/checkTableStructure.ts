// checkTableStructure.ts
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

async function checkTableStructure() {
  try {
    console.log('Checking table structure...');
    
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
    
    if (!supabaseUrl || !supabaseKey) {
      console.error('Supabase credentials are not set');
      return;
    }
    
    const supabase = createClient(supabaseUrl, supabaseKey);
    
    // Check if the documents table exists and get its structure
    const { data, error } = await supabase
      .from('documents')
      .select('*')
      .limit(1);
    
    if (error) {
      console.error('Error querying documents table:', error);
      return;
    }
    
    console.log('Table exists and is accessible');
    console.log('Column information:');
    
    if (data.length > 0) {
      const columns = Object.keys(data[0]);
      console.log('Columns:', columns);
      
      // Print sample data
      console.log('Sample row:', data[0]);
    } else {
      console.log('Table is empty');
    }
    
  } catch (error) {
    console.error('Table structure check failed:', error);
  }
}

checkTableStructure();