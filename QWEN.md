## Qwen Added Memories
- Для запуска проекта ff-base-ai-search:
1. Активировать виртуальное окружение: source backend/venv/bin/activate
2. Запустить сервер: cd backend && ./start.sh
   Или альтернативно: python python/run.py
3. Сервер будет доступен по адресу http://localhost:8000

## Project Overview

This project is a web application designed for intelligent search and comprehensive answer generation from personal Markdown notes stored in the local directory specified by the `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`). It leverages vector search and large language models (LLMs) to provide quick and accurate answers based on a user's knowledge base.

**Key Technologies:**

*   **Backend:** Python 3.9+, FastAPI, Google Gemini API, and Google Cloud Run for deployment.
*   **Frontend:** Vanilla JavaScript, deployed on Firebase Hosting.
*   **Data Storage:** Embeddings are stored in a local JSON file (`knowledge_base/embeddings.json`), containing vector representations for all 276 Markdown notes.
*   **Vector Search:** Semantic search using Google Gemini embeddings for finding relevant notes.
*   **Query Logging:** All search queries are logged to a JSON file (`knowledge_base/search_log.json`) with timestamps.

## Recent Recovery of Knowledge Base

The project's knowledge base has been recently restored with a complete set of embeddings for all 276 Markdown notes. The `knowledge_base/embeddings.json` file was regenerated using a custom script that processed all notes and generated corresponding vector representations. This ensures full functionality of the semantic search capabilities.

**Architecture Highlights:**

*   **Synchronization:** Reading Markdown notes from the local directory specified by the `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`).
*   **Embedding Generation:** Creation and storage of vector embeddings for each note using Google Gemini Embeddings API (`models/embedding-001`). Recently regenerated for all 276 notes.
*   **Search & Answer Generation:**
    *   User queries are transformed into embeddings via the Google Gemini Embeddings API.
    *   Relevant notes are identified through vector similarity search using cosine similarity.
    *   Markdown files for relevant notes are read from the local filesystem.
    *   A context is formed from these notes and sent to the Google Gemini LLM (`gemini-1.5-flash`) for comprehensive answer generation.
    *   The generated answer is returned to the user.
*   **Logging:** All requests are logged to a JSON file for monitoring and debugging.

## Building and Running

### Backend (FastAPI)

To run the FastAPI backend locally, you would typically use `uvicorn`.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided startup script:

```bash
# Navigate to the backend directory
cd backend

# Make the script executable (if not already)
chmod +x start.sh

# Run the backend server
./start.sh
```

Endpoints:

*   `GET /` - Health check endpoint
*   `GET /update-knowledge-base-local` - Update embeddings from local directory specified by the `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`)
*   `GET /search?query={query}` - Search for relevant notes and generate answers
*   `GET /notes-count` - Get the total number of notes in the knowledge base

### Frontend (Vanilla JS)

The frontend is a static web application. It would be served by a web server or deployed to a static hosting service.

```bash
# To serve locally (example using Python's http.server)
cd frontend
python -m http.server 3000
```

### Deployment

*   **Backend:** Deployed on Google Cloud Run.
*   **Frontend:** Deployed on Firebase Hosting.

## Development Conventions

*   **Asynchronous Processing:** Backend requests are designed for asynchronous handling.
*   **Logging:** All requests are logged to a JSON file for monitoring and debugging.
*   **Google Cloud Ecosystem:** The project is designed to integrate seamlessly with Google Cloud services for deployment, security, and scalability.
*   **LLM Interaction:** Google Gemini API is used for query embedding and answer generation. Direct calls to the Gemini API are preferred for production stability and scalability.

*   **Local File System:** Used for reading Markdown notes from the local directory specified by the `FF_BASE_DIR` environment variable (default `/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE`).
*   **Scalability:** Initial local JSON storage for embeddings, with a plan to migrate to a specialized vector store (e.g., Chromadb) as the note base grows.

## Documentation Workflow

Чтобы документация была консистентной и легкой в поддержке, пожалуйста, следуйте этим правилам:

1.  **Основной хаб документации:** Вся статичная документация по проекту (руководства, инструкции, справочники) находится в директории `/docs`.
2.  **Чтение документации:** Когда вас спрашивают о функциях проекта, настройке или архитектуре, в первую очередь ищите информацию в директории `/docs`.
3.  **Обновление статичной документации:** Любые изменения или дополнения в статичную документацию (например, инструкции по деплою, справочник по API) должны вноситься в файлы внутри директории `/docs`.
4.  **Динамические файлы контекста:** Файлы `GEMINI.md` и `QWEN.md` являются особенными. Они находятся в корневой директории и обновляются динамически внешними процессами.
    *   **Не перемещайте, не переименовывайте и не удаляйте `GEMINI.md` или `QWEN.md`**.
    *   Обновления, касающиеся общего обзора проекта или "памяти" AI-ассистента, должны записываться непосредственно в эти файлы в корневой директории.
5.  **Главный README:** Файл `README.md` в корне является кратким обзором. Не добавляйте в него подробную документацию. Он должен содержать только высокоуровневое описание и ссылку на директорию `/docs`.