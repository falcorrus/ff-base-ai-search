// test-search-detailed.ts
import { SearchController } from './src/controllers/searchController';
import { Request, Response } from 'express';

// Создаем mock объекты для запроса и ответа
const mockRequest = {
  query: {
    q: 'Как использовать API?'
  }
} as unknown as Request;

const responses: any[] = [];

const mockResponse = {
  status: function(code: number) {
    responses.push({ type: 'status', code });
    return this;
  },
  json: function(data: any) {
    responses.push({ type: 'json', data });
    console.log('Response data:', JSON.stringify(data, null, 2));
    return this;
  }
} as unknown as Response;

async function testSearch() {
  console.log('Testing search controller with detailed logging');
  const controller = new SearchController();
  await controller.search(mockRequest, mockResponse);
  
  console.log('All responses:', responses);
}

testSearch();