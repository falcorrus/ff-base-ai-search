// test-api.ts
import axios from 'axios';

async function testApi() {
  try {
    console.log('Testing API...');
    
    const response = await axios.get('http://localhost:3001/api/search?q=test');
    
    console.log('Status:', response.status);
    console.log('Data:', response.data);
  } catch (err) {
    console.error('Error:', err);
  }
}

testApi();