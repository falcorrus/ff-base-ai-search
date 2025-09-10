#!/usr/bin/env python3
import os
import sys
import json
import requests
import base64
import hashlib
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Add the python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables
load_dotenv()

def get_github_file_content(file_path: str) -> Optional[str]:
    """Получение содержимого файла из GitHub"""
    token = os.getenv('GITHUB_PAT')
    if not token:
        print("Токен GITHUB_PAT не найден")
        return None
    
    headers = {'Authorization': f'Bearer {token}'}
    # URL-кодируем путь к файлу
    encoded_path = requests.utils.quote(file_path)
    url = f'https://api.github.com/repos/falcorrus/ff-base/contents/{encoded_path}'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            content = data['content']
            decoded_content = base64.b64decode(content).decode('utf-8')
            return decoded_content
        else:
            print(f"Ошибка при получении файла {file_path}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при получении файла {file_path}: {e}")
        return None

def split_large_text(text: str, max_chunk_size: int = 30000) -> List[str]:
    """Разбиение большого текста на части"""
    if len(text.encode('utf-8')) <= max_chunk_size:
        return [text]
    
    # Разбиваем текст на абзацы
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # Проверяем, поместится ли абзац в текущий чанк
        test_chunk = current_chunk + '\n\n' + paragraph if current_chunk else paragraph
        if len(test_chunk.encode('utf-8')) <= max_chunk_size:
            current_chunk = test_chunk
        else:
            # Если текущий чанк не пуст, сохраняем его
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                # Если абзац слишком большой, разбиваем его по предложениям
                sentences = paragraph.split('. ')
                sub_chunk = ""
                for sentence in sentences:
                    test_sub = sub_chunk + '. ' + sentence if sub_chunk else sentence
                    if len(test_sub.encode('utf-8')) <= max_chunk_size:
                        sub_chunk = test_sub
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        sub_chunk = sentence
                
                if sub_chunk:
                    current_chunk = sub_chunk
    
    # Добавляем последний чанк
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def generate_embedding_for_chunk(text: str) -> Optional[List[float]]:
    """Генерация embedding для части текста"""
    try:
        # Configure Gemini API
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if not gemini_api_key:
            print("GOOGLE_API_KEY не найден")
            return None
            
        genai.configure(api_key=gemini_api_key)
        embedding_model = "models/embedding-001"
        
        result = genai.embed_content(
            model=embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
    except Exception as e:
        print(f"Ошибка при генерации embedding: {e}")
        return None

def generate_embedding_for_large_text(text: str) -> Optional[List[float]]:
    """Генерация embedding для большого текста путем разбиения на части и усреднения"""
    chunks = split_large_text(text)
    
    if len(chunks) == 1:
        # Если текст помещается в один чанк, генерируем embedding напрямую
        return generate_embedding_for_chunk(chunks[0])
    
    # Для больших текстов генерируем embeddings для каждой части и усредняем их
    embeddings = []
    for i, chunk in enumerate(chunks):
        print(f"  Обработка части {i+1}/{len(chunks)} (размер: {len(chunk.encode('utf-8'))} байт)")
        embedding = generate_embedding_for_chunk(chunk)
        if embedding:
            embeddings.append(embedding)
        else:
            print(f"  Не удалось сгенерировать embedding для части {i+1}")
            return None
    
    # Усредняем все embeddings
    if embeddings:
        avg_embedding = []
        for i in range(len(embeddings[0])):
            avg_value = sum(embedding[i] for embedding in embeddings) / len(embeddings)
            avg_embedding.append(avg_value)
        return avg_embedding
    
    return None

def process_file(file_path: str) -> Optional[Dict]:
    """Обработка одного файла"""
    print(f"Обработка файла: {file_path}")
    
    # Получаем содержимое файла
    content = get_github_file_content(file_path)
    if not content:
        print(f"  Не удалось получить содержимое файла")
        return None
    
    # Проверяем размер файла
    content_size = len(content.encode('utf-8'))
    print(f"  Размер файла: {content_size} байт")
    
    # Генерируем embedding
    if content_size > 36000:
        print(f"  Файл слишком большой, разбиваем на части...")
        embedding = generate_embedding_for_large_text(content)
    else:
        embedding = generate_embedding_for_chunk(content)
    
    if not embedding:
        print(f"  Не удалось сгенерировать embedding")
        return None
    
    # Создаем хэш содержимого
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    
    return {
        "file_path": file_path,
        "content": content,
        "embedding": embedding,
        "file_hash": content_hash,
        "file_size": content_size,
        "updated_at": "2025-09-09T00:00:00"
    }

def load_existing_embeddings() -> List[Dict]:
    """Загрузка существующих embeddings"""
    embeddings_file = "knowledge_base/embeddings.json"
    if os.path.exists(embeddings_file):
        try:
            with open(embeddings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке существующих embeddings: {e}")
            return []
    return []

def save_embeddings(embeddings_data: List[Dict]) -> None:
    """Сохранение embeddings в файл"""
    embeddings_file = "knowledge_base/embeddings.json"
    os.makedirs(os.path.dirname(embeddings_file), exist_ok=True)
    
    try:
        with open(embeddings_file, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(embeddings_data)} embeddings")
    except Exception as e:
        print(f"Ошибка при сохранении embeddings: {e}")

def main():
    # Список файлов, которые нужно обработать
    files_to_process = [
        "..temp/image_Градиентная заливка4.txt.md",
        ".trash/Без названия 2.md",
        ".trash/Без названия.md",
        "Flutterflow/Политика обработки персональных данных (пример).md",
        "Базы данных (бекэнд)/Nhost.md",
        "Базы данных (бекэнд)/Supabase/Установка Supabase на свой сервер (Self-hosted).md",
        "Дизайн и пользовательский интерфейс/Принципы mui дизайна - хороший разбор.md"
    ]
    
    print(f"Начинаем обработку {len(files_to_process)} файлов...")
    
    # Загружаем существующие embeddings
    existing_embeddings = load_existing_embeddings()
    print(f"Загружено {len(existing_embeddings)} существующих embeddings")
    
    # Создаем словарь существующих embeddings по пути файла для быстрого поиска
    existing_files = {item["file_path"]: item for item in existing_embeddings}
    
    # Обрабатываем файлы
    new_embeddings = []
    processed_count = 0
    
    for file_path in files_to_process:
        # Проверяем, не обработан ли файл уже
        if file_path in existing_files:
            print(f"Файл {file_path} уже обработан, пропускаем")
            new_embeddings.append(existing_files[file_path])
            continue
        
        # Обрабатываем файл
        result = process_file(file_path)
        if result:
            new_embeddings.append(result)
            processed_count += 1
            print(f"  Успешно обработан")
        else:
            print(f"  Не удалось обработать")
    
    # Объединяем существующие и новые embeddings
    # Удаляем дубликаты, если есть
    all_file_paths = set()
    final_embeddings = []
    
    # Сначала добавляем новые embeddings
    for item in new_embeddings:
        if item["file_path"] not in all_file_paths:
            final_embeddings.append(item)
            all_file_paths.add(item["file_path"])
    
    # Затем добавляем существующие, которых нет в новых
    for item in existing_embeddings:
        if item["file_path"] not in all_file_paths:
            final_embeddings.append(item)
            all_file_paths.add(item["file_path"])
    
    # Сохраняем все embeddings
    save_embeddings(final_embeddings)
    
    print(f"\nОбработано файлов: {processed_count}")
    print(f"Всего embeddings в базе: {len(final_embeddings)}")

if __name__ == "__main__":
    main()