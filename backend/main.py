import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
from pathlib import Path
import hashlib
import base64

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Google Cloud Storage
from google.cloud import storage

import google.generativeai as genai

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

# Google Cloud Storage
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "ff-base-embeddings")
EMBEDDINGS_FILE_NAME = "embeddings.json"
SEARCH_LOG_FILE_NAME = "search_log.json"

# Local fallback
EMBEDDINGS_FILE = "../knowledge_base/embeddings.json"
SEARCH_LOG_FILE = "../knowledge_base/search_log.json"
FF_BASE_DIR = "../FF-BASE"

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
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Knowledge Base ---
knowledge_base: List[Dict] = []

def get_gcs_client():
    """Get Google Cloud Storage client."""
    try:
        # Log the GOOGLE_APPLICATION_CREDENTIALS environment variable
        logger.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
        client = storage.Client()
        logger.info("GCS client initialized successfully")
        return client
    except Exception as e:
        logger.warning(f"Failed to initialize GCS client: {e}")
        return None

def load_knowledge_base_from_gcs():
    """Load the knowledge base from Google Cloud Storage."""
    global knowledge_base
    try:
        client = get_gcs_client()
        if not client:
            return False
            
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(EMBEDDINGS_FILE_NAME)
        
        if blob.exists():
            # Download the file content
            content = blob.download_as_text()
            knowledge_base = json.loads(content)
            logger.info(f"Knowledge base loaded from GCS with {len(knowledge_base)} documents.")
            return True
        else:
            logger.warning("Embeddings file not found in GCS. Knowledge base is empty.")
            knowledge_base = []
            return False
    except Exception as e:
        logger.error(f"Error loading knowledge base from GCS: {e}")
        return False

def load_knowledge_base_from_local():
    """Load the knowledge base from local file."""
    global knowledge_base
    if os.path.exists(EMBEDDINGS_FILE):
        try:
            with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                knowledge_base = json.load(f)
            logger.info(f"Knowledge base loaded from local file with {len(knowledge_base)} documents.")
            return True
        except Exception as e:
            logger.error(f"Error loading knowledge base from local file: {e}")
            knowledge_base = []
            return False
    else:
        logger.warning("Local embeddings file not found. Knowledge base is empty.")
        knowledge_base = []
        return False

def load_knowledge_base():
    """Load the knowledge base from GCS if available, otherwise from local file."""
    # Try to load from GCS first
    if load_knowledge_base_from_gcs():
        return
    
    # Fallback to local file
    load_knowledge_base_from_local()

def save_knowledge_base_to_gcs(embeddings_data: List[Dict]):
    """Save the knowledge base to Google Cloud Storage."""
    try:
        client = get_gcs_client()
        if not client:
            return False
            
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(EMBEDDINGS_FILE_NAME)
        
        # Upload the file
        content = json.dumps(embeddings_data, ensure_ascii=False, indent=2)
        blob.upload_from_string(content, content_type="application/json")
        
        logger.info(f"Knowledge base saved to GCS with {len(embeddings_data)} documents.")
        return True
    except Exception as e:
        logger.error(f"Error saving knowledge base to GCS: {e}")
        return False

def save_knowledge_base_to_local(embeddings_data: List[Dict]):
    """Save the knowledge base to local file."""
    try:
        os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
        with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Knowledge base saved to local file with {len(embeddings_data)} documents.")
        return True
    except Exception as e:
        logger.error(f"Error saving knowledge base to local file: {e}")
        return False

def save_search_log_to_gcs(query: str, timestamp: str):
    """Save search query to log file in GCS."""
    try:
        client = get_gcs_client()
        if not client:
            return False
            
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(SEARCH_LOG_FILE_NAME)
        
        # Load existing logs
        logs = []
        if blob.exists():
            try:
                content = blob.download_as_text()
                logs = json.loads(content)
            except Exception as e:
                logger.error(f"Error loading search logs from GCS: {e}")
        
        # Add new entry
        log_entry = {
            "query": query,
            "timestamp": timestamp
        }
        logs.append(log_entry)
        
        # Save updated logs
        content = json.dumps(logs, ensure_ascii=False, indent=2)
        blob.upload_from_string(content, content_type="application/json")
        
        return True
    except Exception as e:
        logger.error(f"Error saving search log to GCS: {e}")
        return False

def save_search_log_to_local(query: str, timestamp: str):
    """Save search query to local log file."""
    log_entry = {
        "query": query,
        "timestamp": timestamp
    }
    
    # Load existing logs
    logs = []
    if os.path.exists(SEARCH_LOG_FILE):
        try:
            with open(SEARCH_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception as e:
            logger.error(f"Error loading search logs from local file: {e}")
    
    # Add new entry
    logs.append(log_entry)
    
    # Save updated logs
    try:
        os.makedirs(os.path.dirname(SEARCH_LOG_FILE), exist_ok=True)
        with open(SEARCH_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving search log to local file: {e}")

def save_search_log(query: str, timestamp: str):
    """Save search query to log file (GCS if available, otherwise local)."""
    # Try to save to GCS first
    if save_search_log_to_gcs(query, timestamp):
        return
    
    # Fallback to local file
    save_search_log_to_local(query, timestamp)

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
    
    # Return documents with their similarity scores
    results = []
    for i in top_indices:
        doc = knowledge_base[i].copy()
        doc["similarity"] = float(similarities[i])
        results.append(doc)
    
    return results

async def update_knowledge_base_from_local() -> Dict:
    """Update the knowledge base from local FF-BASE directory incrementally."""
    try:
        ff_base_path = Path(FF_BASE_DIR)
        if not ff_base_path.exists():
            return {"message": "FF-BASE directory not found", "files_processed": 0}

        # Get all .md files recursively
        md_files = list(ff_base_path.rglob("*.md"))
        logger.info(f"Found {len(md_files)} Markdown files in FF-BASE")
        
        # Load existing embeddings and metadata
        existing_embeddings = {}
        existing_metadata = {}
        
        # Try to load from GCS first
        client = get_gcs_client()
        if client:
            try:
                bucket = client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(EMBEDDINGS_FILE_NAME)
                if blob.exists():
                    content = blob.download_as_text()
                    existing_data = json.loads(content)
                    existing_embeddings = {item["file_path"]: item for item in existing_data}
                    
                # Load metadata if it exists
                metadata_blob = bucket.blob(EMBEDDINGS_FILE_NAME.replace(".json", "_metadata.json"))
                if metadata_blob.exists():
                    metadata_content = metadata_blob.download_as_text()
                    existing_metadata = json.loads(metadata_content)
            except Exception as e:
                logger.error(f"Error loading existing embeddings from GCS: {e}")
        else:
            # Fallback to local files
            if os.path.exists(EMBEDDINGS_FILE):
                try:
                    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)
                        existing_embeddings = {item["file_path"]: item for item in existing_data}
                except Exception as e:
                    logger.error(f"Error loading existing embeddings from local file: {e}")
            
            # Load metadata if it exists
            metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        existing_metadata = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading metadata from local file: {e}")
        
        # Process files incrementally
        embeddings_data = []
        processed_count = 0
        unchanged_count = 0
        
        for file_path in md_files:
            try:
                # Get relative path from FF-BASE directory
                relative_path = str(file_path.relative_to(ff_base_path))
                
                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Generate content hash
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                
                # Get file modification time
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                
                # Check if we already have an embedding for this file and if it's unchanged
                if relative_path in existing_embeddings and relative_path in existing_metadata:
                    metadata = existing_metadata[relative_path]
                    if (metadata.get("content_hash") == content_hash and 
                        metadata.get("last_modified") == mod_time):
                        # File unchanged, reuse existing embedding
                        embeddings_data.append(existing_embeddings[relative_path])
                        unchanged_count += 1
                        continue
                
                # File is new or changed, generate new embedding
                logger.info(f"Generating embedding for: {relative_path}")
                result = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=content,
                    task_type="retrieval_document"
                )
                embedding = result["embedding"]
                
                embeddings_data.append({
                    "file_path": relative_path,
                    "content": content,
                    "embedding": embedding
                })
                
                # Update metadata
                existing_metadata[relative_path] = {
                    "content_hash": content_hash,
                    "last_modified": mod_time,
                    "processed_at": datetime.now().isoformat()
                }
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                continue
        
        # Save embeddings
        if client:
            # Save to GCS
            try:
                bucket = client.bucket(GCS_BUCKET_NAME)
                
                # Save embeddings
                blob = bucket.blob(EMBEDDINGS_FILE_NAME)
                content = json.dumps(embeddings_data, ensure_ascii=False, indent=2)
                blob.upload_from_string(content, content_type="application/json")
                
                # Save metadata
                metadata_blob = bucket.blob(EMBEDDINGS_FILE_NAME.replace(".json", "_metadata.json"))
                metadata_content = json.dumps(existing_metadata, ensure_ascii=False, indent=2)
                metadata_blob.upload_from_string(metadata_content, content_type="application/json")
                
                logger.info(f"Knowledge base saved to GCS")
            except Exception as e:
                logger.error(f"Error saving to GCS: {e}")
                # Fallback to local save
                save_knowledge_base_to_local(embeddings_data)
                # Save metadata locally
                metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(existing_metadata, f, ensure_ascii=False, indent=2)
        else:
            # Save to local file
            save_knowledge_base_to_local(embeddings_data)
            # Save metadata locally
            metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(existing_metadata, f, ensure_ascii=False, indent=2)
        
        # Reload knowledge base
        load_knowledge_base()
        
        return {
            "message": f"Knowledge base updated successfully from local FF-BASE ({processed_count} files processed, {unchanged_count} files unchanged)",
            "files_processed": processed_count,
            "files_unchanged": unchanged_count
        }
        
    except Exception as e:
        logger.error(f"Error updating knowledge base: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update knowledge base: {str(e)}")


async def update_knowledge_base_from_github() -> Dict:
    """Update the knowledge base from the falcorrus/ff-base GitHub repository incrementally."""
    try:
        if not GITHUB_TOKEN:
            raise ValueError("GITHUB_PAT environment variable is not set.")
        
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Get the main branch SHA
        ref_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/git/ref/heads/main"
        ref_response = requests.get(ref_url, headers=headers)
        if ref_response.status_code != 200:
            raise Exception(f"Failed to get main branch ref: {ref_response.status_code}")
        
        commit_sha = ref_response.json()["object"]["sha"]
        
        # Get the tree SHA
        commit_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/git/commits/{commit_sha}"
        commit_response = requests.get(commit_url, headers=headers)
        if commit_response.status_code != 200:
            raise Exception(f"Failed to get commit details: {commit_response.status_code}")
        
        tree_sha = commit_response.json()["tree"]["sha"]
        
        # Get all files in the repository
        tree_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/git/trees/{tree_sha}?recursive=1"
        tree_response = requests.get(tree_url, headers=headers)
        if tree_response.status_code != 200:
            raise Exception(f"Failed to get tree: {tree_response.status_code}")
        
        tree_data = tree_response.json()
        md_files = [item for item in tree_data["tree"] if item["type"] == "blob" and item["path"].endswith(".md")]
        
        logger.info(f"Found {len(md_files)} Markdown files in GitHub repository")
        
        # Load existing embeddings and metadata
        existing_embeddings = {}
        existing_metadata = {}
        
        # Try to load from GCS first
        client = get_gcs_client()
        if client:
            try:
                bucket = client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(EMBEDDINGS_FILE_NAME)
                if blob.exists():
                    content = blob.download_as_text()
                    existing_data = json.loads(content)
                    existing_embeddings = {item["file_path"]: item for item in existing_data}
                    
                # Load metadata if it exists
                metadata_blob = bucket.blob(EMBEDDINGS_FILE_NAME.replace(".json", "_metadata.json"))
                if metadata_blob.exists():
                    metadata_content = metadata_blob.download_as_text()
                    existing_metadata = json.loads(metadata_content)
            except Exception as e:
                logger.error(f"Error loading existing embeddings from GCS: {e}")
        else:
            # Fallback to local files
            if os.path.exists(EMBEDDINGS_FILE):
                try:
                    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
                        existing_data = json.load(f)
                        existing_embeddings = {item["file_path"]: item for item in existing_data}
                except Exception as e:
                    logger.error(f"Error loading existing embeddings from local file: {e}")
            
            # Load metadata if it exists
            metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        existing_metadata = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading metadata from local file: {e}")
        
        # Process files incrementally
        embeddings_data = []
        processed_count = 0
        unchanged_count = 0
        
        for file_item in md_files:
            try:
                file_path = file_item["path"]
                
                # Get file content
                blob_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/git/blobs/{file_item['sha']}"
                blob_response = requests.get(blob_url, headers=headers)
                if blob_response.status_code != 200:
                    logger.error(f"Failed to get blob for {file_path}: {blob_response.status_code}")
                    continue
                
                blob_data = blob_response.json()
                content = base64.b64decode(blob_data["content"]).decode("utf-8")
                
                # Generate content hash
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                
                # Use the blob SHA as a proxy for modification time
                file_sha = file_item["sha"]
                
                # Check if we already have an embedding for this file and if it's unchanged
                if file_path in existing_embeddings and file_path in existing_metadata:
                    metadata = existing_metadata[file_path]
                    if (metadata.get("content_hash") == content_hash and 
                        metadata.get("file_sha") == file_sha):
                        # File unchanged, reuse existing embedding
                        embeddings_data.append(existing_embeddings[file_path])
                        unchanged_count += 1
                        continue
                
                # File is new or changed, generate new embedding
                logger.info(f"Generating embedding for: {file_path}")
                result = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=content,
                    task_type="retrieval_document"
                )
                embedding = result["embedding"]
                
                embeddings_data.append({
                    "file_path": file_path,
                    "content": content,
                    "embedding": embedding
                })
                
                # Update metadata
                existing_metadata[file_path] = {
                    "content_hash": content_hash,
                    "file_sha": file_sha,
                    "processed_at": datetime.now().isoformat()
                }
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing file {file_item['path']}: {e}")
                continue
        
        # Save embeddings
        if client:
            # Save to GCS
            try:
                bucket = client.bucket(GCS_BUCKET_NAME)
                
                # Save embeddings
                blob = bucket.blob(EMBEDDINGS_FILE_NAME)
                content = json.dumps(embeddings_data, ensure_ascii=False, indent=2)
                blob.upload_from_string(content, content_type="application/json")
                
                # Save metadata
                metadata_blob = bucket.blob(EMBEDDINGS_FILE_NAME.replace(".json", "_metadata.json"))
                metadata_content = json.dumps(existing_metadata, ensure_ascii=False, indent=2)
                metadata_blob.upload_from_string(metadata_content, content_type="application/json")
                
                logger.info(f"Knowledge base saved to GCS")
            except Exception as e:
                logger.error(f"Error saving to GCS: {e}")
                # Fallback to local save
                save_knowledge_base_to_local(embeddings_data)
                # Save metadata locally
                metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(existing_metadata, f, ensure_ascii=False, indent=2)
        else:
            # Save to local file
            save_knowledge_base_to_local(embeddings_data)
            # Save metadata locally
            metadata_file = EMBEDDINGS_FILE.replace(".json", "_metadata.json")
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(existing_metadata, f, ensure_ascii=False, indent=2)
        
        # Reload knowledge base
        load_knowledge_base()
        
        return {
            "message": f"Knowledge base updated successfully from GitHub ({processed_count} files processed, {unchanged_count} files unchanged)",
            "files_processed": processed_count,
            "files_unchanged": unchanged_count
        }
        
    except Exception as e:
        logger.error(f"Error updating knowledge base from GitHub: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update knowledge base from GitHub: {str(e)}")

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    """Load the knowledge base on startup."""
    load_knowledge_base()

@app.get("/", summary="Health Check")
def health_check() -> Dict[str, str]:
    """Check if the server is running."""
    return {"status": "ok", "message": "Intelligent Search API is running!"}

@app.get("/update-knowledge-base", summary="Update Knowledge Base")
async def update_knowledge_base_endpoint() -> Dict:
    """Update the knowledge base from the GitHub repository."""
    if not GITHUB_TOKEN:
        raise HTTPException(
            status_code=500, 
            detail="Missing GITHUB_PAT environment variable."
        )

    result = await update_knowledge_base_from_github()
    return result


@app.get("/update-knowledge-base-local", summary="Update Knowledge Base from Local")
async def update_knowledge_base_local_endpoint() -> Dict:
    """Update the knowledge base from the local FF-BASE directory."""
    result = await update_knowledge_base_from_local()
    return result

@app.get("/search", summary="Search Knowledge Base")
def search(
    query: str = Query(..., description="The search query."),
    top_k: int = Query(5, description="The number of results to return.")
) -> Dict:
    """Search the knowledge base and return the most relevant documents."""
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    # Ensure top_k is an integer
    top_k_value = int(top_k)
    
    # Log the search query
    timestamp = datetime.now().isoformat()
    save_search_log(query, timestamp)
    
    query_embedding = get_embedding(query)
    if not query_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate query embedding.")

    relevant_docs = find_most_relevant(query_embedding, top_k=top_k_value)

    # Generate a comprehensive answer using the generative model
    try:
        # Format context from relevant documents
        context_parts = []
        for doc in relevant_docs:
            context_parts.append(f"File: {doc['file_path']}\nContent:\n{doc['content']}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Create prompt for answer generation
        prompt = f"""Вы — AI-ассистент, который отвечает на вопросы на основе предоставленного контекста из личных заметок.
Используйте следующие документы, чтобы ответить на вопрос в конце.
Если вы не знаете ответа, просто скажите, что не знаете, не пытайтесь придумать ответ.
ВАЖНО: Отвечайте ТОЛЬКО на русском языке. Даже если вопрос на другом языке, переведите его и ответьте на русском.

Контекст:
{context}

Вопрос: {query}

Ответ (на русском языке):"""

        model = genai.GenerativeModel(GENERATIVE_MODEL)
        response = model.generate_content(prompt)

        return {
            "answer": response.text,
            "relevant_documents": [
                {
                    "file_path": doc["file_path"],
                    "content": doc["content"],
                    "similarity": doc.get("similarity", 0)
                } 
                for doc in relevant_docs
            ],
        }
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate answer.")

@app.get("/notes-count", summary="Get Notes Count")
def get_notes_count() -> Dict[str, int]:
    """Get the total number of notes in the knowledge base."""
    return {"count": len(knowledge_base)}

# --- Main Execution ---
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)