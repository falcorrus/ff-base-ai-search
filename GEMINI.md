# Project: ff-base-ai-search

## Project Overview

This project is a web application designed for intelligent search and comprehensive answer generation from personal Markdown notes stored in the GitHub repository `falcorrus/ff-base`. It leverages vector search and large language models (LLMs) to provide quick and accurate answers based on a user's knowledge base.

**Key Technologies:**

*   **Backend:** Python 3.9+, FastAPI, Google Gemini API, GitHub API, and Google Cloud Run for deployment.
*   **Frontend:** Vanilla JavaScript, intended for deployment on Firebase Hosting or other Google Cloud static platforms.
*   **Data Storage:** Initially, embeddings are stored in a local JSON file, with a future plan to migrate to a specialized vector store like Chromadb.
*   **Vector Search:** Semantic search using Google Gemini embeddings for finding relevant notes.

**Architecture Highlights:**

*   **Synchronization:** Fetching Markdown notes from the `falcorrus/ff-base` GitHub repository.
*   **Embedding Generation:** Creation and storage of vector embeddings for each note using Google Gemini API.
*   **Search & Answer Generation:**
    *   User queries are transformed into embeddings via the Google Gemini API.
    *   Relevant notes are identified through vector similarity search.
    *   Markdown files for relevant notes are fetched from GitHub.
    *   A context is formed from these notes and sent to the Google Gemini LLM for comprehensive answer generation.
    *   The generated answer is returned to the user.
*   **Logging:** All requests are logged to a JSON file, including timestamps and query text.

## Building and Running

### Backend (FastAPI)

To run the FastAPI backend locally, you would typically use `uvicorn`.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
*   `GET /` - Health check endpoint
*   `GET /update-knowledge-base` - Update embeddings from GitHub repository
*   `GET /search?query={query}` - Search for relevant notes and generate answers

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
*   **Scalability:** Initial local JSON storage for embeddings, with a plan to migrate to a specialized vector store (e.g., Chromadb) as the note base grows.