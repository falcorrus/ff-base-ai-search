import os
import json
import logging
from typing import List, Dict, Optional

import numpy as np
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity

import google.generativeai as genai
from updater_enhanced import KnowledgeBaseUpdater

# --- Configuration ---
load_dotenv()

# General
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")
genai.configure(api_key=GEMINI_API_KEY)
EMBEDDING_MODEL = "models/embedding-001"
GENERATIVE_MODEL = "gemini-1.5-flash"

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_PAT")
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "falcorrus")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "ff-base")

# Data
EMBEDDINGS_FILE = "knowledge_base/embeddings.json"

# --- Logging ---
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# --- FastAPI App ---
app = FastAPI(
    title="ff-base-ai-search",
    description="AI-powered search for your personal knowledge base.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Knowledge Base ---
knowledge_base: List[Dict] = []

def load_knowledge_base():
    """Load the knowledge base from the embeddings file."""
    global knowledge_base
    if os.path.exists(EMBEDDINGS_FILE):
        try:
            with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                knowledge_base = json.load(f)
            logger.info(f"Knowledge base loaded with {len(knowledge_base)} documents.")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            knowledge_base = []
    else:
        logger.warning("Embeddings file not found. Knowledge base is empty.")
        knowledge_base = []

# --- Helper Functions ---

def get_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding for a given text."""
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result["embedding"]
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None


def find_most_relevant(query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """Find the most relevant documents in the knowledge base."""
    if not knowledge_base:
        return []

    embeddings = np.array([item["embedding"] for item in knowledge_base])
    query_embedding = np.array(query_embedding).reshape(1, -1)

    similarities = cosine_similarity(query_embedding, embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]
    
    # Include similarity scores in the returned documents
    results = []
    for i in top_indices:
        doc = knowledge_base[i].copy()  # Make a copy to avoid modifying the original
        doc["similarity"] = float(similarities[i])  # Add similarity score
        results.append(doc)
    
    return results

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    """Load the knowledge base on startup."""
    load_knowledge_base()

@app.get("/", summary="Health Check")
def health_check() -> Dict[str, str]:
    """Check if the server is running."""
    return {"status": "ok"}

@app.get("/update-knowledge-base", summary="Update Knowledge Base")
async def update_knowledge_base_endpoint() -> Dict:
    """Update the knowledge base from the GitHub repository."""
    if not GITHUB_TOKEN:
        raise HTTPException(
            status_code=500, 
            detail="Missing GITHUB_PAT environment variable."
        )

    updater = KnowledgeBaseUpdater(
        github_token=GITHUB_TOKEN,
        repo_owner=GITHUB_REPO_OWNER,
        repo_name=GITHUB_REPO_NAME,
        embeddings_file=EMBEDDINGS_FILE,
        gemini_api_key=GEMINI_API_KEY,
    )
    
    result = await updater.update_knowledge_base()
    load_knowledge_base()  # Reload the knowledge base after update
    return result

@app.get("/search", summary="Search Knowledge Base")
def search(
    query: str = Query(..., description="The search query."),
    top_k: int = Query(5, description="The number of results to return.")
) -> Dict:
    """Search the knowledge base and return the most relevant documents."""
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    query_embedding = get_embedding(query)
    if not query_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate query embedding.")

    relevant_docs = find_most_relevant(query_embedding, top_k=top_k)

    # Generate a comprehensive answer using the generative model
    try:
        if not relevant_docs:
            return {
                "answer": "Я не нашел релевантных документов для вашего запроса.",
                "relevant_documents": [],
            }
            
        context = "\n".join([doc["content"] for doc in relevant_docs])
        prompt = f"Based on the following context, answer the query: '{query}'\n\nContext:\n{context}"

        model = genai.GenerativeModel(GENERATIVE_MODEL)
        response = model.generate_content(prompt)

        return {
            "answer": response.text,
            "relevant_documents": relevant_docs,
        }
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        # Return relevant documents even if answer generation fails
        return {
            "answer": "Произошла ошибка при генерации ответа.",
            "relevant_documents": relevant_docs,
        }


@app.get("/notes-count", summary="Get Notes Count")
def get_notes_count() -> Dict[str, int]:
    """Get the total number of notes in the knowledge base."""
    return {"count": len(knowledge_base)}

# --- Main Execution ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
