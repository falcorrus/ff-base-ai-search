# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

ff-base-ai-search is an intelligent semantic search system for personal knowledge bases stored as Markdown files in GitHub repositories. The system uses RAG (Retrieval-Augmented Generation) to provide semantic search capabilities with AI-generated answers.

### Key Technologies
- **Backend**: Node.js + Express + TypeScript
- **Frontend**: Vanilla TypeScript + HTMX + Tailwind CSS
- **AI/ML**: Google Gemini API for embeddings and text generation
- **Vector Database**: Supabase (production), JSON files (development/prototype)
- **Deployment**: Vercel (full-stack deployment with serverless functions)

## Development Commands

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Development mode with hot reload
npm run dev

# Build TypeScript to JavaScript
npm run build

# Production start
npm start

# Run embeddings generation script
npm run generate-embeddings

# Test search functionality
npm run test-search

# Test LLM service
npm run test-llm

# Test API endpoints
npm run test-api
```

### Frontend Development
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Full Stack Development
```bash
# Install all dependencies (root + workspaces)
npm install

# Build both frontend and backend
npm run build --workspace=frontend && npm run build --workspace=backend
```

## Architecture Overview

### Backend Structure (`backend/src/`)
- **config/**: Environment configuration and constants
- **controllers/**: Request handlers (searchController.ts handles search logic)
- **services/**: Business logic services
  - `llmService.ts`: Google Gemini API integration for embeddings and text generation
  - `vectorDbService.ts`: Supabase vector database operations
- **models/**: TypeScript interfaces (Document model)
- **routes/**: Express route definitions
- **scripts/**: Utility scripts for data processing and testing

### Key Backend Services

#### LLM Service
- Handles Google Gemini API integration
- Creates 768-dimensional embeddings using `embedding-001` model
- Generates responses using `gemini-1.5-flash` model
- Embeddings are converted to 1536 dimensions for Supabase compatibility

#### Vector Database Service
- Manages Supabase vector database operations
- Uses `match_documents` RPC function for similarity search
- Handles document retrieval by ID
- Configured with similarity threshold of 0.7

### Frontend Architecture
- **HTMX-based SPA**: Uses HTMX for dynamic content loading without traditional JavaScript frameworks
- **Tailwind CSS**: Utility-first CSS framework for styling
- **TypeScript**: Type-safe client-side logic in `src/main.ts`
- **Modal system**: Custom modal for viewing document details

## Database Schema

The system uses Supabase with a `documents` table containing:
- `id`: Document identifier
- `text`: Document content
- `embedding`: 1536-dimensional vector (converted from 768-dim Gemini embeddings)
- `date`: Document date
- `sender`: Document author/source
- `origin`: Source URL or path

## Environment Variables

### Required Backend Variables
```bash
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_key
SUPABASE_ANON_KEY=your_supabase_anon_key
PORT=3001
```

## API Endpoints

### Search API
- `GET /api/search?q={query}`: Semantic search with AI-generated answer
  - Returns: `{ answer: string, results: SearchResult[] }`
- `GET /api/note/:id`: Get document content by ID
  - Returns: `{ title: string, content: string, path: string, githubUrl: string }`

## Data Processing Workflow

### Embedding Generation and Upload
1. **Data Sources**: JSON files containing processed documents (`input_base.json`, `knowledge_base.json`)
2. **Scripts**: Use `backend/src/scripts/upload.ts` to upload documents to Supabase
3. **Embedding Conversion**: 768-dim Gemini embeddings are padded to 1536-dim for Supabase
4. **Batch Processing**: Documents are processed in batches of 1000 for efficiency

### Search Flow
1. User query is embedded using Gemini API
2. Vector similarity search in Supabase using cosine similarity
3. Top 5 similar documents retrieved
4. LLM generates contextual answer using retrieved documents
5. Frontend displays AI answer and source documents

## Testing Commands

### Backend Testing Scripts
```bash
# Test individual components
npm run test-search      # Test search functionality
npm run test-llm        # Test LLM service
npm run test-api        # Test API endpoints

# Manual testing files (use ts-node to run)
ts-node src/scripts/testSearch.ts
ts-node src/scripts/testLLM.ts
ts-node src/scripts/testVectorDb.ts
```

## Deployment

### Vercel Configuration
- **Build Command**: `npm run build --workspace=frontend && npm run build --workspace=backend`
- **Frontend**: Static build deployed to Vercel Edge
- **Backend**: Serverless functions deployment
- **Routes**: `/api/*` → backend, `/*` → frontend

### Production Setup
1. Configure environment variables in Vercel dashboard
2. Ensure Supabase database is set up with proper RPC functions
3. Upload knowledge base data using upload scripts
4. Deploy via Git integration or Vercel CLI

## Common Development Patterns

### Adding New Search Features
1. Extend `searchController.ts` for new endpoints
2. Add corresponding routes in `routes/searchRoutes.ts`
3. Update frontend HTMX attributes for new interactions

### Data Processing
1. Add new scripts in `backend/src/scripts/` for data processing
2. Use existing embedding conversion utilities
3. Follow batch processing patterns for large datasets

### Frontend Enhancements
1. Extend `main.ts` for new interactive features
2. Use HTMX attributes for server interactions
3. Follow existing modal and event handling patterns

## Important Notes

- Embedding dimension conversion is critical for Supabase compatibility
- All API responses include CORS headers for cross-origin requests
- Frontend uses HTMX event system for dynamic content updates
- Vector similarity threshold is configurable in `vectorDbService.ts`
- Supabase RPC functions are used for efficient vector similarity search
