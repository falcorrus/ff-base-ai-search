// test-request.js
const http = require('http');
const querystring = require('querystring');

// Создаем GET-запрос
const queryParams = querystring.stringify({ q: 'безопасность' });
const options = {
  hostname: 'localhost',
  port: 3001,
  path: `/api/search?${queryParams}`,
  method: 'GET'
};

console.log('Request path:', options.path);

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers: ${JSON.stringify(res.headers)}`);
  
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    console.log('Response body:', data);
  });
});

req.on('error', (error) => {
  console.error('Request error:', error);
});

req.end();