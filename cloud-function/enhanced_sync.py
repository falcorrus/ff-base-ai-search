#!/usr/bin/env python3
"""
Enhanced Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Handles streaming timeouts and large file processing.
"""

import os
import json
import io
import hashlib
import base64
import time
import random
import concurrent.futures
from datetime import datetime, timezone, timedelta
import pytz
from google.cloud import storage
from googleapiclient.discovery import build
from google.auth import default
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Configuration
MAX_WORKERS = 5  # Reduced for better reliability
BATCH_SIZE = 20  # Small batch size to avoid timeouts
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # Base delay for exponential backoff
BUCKET_NAME = "ff-base-knowledge-base"
FF_BASE_FOLDER_NAME = "FF-BASE"
SYNC_STATE_FILE = "sync_state.json"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size
SERVICE_ACCOUNT_KEY_PATH = "../backend/service-account-key.json"  # Path to service account key

# Time zones
UTC = pytz.UTC
BRT = pytz.timezone('America/Sao_Paulo')  # Brasília Time (UTC-3)

def utc_to_brt(utc_time_str):
    """Convert UTC time string to BRT for display in logs."""
    try:
        # Handle different time string formats
        if 'T' in utc_time_str and 'Z' in utc_time_str:
            # ISO format with Z suffix
            utc_dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        elif 'T' in utc_time_str and '+' in utc_time_str:
            # ISO format with timezone offset
            utc_dt = datetime.fromisoformat(utc_time_str)
        else:
            # Assume it's already in a compatible format
            return utc_time_str
        
        # Convert to BRT
        brt_dt = utc_dt.astimezone(BRT)
        
        # Format for display
        return brt_dt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        print(f"Error converting time {utc_time_str} to BRT: {e}")
        return utc_time_str

def get_current_time_brt():
    """Get current time in BRT format for display."""
    try:
        current_utc = datetime.now(UTC)
        current_brt = current_utc.astimezone(BRT)
        return current_brt.strftime('%Y-%m-%d %H:%M:%S BRT')
    except Exception as e:
        print(f"Error getting current time in BRT: {e}")
        return "Unknown BRT time"

def get_current_time_utc():
    """Get current time in UTC format for internal operations."""
    try:
        current_utc = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        return current_utc
    except Exception as e:
        print(f"Error getting current time in UTC: {e}")
        return "1970-01-01T00:00:00Z"

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
        # Try alternative initialization with service account key
        try:
            from google.oauth2 import service_account
            service_account_path = SERVICE_ACCOUNT_KEY_PATH
            if os.path.exists(service_account_path):
                scopes = [
                    "https://www.googleapis.com/auth/drive.readonly",
                    "https://www.googleapis.com/auth/devstorage.read_write"
                ]
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path, scopes=scopes)
                service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
                print("✅ Google Drive service initialized with service account key")
                print(f"🕒 Current time (BRT): {get_current_time_brt()}")
                return service
            else:
                print(f"Service account key not found at {service_account_path}")
        except Exception as alt_e:
            print(f"Alternative initialization failed: {alt_e}")
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
        # Try alternative initialization with service account key
        try:
            from google.oauth2 import service_account
            service_account_path = SERVICE_ACCOUNT_KEY_PATH
            if os.path.exists(service_account_path):
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path)
                client = storage.Client(credentials=credentials)
                print("✅ Google Cloud Storage client initialized with service account key")
                print(f"🕒 Current time (BRT): {get_current_time_brt()}")
                return client
            else:
                print(f"Service account key not found at {service_account_path}")
        except Exception as alt_e:
            print(f"Alternative initialization failed: {alt_e}")
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

def calculate_drive_folder_hash(service, folder_id):
    """Calculate hierarchical hash for Google Drive folder."""
    try:
        print("🔍 Calculating Google Drive folder hash...")
        print(f"🕒 Calculation started at (BRT): {get_current_time_brt()}")
        
        # Get all .md files in the folder recursively
        all_files = []
        
        def list_files_recursive(parent_id, path_prefix=""):
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
                list_files_recursive(folder['id'], full_path)
            
            # List .md files
            file_query = f"'{parent_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false"
            
            for attempt in range(RETRY_ATTEMPTS):
                try:
                    file_results = service.files().list(
                        q=file_query,
                        fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime, size)"
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
                all_files.append(file)
        
        # Start recursive listing
        list_files_recursive(folder_id)
        
        print(f"✅ Found {len(all_files)} Markdown files in {FF_BASE_FOLDER_NAME} folder (including subfolders)")
        print(f"🕒 Calculation completed at (BRT): {get_current_time_brt()}")
        
        # Sort files for consistent hashing
        sorted_files = sorted(all_files, key=lambda x: x.get('full_path', ''))
        
        # Create metadata string
        metadata_string = ""
        for file in sorted_files:
            # Include path, modification time, checksum, and size if available
            path = file.get('full_path', '')
            mod_time = file.get('modifiedTime', '')
            checksum = file.get('md5Checksum', '')
            size = file.get('size', '')
            metadata_string += f"{path}|{mod_time}|{checksum}|{size}\n"
        
        # Calculate MD5 hash of the metadata string
        folder_hash = hashlib.md5(metadata_string.encode('utf-8')).hexdigest()
        print(f"✅ Google Drive folder hash calculated: {folder_hash[:16]}...")
        print(f"🕒 Hash calculation completed at (BRT): {get_current_time_brt()}")
        return folder_hash
        
    except Exception as e:
        print(f"Error calculating Google Drive folder hash: {e}")
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
            long_ago = (datetime.now(UTC) - timedelta(days=365)).isoformat().replace('+00:00', 'Z')
            print(f"⚠️  No sync state found, using: {long_ago}")
            print(f"🕒 No sync state found, using (BRT): {utc_to_brt(long_ago)}")
            return long_ago
            
    except Exception as e:
        print(f"Error getting sync state: {e}")
        # If error, use a long time ago
        long_ago = (datetime.now(UTC) - timedelta(days=365)).isoformat().replace('+00:00', 'Z')
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
            'updated_at': datetime.now(UTC).isoformat().replace('+00:00', 'Z')
        }
        
        blob.upload_from_string(json.dumps(state, indent=2))
        print(f"✅ Sync state saved (UTC): {last_sync}")
        print(f"🕒 Sync state saved (BRT): {utc_to_brt(last_sync)}")
        
    except Exception as e:
        print(f"Error saving sync state: {e}")

def list_recently_changed_files(service, folder_id, last_sync_time):
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
                        fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime, size)"
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
                # Skip very large files
                file_size = int(file.get('size', 0))
                if file_size > MAX_FILE_SIZE:
                    print(f"⏭️  Skipped (too large): {file['name']} ({file_size} bytes)")
                    continue
                
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
                    print(f"⚠️  Retryable error downloading file, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
            print(f"❌ HTTP error downloading file: {e}")
            return None
        except Exception as e:
            print(f"❌ Error downloading file: {e}")
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
        print(f"🔄 Processing: {file_path}")
        
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

def sync_drive_to_gcs_enhanced():
    """Enhanced sync from Google Drive to GCS with timeout handling."""
    try:
        print("🔄 Starting enhanced sync from Google Drive to GCS...")
        print(f"🕒 Sync started at (BRT): {get_current_time_brt()}")
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
        
        # Calculate folder hash
        current_folder_hash = calculate_drive_folder_hash(drive_service, folder_id)
        if current_folder_hash:
            # Check saved folder hash
            saved_hash = get_sync_state(gcs_client, BUCKET_NAME)
            if saved_hash and saved_hash == current_folder_hash:
                print("⏭️  Folder unchanged, skipping sync")
                end_time = datetime.now(UTC)
                duration = end_time - start_time
                print(f"✅ Sync completed: 0 files synced in {duration}")
                print(f"🕒 Sync completed at (BRT): {get_current_time_brt()}")
                return True
            else:
                print("📁 Folder has changed, proceeding with sync")
        else:
            print("⚠️  Could not calculate folder hash, proceeding with full sync")
        
        # List recently changed files
        print("🔍 Listing recently changed files...")
        recent_files = list_recently_changed_files(drive_service, folder_id, last_sync_time)
        if not recent_files:
            print("✅ No recently changed files found")
            # Still update sync state to current time
            current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
            save_sync_state(gcs_client, BUCKET_NAME, current_time)
            
            end_time = datetime.now(UTC)
            duration = end_time - start_time
            print(f"✅ Sync completed: 0 files synced in {duration}")
            print(f"🕒 Sync completed at (BRT): {get_current_time_brt()}")
            return True
        
        print(f"Found {len(recent_files)} recently changed files")
        
        # Process files in batches to avoid timeouts
        synced_count = 0
        skipped_count = 0
        failed_count = 0
        batch_number = 0
        
        print(f"🔄 Processing files in batches of {BATCH_SIZE}")
        
        for i in range(0, len(recent_files), BATCH_SIZE):
            batch = recent_files[i:i + BATCH_SIZE]
            batch_number += 1
            batch_start = datetime.now(UTC)
            
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
            
            batch_end = datetime.now(UTC)
            batch_duration = batch_end - batch_start
            print(f"✅ Batch {batch_number} completed in {batch_duration}: {len([r for r in results if r[0] == 'synced'])} synced, {len([r for r in results if r[0] == 'skipped'])} skipped, {len([r for r in results if r[0] == 'failed'])} failed")
            print(f"🕒 Batch {batch_number} completed at (BRT): {get_current_time_brt()}")
            
            # Add small delay between batches to avoid rate limits
            if i + BATCH_SIZE < len(recent_files):
                print("⏳ Waiting between batches...")
                time.sleep(2)
        
        # Save folder hash for next run
        if current_folder_hash:
            current_time = datetime.now(UTC).isoformat().replace('+00:00', 'Z')
            save_sync_state(gcs_client, BUCKET_NAME, current_folder_hash)
        
        end_time = datetime.now(UTC)
        duration = end_time - start_time
        print(f"✅ Enhanced sync completed: {synced_count} files synced, {skipped_count} files unchanged, {failed_count} files failed in {duration}")
        print(f"🕒 Sync completed at (BRT): {get_current_time_brt()}")
        
        return True
        
    except Exception as e:
        print(f"Error in enhanced sync: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_drive_to_gcs_http(request):
    """HTTP Cloud Function entry point - enhanced version."""
    try:
        print("🚀 HTTP Cloud Function triggered - enhanced sync")
        print(f"🕒 Function triggered at (BRT): {get_current_time_brt()}")
        
        success = sync_drive_to_gcs_enhanced()
        
        if success:
            print("✅ Enhanced sync completed successfully")
            return ("✅ Enhanced sync completed successfully", 200)
        else:
            print("❌ Enhanced sync failed")
            return ("❌ Enhanced sync failed", 500)
        
    except Exception as e:
        print(f"Error in HTTP function: {e}")
        import traceback
        traceback.print_exc()
        return (f"❌ Error: {e}", 500)

def sync_drive_to_gcs(event, context):
    """Background Cloud Function entry point - enhanced version."""
    try:
        print("🚀 Background Cloud Function triggered - enhanced sync")
        print(f"🕒 Function triggered at (BRT): {get_current_time_brt()}")
        
        success = sync_drive_to_gcs_enhanced()
        
        if success:
            print("✅ Background enhanced sync completed successfully")
        else:
            print("❌ Background enhanced sync failed")
        
    except Exception as e:
        print(f"Error in background function: {e}")
        import traceback
        traceback.print_exc()