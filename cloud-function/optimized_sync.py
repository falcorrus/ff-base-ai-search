#!/usr/bin/env python3
"""
Highly optimized Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Uses incremental sync with timeout handling and batch processing.
"""

import os
import json
import io
import hashlib
import base64
import time
import random
from datetime import datetime, timedelta
import pytz
from google.cloud import storage
from googleapiclient.discovery import build
from google.auth import default
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Import time utilities
from time_utils import utc_to_brt, get_current_time_brt, get_current_time_utc

# Configuration
MAX_WORKERS = 5  # Reduced for better reliability
BATCH_SIZE = 10  # Process files in small batches to avoid timeouts
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # Base delay for exponential backoff
BUCKET_NAME = "ff-base-knowledge-base"
FF_BASE_FOLDER_NAME = "FF-BASE"
SYNC_STATE_FILE = "sync_state.json"
MAX_EXECUTION_TIME = 480  # 8 minutes (less than 9-minute Cloud Function limit)

# Time zones
UTC = pytz.UTC
BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)

def get_drive_service():
    """Initialize and return Google Drive service using default credentials."""
    try:
        # Use default credentials (works in Cloud Functions environment)
        credentials, project = default()
        
        # Add required scopes
        scoped_credentials = credentials.with_scopes([
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/devstorage.read_write"
        ])
        
        # Build the service
        service = build('drive', 'v3', credentials=scoped_credentials, cache_discovery=False)
        print("✅ Google Drive service initialized")
        print(f"🕒 Current time (BRT): {get_current_time_brt()}")
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
        print(f"🕒 Current time (BRT): {get_current_time_brt()}")
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
        print(f"🕒 Search completed at (BRT): {get_current_time_brt()}")
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
            print(f"✅ Last sync timestamp (UTC): {last_sync}")
            print(f"🕒 Last sync timestamp (BRT): {utc_to_brt(last_sync)}")
            return last_sync
        else:
            # If no sync state, use a long time ago
            long_ago = (datetime.now(UTC) - timedelta(days=365)).isoformat() + 'Z'
            print(f"⚠️  No sync state found, using: {long_ago}")
            print(f"🕒 No sync state found, using (BRT): {utc_to_brt(long_ago)}")
            return long_ago
            
    except Exception as e:
        print(f"Error getting sync state: {e}")
        # If error, use a long time ago
        long_ago = (datetime.now(UTC) - timedelta(days=365)).isoformat() + 'Z'
        print(f"⚠️  Error getting sync state, using: {long_ago}")
        print(f"🕒 Error getting sync state, using (BRT): {utc_to_brt(long_ago)}")
        return long_ago

def save_sync_state(gcs_client, bucket_name, last_sync):
    """Save the last sync timestamp to GCS."""
    try:
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(SYNC_STATE_FILE)
        
        state = {
            'last_sync': last_sync,
            'updated_at': datetime.now(UTC).isoformat() + 'Z'
        }
        
        blob.upload_from_string(json.dumps(state, indent=2))
        print(f"✅ Sync state saved (UTC): {last_sync}")
        print(f"🕒 Sync state saved (BRT): {utc_to_brt(last_sync)}")
        
    except Exception as e:
        print(f"Error saving sync state: {e}")

def list_drive_files_incremental(service, folder_id, last_sync_time):
    """List files changed since last sync time."""
    try:
        print(f"🔍 Looking for files changed since (UTC): {last_sync_time}")
        print(f"🕒 Looking for files changed since (BRT): {utc_to_brt(last_sync_time)}")
        
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
                # Get full path
                full_path = f"{path_prefix}/{file['name']}" if path_prefix else file['name']
                file['full_path'] = full_path
                
                # Display modification time in both UTC and BRT
                mod_time = file.get('modifiedTime', '')
                if mod_time:
                    print(f"📄 Found changed file: {full_path}")
                    print(f"   Modified (UTC): {mod_time}")
                    print(f"   Modified (BRT): {utc_to_brt(mod_time)}")
                
                all_files.append(file)
        
        # Start recursive listing
        list_files_since_recursive(folder_id)
        
        print(f"✅ Found {len(all_files)} recently changed Markdown files")
        return all_files
        
    except Exception as e:
        print(f"Error listing recently changed files: {e}")
        return []

def download_drive_file_with_retry(service, file_id):
    """Download file content from Google Drive with retry logic."""
    for attempt in range(RETRY_ATTEMPTS):
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
            
        except HttpError as e:
            if e.resp.status in [429, 500, 502, 503, 504]:
                # Retryable errors
                if attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Retryable error downloading file {file_id}, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
            print(f"❌ HTTP error downloading file {file_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error downloading file {file_id}: {e}")
            if attempt < RETRY_ATTEMPTS - 1:
                delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                print(f"⚠️  Retrying download in {delay:.2f}s...")
                time.sleep(delay)
                continue
            return None
    
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
                    return "skipped", file_path
        
        # Download file content with retry logic
        content = download_drive_file_with_retry(service, file['id'])
        if content is None:
            return "failed", file_path
        
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
        return "synced", file_path
        
    except Exception as e:
        print(f"❌ Error syncing file {file.get('full_path', file['name'])}: {e}")
        return "failed", file.get('full_path', file['name'])

def sync_drive_to_gcs_optimized():
    """Optimized sync from Google Drive to GCS with timeout handling."""
    try:
        print("🔄 Starting optimized sync from Google Drive to GCS...")
        start_time = datetime.now(UTC)
        
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
        recent_files = list_drive_files_incremental(drive_service, folder_id, last_sync_time)
        if not recent_files:
            print("✅ No recently changed files found")
            # Still update sync state to current time
            current_time = datetime.now(UTC).isoformat() + 'Z'
            save_sync_state(gcs_client, BUCKET_NAME, current_time)
            
            end_time = datetime.now(UTC)
            duration = end_time - start_time
            print(f"✅ Sync completed: 0 files synced in {duration}")
            print(f"🕒 Sync completed at (BRT): {get_current_time_brt()}")
            return True
        
        print(f"Found {len(recent_files)} recently changed files")
        
        # Process files in small batches to avoid timeouts
        synced_count = 0
        skipped_count = 0
        failed_count = 0
        batch_number = 0
        
        # Track execution time to avoid exceeding Cloud Function limits
        execution_start = datetime.now()
        
        for i in range(0, len(recent_files), BATCH_SIZE):
            batch = recent_files[i:i + BATCH_SIZE]
            batch_number += 1
            batch_start = datetime.now()
            
            # Check if we're approaching the timeout limit
            execution_duration = datetime.now() - execution_start
            if execution_duration.total_seconds() > MAX_EXECUTION_TIME:
                print(f"⚠️  Approaching execution time limit, stopping sync")
                print(f"⏱️  Execution time: {execution_duration}")
                break
            
            print(f"🔄 Processing batch {batch_number}/{(len(recent_files) + BATCH_SIZE - 1) // BATCH_SIZE}: {len(batch)} files")
            print(f"🕒 Batch {batch_number} started at (BRT): {get_current_time_brt()}")
            
            # Prepare arguments for parallel processing
            args_list = [(drive_service, gcs_client, BUCKET_NAME, file) for file in batch]
            
            # Process files in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                results = list(executor.map(sync_single_file, args_list))
                
                # Count results
                for status, file_path in results:
                    if status == "synced":
                        synced_count += 1
                    elif status == "skipped":
                        skipped_count += 1
                    else:  # failed
                        failed_count += 1
            
            batch_end = datetime.now()
            batch_duration = batch_end - batch_start
            print(f"✅ Batch {batch_number} completed in {batch_duration}: {len([r for r in results if r[0] == 'synced'])} synced, {len([r for r in results if r[0] == 'skipped'])} skipped, {len([r for r in results if r[0] == 'failed'])} failed")
            print(f"🕒 Batch {batch_number} completed at (BRT): {get_current_time_brt()}")
            
            # Add small delay between batches to avoid rate limits
            if i + BATCH_SIZE < len(recent_files):
                print("⏳ Waiting between batches...")
                time.sleep(2)
        
        # Update sync state to current time
        current_time = datetime.now(UTC).isoformat() + 'Z'
        save_sync_state(gcs_client, BUCKET_NAME, current_time)
        
        end_time = datetime.now(UTC)
        duration = end_time - start_time
        print(f"✅ Optimized sync completed: {synced_count} files synced, {skipped_count} files unchanged, {failed_count} files failed in {duration}")
        print(f"🕒 Sync completed at (BRT): {get_current_time_brt()}")
        
        return True
        
    except Exception as e:
        print(f"Error in optimized sync: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_drive_to_gcs_http(request):
    """HTTP Cloud Function entry point - optimized version."""
    try:
        print("🚀 HTTP Cloud Function triggered - optimized sync")
        print(f"🕒 Function triggered at (BRT): {get_current_time_brt()}")
        start_time = datetime.now(UTC)
        
        success = sync_drive_to_gcs_optimized()
        
        end_time = datetime.now(UTC)
        duration = end_time - start_time
        
        if success:
            print(f"✅ Optimized sync completed in {duration}")
            print(f"🕒 Function completed at (BRT): {get_current_time_brt()}")
            return (f"Optimized sync completed in {duration}", 200)
        else:
            print(f"❌ Optimized sync failed after {duration}")
            print(f"🕒 Function failed at (BRT): {get_current_time_brt()}")
            return (f"Optimized sync failed after {duration}", 500)
        
    except Exception as e:
        print(f"Error in HTTP function: {e}")
        import traceback
        traceback.print_exc()
        print(f"🕒 Function error at (BRT): {get_current_time_brt()}")
        return (f"Error: {e}", 500)

def sync_drive_to_gcs(event, context):
    """Background Cloud Function entry point - optimized version."""
    try:
        print("🚀 Background Cloud Function triggered - optimized sync")
        print(f"🕒 Function triggered at (BRT): {get_current_time_brt()}")
        start_time = datetime.now(UTC)
        
        success = sync_drive_to_gcs_optimized()
        
        end_time = datetime.now(UTC)
        duration = end_time - start_time
        
        if success:
            print(f"✅ Background optimized sync completed in {duration}")
            print(f"🕒 Function completed at (BRT): {get_current_time_brt()}")
        else:
            print(f"❌ Background optimized sync failed after {duration}")
            print(f"🕒 Function failed at (BRT): {get_current_time_brt()}")
        
    except Exception as e:
        print(f"Error in background function: {e}")
        import traceback
        traceback.print_exc()
        print(f"🕒 Function error at (BRT): {get_current_time_brt()}")