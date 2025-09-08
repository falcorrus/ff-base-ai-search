# Project Setup and Development Steps

This document outlines the key steps for setting up, developing, and deploying the `ff-base-ai-search` project, based on the `GEMINI.md` project overview.

## 1. Initial Project Setup

*   [x] **1.1 Backend Environment:** Set up a Python 3.9+ development environment.
*   [x] **1.2 Backend Dependencies:** Install FastAPI and any other required Python libraries (e.g., for GitHub API interaction, Google Gemini API client).
*   [x] **1.3 Frontend Environment:** Prepare a development environment for Vanilla JavaScript.

## 2. Backend Development

*   [ ] **2.1 GitHub Integration:** Implement functionality to fetch Markdown notes from a specified GitHub repository using the GitHub API.
*   [ ] **2.2 Embedding Generation:** Develop the logic to generate vector embeddings for each Markdown note using the Google Gemini Embeddings API (`gemini-embedding-001`).
*   [x] **2.3 Embedding Storage:** Implement the storage mechanism for these embeddings, initially in a local JSON file.
*   [ ] **2.4 Search API Endpoint:** Create a FastAPI endpoint to receive user search queries.
*   [ ] **2.5 Relevant Note Retrieval:** Implement the vector search logic to find relevant notes based on the user's query embedding.
*   [ ] **2.6 Context Formation:** Develop the process to form a comprehensive context from the content of the retrieved Markdown notes.
*   [ ] **2.7 Answer Generation:** Integrate with the Google Gemini LLM to generate a comprehensive answer based on the formed context.
*   [ ] **2.8 API Response:** Return the generated answer to the frontend via the API.
*   [x] **2.9 Request Logging:** Implement logging of all incoming requests to a JSON file, including timestamps and query text.

## 3. Frontend Development

*   [x] **3.1 User Interface:** Develop the main search page with a search input field and a display area for results.
*   [ ] **3.2 Backend Communication:** Implement asynchronous JavaScript to send search queries to the backend API and receive responses.
*   [ ] **3.3 Result Display:** Render the generated answer from the backend on the frontend.

## 4. Deployment

*   [ ] **4.1 Backend Deployment:** Prepare and deploy the FastAPI backend application to Google Cloud Run.
*   [ ] **4.2 Frontend Deployment:** Prepare and deploy the Vanilla JavaScript frontend application to Firebase Hosting (or another suitable Google Cloud static hosting platform).

## 5. Future Enhancements (as per PLAN.md)

*   [ ] **5.1 Vector Store Migration:** Migrate from local JSON storage to a specialized vector store (e.g., Chromadb) for embeddings as the note base grows.
*   [ ] **5.2 GitHub Loading Optimization:** Optimize the process of loading notes from GitHub.
*   [ ] **5.3 LLM Context Optimization:** Improve handling of long contexts when interacting with the LLM.
*   [ ] **5.4 Authorization:** Implement user authorization and access control mechanisms.