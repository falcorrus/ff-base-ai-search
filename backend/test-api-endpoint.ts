// test-api-endpoint.ts
import axios from 'axios';

async function testApiEndpoint() {
  try {
    console.log('Testing API endpoint...');
    
    // Попробуем выполнить запрос к API endpoint
    const response = await axios.get('http://localhost:3001/api/search?q=test');
    
    console.log('Status:', response.status);
    console.log('Data:', JSON.stringify(response.data, null, 2));
  } catch (err) {
    console.error('API endpoint error:', err);
  }
}

testApiEndpoint();