// test-search-real.ts
import axios from 'axios';

async function testSearch() {
  try {
    console.log('Testing search with a real query...');
    
    // Попробуем более конкретный запрос
    const response = await axios.get('http://localhost:3001/api/search?q=как использовать API');
    
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(response.data, null, 2));
  } catch (err) {
    console.error('Search Error:', err);
  }
}

testSearch();