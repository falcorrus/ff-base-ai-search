// test-cors.ts
import axios from 'axios';

async function testCors() {
  try {
    console.log('Testing CORS...');
    
    // Попробуем выполнить OPTIONS запрос (предварительный запрос CORS)
    const optionsResponse = await axios.options('http://localhost:3000/api/search?q=test', {
      headers: {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type'
      }
    });
    
    console.log('OPTIONS status:', optionsResponse.status);
    console.log('OPTIONS headers:', optionsResponse.headers);
    
    // Попробуем выполнить GET запрос с CORS заголовками
    const getResponse = await axios.get('http://localhost:3000/api/search?q=test', {
      headers: {
        'Origin': 'http://localhost:3000'
      }
    });
    
    console.log('GET status:', getResponse.status);
    console.log('GET data:', getResponse.data);
  } catch (err) {
    console.error('CORS Error:', err);
  }
}

testCors();