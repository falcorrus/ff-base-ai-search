#!/usr/bin/env python3
"""
Enhanced Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Uses timestamp-based incremental sync with proper credential handling.
"""

import os
import json
import io
import hashlib
import base64
import time
import random
from datetime import datetime, timedelta
from google.cloud import storage
from googleapiclient.discovery import build
from google.auth import default
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Configuration
MAX_WORKERS = 5  # Reduced for better reliability
BATCH_SIZE = 20  # Small batch size to avoid memory issues
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # Base delay for exponential backoff
BUCKET_NAME = "ff-base-knowledge-base"
FF_BASE_FOLDER_NAME = "FF-BASE"
SYNC_STATE_FILE = "sync_state.json"

def get_drive_service():
    """Initialize and return Google Drive service with proper credential handling."""
    try:
        # Use default credentials with proper error handling
        credentials, project = default()
        
        # Add required scopes
        scoped_credentials = credentials.with_scopes([
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/devstorage.read_write"
        ])
        
        # Build the service
        service = build('drive', 'v3', credentials=scoped_credentials, cache_discovery=False)
        print("✅ Google Drive service initialized")
        print(f"Project: {project}")
        return service
        
    except Exception as e:
        print(f"Error initializing Google Drive service: {e}")
        return None

def get_gcs_client():
    """Initialize and return Google Cloud Storage client with proper credential handling."""
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

def get_sync_state(gcs_client, bucket_name):
    """Get the last sync timestamp from GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(SYNC_STATE_FILE)
        
        if blob.exists():
            content = blob.download_as_text()
            state = json.loads(content)
            last_sync = state.get('last_sync', '1970-01-01T00:00:00Z')
            print(f"✅ Last sync timestamp: {last_sync}")
            return last_sync
        else:
            # If no sync state, use a long time ago
            long_ago = (datetime.utcnow() - timedelta(days=365)).isoformat() + 'Z'
            print(f"⚠️  No sync state found, using: {long_ago}")
            return long_ago
            
    except Exception as e:
        print(f"Error getting sync state: {e}")
        # If error, use a long time ago
        long_ago = (datetime.utcnow() - timedelta(days=365)).isoformat() + 'Z'
        print(f"⚠️  Error getting sync state, using: {long_ago}")
        return long_ago

def save_sync_state(gcs_client, bucket_name, last_sync):
    """Save the last sync timestamp to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(SYNC_STATE_FILE)
        
        state = {
            'last_sync': last_sync,
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        blob.upload_from_string(json.dumps(state, indent=2))
        print("✅ Sync state saved to GCS")
        
    except Exception as e:
        print(f"Error saving sync state: {e}")

def list_recently_changed_files(service, folder_id, last_sync_time):
    """List files changed since last sync time."""
    try:
        print(f"🔍 Looking for files changed since: {last_sync_time}")
        
        all_files = []
        
        def list_files_since_recursive(parent_id, path_prefix=""):
            # List folders
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
                full_path = f"{path_prefix}/{folder['name']}" if path_prefix else folder['name']
                list_files_since_recursive(folder['id'], full_path)
            
            # List .md files changed since last sync
            file_query = f"'{parent_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false and modifiedTime > '{last_sync_time}'"
            
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
                full_path = f"{path_prefix}/{file['name']}" if path_prefix else file['name']
                file['full_path'] = full_path
                all_files.append(file)
        
        # Start recursive listing
        list_files_since_recursive(folder_id)
        
        print(f"Found {len(all_files)} recently changed Markdown files")
        return all_files
        
    except Exception as e:
        print(f"Error listing recently changed files: {e}")
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
            if existing_blob and existing_blob.md5_hash:
                # Convert base64 hash to hex
                existing_md5 = base64.b64decode(existing_blob.md5_hash).hex()
                
                # Compare hashes
                if existing_md5.lower() == drive_md5.lower() if drive_md5 else False:
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

def sync_drive_to_gcs_timestamp_based():
    """Timestamp-based sync from Google Drive to GCS."""
    try:
        print("🔄 Starting timestamp-based sync from Google Drive to GCS...")
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
            
        # Get last sync time
        last_sync_time = get_sync_state(gcs_client, BUCKET_NAME)
        
        # List recently changed files
        print("🔍 Listing recently changed files...")
        recent_files = list_recently_changed_files(drive_service, folder_id, last_sync_time)
        if not recent_files:
            print("✅ No recently changed files found")
            # Still update sync state to current time
            current_time = datetime.utcnow().isoformat() + 'Z'
            save_sync_state(gcs_client, BUCKET_NAME, current_time)
            
            end_time = datetime.now()
            duration = end_time - start_time
            print(f"✅ Sync completed: 0 files synced in {duration}")
            return True
        
        print(f"Found {len(recent_files)} recently changed files")
        
        # Process files in small batches to avoid memory issues
        synced_count = 0
        skipped_count = 0
        failed_count = 0
        batch_number = 0
        
        for i in range(0, len(recent_files), BATCH_SIZE):
            batch = recent_files[i:i + BATCH_SIZE]
            batch_number += 1
            batch_start = datetime.now()
            
            print(f"🔄 Processing batch {batch_number}/{(len(recent_files) + BATCH_SIZE - 1) // BATCH_SIZE}: {len(batch)} files")
            
            # Process files in this batch
            batch_results = []
            for file in batch:
                args = (drive_service, gcs_client, BUCKET_NAME, file)
                result = sync_single_file(args)
                batch_results.append(result)
            
            # Count results
            for status, file_path in batch_results:
                if status == True:  # synced
                    synced_count += 1
                elif status == False:  # skipped
                    skipped_count += 1
                else:  # failed
                    failed_count += 1
            
            batch_end = datetime.now()
            batch_duration = batch_end - batch_start
            print(f"✅ Batch {batch_number} completed in {batch_duration}: {len([r for r in batch_results if r[0] == True])} synced, {len([r for r in batch_results if r[0] == False])} skipped, {len([r for r in batch_results if r[0] is None])} failed")
            
            # Add small delay between batches to avoid rate limits
            if i + BATCH_SIZE < len(recent_files):
                print("⏳ Waiting between batches...")
                time.sleep(2)
        
        # Update sync state to current time
        current_time = datetime.utcnow().isoformat() + 'Z'
        save_sync_state(gcs_client, BUCKET_NAME, current_time)
        
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"✅ Timestamp-based sync completed: {synced_count} files synced, {skipped_count} files unchanged, {failed_count} files failed in {duration}")
        
        return True
        
    except Exception as e:
        print(f"Error in timestamp-based sync: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_drive_to_gcs_http(request):
    """HTTP Cloud Function entry point - timestamp-based version."""
    try:
        print("🚀 HTTP Cloud Function triggered - timestamp-based sync")
        start_time = datetime.now()
        
        success = sync_drive_to_gcs_timestamp_based()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            print(f"✅ Timestamp-based sync completed in {duration}")
            return (f"Timestamp-based sync completed in {duration}", 200)
        else:
            print(f"❌ Timestamp-based sync failed after {duration}")
            return (f"Timestamp-based sync failed after {duration}", 500)
        
    except Exception as e:
        print(f"Error in HTTP function: {e}")
        import traceback
        traceback.print_exc()
        return (f"Error: {e}", 500)

def sync_drive_to_gcs(event, context):
    """Background Cloud Function entry point - timestamp-based version."""
    try:
        print("🚀 Background Cloud Function triggered - timestamp-based sync")
        start_time = datetime.now()
        
        success = sync_drive_to_gcs_timestamp_based()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            print(f"✅ Background timestamp-based sync completed in {duration}")
        else:
            print(f"❌ Background timestamp-based sync failed after {duration}")
        
    except Exception as e:
        print(f"Error in background function: {e}")
        import traceback
        traceback.print_exc()