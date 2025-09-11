#!/usr/bin/env python3
"""
Highly optimized script to sync notes from Google Drive to Google Cloud Storage.
Compares Google Drive folder hash with saved hash in GCS first, then incremental sync.
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
MAX_WORKERS = 20  # Increased parallel workers
METADATA_CACHE_FILE = "knowledge_base/metadata_cache.json"
LAST_SYNC_FILE = "knowledge_base/last_sync_token.json"

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

def calculate_drive_folder_hash(service, folder_id):
    """Calculate hash of the entire Google Drive folder."""
    try:
        print("🔍 Calculating Google Drive folder hash...")
        
        # Get all .md files in the folder recursively
        all_files = []
        
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
        
        print(f"Found {len(all_files)} Markdown files in Google Drive FF-BASE folder")
        
        # Sort files for consistent hashing
        sorted_files = sorted(all_files, key=lambda x: x.get('full_path', ''))
        
        # Create metadata string
        metadata_string = ""
        for file in sorted_files:
            # Include path, modification time, and checksum if available
            path = file.get('full_path', '')
            mod_time = file.get('modifiedTime', '')
            checksum = file.get('md5Checksum', '')
            metadata_string += f"{path}|{mod_time}|{checksum}\n"
        
        # Calculate MD5 hash of the metadata string
        folder_hash = hashlib.md5(metadata_string.encode('utf-8')).hexdigest()
        print(f"✅ Google Drive folder hash calculated: {folder_hash[:16]}...")
        return folder_hash
        
    except Exception as e:
        print(f"Error calculating Google Drive folder hash: {e}")
        return None

def get_saved_drive_folder_hash(gcs_client, bucket_name):
    """Get the saved Google Drive folder hash from GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob("drive_folder_hash.txt")
        
        if blob.exists():
            content = blob.download_as_text()
            return content.strip()
        return None
        
    except Exception as e:
        print(f"Error getting saved Google Drive folder hash: {e}")
        return None

def save_drive_folder_hash(gcs_client, bucket_name, folder_hash):
    """Save the Google Drive folder hash to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob("drive_folder_hash.txt")
        blob.upload_from_string(folder_hash)
        print("✅ Google Drive folder hash saved to GCS")
        
    except Exception as e:
        print(f"Error saving Google Drive folder hash: {e}")

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

def load_metadata_cache():
    """Load metadata cache from local file."""
    try:
        if os.path.exists(METADATA_CACHE_FILE):
            with open(METADATA_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading metadata cache: {e}")
        return {}

def save_metadata_cache(metadata_cache):
    """Save metadata cache to local file."""
    try:
        os.makedirs(os.path.dirname(METADATA_CACHE_FILE), exist_ok=True)
        with open(METADATA_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata_cache, f, ensure_ascii=False, indent=2)
        print("✅ Metadata cache saved locally")
    except Exception as e:
        print(f"Error saving metadata cache: {e}")

def get_last_sync_token():
    """Get last sync token from local file."""
    try:
        if os.path.exists(LAST_SYNC_FILE):
            with open(LAST_SYNC_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('page_token'), data.get('timestamp')
        return None, None
    except Exception as e:
        print(f"Error loading last sync token: {e}")
        return None, None

def save_last_sync_token(page_token):
    """Save last sync token to local file."""
    try:
        os.makedirs(os.path.dirname(LAST_SYNC_FILE), exist_ok=True)
        data = {
            'page_token': page_token,
            'timestamp': datetime.now().isoformat()
        }
        with open(LAST_SYNC_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ Last sync token saved locally")
    except Exception as e:
        print(f"Error saving last sync token: {e}")

def list_drive_files_incremental(service, folder_id):
    """List changed files in Google Drive using pageToken."""
    try:
        # Get last sync token
        last_page_token, last_sync_time = get_last_sync_token()
        
        all_files = []
        page_token = last_page_token
        
        # If we have a page token, use it for incremental sync
        if page_token:
            print(f"🔄 Using incremental sync from last token (last sync: {last_sync_time})")
        else:
            print("🔄 Full sync (no previous sync token)")
        
        while True:
            # List files with page token
            query = f"'{folder_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false"
            
            results = service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, parents, mimeType, md5Checksum, modifiedTime)",
                pageToken=page_token,
                pageSize=1000  # Get more files per request
            ).execute()
            
            files = results.get('files', [])
            all_files.extend(files)
            
            # Get next page token
            page_token = results.get('nextPageToken')
            
            # If no more pages, break
            if not page_token:
                break
        
        print(f"Found {len(all_files)} files (changed since last sync or all files)")
        
        # Save the new page token for next sync
        if page_token:
            save_last_sync_token(page_token)
        
        return all_files
        
    except Exception as e:
        print(f"Error listing files incrementally: {e}")
        return []

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
    service, gcs_client, bucket_name, file, metadata_cache = args
    
    try:
        file_path = file.get('full_path', file['name'])
        print(f"Processing: {file_path}")
        
        # Get file's MD5 checksum from Google Drive
        drive_md5 = file.get('md5Checksum')
        mod_time = file.get('modifiedTime', '')
        
        # Check if we have this file in cache and if it's unchanged
        cache_key = file_path
        if cache_key in metadata_cache:
            cached_data = metadata_cache[cache_key]
            if cached_data.get('md5Checksum') == drive_md5 and cached_data.get('modifiedTime') == mod_time:
                print(f"⏭️  Skipped (unchanged, cached): {file_path}")
                return False, file_path
        
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
                    # Update cache
                    metadata_cache[cache_key] = {
                        'md5Checksum': drive_md5,
                        'modifiedTime': mod_time
                    }
                    print(f"⏭️  Skipped (unchanged): {file_path}")
                    return False, file_path
        
        # Download file content
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
            
        # Update cache
        metadata_cache[cache_key] = {
            'md5Checksum': drive_md5,
            'modifiedTime': mod_time
        }
        
        print(f"✅ Synced: {file_path}")
        return True, file_path
        
    except Exception as e:
        print(f"❌ Error syncing file {file.get('full_path', file['name'])}: {e}")
        return False, file.get('full_path', file['name'])

def sync_drive_to_gcs():
    """Highly optimized sync from Google Drive to GCS using Drive folder hash comparison."""
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
        
        # Step 1: Compare Google Drive folder hashes
        print("🔍 Step 1: Comparing Google Drive folder hashes...")
        folder_id = find_ff_base_folder(drive_service)
        if not folder_id:
            return False
            
        drive_folder_hash = calculate_drive_folder_hash(drive_service, folder_id)
        if drive_folder_hash:
            saved_hash = get_saved_drive_folder_hash(gcs_client, gcs_bucket_name)
            if saved_hash and saved_hash == drive_folder_hash:
                print("✅ Google Drive folder unchanged, skipping sync completely")
                print("✅ Sync completed: 0 files synced")
                return True
            else:
                print("📁 Google Drive folder has changed, proceeding with sync")
                # Save new hash for next run
                save_drive_folder_hash(gcs_client, gcs_bucket_name, drive_folder_hash)
        else:
            print("⚠️  Could not calculate Google Drive folder hash, proceeding with normal sync")
        
        # Load metadata cache
        metadata_cache = load_metadata_cache()
        
        # Step 2: Get changed files using pageToken
        print("🔍 Step 2: Getting changed files...")
        files = list_drive_files_incremental(drive_service, folder_id)
        if not files:
            print("No files found to sync")
            # Save cache even if no files
            save_metadata_cache(metadata_cache)
            return True
        
        # Add full paths to files
        print("🔍 Adding full paths to files...")
        enhanced_files = []
        for file in files:
            if 'full_path' not in file:
                full_path = get_full_path(drive_service, file['id'], folder_id)
                if full_path:
                    file['full_path'] = full_path
                    enhanced_files.append(file)
            else:
                enhanced_files.append(file)
        
        # Step 3: Sync files using parallel processing
        print("🔍 Step 3: Syncing files...")
        synced_count = 0
        skipped_count = 0
        
        # Prepare arguments for parallel processing
        args_list = [(drive_service, gcs_client, gcs_bucket_name, file, metadata_cache) for file in enhanced_files]
        
        # Process files in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(sync_single_file, args_list))
            
            # Count results
            for success, file_path in results:
                if success:
                    synced_count += 1
                else:
                    skipped_count += 1
        
        print(f"✅ Sync completed: {synced_count} files synced, {skipped_count} files unchanged")
        
        # Save metadata cache
        save_metadata_cache(metadata_cache)
        
        return True
        
    except Exception as e:
        print(f"Error syncing notes from Drive to GCS: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("🔄 Syncing notes from Google Drive to GCS (ultra-optimized with Drive hash comparison)...")
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