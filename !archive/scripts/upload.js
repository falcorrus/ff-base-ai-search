// scripts/upload.js
const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');

// Read the JSON file synchronously
const rawData = fs.readFileSync('../base.json', 'utf-8');
const data = JSON.parse(rawData);

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY; // ВАЖНО: используй service role key
const supabase = createClient(supabaseUrl, supabaseKey);

async function upload() {
  const batchSize = 1000;
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);
    const { error } = await supabase.from('messages').insert(batch);
    if (error) {
      console.error('Ошибка загрузки:', error);
    } else {
      console.log(`Загружено ${Math.min(i + batchSize, data.length)} из ${data.length}`);
    }
  }
}

upload();