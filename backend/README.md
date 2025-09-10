# ff-base-ai-search Backend

This is the Python FastAPI backend for the ff-base-ai-search application, designed for intelligent search and comprehensive answer generation from personal Markdown notes.

## Technologies

- **Python 3.9+**: Programming language
- **FastAPI**: Web framework for building APIs with Python
- **Google Gemini API**: For creating embeddings and generating answers
- **Local JSON Storage**: Embeddings stored in `knowledge_base/embeddings.json`
- **Google Cloud Run**: Intended deployment platform

## Project Structure

```
backend/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── start.sh               # Script to start the server
├── init_knowledge_base.py # Script to initialize knowledge base from FF-BASE
├── Dockerfile             # Docker configuration
└── README.md              # This file
```

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### Knowledge Base Management
- `GET /update-knowledge-base-local` - Update embeddings from local FF-BASE directory
- `GET /update-knowledge-base` - Update embeddings from GitHub repository (requires GITHUB_PAT)

### Search
- `GET /search?query={query}&top_k={count}` - Search for relevant notes and generate answers
  - `query` (required) - Search query text
  - `top_k` (optional) - Number of results to return (default: 5)
- `GET /notes-count` - Get the total number of notes in the knowledge base

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
GOOGLE_API_KEY=your_google_api_key_here
LOG_LEVEL=INFO
```

See `.env.example` for a template.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Google API key:
   ```bash
   cp .env.example .env
   # Edit .env to add your GOOGLE_API_KEY
   ```

## Running the Application

To run the backend server:

```bash
# Using the start script (recommended)
./start.sh

# Or directly with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

## Deployment

This backend is designed for deployment on Google Cloud Run. For deployment instructions, refer to the Google Cloud Run documentation.