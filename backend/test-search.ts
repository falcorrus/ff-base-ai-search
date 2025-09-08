// test-search.ts
import { SearchController } from './src/controllers/searchController';
import { Request, Response } from 'express';

// Создаем mock объекты для запроса и ответа
const mockRequest = {
  query: {
    q: 'Как использовать API?'
  }
} as unknown as Request;

const mockResponse = {
  status: function(code: number) {
    console.log('Status code:', code);
    return this;
  },
  json: function(data: any) {
    console.log('Response data:', JSON.stringify(data, null, 2));
    return this;
  }
} as unknown as Response;

async function testSearch() {
  console.log('Testing search controller');
  const controller = new SearchController();
  await controller.search(mockRequest, mockResponse);
}

testSearch();