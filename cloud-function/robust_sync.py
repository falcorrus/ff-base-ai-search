#!/usr/bin/env python3
"""
Robust Cloud Function to sync notes from Google Drive to Google Cloud Storage.
Handles network errors and processes files in small batches.
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
MAX_WORKERS = 5  # Reduced for better reliability
BATCH_SIZE = 20  # Small batch size to avoid timeouts
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # Base delay for exponential backoff
BUCKET_NAME = "ff-base-knowledge-base"
FF_BASE_FOLDER_NAME = "FF-BASE"

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
        
        # Build the service with retry configuration
        service = build(
            'drive', 'v3', 
            credentials=scoped_credentials,
            cache_discovery=False,
            num_retries=RETRY_ATTEMPTS
        )
        print("✅ Google Drive service initialized")
        return service
        
    except Exception as e:
        print(f"❌ Error initializing Google Drive service: {e}")
        return None

def get_gcs_client():
    """Initialize and return Google Cloud Storage client."""
    try:
        # Initialize GCS client
        client = storage.Client()
        print("✅ Google Cloud Storage client initialized")
        return client
        
    except Exception as e:
        print(f"❌ Error initializing GCS client: {e}")
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
            print(f"❌ {FF_BASE_FOLDER_NAME} folder not found in Google Drive")
            return None
            
        folder = items[0]
        print(f"✅ Found {FF_BASE_FOLDER_NAME} folder: {folder['name']} (ID: {folder['id']})")
        return folder['id']
        
    except Exception as e:
        print(f"❌ Error finding {FF_BASE_FOLDER_NAME} folder: {e}")
        return None

def get_full_path(service, file_id, folder_id):
    """Get the full path of a file in Google Drive with retry logic."""
    for attempt in range(RETRY_ATTEMPTS):
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
            
        except HttpError as e:
            if e.resp.status in [429, 500, 502, 503, 504]:
                # Retryable errors
                if attempt < RETRY_ATTEMPTS - 1:
                    delay = RETRY_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    print(f"⚠️  Retryable error getting path for file {file_id}, retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
            print(f"❌ Error getting full path for file {file_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error getting path for file {file_id}: {e}")
            return None
    
    return None

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

def sync_single_file_robust(args):
    """Sync a single file with robust error handling."""
    service, gcs_client, bucket_name, file = args
    
    try:
        file_path = file.get('full_path', file.get('name', 'unknown'))
        print(f"🔄 Processing: {file_path}")
        
        # Get file's MD5 checksum from Google Drive
        drive_md5 = file.get('md5Checksum')
        
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
            print(f"❌ Failed to download: {file_path}")
            return "failed", file_path
        
        # Upload to GCS
        try:
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
            print(f"❌ Error uploading to GCS {file_path}: {e}")
            return "failed", file_path
        
    except Exception as e:
        print(f"❌ Unexpected error syncing file {file.get('full_path', file.get('name', 'unknown'))}: {e}")
        return "failed", file.get('full_path', file.get('name', 'unknown'))

def list_all_drive_files(service, folder_id):
    """List all .md files in Google Drive folder with robust error handling."""
    try:
        all_files = []
        
        def list_files_recursive(parent_id, path_prefix=""):
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
                # Recursively list files in subfolder
                subfolder_path = f"{path_prefix}/{folder['name']}" if path_prefix else folder['name']
                list_files_recursive(folder['id'], subfolder_path)
            
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
                # Get full path
                if path_prefix:
                    file['full_path'] = f"{path_prefix}/{file['name']}"
                else:
                    file['full_path'] = file['name']
                all_files.append(file)
        
        # Start recursive listing
        list_files_recursive(folder_id)
        
        print(f"✅ Found {len(all_files)} Markdown files in {FF_BASE_FOLDER_NAME} folder")
        return all_files
        
    except Exception as e:
        print(f"❌ Error listing files in Drive folder: {e}")
        return []

def sync_drive_to_gcs_robust():
    """Robust sync from Google Drive to GCS with error handling and batching."""
    try:
        print("🔄 Starting robust sync from Google Drive to GCS...")
        start_time = datetime.now()
        
        # Initialize services
        drive_service = get_drive_service()
        if not drive_service:
            return False
            
        gcs_client = get_gcs_client()
        if not gcs_client:
            return False
        
        print(f"✅ Services initialized, syncing to bucket: {BUCKET_NAME}")
        
        # Find FF-BASE folder
        folder_id = find_ff_base_folder(drive_service)
        if not folder_id:
            return False
            
        # List all files
        print("🔍 Listing files in Google Drive...")
        all_files = list_all_drive_files(drive_service, folder_id)
        if not all_files:
            print("⚠️  No files found to sync")
            return True
        
        total_files = len(all_files)
        print(f"✅ Found {total_files} files to process")
        
        # Process files in small batches
        synced_count = 0
        skipped_count = 0
        failed_count = 0
        batch_number = 0
        
        for i in range(0, total_files, BATCH_SIZE):
            batch = all_files[i:i + BATCH_SIZE]
            batch_number += 1
            batch_start = datetime.now()
            
            print(f"🔄 Processing batch {batch_number}/{(total_files + BATCH_SIZE - 1) // BATCH_SIZE}: {len(batch)} files")
            
            # Prepare arguments for parallel processing
            args_list = [(drive_service, gcs_client, BUCKET_NAME, file) for file in batch]
            
            # Process files in this batch
            batch_results = []
            for args in args_list:
                result = sync_single_file_robust(args)
                batch_results.append(result)
            
            # Count results
            for status, file_path in batch_results:
                if status == "synced":
                    synced_count += 1
                elif status == "skipped":
                    skipped_count += 1
                else:  # failed
                    failed_count += 1
            
            batch_end = datetime.now()
            batch_duration = batch_end - batch_start
            print(f"✅ Batch {batch_number} completed in {batch_duration}: {len([r for r in batch_results if r[0] == 'synced'])} synced, {len([r for r in batch_results if r[0] == 'skipped'])} skipped, {len([r for r in batch_results if r[0] == 'failed'])} failed")
            
            # Add small delay between batches to avoid rate limits
            if i + BATCH_SIZE < total_files:
                print("⏳ Waiting between batches...")
                time.sleep(2)
        
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"✅ Robust sync completed in {duration}")
        print(f"📊 Summary: {synced_count} synced, {skipped_count} skipped, {failed_count} failed out of {total_files} total files")
        
        return True
        
    except Exception as e:
        print(f"❌ Fatal error in robust sync: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_drive_to_gcs_http(request):
    """HTTP Cloud Function entry point - robust version."""
    try:
        print("🚀 HTTP Cloud Function triggered - robust sync")
        
        success = sync_drive_to_gcs_robust()
        
        if success:
            return ("✅ Robust sync completed successfully", 200)
        else:
            return ("❌ Robust sync failed", 500)
        
    except Exception as e:
        print(f"❌ Error in HTTP function: {e}")
        import traceback
        traceback.print_exc()
        return (f"❌ Error: {e}", 500)

def sync_drive_to_gcs(event, context):
    """Background Cloud Function entry point - robust version."""
    try:
        print("🚀 Background Cloud Function triggered - robust sync")
        
        success = sync_drive_to_gcs_robust()
        
        if success:
            print("✅ Background robust sync completed successfully")
        else:
            print("❌ Background robust sync failed")
        
    except Exception as e:
        print(f"❌ Error in background function: {e}")
        import traceback
        traceback.print_exc()