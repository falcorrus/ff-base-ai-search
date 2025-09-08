import os
import json
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

# Загрузка переменных окружения из .env файла
load_dotenv()

app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Получение токенов и параметров из переменных окружения
GITHUB_TOKEN = os.getenv("GITHUB_PAT")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "falcorrus")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "ff-base")
GITHUB_NOTES_REPO_OWNER = os.getenv("GITHUB_NOTES_REPO_OWNER", "falcorrus")
GITHUB_NOTES_REPO_NAME = os.getenv("GITHUB_NOTES_REPO_NAME", "ff-base")

# Настройка Google Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    embedding_model = "models/embedding-001"
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("Warning: GEMINI_API_KEY not found. Gemini features will be disabled.")

# Путь к файлу для хранения эмбеддингов
EMBEDDINGS_FILE = "knowledge_base/embeddings.json"
LOG_FILE = "knowledge_base/search_log.json"

def get_github_files():
    """Получение списка файлов из GitHub репозитория с заметками"""
    print(f"Attempting to access notes repository: {GITHUB_NOTES_REPO_OWNER}/{GITHUB_NOTES_REPO_NAME}")
    
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found")
        return []
    
    url = f"https://api.github.com/repos/{GITHUB_NOTES_REPO_OWNER}/{GITHUB_NOTES_REPO_NAME}/git/trees/main?recursive=1"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    print(f"GitHub API response status: {response.status_code}")
    
    if response.status_code == 200:
        tree = response.json()["tree"]
        print(f"Total files in repository: {len(tree)}")
        # Фильтрация только Markdown файлов
        md_files = [item for item in tree if item["path"].endswith(".md")]
        print(f"Markdown files found: {len(md_files)}")
        return md_files
    else:
        print(f"Error fetching repository tree: {response.status_code}")
        print(f"Response content: {response.text}")
        return []

def get_file_content(file_sha):
    """Получение содержимого файла по его SHA из репозитория заметок"""
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found")
        return ""
    
    url = f"https://api.github.com/repos/{GITHUB_NOTES_REPO_OWNER}/{GITHUB_NOTES_REPO_NAME}/git/blobs/{file_sha}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        import base64
        content = response.json()["content"]
        # Декодирование base64 контента
        decoded_content = base64.b64decode(content).decode("utf-8")
        return decoded_content
    else:
        print(f"Error fetching file content: {response.status_code}")
        return ""

def generate_embedding(text):
    """Генерация эмбеддинга для текста с помощью Google Gemini"""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found")
        return None
    
    try:
        result = genai.embed_content(
            model=embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def save_embeddings(embeddings_data):
    """Сохранение эмбеддингов в JSON файл"""
    # Создание директории, если она не существует
    os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
    
    with open(EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

def load_embeddings():
    """Загрузка эмбеддингов из JSON файла"""
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def log_request(query, timestamp):
    """Логирование запросов в JSON файл"""
    # Создание директории, если она не существует
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    log_entry = {
        "timestamp": timestamp,
        "query": query
    }
    
    # Создание файла логов, если он не существует
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    
    # Чтение существующих записей
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
    
    # Добавление новой записи
    logs.append(log_entry)
    
    # Сохранение обновленных записей
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

@app.get("/")
async def read_root():
    return {"message": "Backend is running!"}

@app.get("/notes-count")
async def get_notes_count():
    """Возвращает количество загруженных заметок в базе знаний"""
    embeddings_data = load_embeddings()
    return {"count": len(embeddings_data)}

@app.get("/update-knowledge-base")
async def update_knowledge_base():
    """Обновление базы знаний из GitHub репозитория"""
    try:
        # Получение списка файлов из репозитория
        files = get_github_files()
        if not files:
            return {"message": "No files found or error occurred"}
        
        embeddings_data = []
        
        # Обработка каждого Markdown файла
        for file_info in files:
            file_path = file_info["path"]
            file_sha = file_info["sha"]
            
            # Получение содержимого файла
            content = get_file_content(file_sha)
            if content:
                # Генерация эмбеддинга для содержимого файла
                embedding = generate_embedding(content)
                if embedding:
                    # Сохранение данных об эмбеддинге
                    embeddings_data.append({
                        "file_path": file_path,
                        "content": content,
                        "embedding": embedding
                    })
        
        # Сохранение эмбеддингов в файл
        save_embeddings(embeddings_data)
        
        return {
            "message": f"Knowledge base updated successfully with {len(embeddings_data)} files",
            "files_processed": len(embeddings_data)
        }
    except Exception as e:
        return {"error": f"Failed to update knowledge base: {str(e)}"}

@app.get("/search")
async def search_notes(query: str):
    """Поиск релевантных заметок на основе запроса пользователя"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Логирование запроса
    log_request(query, timestamp)
    
    try:
        # Загрузка эмбеддингов
        embeddings_data = load_embeddings()
        print(f"DEBUG: Loaded embeddings_data length: {len(embeddings_data)}")
        if not embeddings_data:
            return {"query": query, "results": [], "message": "Knowledge base is empty. Please update it first."}
        
        # Check if embeddings_data contains actual embeddings
        # This handles cases where embeddings_data might be loaded but empty of actual embeddings
        if not any("embedding" in item and item["embedding"] is not None for item in embeddings_data):
            print("DEBUG: No valid embeddings found in embeddings_data.")
            return {"query": query, "results": [], "message": "No valid embeddings found in the knowledge base. Please update it first."}

        # Генерация эмбеддинга для запроса
        query_embedding = generate_embedding(query)
        print(f"DEBUG: query_embedding is None: {query_embedding is None}")
        if not query_embedding:
            return {"query": query, "results": [], "message": "Failed to generate embedding for the query."}
        
        # Поиск наиболее релевантных документов
        doc_embeddings = np.array([item["embedding"] for item in embeddings_data if "embedding" in item and item["embedding"] is not None])
        print(f"DEBUG: doc_embeddings shape: {doc_embeddings.shape}")
        
        # Ensure doc_embeddings is not empty after filtering
        if doc_embeddings.size == 0:
            print("DEBUG: doc_embeddings is empty after filtering.")
            return {"query": query, "results": [], "message": "No valid document embeddings to compare with. Please update the knowledge base."}

        query_emb = np.array(query_embedding).reshape(1, -1)
        print(f"DEBUG: query_emb shape: {query_emb.shape}")
        
        similarities = cosine_similarity(query_emb, doc_embeddings)[0]
        print(f"DEBUG: similarities shape: {similarities.shape}")
        
        # Получение индексов N наиболее релевантных документов
        top_n = 5
        # Ensure top_n does not exceed the number of available documents
        num_available_docs = len(embeddings_data)
        actual_top_n = min(top_n, num_available_docs)

        if actual_top_n == 0: # No documents to search
            print("DEBUG: actual_top_n is 0.")
            return {"query": query, "results": [], "message": "No documents available for search."} # This line is redundant due to the previous check, but harmless

        top_indices = similarities.argsort()[-actual_top_n:][::-1]
        print(f"DEBUG: top_indices: {top_indices}")
        
        results = []
        for idx in top_indices:
            file_path = embeddings_data[idx]["file_path"]
            similarity = similarities[idx]
            
            # Извлечение названия заметки из пути файла
            title = os.path.splitext(os.path.basename(file_path))[0]
            
            # Формирование GitHub URL для файла
            github_url = f"https://github.com/{GITHUB_NOTES_REPO_OWNER}/{GITHUB_NOTES_REPO_NAME}/blob/main/{file_path}"
            
            results.append({
                "title": title,
                "url": github_url,
                "similarity": float(similarity)
            })
        
        return {
            "query": query,
            "results": results,
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"DEBUG: Exception caught: {e}")
        return {"error": f"Search failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}
