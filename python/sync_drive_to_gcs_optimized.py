#!/usr/bin/env python3
"""
Optimized script to sync notes from Google Drive to Google Cloud Storage.
Only syncs files that have changed since last sync.
"""

import os
import sys
import json
import io
import hashlib
import base64
import concurrent.futures
from pathlib import Path
from google.cloud import storage
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv
from datetime import datetime

# Configuration
MAX_WORKERS = 10  # Number of parallel workers
CHUNK_SIZE = 100  # Process files in chunks

def load_environment():
    """Load environment variables from .env file."""
    env_file = Path("backend/.env")
    if env_file.exists():
        load_dotenv(env_file)
        print("Environment variables loaded")

def get_drive_service():
    """Initialize and return Google Drive service."""
    try:
        # Load service account credentials
        service_account_path = "./backend/service-account-key.json"
        if not os.path.exists(service_account_path):
            print("Service account key not found")
            return None
            
        # Define scopes
        scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/devstorage.read_write"
        ]
        
        # Create credentials
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path, scopes=scopes)
        
        # Build the service
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive service initialized")
        return service
        
    except Exception as e:
        print(f"Error initializing Google Drive service: {e}")
        return None

def get_gcs_client():
    """Initialize and return Google Cloud Storage client."""
    try:
        # Set the service account key
        service_account_key = "./backend/service-account-key.json"
        if os.path.exists(service_account_key):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
            print("✅ Service account key set for GCS")
        else:
            print("Service account key not found")
            return None
            
        # Initialize GCS client
        client = storage.Client()
        print("✅ Google Cloud Storage client initialized")
        return client
        
    except Exception as e:
        print(f"Error initializing GCS client: {e}")
        return None

def find_ff_base_folder(service):
    """Find the FF-BASE folder in Google Drive."""
    try:
        # Search for the folder by name
        query = "name='FF-BASE' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            print("FF-BASE folder not found in Google Drive")
            return None
            
        folder = items[0]
        print(f"Found FF-BASE folder: {folder['name']} (ID: {folder['id']})")
        return folder['id']
        
    except Exception as e:
        print(f"Error finding FF-BASE folder: {e}")
        return None

def get_full_path(service, file_id, folder_id):
    """Get the full path of a file in Google Drive."""
    try:
        # Get file metadata
        file = service.files().get(fileId=file_id, fields="id, name, parents").execute()
        
        path_parts = [file['name']]
        current_id = file.get('parents', [None])[0]
        
        # Traverse up the folder hierarchy until we reach the FF-BASE folder
        while current_id and current_id != folder_id:
            folder = service.files().get(fileId=current_id, fields="id, name, parents").execute()
            path_parts.insert(0, folder['name'])
            current_id = folder.get('parents', [None])[0]
            
        return "/".join(path_parts)
        
    except Exception as e:
        print(f"Error getting full path for file {file_id}: {e}")
        return None

def list_drive_files(service, folder_id):
    """List all .md files in the specified Google Drive folder (recursively)."""
    try:
        all_files = []
        
        # Function to recursively list files
        def list_files_recursive(parent_id):
            # List folders
            folder_query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            folder_results = service.files().list(
                q=folder_query,
                fields="files(id, name, parents, mimeType)"
            ).execute()
            
            folders = folder_results.get('files', [])
            for folder in folders:
                list_files_recursive(folder['id'])
            
            # List .md files
            file_query = f"'{parent_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false"
            file_results = service.files().list(
                q=file_query,
                fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime)"
            ).execute()
            
            files = file_results.get('files', [])
            for file in files:
                # Get full path
                full_path = get_full_path(service, file['id'], folder_id)
                if full_path:
                    file['full_path'] = full_path
                    all_files.append(file)
        
        # Start recursive listing
        list_files_recursive(folder_id)
        
        print(f"Found {len(all_files)} Markdown files in FF-BASE folder (including subfolders)")
        return all_files
        
    except Exception as e:
        print(f"Error listing files in Drive folder: {e}")
        return []

def calculate_folder_hash(files):
    """Calculate hash of the entire folder based on file metadata."""
    try:
        # Sort files by path for consistent hashing
        sorted_files = sorted(files, key=lambda x: x.get('full_path', ''))
        
        # Create a string with file metadata
        metadata_string = ""
        for file in sorted_files:
            # Include path, modification time, and checksum if available
            path = file.get('full_path', '')
            mod_time = file.get('modifiedTime', '')
            checksum = file.get('md5Checksum', '')
            metadata_string += f"{path}|{mod_time}|{checksum}\n"
        
        # Calculate MD5 hash of the metadata string
        folder_hash = hashlib.md5(metadata_string.encode('utf-8')).hexdigest()
        return folder_hash
        
    except Exception as e:
        print(f"Error calculating folder hash: {e}")
        return None

def get_saved_folder_hash(gcs_client, bucket_name):
    """Get the saved folder hash from GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob("folder_hash.txt")
        
        if blob.exists():
            content = blob.download_as_text()
            return content.strip()
        return None
        
    except Exception as e:
        print(f"Error getting saved folder hash: {e}")
        return None

def save_folder_hash(gcs_client, bucket_name, folder_hash):
    """Save the folder hash to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob("folder_hash.txt")
        blob.upload_from_string(folder_hash)
        print("✅ Folder hash saved to GCS")
        
    except Exception as e:
        print(f"Error saving folder hash: {e}")

def download_drive_file(service, file_id):
    """Download file content from Google Drive."""
    try:
        # Download file content
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            
        # Get content as bytes
        content = fh.getvalue()
        return content
        
    except Exception as e:
        print(f"Error downloading file from Drive: {e}")
        return None

def sync_single_file(args):
    """Sync a single file - used for parallel processing."""
    service, gcs_client, bucket_name, file = args
    
    try:
        file_path = file['full_path']
        print(f"Processing: {file_path}")
        
        # Get file's MD5 checksum from Google Drive
        drive_md5 = file.get('md5Checksum')
        if not drive_md5:
            # If no checksum from Drive, download content and calculate
            content = download_drive_file(service, file['id'])
            if content is None:
                return False, file_path
                
            # Calculate MD5 hash of the content
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = content
                
            drive_md5 = hashlib.md5(content_bytes).hexdigest()
        
        # Check if file already exists in GCS
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        if blob.exists():
            # Get the MD5 hash of the existing file
            existing_blob = bucket.get_blob(file_path)
            if existing_blob.md5_hash:
                # Convert base64 hash to hex
                existing_md5 = base64.b64decode(existing_blob.md5_hash).hex()
                
                # Compare hashes
                if existing_md5.lower() == drive_md5.lower():
                    print(f"⏭️  Skipped (unchanged): {file_path}")
                    return False, file_path
        
        # If we didn't download the content earlier, do it now
        if 'content' not in locals() or content is None:
            content = download_drive_file(service, file['id'])
            if content is None:
                return False, file_path
        
        # Upload to GCS
        if isinstance(content, bytes):
            try:
                content_str = content.decode('utf-8')
                blob.upload_from_string(content_str, content_type='text/markdown')
            except UnicodeDecodeError:
                # If it's not UTF-8, upload as binary
                blob.upload_from_string(content, content_type='application/octet-stream')
        else:
            blob.upload_from_string(content, content_type='text/markdown')
            
        print(f"✅ Synced: {file_path}")
        return True, file_path
        
    except Exception as e:
        print(f"❌ Error syncing file {file.get('full_path', file['name'])}: {e}")
        return False, file.get('full_path', file['name'])

def sync_drive_to_gcs():
    """Sync notes from Google Drive FF-BASE folder to GCS bucket.
    Only syncs files that have changed since last sync.
    """
    try:
        # Load environment variables
        load_environment()
        
        # Initialize services
        drive_service = get_drive_service()
        if not drive_service:
            return False
            
        gcs_client = get_gcs_client()
        if not gcs_client:
            return False
        
        # Get GCS configuration
        gcs_bucket_name = "ff-base-knowledge-base"
        
        print(f"Syncing notes from Google Drive to GCS bucket: {gcs_bucket_name}")
        
        # Find FF-BASE folder
        folder_id = find_ff_base_folder(drive_service)
        if not folder_id:
            return False
            
        # List files in the folder
        files = list_drive_files(drive_service, folder_id)
        if not files:
            print("No files found to sync")
            return True
        
        # Calculate folder hash
        current_folder_hash = calculate_folder_hash(files)
        if current_folder_hash:
            # Check saved folder hash
            saved_hash = get_saved_folder_hash(gcs_client, gcs_bucket_name)
            if saved_hash and saved_hash == current_folder_hash:
                print("⏭️  Folder unchanged, skipping sync")
                print(f"✅ Sync completed: 0 files synced")
                return True
            else:
                print("📁 Folder has changed, proceeding with sync")
        
        # Sync files using parallel processing
        synced_count = 0
        skipped_count = 0
        
        # Prepare arguments for parallel processing
        args_list = [(drive_service, gcs_client, gcs_bucket_name, file) for file in files]
        
        # Process files in chunks to avoid memory issues
        for i in range(0, len(args_list), CHUNK_SIZE):
            chunk = args_list[i:i + CHUNK_SIZE]
            
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                results = list(executor.map(sync_single_file, chunk))
                
                # Count results
                for success, file_path in results:
                    if success:
                        synced_count += 1
                    else:
                        skipped_count += 1
        
        print(f"✅ Sync completed: {synced_count} files synced, {skipped_count} files unchanged")
        
        # Save folder hash for next run
        if current_folder_hash:
            save_folder_hash(gcs_client, gcs_bucket_name, current_folder_hash)
        
        return True
        
    except Exception as e:
        print(f"Error syncing notes from Drive to GCS: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🔄 Syncing notes from Google Drive to GCS (optimized incremental sync)...")
    start_time = datetime.now()
    
    success = sync_drive_to_gcs()
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"⏱️  Sync duration: {duration}")
    
    if success:
        print("✅ Notes sync completed successfully")
    else:
        print("❌ Failed to sync notes to GCS")
        sys.exit(1)

if __name__ == "__main__":
    main()