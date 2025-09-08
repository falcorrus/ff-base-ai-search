// backend/src/scripts/testApiEndpoints.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:3001/api';

async function testApiEndpoints() {
  console.log('Тестирование API endpoints...\n');
  
  try {
    // Test text search
    console.log('1. Тестирование текстового поиска:');
    const textSearchResponse = await axios.get(`${API_BASE_URL}/text-search?query=идея`);
    console.log(`   Статус: ${textSearchResponse.status}`);
    console.log(`   Найдено документов: ${textSearchResponse.data.length}`);
    
    if (textSearchResponse.data.length > 0) {
      console.log(`   Первый документ: "${textSearchResponse.data[0].text.substring(0, 100)}..."`);
    }
    
    console.log('\n' + '='.repeat(50) + '\n');
    
    // Test semantic search
    console.log('2. Тестирование семантического поиска:');
    const semanticSearchResponse = await axios.get(`${API_BASE_URL}/search?q=идея`);
    console.log(`   Статус: ${semanticSearchResponse.status}`);
    console.log(`   Ответ: ${JSON.stringify(semanticSearchResponse.data).substring(0, 200)}...`);
    
    console.log('\n' + '='.repeat(50) + '\n');
    
    // Test text search for "мысли"
    console.log('3. Тестирование текстового поиска для "мысли":');
    const myshiSearchResponse = await axios.get(`${API_BASE_URL}/text-search?query=мысли`);
    console.log(`   Статус: ${myshiSearchResponse.status}`);
    console.log(`   Найдено документов: ${myshiSearchResponse.data.length}`);
    
    if (myshiSearchResponse.data.length > 0) {
      console.log(`   Первый документ: "${myshiSearchResponse.data[0].text.substring(0, 100)}..."`);
    }
    
    console.log('\n=== Все тесты пройдены успешно ===');
    
  } catch (error: any) {
    console.error('Ошибка при тестировании API:');
    if (error.response) {
      console.error(`   Статус: ${error.response.status}`);
      console.error(`   Данные: ${JSON.stringify(error.response.data)}`);
    } else {
      console.error(`   Сообщение: ${error.message}`);
    }
  }
}

testApiEndpoints();