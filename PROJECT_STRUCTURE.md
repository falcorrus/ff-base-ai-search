# Project Structure

```
ff-base-ai-search/
├── !Screenshots/
├── .gemini/
├── .git/
├── .vercel/
├── api/
├── backend/
│   ├── data/
│   ├── dist/
│   ├── node_modules/
│   ├── src/
│   │   ├── config/
│   │   │   └── index.ts
│   │   ├── controllers/
│   │   │   └── searchController.ts
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── scripts/
│   │   ├── services/
│   │   │   ├── llmService.ts
│   │   │   └── vectorDbService.ts
│   │   ├── utils/
│   │   └── index.ts
│   ├── .env.example
│   ├── .env.txt
│   ├── add-embeddings-js.js
│   ├── create-chat-vector-db.js
│   ├── create-clean-vector-db.js
│   ├── create-test-vector-db.js
│   ├── generate-chat-embeddings.js
│   ├── generate-test-embeddings.js
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   ├── run-generate-embeddings.js
│   ├── test-api-endpoint.ts
│   ├── test-api.ts
│   ├── test-config-real.ts
│   ├── test-config.ts
│   ├── test-controller-logs.ts
│   ├── test-conversion-real.ts
│   ├── test-cors.ts
│   ├── test-embedding-real.ts
│   ├── test-env-vercel-fixed.ts
│   ├── test-env-vercel.ts
│   ├── test-env.ts
│   ├── test-llm-real.ts
│   ├── test-llm.js
│   ├── test-llm.ts
│   ├── test-rpc-real.ts
│   ├── test-rpc.js
│   ├── test-search-controller-real.ts
│   ├── test-search-detailed.ts
│   ├── test-search-real.ts
│   ├── test-search.ts
│   ├── test-supabase-real.ts
│   ├── test-supabase.js
│   ├── test-vector-db.ts
│   └── tsconfig.json
├── ChatExport_2025-09-03-v1/
├── frontend/
│   ├── dist/
│   ├── node_modules/
│   ├── src/
│   │   ├── main.ts
│   │   └── search-result.html
│   ├── .gitignore
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── node_modules/
├── scripts/
│   ├── clear_and_upload.ts
│   ├── parseChatExport.js
│   ├── tsconfig.json
│   ├── upload.js
│   └── upload.ts
├── .gitignore
├── пустой поиск.md
├── base.json
├── base3y.json
├── GEMINI.md
├── input_base.json
├── knowledge_base_copy.json
├── knowledge_base-2025.json
├── package-lock.json
├── package.json
├── README.md
├── TECHNICAL_SPECIFICATION.md
├── test-request.js
├── test-supabase.js
├── vercel.json
```