# How the Search System Works

This document explains how the search system in this project works, from data ingestion to search functionality.

## Overview

The search system is built around the following components:

1. **Knowledge Base Creation**: Markdown files are processed and converted into embeddings
2. **Embedding Generation**: Text content is converted to vector representations using Google's embedding models
3. **Search Engine**: Queries are matched against the knowledge base using cosine similarity
4. **Response Generation**: Relevant documents are used as context for generating comprehensive answers

## System Architecture

### 1. Data Ingestion and Embedding Generation

The system processes Markdown files from a source directory (typically a documentation repository) and converts them into embeddings:

- **`generate_embeddings.py`**: Main script for generating embeddings from Markdown files
- Reads all `.md` files from a specified directory
- Uses Google's `embedding-001` model to generate vector representations
- Stores the file path, content, and embedding in a JSON file

### 2. Knowledge Base Storage

The embeddings are stored in `knowledge_base/embeddings.json` with the following structure:

```json
[
  {
    "file_path": "path/to/file.md",
    "content": "Full content of the file",
    "embedding": [0.123, 0.456, ...]  // Vector representation
  },
  ...
]
```

### 3. Search API

The main search functionality is provided through a FastAPI application in `main.py`:

#### Endpoints:

1. **Health Check**: `GET /` - Simple health check endpoint
2. **Knowledge Base Update**: `GET /update-knowledge-base` - Updates the knowledge base from a GitHub repository
3. **Search**: `GET /search?query={query}&top_k={count}` - Main search endpoint

#### Search Process:

1. **Query Embedding**: When a search query is received, it's converted to an embedding using the same model
2. **Similarity Calculation**: Cosine similarity is calculated between the query embedding and all document embeddings
3. **Top-K Selection**: The most relevant documents are selected based on similarity scores
4. **Response Generation**: The relevant documents are used as context for generating a comprehensive answer using Google's generative model

### 4. Components

#### Main Components:

- **`main.py`**: FastAPI application that serves the search API
- **`updater.py`**: Handles updating the knowledge base from a GitHub repository
- **`generate_embeddings.py`**: Script for creating embeddings from Markdown files

#### Helper Scripts:

- **`count_embeddings.py`**: Counts the number of embeddings in the knowledge base
- **`regenerate_embeddings.py`**: Regenerates embeddings for existing files
- **`generate_local_embeddings.py`**: Generates embeddings from local files
- **`search_*.py`**: Various specialized search scripts for different use cases

## How Search Works

### 1. Query Processing

When a user submits a search query:

1. The query text is sent to Google's embedding model
2. An embedding vector is generated for the query

### 2. Similarity Matching

Using cosine similarity:

1. The system compares the query embedding with all document embeddings
2. Cosine similarity scores are calculated for each document
3. Documents are ranked by similarity score

### 3. Response Generation

For the top matching documents:

1. The content of the most relevant documents is extracted
2. This content is used as context for a generative AI model
3. The model generates a comprehensive answer based on the context
4. Both the generated answer and the source documents are returned

## Running the System

### Prerequisites

1. Python 3.8+
2. Required packages from `requirements.txt`
3. Google API key for Gemini models
4. GitHub Personal Access Token (for knowledge base updates)

### Starting the Server

```bash
python run.py
```

The server will start on `http://localhost:8000`

### Using the Search API

```bash
# Simple search
curl "http://localhost:8000/search?query=api%20запросы"

# Search with custom number of results
curl "http://localhost:8000/search?query=api%20запросы&top_k=10"
```

### Updating the Knowledge Base

To update the knowledge base from the configured GitHub repository:

```bash
curl "http://localhost:8000/update-knowledge-base"
```

## File Structure

```
.
├── python/                 # All Python code
│   ├── main.py            # Main FastAPI application
│   ├── updater.py         # Knowledge base updater
│   ├── generate_embeddings.py  # Embedding generation
│   ├── search_*.py        # Search utilities
│   └── *.py               # Other utility scripts
├── knowledge_base/        # Generated embeddings
│   └── embeddings.json    # Main knowledge base file
├── FF-BASE/               # Source documentation (if local)
├── run.py                 # Entry point script
├── requirements.txt       # Python dependencies
└── PROCESS.md             # This file
```

## Dependencies

The system relies on several key technologies:

- **FastAPI**: Web framework for the API
- **Google Generative AI**: For embedding generation and response generation
- **scikit-learn**: For cosine similarity calculations
- **NumPy**: For numerical operations
- **aiohttp**: For asynchronous HTTP requests (knowledge base updates)