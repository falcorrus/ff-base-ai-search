import json

# Путь к файлу с эмбеддингами
filename = '/Users/eugene/MyProjects/ff-base-ai-search/knowledge_base/embeddings.json'

# Открываем файл и загружаем данные
with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Подсчитываем количество документов (элементов в списке)
num_documents = len(data)

print(f"Количество документов в векторной базе ({filename}): {num_documents}")