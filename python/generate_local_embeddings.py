import os
import json
import glob
from dotenv import load_dotenv
import google.generativeai as genai

# Загрузка переменных окружения из .env файла
# Load from root .env file first
env_file = Path("../.env")
if env_file.exists():
    load_dotenv(env_file)
    print("Environment variables loaded from root .env")
else:
    # Fallback to backend/.env
    backend_env_file = Path("../backend/.env")
    if backend_env_file.exists():
        load_dotenv(backend_env_file)
        print("Environment variables loaded from backend/.env")

# Получение токенов и параметров из переменных окружения
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Настройка Google Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    embedding_model = "models/embedding-001"
else:
    print("Error: GEMINI_API_KEY not found")
    exit(1)

# Путь к файлу для хранения эмбеддингов
EMBEDDINGS_FILE = "knowledge_base/embeddings.json"

def get_local_files(root_dir):
    """Получение списка всех .md файлов из локальной директории"""
    print(f"Searching for .md files in directory: {root_dir}")
    
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        # Пропускаем скрытые директории
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, root_dir)
                md_files.append({
                    "path": relative_path,
                    "full_path": full_path
                })
    
    print(f"Found {len(md_files)} .md files")
    return md_files

def get_file_content(file_path):
    """Получение содержимого файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def generate_embedding(text):
    """Генерация эмбеддинга для текста с помощью Google Gemini"""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found")
        return None
    
    try:
        # Ограничиваем размер текста для API
        if len(text) > 10000:
            text = text[:10000]
            
        result = genai.embed_content(
            model=embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def create_embeddings_for_local_files(source_dir, output_file):
    """Создание эмбеддингов для всех .md файлов в локальной директории"""
    # Получение списка файлов
    files = get_local_files(source_dir)
    if not files:
        print("No .md files found")
        return
    
    embeddings_data = []
    
    # Обработка каждого файла
    for i, file_info in enumerate(files):
        file_path = file_info["path"]
        full_path = file_info["full_path"]
        
        print(f"Processing file {i+1}/{len(files)}: {file_path}")
        
        # Получение содержимого файла
        content = get_file_content(full_path)
        if not content:
            continue
        
        # Генерация эмбеддинга для содержимого файла
        embedding = generate_embedding(content)
        if embedding:
            # Сохранение данных об эмбеддинге
            embeddings_data.append({
                "file_path": file_path,
                "content": content,
                "embedding": embedding
            })
        else:
            print(f"Failed to generate embedding for {file_path}")
    
    # Сохранение эмбеддингов в файл
    print(f"Saving {len(embeddings_data)} embeddings to {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
    
    print("Embeddings saved successfully!")
    return len(embeddings_data)

if __name__ == "__main__":
    source_directory = os.getenv("FF_BASE_DIR", "/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE")
    output_file = "knowledge_base/embeddings.json"
    
    print("Starting embeddings generation for local files...")
    result = create_embeddings_for_local_files(source_directory, output_file)
    print(f"Process completed. Generated embeddings for {result} files.")