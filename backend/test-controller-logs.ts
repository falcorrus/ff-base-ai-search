// test-controller-logs.ts
import { SearchController } from './src/controllers/searchController';
import { Request, Response } from 'express';

// Создаем mock объекты для запроса и ответа
const mockRequest = {
  query: {
    q: 'test'
  }
} as unknown as Request;

let responseData: any = null;

const mockResponse = {
  status: function(code: number) {
    console.log('Status code:', code);
    return this;
  },
  json: function(data: any) {
    responseData = data;
    console.log('Response data set');
    return this;
  }
} as unknown as Response;

async function testControllerWithLogs() {
  console.log('Testing controller with detailed logs...');
  const controller = new SearchController();
  await controller.search(mockRequest, mockResponse);
  
  console.log('Final response data:', JSON.stringify(responseData, null, 2));
}

testControllerWithLogs();