#!/usr/bin/env python3
"""
Highly optimized Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Uses hierarchical folder-level hashes for maximum performance.
"""

import os
import json
import io
import hashlib
import base64
import time
import random
from datetime import datetime
from google.cloud import storage
from googleapiclient.discovery import build
from google.auth import default
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Configuration
MAX_WORKERS = 5
BATCH_SIZE = 20
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1
BUCKET_NAME = "ff-base-knowledge-base"
FF_BASE_FOLDER_NAME = "FF-BASE"
HASH_PREFIX = "folder_hashes/"

def get_drive_service():
    """Initialize and return Google Drive service with error handling."""
    try:
        # Use default credentials (works in Cloud Functions environment)
        credentials, _ = default()
        
        # Add required scopes
        scoped_credentials = credentials.with_scopes([
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/devstorage.read_write"
        ])
        
        # Build the service
        service = build('drive', 'v3', credentials=scoped_credentials, cache_discovery=False)
        print("✅ Google Drive service initialized")
        return service
        
    except Exception as e:
        print(f"Error initializing Google Drive service: {e}")
        return None

def get_gcs_client():
    """Initialize and return Google Cloud Storage client."""
    try:
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
        query = f"name='{FF_BASE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            print(f"{FF_BASE_FOLDER_NAME} folder not found in Google Drive")
            return None
            
        folder = items[0]
        print(f"Found {FF_BASE_FOLDER_NAME} folder: {folder['name']} (ID: {folder['id']})")
        return folder['id']
        
    except Exception as e:
        print(f"Error finding {FF_BASE_FOLDER_NAME} folder: {e}")
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

def calculate_folder_hash(service, folder_id, parent_path=""):
    """Calculate hierarchical hash for a folder and its subfolders."""
    try:
        print(f"🔍 Calculating hash for folder: {parent_path or 'root'}")
        
        # Get all items in the folder
        all_items = []
        
        # List folders with retry logic
        folder_query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                folder_results = service.files().list(
                    q=folder_query,
                    fields="files(id, name, parents, mimeType)"
                ).execute()
                break
            except HttpError as e:
                if e.resp.status in [429, 500, 502, 503, 504] and attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Retryable error listing folders, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Error listing folders, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise e
        
        folders = folder_results.get('files', [])
        
        # List files (Markdown) with retry logic
        file_query = f"'{folder_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false"
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                file_results = service.files().list(
                    q=file_query,
                    fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime)"
                ).execute()
                break
            except HttpError as e:
                if e.resp.status in [429, 500, 502, 503, 504] and attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Retryable error listing files, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Error listing files, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                else:
                    raise e
        
        files = file_results.get('files', [])
        
        # Create metadata string for current folder
        metadata_string = ""
        
        # Process subfolders recursively
        for folder in folders:
            full_path = f"{parent_path}/{folder['name']}" if parent_path else folder['name']
            # Calculate hash for subfolder
            subfolder_hash = calculate_folder_hash(service, folder['id'], full_path)
            if subfolder_hash:
                metadata_string += f"FOLDER:{full_path}|{subfolder_hash}\n"
        
        # Process files in current folder
        for file in files:
            full_path = f"{parent_path}/{file['name']}" if parent_path else file['name']
            mod_time = file.get('modifiedTime', '')
            checksum = file.get('md5Checksum', '')
            metadata_string += f"FILE:{full_path}|{mod_time}|{checksum}\n"
        
        # Calculate MD5 hash of the metadata string
        if metadata_string:
            folder_hash = hashlib.md5(metadata_string.encode('utf-8')).hexdigest()
            print(f"✅ Hash calculated for {parent_path}: {folder_hash[:16]}...")
            return folder_hash
        else:
            # Empty folder hash
            empty_hash = hashlib.md5(b"").hexdigest()
            print(f"✅ Empty folder hash for {parent_path}: {empty_hash[:16]}...")
            return empty_hash
            
    except Exception as e:
        print(f"Error calculating folder hash for {parent_path}: {e}")
        return None

def save_folder_hash(gcs_client, bucket_name, folder_path, folder_hash):
    """Save folder hash to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        hash_key = f"{HASH_PREFIX}{folder_path}.hash" if folder_path else f"{HASH_PREFIX}root.hash"
        blob = bucket.blob(hash_key)
        blob.upload_from_string(folder_hash)
        print(f"✅ Folder hash saved for {folder_path}")
        
    except Exception as e:
        print(f"Error saving folder hash for {folder_path}: {e}")

def get_saved_folder_hash(gcs_client, bucket_name, folder_path):
    """Get saved folder hash from GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        hash_key = f"{HASH_PREFIX}{folder_path}.hash" if folder_path else f"{HASH_PREFIX}root.hash"
        blob = bucket.blob(hash_key)
        
        if blob.exists():
            content = blob.download_as_text()
            return content.strip()
        return None
        
    except Exception as e:
        print(f"Error getting saved folder hash for {folder_path}: {e}")
        return None

def compare_folder_hashes(current_hash, saved_hash):
    """Compare folder hashes to determine if sync is needed."""
    return current_hash != saved_hash

def list_changed_folders(service, folder_id, gcs_client, bucket_name, parent_path=""):
    """List folders that have changed based on hash comparison."""
    try:
        print(f"🔍 Checking for changes in: {parent_path or 'root'}")
        
        changed_folders = []
        
        # Calculate current hash for this folder
        current_hash = calculate_folder_hash(service, folder_id, parent_path)
        if not current_hash:
            return changed_folders
        
        # Compare with saved hash
        saved_hash = get_saved_folder_hash(gcs_client, bucket_name, parent_path)
        
        if compare_folder_hashes(current_hash, saved_hash):
            print(f"📁 Changes detected in: {parent_path or 'root'}")
            changed_folders.append({
                'id': folder_id,
                'path': parent_path,
                'current_hash': current_hash,
                'saved_hash': saved_hash
            })
            
            # Recursively check subfolders
            folder_query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            folder_results = service.files().list(
                q=folder_query,
                fields="files(id, name, parents, mimeType)"
            ).execute()
            
            folders = folder_results.get('files', [])
            for folder in folders:
                full_path = f"{parent_path}/{folder['name']}" if parent_path else folder['name']
                # Recursively check subfolder
                sub_changed = list_changed_folders(service, folder['id'], gcs_client, bucket_name, full_path)
                changed_folders.extend(sub_changed)
        else:
            print(f"⏭️  No changes in: {parent_path or 'root'}")
        
        return changed_folders
        
    except Exception as e:
        print(f"Error checking folder changes for {parent_path}: {e}")
        return []

def list_files_in_folder(service, folder_id, parent_path=""):
    """List all .md files in a folder (recursively)."""
    try:
        all_files = []
        
        def list_files_recursive(parent_id, current_path):
            # List folders with retry logic
            folder_query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    folder_results = service.files().list(
                        q=folder_query,
                        fields="files(id, name, parents, mimeType)"
                    ).execute()
                    break
                except HttpError as e:
                    if e.resp.status in [429, 500, 502, 503, 504] and attempt < RETRY_ATTEMPTS - 1:
                        delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                        print(f"⚠️  Retryable error listing folders, retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        raise e
                except Exception as e:
                    if attempt < RETRY_ATTEMPTS - 1:
                        delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                        print(f"⚠️  Error listing folders, retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        raise e
            
            folders = folder_results.get('files', [])
            for folder in folders:
                folder_path = f"{current_path}/{folder['name']}"
                list_files_recursive(folder['id'], folder_path)
            
            # List .md files with retry logic
            file_query = f"'{parent_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false"
            
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    file_results = service.files().list(
                        q=file_query,
                        fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime)"
                    ).execute()
                    break
                except HttpError as e:
                    if e.resp.status in [429, 500, 502, 503, 504] and attempt < RETRY_ATTEMPTS - 1:
                        delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                        print(f"⚠️  Retryable error listing files, retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        raise e
                except Exception as e:
                    if attempt < RETRY_ATTEMPTS - 1:
                        delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                        print(f"⚠️  Error listing files, retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        raise e
            
            files = file_results.get('files', [])
            for file in files:
                file_path = f"{current_path}/{file['name']}"
                file['full_path'] = file_path
                all_files.append(file)
        
        # Start recursive listing
        list_files_recursive(folder_id, parent_path)
        
        return all_files
        
    except Exception as e:
        print(f"Error listing files in folder {parent_path}: {e}")
        return []

def download_drive_file(service, file_id):
    """Download file content from Google Drive."""
    try:
        # Download file content with retry logic
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
        mod_time = file.get('modifiedTime', '')
        
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
            
        print(f"✅ Synced: {file_path}")
        return True, file_path
        
    except Exception as e:
        print(f"❌ Error syncing file {file.get('full_path', file['name'])}: {e}")
        return False, file.get('full_path', file['name'])

def sync_changed_folders(service, gcs_client, bucket_name, changed_folders):
    """Sync files in changed folders."""
    try:
        synced_count = 0
        skipped_count = 0
        
        for folder_info in changed_folders:
            folder_id = folder_info['id']
            folder_path = folder_info['path']
            current_hash = folder_info['current_hash']
            
            print(f"🔄 Syncing folder: {folder_path}")
            
            # List files in the changed folder
            files = list_files_in_folder(service, folder_id, folder_path)
            if not files:
                print(f"No files found in folder: {folder_path}")
                # Save folder hash even if no files
                save_folder_hash(gcs_client, bucket_name, folder_path, current_hash)
                continue
            
            print(f"Found {len(files)} files in folder: {folder_path}")
            
            # Sync files in batches
            for i in range(0, len(files), BATCH_SIZE):
                batch = files[i:i + BATCH_SIZE]
                
                # Prepare arguments for parallel processing
                args_list = [(service, gcs_client, bucket_name, file) for file in batch]
                
                # Process files in parallel
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    results = list(executor.map(sync_single_file, args_list))
                    
                    # Count results
                    for success, file_path in results:
                        if success:
                            synced_count += 1
                        else:
                            skipped_count += 1
            
            # Save folder hash after successful sync
            save_folder_hash(gcs_client, bucket_name, folder_path, current_hash)
        
        return synced_count, skipped_count
        
    except Exception as e:
        print(f"Error syncing changed folders: {e}")
        return 0, 0

def sync_drive_to_gcs_hierarchical():
    """Hierarchical sync from Google Drive to GCS using folder-level hashes."""
    try:
        print("🔄 Starting hierarchical sync from Google Drive to GCS...")
        start_time = datetime.now()
        
        # Initialize services
        drive_service = get_drive_service()
        if not drive_service:
            return False
            
        gcs_client = get_gcs_client()
        if not gcs_client:
            return False
        
        print(f"Syncing notes from Google Drive to GCS bucket: {BUCKET_NAME}")
        
        # Find FF-BASE folder
        folder_id = find_ff_base_folder(drive_service)
        if not folder_id:
            return False
            
        # Check for changed folders using hierarchical hash comparison
        changed_folders = list_changed_folders(drive_service, folder_id, gcs_client, BUCKET_NAME)
        
        if not changed_folders:
            print("✅ No changes detected in any folders")
            end_time = datetime.now()
            duration = end_time - start_time
            print(f"✅ Sync completed: 0 files synced in {duration}")
            return True
        
        print(f"📁 Found {len(changed_folders)} changed folders")
        
        # Sync files in changed folders
        synced_count, skipped_count = sync_changed_folders(drive_service, gcs_client, BUCKET_NAME, changed_folders)
        
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"✅ Sync completed: {synced_count} files synced, {skipped_count} files unchanged in {duration}")
        
        return True
        
    except Exception as e:
        print(f"Error in hierarchical sync: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_drive_to_gcs_http(request):
    """HTTP Cloud Function entry point - hierarchical version."""
    try:
        print("🔄 Syncing notes from Google Drive to GCS (hierarchical hash optimization)...")
        start_time = datetime.now()
        
        success = sync_drive_to_gcs_hierarchical()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            print(f"✅ Hierarchical sync completed in {duration}")
            return (f"Hierarchical sync completed in {duration}", 200)
        else:
            print(f"❌ Hierarchical sync failed after {duration}")
            return (f"Hierarchical sync failed after {duration}", 500)
        
    except Exception as e:
        print(f"Error in hierarchical sync: {e}")
        import traceback
        traceback.print_exc()
        return (f"Error in hierarchical sync: {e}", 500)

def sync_drive_to_gcs(event, context):
    """Background Cloud Function entry point - hierarchical version."""
    try:
        print("🔄 Syncing notes from Google Drive to GCS (background hierarchical sync)...")
        start_time = datetime.now()
        
        success = sync_drive_to_gcs_hierarchical()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            print(f"✅ Background hierarchical sync completed in {duration}")
        else:
            print(f"❌ Background hierarchical sync failed after {duration}")
        
    except Exception as e:
        print(f"Error in background hierarchical sync: {e}")
        import traceback
        traceback.print_exc()