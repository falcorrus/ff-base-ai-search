// backend/src/scripts/README.md
# Upload Script for Documents to Supabase

This script uploads documents from `base.json` to a Supabase database table called `documents`.

## What the script does

1. Reads data from `base.json` which contains documents with the following structure:
   - `id`: Document ID
   - `date`: Date of the message
   - `sender`: Sender of the message
   - `text`: Text content of the message
   - `origin`: Source of the message
   - `embedding`: 768-dimensional vector embedding

2. Converts the 768-dimensional embeddings to 1536-dimensional embeddings by padding with zeros (required by Supabase)

3. Uploads the documents to the Supabase `documents` table in batches of 1000

## How to run

1. Make sure you're in the `backend` directory:
   ```bash
   cd backend
   ```

2. Set the required environment variables:
   ```bash
   export SUPABASE_URL="your_supabase_url"
   export SUPABASE_SERVICE_ROLE_KEY="your_service_role_key"
   ```

3. Run the upload script:
   ```bash
   npx ts-node src/scripts/upload.ts
   ```

## Verification

You can verify the upload by running:
```bash
npx ts-node src/scripts/verifyUpload.ts
```

## Notes

- The `documents` table must already exist with the proper schema
- The `embedding` column should be of type `VECTOR(1536)`
- Supabase returns vector data as a string representation when queried, which is normal behavior