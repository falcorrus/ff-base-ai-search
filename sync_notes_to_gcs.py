#!/usr/bin/env python3
"""
Script to sync notes from Google Drive FF-BASE directory to Google Cloud Storage.
"""

import os
import sys
from pathlib import Path
from google.cloud import storage
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file."""
    env_file = Path("backend/.env")
    if env_file.exists():
        load_dotenv(env_file)
        print("Environment variables loaded")

def sync_notes_to_gcs():
    """Sync notes from Google Drive FF-BASE directory to GCS bucket."""
    try:
        # Load environment variables
        load_environment()
        
        # Set the service account key
        service_account_key = "./backend/service-account-key.json"
        if os.path.exists(service_account_key):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
            print("✅ Service account key set")
        else:
            print("Service account key not found")
            return False
        
        # Import Google Cloud Storage client
        from google.cloud import storage
        
        # Get GCS configuration
        gcs_bucket_name = "ff-base-knowledge-base"
        ff_base_dir = "/Users/eugene/Library/CloudStorage/GoogleDrive-ekirshin@gmail.com/Мой диск/OBSIDIAN/FF-BASE"
        
        print(f"Syncing notes from {ff_base_dir} to GCS bucket: {gcs_bucket_name}")
        
        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(gcs_bucket_name)
        
        # Get all .md files recursively
        ff_base_path = Path(ff_base_dir)
        if not ff_base_path.exists():
            print("FF-BASE directory not found")
            return False
            
        md_files = list(ff_base_path.rglob("*.md"))
        print(f"Found {len(md_files)} Markdown files in FF-BASE")
        
        # Upload files
        uploaded_count = 0
        for file_path in md_files:
            try:
                # Get relative path from FF-BASE directory
                relative_path = str(file_path.relative_to(ff_base_path))
                
                # Upload file
                blob = bucket.blob(relative_path)
                blob.upload_from_filename(str(file_path))
                print(f"Uploaded: {relative_path}")
                uploaded_count += 1
            except Exception as e:
                print(f"Error uploading file {relative_path}: {e}")
                continue
        
        print(f"✅ {uploaded_count} files synced to GCS successfully!")
        return True
        
    except Exception as e:
        print(f"Error syncing notes to GCS: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🔄 Syncing notes to GCS...")
    
    success = sync_notes_to_gcs()
    if success:
        print("✅ Notes sync completed successfully")
    else:
        print("❌ Failed to sync notes to GCS")
        sys.exit(1)

if __name__ == "__main__":
    main()