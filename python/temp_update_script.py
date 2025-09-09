import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np
import time

# Загрузка переменных окружения из .env файла
load_dotenv()

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

    all_md_files = []

    def fetch_tree_recursive(tree_url):
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(tree_url, headers=headers)
        
        if response.status_code == 200:
            tree_data = response.json()
            # Check for truncation
            if tree_data.get("truncated", False):
                print(f"Warning: GitHub API response for {tree_url} was truncated. This might indicate a very large directory.")
                # For now, we'll proceed with the partial tree. A more robust solution would involve fetching sub-trees individually.

            for item in tree_data["tree"]:
                if item["type"] == "blob" and item["path"].endswith(".md"):
                    all_md_files.append({"path": item["path"], "sha": item["sha"]})
                elif item["type"] == "tree":
                    # Recursively fetch sub-tree
                    fetch_tree_recursive(item["url"])
        else:
            print(f"Error fetching repository tree from {tree_url}: {response.status_code}")
            print(f"Response content: {response.text}")

    # Start fetching from the main branch's root tree
    initial_tree_url = f"https://api.github.com/repos/{GITHUB_NOTES_REPO_OWNER}/{GITHUB_NOTES_REPO_NAME}/git/trees/main"
    fetch_tree_recursive(initial_tree_url)
    
    print(f"Total Markdown files found: {len(all_md_files)}")
    return all_md_files

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

def update_knowledge_base_script():
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

if __name__ == "__main__":
    print("Running knowledge base update script...")
    result = update_knowledge_base_script()
    print(json.dumps(result, indent=2, ensure_ascii=False))
