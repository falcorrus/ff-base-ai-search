#!/usr/bin/env python3
import os
import sys
import json
import requests
import time

# Add the python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def get_all_md_files_from_github():
    """Получение всех .md файлов из репозитория через Git Trees API"""
    # Получаем токен из переменных окружения
    token = os.getenv('GITHUB_PAT')
    if not token:
        print("Токен GITHUB_PAT не найден в переменных окружения")
        return []
    
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # Получаем SHA главной ветки
        ref_url = 'https://api.github.com/repos/falcorrus/ff-base/git/ref/heads/main'
        response = requests.get(ref_url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка при получении ссылки: {response.status_code}")
            return []
        
        ref_data = response.json()
        commit_sha = ref_data['object']['sha']
        
        # Получаем SHA дерева
        commit_url = f'https://api.github.com/repos/falcorrus/ff-base/git/commits/{commit_sha}'
        response = requests.get(commit_url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка при получении коммита: {response.status_code}")
            return []
        
        commit_data = response.json()
        tree_sha = commit_data['tree']['sha']
        
        # Получаем все файлы рекурсивно
        tree_url = f'https://api.github.com/repos/falcorrus/ff-base/git/trees/{tree_sha}?recursive=1'
        response = requests.get(tree_url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка при получении дерева: {response.status_code}")
            return []
        
        tree_data = response.json()
        md_files = [item for item in tree_data.get('tree', []) if item['type'] == 'blob' and item['path'].endswith('.md')]
        return [item['path'] for item in md_files]
    
    except Exception as e:
        print(f"Ошибка при получении файлов из GitHub: {e}")
        return []

def get_processed_files():
    """Получение списка обработанных файлов из embeddings.json"""
    embeddings_file = "knowledge_base/embeddings.json"
    if not os.path.exists(embeddings_file):
        print("Файл embeddings.json не найден")
        return []
    
    try:
        with open(embeddings_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [item['file_path'] for item in data]
    except Exception as e:
        print(f"Ошибка при чтении embeddings.json: {e}")
        return []

def main():
    print("Сравнение файлов в репозитории и обработанных файлов...")
    
    # Получаем все .md файлы из репозитория
    all_files = get_all_md_files_from_github()
    print(f"Всего .md файлов в репозитории: {len(all_files)}")
    
    # Получаем список обработанных файлов
    processed_files = get_processed_files()
    print(f"Обработано файлов: {len(processed_files)}")
    
    # Находим непrocessed файлы
    unprocessed_files = set(all_files) - set(processed_files)
    print(f"Необработанных файлов: {len(unprocessed_files)}")
    
    if unprocessed_files:
        print("\nНеобработанные файлы:")
        for file_path in sorted(unprocessed_files)[:20]:  # Покажем первые 20
            print(f"  - {file_path}")
        if len(unprocessed_files) > 20:
            print(f"  ... и еще {len(unprocessed_files) - 20} файлов")
    
    # Проверим, есть ли файлы в embeddings, которых нет в репозитории
    extra_files = set(processed_files) - set(all_files)
    if extra_files:
        print(f"\nФайлы в embeddings, которых нет в репозитории: {len(extra_files)}")
        for file_path in sorted(extra_files):
            print(f"  - {file_path}")

if __name__ == "__main__":
    main()