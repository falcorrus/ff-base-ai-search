#!/usr/bin/env python3
"""
Script to check recently modified files in Google Drive FF-BASE folder.
"""

import os
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

# Configuration
FF_BASE_FOLDER_NAME = "FF-BASE"

def load_environment():
    """Load environment variables from .env file."""
    env_file = os.path.join("backend", ".env")
    if os.path.exists(env_file):
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
            "https://www.googleapis.com/auth/drive.readonly"
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

def list_recent_files(service, folder_id, days=7):
    """List recently modified files in the FF-BASE folder."""
    try:
        print(f"🔍 Finding files modified in the last {days} days...")
        
        # Calculate the date threshold
        threshold_date = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
        
        all_files = []
        
        def list_files_recursive(parent_id, path_prefix=""):
            # List folders
            folder_query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            folder_results = service.files().list(
                q=folder_query,
                fields="files(id, name, parents, mimeType)"
            ).execute()
            
            folders = folder_results.get('files', [])
            for folder in folders:
                full_path = f"{path_prefix}/{folder['name']}" if path_prefix else folder['name']
                list_files_recursive(folder['id'], full_path)
            
            # List .md files modified recently
            file_query = f"'{parent_id}' in parents and (mimeType='text/markdown' or mimeType='text/x-markdown' or name contains '.md') and trashed=false and modifiedTime > '{threshold_date}'"
            file_results = service.files().list(
                q=file_query,
                fields="files(id, name, parents, mimeType, md5Checksum, modifiedTime)",
                orderBy="modifiedTime desc"
            ).execute()
            
            files = file_results.get('files', [])
            for file in files:
                full_path = f"{path_prefix}/{file['name']}" if path_prefix else file['name']
                file['full_path'] = full_path
                all_files.append(file)
        
        # Start recursive listing
        list_files_recursive(folder_id)
        
        # Sort by modification time (newest first)
        sorted_files = sorted(all_files, key=lambda x: x.get('modifiedTime', ''), reverse=True)
        
        print(f"Found {len(sorted_files)} recently modified Markdown files")
        return sorted_files[:10]  # Return only the 10 most recent
        
    except Exception as e:
        print(f"Error listing recent files: {e}")
        return []

def main():
    """Main function."""
    print("🔄 Checking recently modified files in Google Drive FF-BASE folder...")
    
    # Load environment variables
    load_environment()
    
    # Initialize services
    drive_service = get_drive_service()
    if not drive_service:
        return
        
    # Find FF-BASE folder
    folder_id = find_ff_base_folder(drive_service)
    if not folder_id:
        return
        
    # List recent files
    recent_files = list_recent_files(drive_service, folder_id, days=7)
    
    if not recent_files:
        print("No recently modified files found")
        return
        
    print(f"\n📅 Top 10 recently modified files (last 7 days):")
    print("=" * 80)
    
    for i, file in enumerate(recent_files, 1):
        mod_time = file.get('modifiedTime', 'Unknown')
        file_path = file.get('full_path', file['name'])
        print(f"{i:2d}. {mod_time} - {file_path}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()