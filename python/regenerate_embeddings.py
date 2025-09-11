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

# Получение API ключа из переменных окружения
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Настройка Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

def get_all_md_files(root_dir):
    """Получение всех .md файлов из директории и поддиректорий"""
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        # Пропускаем скрытые директории
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                md_files.append(full_path)
    return md_files

def read_file_content(file_path):
    """Чтение содержимого файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def generate_embedding(text):
    """Генерация эмбеддинга для текста"""
    try:
        # Ограничиваем размер текста для API
        if len(text) > 10000:
            text = text[:10000]
        
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def regenerate_embeddings(source_dir, output_file):
    """Пересоздание эмбеддингов для всех .md файлов в директории"""
    print(f"Searching for .md files in {source_dir}")
    
    # Получаем все .md файлы
    md_files = get_all_md_files(source_dir)
    print(f"Found {len(md_files)} .md files")
    
    embeddings_data = []
    
    # Обработка каждого файла
    for i, file_path in enumerate(md_files):
        print(f"Processing file {i+1}/{len(md_files)}: {os.path.basename(file_path)}")
        
        # Читаем содержимое файла
        content = read_file_content(file_path)
        if not content:
            continue
            
        # Генерируем эмбеддинг
        embedding = generate_embedding(content)
        if embedding is None:
            continue
            
        # Относительный путь от корня директории, указанной в переменной окружения `FF_BASE_DIR`
        relative_path = os.path.relpath(file_path, source_dir)
        
        # Добавляем в данные
        embeddings_data.append({
            "file_path": relative_path,
            "content": content,
            "embedding": embedding
        })
        
        # Показываем прогресс каждые 10 файлов
        if (i + 1) % 10 == 0:
            print(f"Processed {i+1} files...")
    
    # Сохраняем в файл
    print(f"Saving {len(embeddings_data)} embeddings to {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
    
    print("Done!")
    return len(embeddings_data)

if __name__ == "__main__":
    source_directory = os.getenv("FF_BASE_DIR", "/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE")
    output_file = "knowledge_base/embeddings.json"
    
    try:
        count = regenerate_embeddings(source_directory, output_file)
        print(f"Successfully regenerated embeddings for {count} files")
    except Exception as e:
        print(f"Error: {e}")