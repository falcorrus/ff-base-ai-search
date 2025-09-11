#!/usr/bin/env python3
"""
Script to sync embeddings between local directory specified by `FF_BASE_DIR` environment variable and Google Cloud Storage.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def load_environment():
    """Load environment variables from .env file."""
    # Load from root .env file first
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    
    # Load from backend/.env file as fallback
    backend_env_file = Path("backend/.env")
    if backend_env_file.exists():
        with open(backend_env_file) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    # Only set if not already set
                    if key not in os.environ:
                        os.environ[key] = value

def update_local_embeddings():
    """Update local embeddings from directory specified by `FF_BASE_DIR` environment variable."""
    print("Updating local embeddings from directory specified by `FF_BASE_DIR` environment variable...")
    try:
        # Change to backend directory and run the update endpoint
        result = subprocess.run([
            "python", "-c", 
            "import asyncio; from main import update_knowledge_base_from_local; "
            "print(asyncio.run(update_knowledge_base_from_local()))"
        ], cwd="backend", capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Local embeddings updated successfully!")
            print(result.stdout)
            return True
        else:
            print("Error updating local embeddings:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("Timeout while updating local embeddings")
        return False
    except Exception as e:
        print(f"Error updating local embeddings: {e}")
        return False

def sync_to_gcs():
    """Sync local embeddings to Google Cloud Storage."""
    try:
        load_environment()
        
        # Set the service account key if it exists
        service_account_key = "./backend/service-account-key.json"
        if os.path.exists(service_account_key):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
            print("✅ Service account key set")
        
        # Import Google Cloud Storage client
        from google.cloud import storage
        
        # Get GCS configuration
        gcs_bucket_name = os.getenv("GCS_BUCKET_NAME", "ff-base-4d8ee")
        embeddings_file = "knowledge_base/embeddings.json"
        embeddings_file_name = "embeddings.json"
        
        print(f"Syncing embeddings to GCS bucket: {gcs_bucket_name}")
        
        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        
        # Upload embeddings file
        blob = bucket.blob(embeddings_file_name)
        blob.upload_from_filename(embeddings_file)
        print("✅ Embeddings synced to GCS successfully!")
        
        # Also upload search log if it exists
        search_log_file = "knowledge_base/search_log.json"
        if os.path.exists(search_log_file):
            search_log_blob = bucket.blob("search_log.json")
            search_log_blob.upload_from_filename(search_log_file)
            print("✅ Search log synced to GCS!")
            
        return True
    except Exception as e:
        print(f"Error syncing to GCS: {e}")
        return False

def sync_from_gcs():
    """Sync embeddings from Google Cloud Storage to local."""
    try:
        load_environment()
        
        # Set the service account key if it exists
        service_account_key = "./backend/service-account-key.json"
        if os.path.exists(service_account_key):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
            print("✅ Service account key set")
        
        # Import Google Cloud Storage client
        from google.cloud import storage
        
        # Get GCS configuration
        gcs_bucket_name = os.getenv("GCS_BUCKET_NAME", "ff-base-4d8ee")
        embeddings_file = "knowledge_base/embeddings.json"
        embeddings_file_name = "embeddings.json"
        
        print(f"Syncing embeddings from GCS bucket: {gcs_bucket_name}")
        
        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        
        # Download embeddings file
        blob = bucket.blob(embeddings_file_name)
        if blob.exists():
            blob.download_to_filename(embeddings_file)
            print("✅ Embeddings synced from GCS successfully!")
        else:
            print("No embeddings file found in GCS")
            return False
        
        # Also download search log if it exists
        search_log_file = "knowledge_base/search_log.json"
        search_log_blob = bucket.blob("search_log.json")
        if search_log_blob.exists():
            search_log_blob.download_to_filename(search_log_file)
            print("✅ Search log synced from GCS!")
            
        return True
    except Exception as e:
        print(f"Error syncing from GCS: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python python/sync_embeddings.py update-local    # Update local embeddings from directory specified by `FF_BASE_DIR` environment variable")
        print("  python python/sync_embeddings.py sync-to-gcs     # Sync local embeddings to GCS")
        print("  python python/sync_embeddings.py sync-from-gcs   # Sync embeddings from GCS to local")
        print("  python python/sync_embeddings.py full-sync       # Update local + sync to GCS")
        return
    
    command = sys.argv[1]
    
    if command == "update-local":
        success = update_local_embeddings()
        if success:
            print("✅ Local embeddings updated successfully")
        else:
            print("❌ Failed to update local embeddings")
            sys.exit(1)
            
    elif command == "sync-to-gcs":
        success = sync_to_gcs()
        if success:
            print("✅ Synced to GCS successfully")
        else:
            print("❌ Failed to sync to GCS")
            sys.exit(1)
            
    elif command == "sync-from-gcs":
        success = sync_from_gcs()
        if success:
            print("✅ Synced from GCS successfully")
        else:
            print("❌ Failed to sync from GCS")
            sys.exit(1)
            
    elif command == "full-sync":
        print("🔄 Performing full sync...")
        # Update local embeddings
        if not update_local_embeddings():
            print("❌ Failed to update local embeddings")
            sys.exit(1)
        
        # Sync to GCS
        if not sync_to_gcs():
            print("❌ Failed to sync to GCS")
            sys.exit(1)
            
        print("✅ Full sync completed successfully")
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()