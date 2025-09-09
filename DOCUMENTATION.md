# ff-base-ai-search Documentation

## Project Overview

This project is a web application designed for intelligent search and comprehensive answer generation from personal Markdown notes stored in the local `FF-BASE` directory. It leverages vector search and large language models (LLMs) to provide quick and accurate answers based on a user's knowledge base.

### Key Technologies

* **Backend:** Python 3.9+, FastAPI
* **AI:** Google Gemini API (for generating embeddings and responses)
* **Data Storage:** Local JSON storage (for embeddings)
* **Frontend:** Vanilla JavaScript (in development)
* **Deployment:** Google Cloud Run (backend), Firebase Hosting (frontend)

### Architecture

1. **Sync:** Retrieval of Markdown notes from the local `FF-BASE` directory
2. **Embedding Generation:** Creation and storage of vector representations for each note using Google Gemini API
3. **Search:** Conversion of user queries to embeddings and finding relevant notes through vector similarity
4. **Response Generation:** Context formation from relevant notes and sending to Google Gemini LLM for comprehensive answer generation
5. **Language Support:** Full support for Russian language search queries using UTF-8 encoding

## Project Structure

```
ff-base-ai-search/
├── backend/                 # Backend FastAPI application
│   ├── main.py             # Main application file
│   ├── requirements.txt    # Python dependencies
│   ├── init_knowledge_base.py # Script to initialize knowledge base from FF-BASE
│   └── .env                # Environment variables
├── frontend/               # Frontend application (in development)
│   ├── index.html          # Main page
│   ├── style.css           # Styles
│   └── script.js           # JavaScript code
├── FF-BASE/                # Local storage of Markdown notes (276 files)
├── knowledge_base/         # Local embeddings storage
│   └── embeddings.json     # Vector representations of notes (276 entries)
└── DOCUMENTATION.md        # Project documentation
```

## Initializing the Knowledge Base

To initialize or update the knowledge base from the FF-BASE directory, run:

```bash
cd backend
python init_knowledge_base.py
```

This script processes all Markdown files in the FF-BASE directory and generates embeddings for them, storing the results in `knowledge_base/embeddings.json`.

## Installation and Setup

### Backend Setup

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Create a `.env` file with required environment variables:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   LOG_LEVEL=INFO
   ```

3. Start the server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Open `frontend/index.html` in a browser or start a local server:
   ```bash
   cd frontend
   python -m http.server 3000
   ```

## API Endpoints

* `GET /` - Health check
* `GET /search?query={query}&top_k={count}` - Search notes and generate response
  * `query` (required) - Search query text (supports Russian)
  * `top_k` (optional) - Number of results to return (default: 5)
* `GET /notes-count` - Get the total number of notes in the knowledge base
* `GET /update-knowledge-base-local` - Update knowledge base from local FF-BASE directory

## How the Search System Works

### Data Ingestion and Embedding Generation

The system processes Markdown files from the FF-BASE directory and converts them into embeddings:

- Each Markdown file is read and converted to a vector representation using Google's embedding models
- These embeddings are stored in `knowledge_base/embeddings.json`
- The system maintains metadata to track file changes and only reprocesses modified files

### Search Process

When a user submits a query:

1. The query is converted to an embedding using the same model
2. Cosine similarity is calculated between the query embedding and all note embeddings
3. The most relevant notes are selected based on similarity scores
4. The relevant notes are used as context for generating a comprehensive answer

### Response Generation

The system uses Google Gemini to generate responses:

1. Relevant documents are formatted as context
2. A prompt is created combining the context and user query
3. The LLM generates a comprehensive answer based on the provided context

## Knowledge Base Management

The knowledge base contains embeddings for all 276 Markdown notes from the FF-BASE directory. The system supports incremental updates, only reprocessing files that have changed since the last update.

## Recent Updates

The knowledge base was recently restored with a complete set of embeddings for all 276 Markdown notes. The `knowledge_base/embeddings.json` file was regenerated to ensure full functionality of the semantic search capabilities.

## License

MIT