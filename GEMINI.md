# Project Overview: ff-base-ai-search

This project, `ff-base-ai-search`, is an intelligent search system designed to provide semantic search capabilities and natural language answers over a user's knowledge base. The knowledge base is expected to be stored as Markdown files, potentially within a GitHub repository.

## Key Features:
*   **Semantic Search:** Enables searching based on the meaning and context of queries, rather than just keywords.
*   **LLM Integration:** Utilizes Large Language Models (LLMs) to generate natural language responses to user queries.
*   **Vector Database:** Employs a vector database to store embeddings of the knowledge base content, facilitating efficient semantic search.

## Technologies Used:
*   **Frontend:**
    *   **Framework:** Vanilla JavaScript/TypeScript
    *   **Interactivity:** HTMX
    *   **Styling:** Tailwind CSS
    *   **Build Tool:** Vite
*   **Backend:**
    *   **Runtime:** Node.js
    *   **Framework:** Express.js
    *   **Language:** TypeScript
    *   **LLM Integration:** Google Gemini API (`@google/generative-ai`)
    *   **Vector Database Interaction:** Supabase (`@supabase/supabase-js`) - intended for ChromaDB in production, with a JSON file-based prototype.
    *   **Other:** `axios`, `cheerio`, `cors`, `dotenv`, `node-html-parser`, `octokit`.
*   **Project Structure:** Monorepo managed with npm workspaces, separating `frontend` and `backend` concerns.

## Building and Running the Project

### Prerequisites
*   Node.js (LTS recommended)
*   npm (Node Package Manager)

### Installation

1.  **Navigate to the project root:**
    ```bash
    cd /Users/eugene/MyProjects/ff-base-ai-search
    ```
2.  **Install root dependencies and hoist workspace dependencies:**
    ```bash
    npm install
    ```

### Development

To run the frontend and backend in development mode (with hot-reloading for the backend):

1.  **Start the Frontend Development Server:**
    ```bash
    cd /Users/eugene/MyProjects/ff-base-ai-search/frontend
    npm run dev
    ```
    This will typically start the frontend on `http://localhost:5173` (or another available port).

2.  **Start the Backend Development Server:**
    ```bash
    cd /Users/eugene/MyProjects/ff-base-ai-search/backend
    npm run dev
    ```
    The backend will usually run on `http://localhost:3000`.

### Building for Production

To create optimized production builds for both frontend and backend:

1.  **From the project root:**
    ```bash
    cd /Users/eugene/MyProjects/ff-base-ai-search
    npm run build
    ```
    This command executes the `build` script in both the `frontend` and `backend` workspaces.

### Starting Production Server

After building, you can start the backend production server:

1.  **From the backend directory:**
    ```bash
    cd /Users/eugene/MyProjects/ff-base-ai-search/backend
    npm start
    ```

### Other Useful Backend Scripts

The `backend` directory contains several utility scripts for specific tasks:

*   **`npm run generate-embeddings`**: Generates embeddings for the knowledge base.
*   **`npm run test-search`**: Runs tests related to the search functionality.
*   **`npm run test-llm`**: Runs tests related to the LLM integration.
*   **`npm run test-api`**: Runs tests for the backend API endpoints.
*   **`npm run parse-telegram`**: Parses Telegram chat exports (likely for knowledge base ingestion).

## Development Conventions

*   **Language:** TypeScript is used consistently across both frontend and backend for type safety and improved developer experience.
*   **Frontend Architecture:** Leverages HTMX for declarative HTML-driven interactivity, minimizing complex JavaScript. Tailwind CSS is used for utility-first styling.
*   **Backend Architecture:** A standard Node.js/Express API structure is followed, likely with separation of concerns (controllers, services, routes, config).
*   **API Interaction:** The backend interacts with the Google Gemini API for LLM capabilities and Supabase for database operations, including vector storage.
*   **Monorepo:** The project is organized as a monorepo, which helps in managing related but distinct frontend and backend applications within a single repository.
