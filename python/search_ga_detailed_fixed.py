import json
import os
import re
from typing import List, Dict

def search_google_analytics_detailed(query: str = "google analytics") -> List[Dict]:
    """Поиск документов, связанных с Google Analytics в контексте FlutterFlow"""
    
    # Путь к файлу с эмбеддингами
    embeddings_file = "knowledge_base/embeddings.json"
    
    # Проверяем, существует ли файл
    if not os.path.exists(embeddings_file):
        print(f"Файл {embeddings_file} не найден")
        return []
    
    # Загружаем данные
    with open(embeddings_file, "r", encoding="utf-8") as f:
        embeddings_data = json.load(f)
    
    print(f"Загружено {len(embeddings_data)} документов из базы знаний")
    
    # Результаты поиска
    results = []
    
    # Ищем документ с названием Google Analytics.md
    for item in embeddings_data:
        file_path = item.get("file_path", "")
        
        # Если это документ Google Analytics.md
        if "Google Analytics.md" in file_path:
            results.append({
                "file_path": file_path,
                "content": item.get("content", ""),
                "relevance": 100  # Максимальная релевантность
            })
            break
    
    # Также ищем документы, содержащие упоминания Google Analytics
    ga_keywords = [
        "google analytics", "flutterflow.*analytics", "analytics.*flutterflow",
        "gtag", "ga4", "universal analytics", "firebase.*analytics"
    ]
    
    for item in embeddings_data:
        content = item.get("content", "").lower()
        file_path = item.get("file_path", "")
        
        # Пропускаем уже найденный документ
        if "Google Analytics.md" in file_path:
            continue
        
        # Проверяем, содержит ли документ ключевые слова
        relevance = 0
        for keyword in ga_keywords:
            if re.search(keyword, content):
                relevance += 10
        
        # Если найдены ключевые слова, добавляем в результаты
        if relevance > 0:
            results.append({
                "file_path": file_path,
                "content": item.get("content", ""),
                "relevance": relevance
            })
    
    # Сортируем результаты по релевантности
    results.sort(key=lambda x: x['relevance'], reverse=True)
    
    print(f"Найдено {len(results)} документов, связанных с Google Analytics")
    return results

def extract_ga_info(content: str) -> Dict:
    """Извлекает ключевую информацию о Google Analytics из содержимого"""
    info = {}
    
    # Извлекаем основные разделы
    sections = re.findall(r"# (.+)", content)
    info["sections"] = sections[:5]  # Первые 5 разделов
    
    # Извлекаем автоматически логируемые события
    auto_events = re.findall(r"- \\*\\*(.+?)\\*\\*: (.+?)(?=\\n-|\\n#|\\Z)", content, re.DOTALL)
    info["auto_events"] = auto_events[:5]  # Первые 5 событий
    
    # Извлекаем ссылки
    links = re.findall(r"$$[^$$]+$$[^)]+?", content)
    info["links"] = links[:10]  # Первые 10 ссылок
    
    return info

def main():
    """Основная функция для выполнения поиска"""
    query = "google analytics"
    print(f"Поиск документов по запросу: {query}")
    
    results = search_google_analytics_detailed(query)
    
    if not results:
        print("Документы, связанные с Google Analytics, не найдены")
        return
    
    # Выводим результаты
    print("\nРезультаты поиска:")
    print("=" * 80)
    
    for i, result in enumerate(results[:5], 1):  # Показываем первые 5 результатов
        print(f"\n{i}. Файл: {result['file_path']}")
        print(f"   Релевантность: {result['relevance']}")
        
        # Извлекаем ключевую информацию
        info = extract_ga_info(result['content'])
        
        if info.get("sections"):
            print(f"   Разделы документа:")
            for section in info["sections"]:
                print(f"     - {section}")
        
        if info.get("auto_events"):
            print(f"   Автоматически логируемые события:")
            for event, description in info["auto_events"]:
                print(f"     - {event}: {description[:100]}...")
        
        if info.get("links"):
            print(f"   Полезные ссылки:")
            for link in info["links"][:3]:  # Показываем первые 3 ссылки
                print(f"     - {link}")
        
        print("-" * 80)

if __name__ == "__main__":
    main()