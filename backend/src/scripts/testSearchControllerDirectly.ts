// testSearchControllerDirectly.ts
import { SearchController } from '../controllers/searchController';
import { VectorDbService } from '../services/vectorDbService';
import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

async function testSearchController() {
  try {
    console.log('Testing search controller directly...');
    
    // Create an instance of the vector database service
    const vectorDbService = new VectorDbService();
    
    // Create an instance of the search controller
    const searchController = new SearchController(vectorDbService);
    
    // Mock request and response objects
    const mockReq = {
      query: {
        q: 'мысль'
      }
    };
    
    const mockRes = {
      status: function(code: number) {
        console.log('Response status:', code);
        return this;
      },
      json: function(data: any) {
        console.log('Response data:', JSON.stringify(data, null, 2));
        return this;
      }
    };
    
    // Call the search method directly
    console.log('Calling search method...');
    await searchController.search(mockReq as any, mockRes as any);
    
  } catch (error) {
    console.error('Test failed:', error);
  }
}

testSearchController();