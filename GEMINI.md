# Project: ff-base-ai-search

## Project Overview

This project is a web application designed for intelligent search and comprehensive answer generation from personal Markdown notes stored in the local `FF-BASE` directory or from the `falcorrus/ff-base` GitHub repository. It leverages vector search and large language models (LLMs) to provide quick and accurate answers based on a user's knowledge base.

**Key Technologies:**

*   **Backend:** Python 3.9+, FastAPI, Google Gemini API, and Google Cloud Run for deployment.
*   **Frontend:** Vanilla JavaScript with Tailwind CSS, intended for deployment on Firebase Hosting or other Google Cloud static platforms.
*   **Data Storage:** Embeddings are stored in a local JSON file (`knowledge_base/embeddings.json`), containing vector representations for all 276 Markdown notes.
*   **Vector Search:** Semantic search using Google Gemini embeddings for finding relevant notes.
*   **Query Logging:** All search queries are logged to a JSON file (`knowledge_base/search_log.json`) with timestamps.

## Recent Recovery of Knowledge Base

The project's knowledge base has been recently restored with a complete set of embeddings for all 276 Markdown notes. The `knowledge_base/embeddings.json` file was regenerated using a custom script that processed all notes and generated corresponding vector representations. This ensures full functionality of the semantic search capabilities.

**Architecture Highlights:**

*   **Synchronization:** Reading Markdown notes from the local `FF-BASE` directory or from the `falcorrus/ff-base` GitHub repository.
*   **Embedding Generation:** Creation and storage of vector embeddings for each note using Google Gemini Embeddings API (`models/embedding-001`). Recently regenerated for all 276 notes.
*   **Search & Answer Generation:**
    *   User queries are transformed into embeddings via the Google Gemini Embeddings API.
    *   Relevant notes are identified through vector similarity search using cosine similarity.
    *   Markdown files for relevant notes are read from the local filesystem or GitHub.
    *   A context is formed from these notes and sent to the Google Gemini LLM (`gemini-1.5-flash`) for comprehensive answer generation.
    *   The generated answer is returned to the user.
*   **Logging:** All requests are logged to a JSON file for monitoring and debugging.

## Building and Running

### Backend (FastAPI)

To run the FastAPI backend locally, you would typically use `uvicorn`.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided startup script:
```bash
# Navigate to the backend directory
cd backend

# Make the script executable (if not already)
chmod +x start.sh

# Run the backend server
./start.sh
```

Endpoints:
*   `GET /` - Health check endpoint
*   `GET /update-knowledge-base` - Update embeddings from GitHub repository
*   `GET /update-knowledge-base-local` - Update embeddings from local FF-BASE directory
*   `GET /search?query={query}` - Search for relevant notes and generate answers
*   `GET /notes-count` - Get the total number of notes in the knowledge base

### Frontend (Vanilla JS)

The frontend is a static web application. It would be served by a web server or deployed to a static hosting service.

```bash
# To serve locally (example using Python's http.server)
cd frontend
python -m http.server 3000
```

### Deployment

*   **Backend:** Intended for deployment on Google Cloud Run.
*   **Frontend:** Intended for deployment on Firebase Hosting or other Google Cloud static platforms.

## Development Conventions

*   **Asynchronous Processing:** Backend requests are designed for asynchronous handling.
*   **Logging:** All requests are logged to a JSON file for monitoring and debugging.
*   **Google Cloud Ecosystem:** The project is designed to integrate seamlessly with Google Cloud services for deployment, security, and scalability.
*   **LLM Interaction:** Google Gemini API is used for query embedding and answer generation. Direct calls to the Gemini API are preferred for production stability and scalability.
*   **GitHub API:** Used for reading Markdown notes from the `falcorrus/ff-base` GitHub repository.
*   **Local File System:** Used for reading Markdown notes from the local `FF-BASE` directory.
*   **Scalability:** Initial local JSON storage for embeddings, with a plan to migrate to a specialized vector store (e.g., Chromadb) as the note base grows.